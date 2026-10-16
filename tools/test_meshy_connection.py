"""Bounded stdio MCP verification: discovery and optional free balance GET only."""
import argparse, json, os, pathlib, queue, subprocess, threading, time

def verify(config_home, balance=False, timeout=180):
    import tomllib
    cfg = tomllib.loads((pathlib.Path(config_home)/'config.toml').read_text(encoding='utf-8-sig'))['mcp_servers']['meshy']
    env = dict(os.environ, TRANSPORT='stdio', MESHY_API_HOST='https://api.meshy.ai')
    if os.name == 'nt' and not env.get('MESHY_API_KEY'):
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as key:
                env['MESHY_API_KEY'] = winreg.QueryValueEx(key, 'MESHY_API_KEY')[0]
        except FileNotFoundError:
            pass
    child = subprocess.Popen([cfg['command'], *cfg['args']], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                             text=True, encoding='utf-8', cwd=cfg['cwd'], env=env)
    messages = queue.Queue()
    def read():
        for line in child.stdout:
            try:
                messages.put(json.loads(line))
            except ValueError:
                pass
        messages.put(None)
    worker = threading.Thread(target=read, daemon=True)
    worker.start()
    def send(msg):
        child.stdin.write(json.dumps(dict(jsonrpc='2.0', **msg))+'\n')
        child.stdin.flush()
    def request(number, method, params):
        send(dict(id=number, method=method, params=params))
        end = time.monotonic()+timeout
        while time.monotonic() < end:
            msg = messages.get(timeout=max(.01, end-time.monotonic()))
            if msg is None:
                raise RuntimeError('MCP server exited before response')
            if msg.get('id') == number:
                if 'error' in msg:
                    raise RuntimeError('MCP protocol returned an error')
                return msg['result']
        raise TimeoutError('MCP response timed out')
    try:
        init = request(1, 'initialize', dict(protocolVersion='2024-11-05', capabilities={},
                         clientInfo=dict(name='b47anced-read-only-verifier', version='1.0')))
        send(dict(method='notifications/initialized'))
        tools = request(2, 'tools/list', {})['tools']
        names={t['name'] for t in tools}
        required={'meshy_text_to_3d','meshy_image_to_3d','meshy_multi_image_to_3d',
                  'meshy_get_task_status','meshy_download_model','meshy_remesh','meshy_convert','meshy_check_balance'}
        if not required.issubset(names):
            raise RuntimeError('Required Meshy tool is missing')
        result = dict(server=init.get('serverInfo'), tool_count=len(tools),
                      tools=sorted(t['name'] for t in tools), api_key_present=bool(env.get('MESHY_API_KEY')),
                      balance_status='NOT_REQUESTED', paid_operations=0)
        if balance:
            if not env.get('MESHY_API_KEY'):
                result['balance_status']='KEY_MISSING'
            else:
                response = request(3, 'tools/call', dict(name='meshy_check_balance', arguments={'response_format':'json'}))
                result['balance_status']='API_ERROR' if response.get('isError') else 'PASS'
                # Never print arbitrary server errors, headers or key material.
                if not response.get('isError'):
                    data=response.get('structuredContent')
                    if data is None:
                        data=json.loads(response['content'][0]['text'])
                    result['credits']={k:data[k] for k in ['balance','monthly_credits','permanent_credits','monthly_resets_at'] if k in data}
        return result
    finally:
        child.stdin.close()
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            child.terminate()
            child.wait(timeout=5)
        worker.join(timeout=1)
        child.stdout.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--codex-home', default=os.environ.get('CODEX_HOME',str(pathlib.Path.home()/'.codex')))
    parser.add_argument('--balance',action='store_true')
    parser.add_argument('--output')
    args=parser.parse_args()
    try:
        result=verify(args.codex_home,args.balance)
    except Exception:
        raise SystemExit('Meshy MCP verification failed; credentials and raw errors were suppressed. Check prerequisites, config and network.')
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    if args.balance and result['balance_status']!='PASS':
        raise SystemExit(1)
