import copy,hashlib,importlib.util,json,pathlib,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'.agents/skills/pz-api-audit/scripts';sys.path.insert(0,str(SCRIPTS))
import api_library as library
import verify_workshop_evidence as check
class WorkshopPromotion(unittest.TestCase):
 def test_prior_knowledge_and_uncertainty_preserved(self):
  rows=library.read(library.CURATED)['records']
  digest=hashlib.sha256(json.dumps(rows[:106],sort_keys=True,separators=(',',':')).encode()).hexdigest()
  self.assertEqual(digest,'d7fd932f7c52af01f3194516f3a6c2f36a7398f4c5e7217e4ab59ddbc01cf449')
  self.assertEqual(len(rows),170);self.assertEqual(sum(e['status']=='UNKNOWN' for e in rows),8);self.assertEqual(sum(e['status']=='INFERRED' for e in rows),3)
  self.assertTrue(all(e['runtime_status']=='NOT_TESTED' for e in rows))
 def fixture(self,root,text):
  p=root/'source.lua';p.write_text(text,encoding='utf-8');rows=library.read(library.CURATED)['records'];e=copy.deepcopy(next(e for e in rows if e['receiver_type']=='ISBaseTimedAction' and e['symbol']=='setActionAnim'))
  e['evidence']=[{'kind':'vanilla_lua','path':'source.lua','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':[1,1],'statement':'Synthetic source fixture'}]
  ledger={'runtime_status':'NOT_TESTED','steam_build':e['steam_build'],'game_version':'UNKNOWN','new_records':1,'records':[copy.deepcopy(e)]}
  return ledger,{'schema':1,'records':[e]}
 def test_matching_source_never_becomes_runtime(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);data,cat=self.fixture(root,'function ISBaseTimedAction:setActionAnim(_action)\nend')
   # Use the observed formal arguments rather than assuming a signature.
   sig=cat['records'][0]['signature'];(root/'source.lua').write_text('function '+sig+'\nend',encoding='utf-8')
   for row in [data['records'][0],cat['records'][0]]:row['evidence'][0]['sha256']=hashlib.sha256((root/'source.lua').read_bytes()).hexdigest()
   out=check.verify(root,data,cat);self.assertEqual(out['runtime_status'],'NOT_TESTED');self.assertEqual(out['scope'],'SOURCE_ONLY')
   (root/'source.lua').write_text('changed');self.assertRaisesRegex(ValueError,'STALE_SOURCE',check.verify,root,data,cat)
 def test_comments_wrong_range_and_runtime_claims_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);data,cat=self.fixture(root,'-- function '+next(e['signature'] for e in library.read(library.CURATED)['records'] if e['symbol']=='setActionAnim'))
   self.assertRaisesRegex(ValueError,'Comment',check.verify,root,data,cat)
   data['runtime_status']='DEDICATED_MP_VERIFIED';self.assertRaisesRegex(ValueError,'runtime',check.verify,root,data,cat)
 def test_animation_contract_reference_and_portable_evidence_links(self):
  ledger=json.loads((library.CURATED.parent/'workshop-source-evidence.json').read_text(encoding='utf-8'))
  self.assertEqual(ledger['new_records'],64);self.assertEqual(ledger['imports'],'NONE')
  names={e['symbol'] for e in ledger['records'] if e['receiver_type']=='ISBaseTimedAction'}
  self.assertTrue({'setActionAnim','setAnimVariable','setOverrideHandModels','setOverrideHandModelsString','overrideWeaponType','restoreWeaponType'}<=names)
  for file in [ROOT/'.agents/skills/pz-clean-room-research/references/workshop-knowledge.md',ROOT/'.agents/skills/pz-character-animation/references/animation-contracts.md',ROOT/'docs/WORKSHOP-KNOWLEDGE.md']:
   import re
   for target in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
    if '://' not in target:self.assertTrue((file.parent/target.split('#')[0]).resolve().is_file(),target)
