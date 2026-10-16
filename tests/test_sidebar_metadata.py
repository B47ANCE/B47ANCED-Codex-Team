from pathlib import Path
import tempfile,sqlite3,json,unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/chat-sidebar'))
from read_metadata import read
class Metadata(unittest.TestCase):
 def test_new_profile_is_empty(self):
  with tempfile.TemporaryDirectory() as td:self.assertEqual(read(Path(td)),[])
 def test_only_original_live_chats_no_writes(self):
  with tempfile.TemporaryDirectory() as td:
   h=Path(td);p=h/'history.jsonl';p.write_text('original history');db=h/'state_5.sqlite';c=sqlite3.connect(db)
   c.execute('CREATE TABLE threads(id,source,title,cwd,archived,rollout_path,updated_at,name)')
   values=[('11111111-2222-4333-8444-555555555555','vscode','first prompt','old cwd',0,str(p),1,'Original named chat'),('21111111-2222-4333-8444-555555555555','vscode','archived','',1,str(p),2,''),('31111111-2222-4333-8444-555555555555','subAgent','child','',0,str(p),3,'')]
   c.executemany('INSERT INTO threads VALUES(?,?,?,?,?,?,?,?)',values);c.commit();c.close();before=db.read_bytes();original=p.read_bytes()
   rows=read(h);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['label'],'Original named chat');self.assertEqual(before,db.read_bytes());self.assertEqual(original,p.read_bytes())
 def test_missing_history_is_not_listed(self):
  with tempfile.TemporaryDirectory() as td:
   h=Path(td);c=sqlite3.connect(h/'state_5.sqlite');c.execute('CREATE TABLE threads(id,source,title,cwd,archived,rollout_path,updated_at)');c.execute('INSERT INTO threads VALUES(?,?,?,?,?,?,?)',('11111111-2222-4333-8444-555555555555','cli','title','',0,str(h/'missing'),1));c.commit();c.close();self.assertEqual(read(h),[])
 def test_unsupported_schema_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   h=Path(td);c=sqlite3.connect(h/'state_5.sqlite');c.execute('CREATE TABLE threads(id)');c.close();before=(h/'state_5.sqlite').read_bytes();self.assertRaises(RuntimeError,read,h);self.assertEqual(before,(h/'state_5.sqlite').read_bytes())
if __name__=='__main__':unittest.main()
