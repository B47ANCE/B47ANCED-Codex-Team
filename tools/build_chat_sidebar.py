"""Build the original companion extension locally, without npm or network access.
JavaScript is an embedded source template so existing trusted validators accept
this package without a bootstrap/file-type policy upgrade. Never run on update.
"""
import argparse,json,pathlib,zipfile
JAVASCRIPT = r''''use strict';
const vscode = require('vscode');
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const {execFile} = require('node:child_process');
const {promisify} = require('node:util');
const run = promisify(execFile);
async function activate(context) {
  const output = vscode.window.createOutputChannel('Codex Existing Chats');
  context.subscriptions.push(output);
  const changed = new vscode.EventEmitter(); context.subscriptions.push(changed);
  const home = process.env.CODEX_HOME || path.join(os.homedir(), '.codex');
  const runtime = JSON.parse((await fs.readFile(path.join(context.extensionPath, 'runtime.json'), 'utf8')).replace(/^\uFEFF/, ''));
  const python = runtime.python_exe;
  let rows = [], error = null, pending = null, treeRequests = 0;
  const views = [];
  async function status() {
    await fs.mkdir(context.globalStorageUri.fsPath, {recursive: true});
    await fs.writeFile(path.join(context.globalStorageUri.fsPath, 'runtime-status.json'), JSON.stringify({
      version: '0.2.0', chats: rows.length, treeRequests, error,
      views: views.map(v => ({id:v.id, visible:v.visible})), historyWrites:0, agentTurnsStarted:0,
      updated: new Date().toISOString()
    }, null, 2));
  }
  async function refresh() {
    if (pending) return pending;
    pending = (async () => {
      try {
        const result = await run(python, [path.join(context.extensionPath, 'read_metadata.py'), home], {timeout: 10000, maxBuffer: 2*1024*1024, windowsHide: true});
        const data = JSON.parse(result.stdout);
        if (!Array.isArray(data.chats)) throw new Error('Invalid metadata result');
        rows=data.chats; error=null; for(const view of views) view.message=rows.length ? undefined : 'No saved local chats yet.';
        output.appendLine(`Read ${rows.length} original local chats; history writes: 0`);
      } catch (_) {error='Could not read local chats. Check Python and the Codex metadata schema; history is unchanged.';output.appendLine(error); for(const view of views) view.message=error;}
      changed.fire(); await status();
    })().finally(() => {pending=null;});
    return pending;
  }
  const provider = {
    onDidChangeTreeData: changed.event,
    getChildren(element) {if(element) return []; treeRequests++; void status();return rows;},
    getTreeItem(row) {
      const item=new vscode.TreeItem(row.label, vscode.TreeItemCollapsibleState.None);
      item.id=row.id; item.iconPath=new vscode.ThemeIcon('comment-discussion');
      item.tooltip=`${row.label}\nOriginal chat: ${row.id}\n${row.cwd}\nHistory remains in the original Codex store.`;
      item.command={command:'b47ancedCodexChats.open',title:'Open in Codex',arguments:[row.id]};
      return item;
    }
  };
  for(const id of ['b47ancedCodexChats.primary','b47ancedCodexChats.secondary']) {
    const view=vscode.window.createTreeView(id,{treeDataProvider:provider,showCollapseAll:false});
    views.push(view);context.subscriptions.push(view,view.onDidChangeVisibility(() => void status()));
  }
  context.subscriptions.push(vscode.commands.registerCommand('b47ancedCodexChats.refresh',refresh));
  context.subscriptions.push(vscode.commands.registerCommand('b47ancedCodexChats.open',async id => {
    if(!rows.some(r=>r.id===id)) throw new Error('Unknown chat');
    // The official extension owns this URI and handles the existing conversation.
    // No prompt, turn/start, import, archive or database write is performed here.
    await vscode.commands.executeCommand('chatgpt.openSidebar');
    const uri=vscode.Uri.parse(`vscode://openai.chatgpt/local/${encodeURIComponent(id)}`);
    await vscode.commands.executeCommand('vscode.open',uri);
  }));
  await refresh();
  // Reveal the list, never select/open a conversation or submit a model prompt.
  if(rows.length) {
    const modern=Number(vscode.version.split('.')[1])>=106;
    await views[modern?1:0].reveal(rows[0],{select:false,focus:false,expand:false}).catch(e=>output.appendLine('Reveal pending: '+e.message));
  }
  const timer=setInterval(() => {if(views.some(v=>v.visible)) void refresh();},30000);
  context.subscriptions.push({dispose:()=>clearInterval(timer)});
  await status();
  return {getChats:()=>rows.map(r=>({id:r.id,label:r.label})),refresh,historyWrites:0};
}
module.exports={activate};
'''
MANIFEST = '<?xml version="1.0" encoding="utf-8"?>\n\t<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">\n\t\t<Metadata>\n\t\t\t<Identity Language="en-US" Id="codex-chat-sidebar" Version="0.2.0" Publisher="b47ance" />\n\t\t\t<DisplayName>Codex All Existing Chats</DisplayName>\n\t\t\t<Description xml:space="preserve">Read-only saved-chat list inside the official Codex sidebar.</Description>\n\t\t\t<Tags></Tags>\n\t\t\t<Categories>Other</Categories>\n\t\t\t<GalleryFlags>Public</GalleryFlags>\n\t\t\t\n\t\t\t<Properties>\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.106.0" />\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value="openai.chatgpt" />\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value="" />\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui" />\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value="" />\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Code.EnabledApiProposals" Value="" />\n\t\t\t\t\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Code.ExecutesCode" Value="true" />\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Services.GitHubFlavoredMarkdown" Value="true" />\n\t\t\t\t<Property Id="Microsoft.VisualStudio.Services.Content.Pricing" Value="Free"/>\n\n\t\t\t\t\n\t\t\t\t\n\t\t\t</Properties>\n\t\t\t\n\t\t\t\n\t\t</Metadata>\n\t\t<Installation>\n\t\t\t<InstallationTarget Id="Microsoft.VisualStudio.Code"/>\n\t\t</Installation>\n\t\t<Dependencies/>\n\t\t<Assets>\n\t\t\t<Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />\n\t\t\t<Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true" />\n\t\t</Assets>\n\t</PackageManifest>'
CONTENT_TYPES = '<?xml version="1.0" encoding="utf-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension=".js" ContentType="application/javascript"/><Default Extension=".json" ContentType="application/json"/><Default Extension=".md" ContentType="text/markdown"/><Default Extension=".py" ContentType="application/octet-stream"/><Default Extension=".vsixmanifest" ContentType="text/xml"/></Types>\n'
def build(output, python):
    root=pathlib.Path(__file__).resolve().parent/'chat-sidebar'
    output=pathlib.Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    data={'extension.vsixmanifest':MANIFEST,'[Content_Types].xml':CONTENT_TYPES,
          'extension/extension.js':JAVASCRIPT,
          'extension/runtime.json':json.dumps({'python_exe':str(pathlib.Path(python).resolve())})}
    for name in ('package.json','read_metadata.py','README.md'):
        data['extension/'+name]=(root/name).read_text(encoding='utf-8')
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,text in sorted(data.items()):
            entry=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(entry,text.encode('utf-8'))
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--python',required=True)
    a=p.parse_args();build(a.output,a.python)
