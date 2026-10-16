"""Read existing Codex metadata only. Never import, rename or write chat history."""
import json,pathlib,sqlite3,sys,os
def read(home):
    home=pathlib.Path(home).resolve();db=home/'state_5.sqlite'
    if not db.is_file():return []
    con=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True,timeout=3)
    try:
        con.execute('PRAGMA query_only=ON')
        cols={r[1] for r in con.execute('PRAGMA table_info(threads)')}
        required={'id','source','title','cwd','archived','rollout_path','updated_at'}
        if not required<=cols:raise RuntimeError('Codex metadata schema changed; history was not modified')
        name='name' if 'name' in cols else 'NULL'
        rows=con.execute('SELECT id,source,title,cwd,rollout_path,updated_at,'+name+" FROM threads WHERE archived=0 AND source IN ('vscode','cli','appServer') ORDER BY updated_at DESC").fetchall()
        result=[]
        for ident,source,title,cwd,rollout,updated,name in rows:
            import uuid
            try:ident=str(uuid.UUID(ident))
            except (ValueError,TypeError):continue
            if not pathlib.Path(rollout).is_file():continue
            label=' '.join(str(name or title or ident).split())[:100]
            result.append(dict(id=ident,label=label,cwd=cwd,updated=updated,source=source))
        return result
    finally:con.close()
if __name__=='__main__':
    try:print(json.dumps({'chats':read(sys.argv[1])}))
    except Exception:print(json.dumps({'error':'Cannot read saved-chat metadata; original history is unchanged'}));sys.exit(1)
