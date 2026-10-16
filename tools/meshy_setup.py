"""Add only Meshy's global MCP entry; preserve unrelated TOML bytes and secrets."""
import argparse, datetime, json, os, pathlib, shutil, tempfile
try:
    import tomllib
except ImportError:
    tomllib = None

PACKAGE = '@meshy-ai/meshy-mcp-server@0.6.4'
READ_ONLY = ['meshy_check_balance', 'meshy_list_usage', 'meshy_list_tasks',
             'meshy_list_models', 'meshy_get_task_status', 'meshy_list_animations',
             'meshy_download_model']

def configure(home, npx, command, check=False):
    if tomllib is None:
        raise ValueError('Meshy setup requires Python 3.11+; use -SkipMeshy on older Python')
    home = pathlib.Path(home)
    config = home / 'config.toml'
    if config.is_symlink():
        raise ValueError('Linked configuration preserved; manual review required')
    old = config.read_bytes() if config.exists() else b''
    data = tomllib.loads(old.decode('utf-8-sig'))
    expected = dict(command=command, args=['/d', '/c', str(npx), '-y', PACKAGE],
                    env_vars=['MESHY_API_KEY'], enabled_tools=READ_ONLY,
                    startup_timeout_sec=120, tool_timeout_sec=120,
                    cwd=str(home / 'meshy-runtime'))
    existing = data.get('mcp_servers', {}).get('meshy')
    if existing is not None:
        if existing != expected:
            raise ValueError('Existing Meshy configuration differs; preserved unchanged. Review it manually.')
        return {'status': 'CURRENT', 'config_changed': False}
    if check:
        raise ValueError('Meshy MCP configuration is missing')
    block = '\n\n# Meshy: environment authentication; paid tools disabled by default.\n[mcp_servers.meshy]\n'
    block += ''.join(f'{k} = {json.dumps(v)}\n' for k, v in expected.items())
    new = old + block.encode('utf-8')
    parsed = tomllib.loads(new.decode('utf-8-sig'))
    compare = dict(parsed)
    compare['mcp_servers'] = dict(compare['mcp_servers'])
    del compare['mcp_servers']['meshy']
    if 'mcp_servers' not in data and not compare['mcp_servers']:
        del compare['mcp_servers']
    if compare != data:
        raise ValueError('Unrelated configuration changed; refusing write')
    home.mkdir(parents=True, exist_ok=True)
    (home / 'meshy-runtime').mkdir(exist_ok=True)
    backup = None
    if old:
        backup_dir = home / 'integration-backups' / ('meshy-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
        backup_dir.mkdir(parents=True)
        backup = backup_dir / 'config.toml'
        shutil.copy2(config, backup)
    fd, temp = tempfile.mkstemp(prefix='.meshy-', dir=home)
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(new)
        if (config.read_bytes() if config.exists() else b'') != old:
            raise ValueError('Configuration changed concurrently; refusing overwrite')
        os.replace(temp, config)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    return {'status': 'CONFIGURED', 'config_changed': True, 'backup_created': backup is not None}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--codex-home', required=True)
    p.add_argument('--npx', required=True)
    p.add_argument('--command', required=True)
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    try:
        print(json.dumps(configure(a.codex_home, a.npx, a.command, a.check)))
    except Exception:
        # Do not echo parser errors, configuration values or credentials.
        raise SystemExit('Meshy configuration check failed: missing, customized, invalid or concurrently changed config; preserved existing files. Python 3.11+ is required.')
