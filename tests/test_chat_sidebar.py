import importlib.util,json,pathlib,sys,tempfile,unittest,zipfile,subprocess,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_chat_sidebar as builder
class SidebarSetup(unittest.TestCase):
 def test_offline_package_is_allowlisted_and_private(self):
  with tempfile.TemporaryDirectory() as td:
   p=builder.build(pathlib.Path(td)/'a.vsix',sys.executable)
   with zipfile.ZipFile(p) as z:
    self.assertEqual(set(z.namelist()),{'[Content_Types].xml','extension.vsixmanifest','extension/extension.js','extension/runtime.json','extension/package.json','extension/read_metadata.py','extension/README.md'})
    package=json.loads(z.read('extension/package.json'));self.assertEqual(package['extensionDependencies'],['openai.chatgpt'])
    self.assertEqual(json.loads(z.read('extension/runtime.json'))['python_exe'],str(pathlib.Path(sys.executable).resolve()))
    self.assertIn('mode=ro',z.read('extension/read_metadata.py').decode())
    before=p.read_bytes();builder.build(p,sys.executable);self.assertEqual(before,p.read_bytes())
 def test_setup_optout_and_inert_update(self):
  setup=(ROOT/'tools/Setup-CodexTeam.ps1').read_text()
  self.assertIn('not $SkipVSCode -and -not $SkipChatSidebar',setup)
  self.assertIn('Setup-ChatSidebar.ps1',setup)
  update=(ROOT/'tools/Update-CodexTeam.ps1').read_text()
  self.assertNotIn('Setup-ChatSidebar',update);self.assertNotIn('build_chat_sidebar',update)
 def test_javascript_lifecycle_with_mocked_vscode(self):
  node=shutil.which('node')
  if not node:self.skipTest('Node is unavailable')
  with tempfile.TemporaryDirectory() as td:
   d=pathlib.Path(td);(d/'extension.js').write_text(builder.JAVASCRIPT);(d/'runtime.json').write_text(json.dumps({'python_exe':sys.executable}))
   # Synthetic metadata only; test no calls can open/resume on activation.
   harness=r'''
const assert=require('assert'),Module=require('module'),real=Module._load,fs=require('fs');
let calls=[],providers=[],commands={},count=0;
const id='11111111-2222-4333-8444-555555555555';
const vscode={version:'1.142.0',EventEmitter:class{constructor(){this.event=()=>{}}fire(){}dispose(){}},
 TreeItem:class{constructor(label){this.label=label}},ThemeIcon:class{},TreeItemCollapsibleState:{None:0},Uri:{parse:x=>x},
 window:{createOutputChannel:()=>({appendLine:()=>{},dispose(){}}),createTreeView:(id,opts)=>{providers.push(opts.treeDataProvider);return{visible:true,onDidChangeVisibility:()=>({dispose(){}}),reveal:async()=>{},dispose(){}}}},
 commands:{registerCommand:(n,f)=>{commands[n]=f;return{dispose(){}}},executeCommand:async(...a)=>calls.push(a)}};
Module._load=function(n,...a){if(n==='vscode')return vscode;if(n==='node:util')return{promisify:()=>async()=>({stdout:JSON.stringify({chats:[{id,label:'Own local chat',cwd:'synthetic'}]})})};if(n==='node:child_process')return{execFile:(_p,_a,_o,cb)=>cb(null,JSON.stringify({chats:[{id,label:'Own local chat',cwd:'synthetic'}]}),'')};return real.call(this,n,...a)};
(async()=>{const c={extensionPath:process.cwd(),globalStorageUri:{fsPath:process.cwd()+'/status'},subscriptions:[]};
 const api=await require('./extension.js').activate(c);assert.equal(api.getChats().length,1);assert.equal(calls.length,0);
 const rows=providers[0].getChildren();assert.equal(rows.length,1);assert.equal(providers[0].getTreeItem(rows[0]).label,'Own local chat');
 await commands['b47ancedCodexChats.open'](id);assert.deepEqual(calls.map(x=>x[0]),['chatgpt.openSidebar','vscode.open']);assert(calls[1][1].endsWith('/local/'+id));
 await assert.rejects(()=>commands['b47ancedCodexChats.open']('bad'));for(const s of c.subscriptions)if(s.dispose)s.dispose();
 const status=JSON.parse(fs.readFileSync('status/runtime-status.json'));assert.equal(status.historyWrites,0);assert.equal(status.agentTurnsStarted,0);
})().catch(e=>{console.error(e);process.exit(1)});
'''
   (d/'test.cjs').write_text(harness)
   subprocess.run([node,'--check','extension.js'],cwd=d,check=True,capture_output=True)
   subprocess.run([node,'test.cjs'],cwd=d,check=True,capture_output=True,timeout=15)
 def test_installer_mock_and_checkonly(self):
  shell=shutil.which('pwsh') or shutil.which('powershell')
  if not shell:self.skipTest('PowerShell unavailable')
  with tempfile.TemporaryDirectory() as td:
   d=pathlib.Path(td);mock=d/'code.ps1';log=d/'calls.txt';marker=d/'installed'
   mock.write_text("$global:LASTEXITCODE=0\nAdd-Content -LiteralPath '"+str(log)+"' -Value ($args -join ' ')\nif($args[0] -eq '--install-extension'){Set-Content -LiteralPath '"+str(marker)+"' -Value yes}\nelse{'openai.chatgpt@26.1007.21434';if(Test-Path -LiteralPath '"+str(marker)+"'){'b47ance.codex-chat-sidebar@0.2.0'}}\n")
   cmd=[shell,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/Setup-ChatSidebar.ps1'),'-HomeDirectory',str(d),'-PythonExe',sys.executable,'-CodeExe',str(mock)]
   subprocess.run(cmd,check=True,capture_output=True,timeout=30)
   self.assertEqual(len(list((d/'.codex/chat-sidebar-build').glob('*.vsix'))),1)
   before=log.read_text();subprocess.run(cmd+['-CheckOnly'],check=True,capture_output=True,timeout=30)
   self.assertEqual(log.read_text().count('--install-extension'),1)
   self.assertNotIn('--uninstall-extension',log.read_text())
