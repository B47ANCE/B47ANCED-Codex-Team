"""Recheck promoted vanilla source observations without loading Lua or game code."""
import argparse,hashlib,json,re
from pathlib import Path
from api_library import read
REFERENCE=Path(__file__).resolve().parents[1]/'references'
def verify(game_root, ledger=None, catalog=None):
 root=Path(game_root).resolve();ledger=ledger or json.loads((REFERENCE/'workshop-source-evidence.json').read_text(encoding='utf-8'));catalog=catalog or read(REFERENCE/'api-library.json')
 if ledger['runtime_status']!='NOT_TESTED':raise ValueError('Source recheck cannot establish runtime evidence')
 if ledger['new_records']!=len(ledger['records']):raise ValueError('Evidence count mismatch')
 normalize=lambda text:re.sub(r'\s+','',text)
 for observed in ledger['records']:
  rows=[e for e in catalog['records'] if all(e[k]==observed[k] for k in ('receiver_type','symbol','signature','side')) and e['steam_build']==ledger['steam_build']]
  if len(rows)!=1 or rows[0]['runtime_status']!='NOT_TESTED':raise ValueError('Missing or ambiguous source-only catalog record')
  if rows[0]['evidence']!=observed['evidence']:raise ValueError('Evidence differs from catalog')
  for proof in observed['evidence']:
   if proof['kind']!='vanilla_lua':raise ValueError('Only vanilla Lua source belongs in this ledger')
   path=(root/proof['path']).resolve()
   if not path.is_relative_to(root):raise ValueError('Source outside game root')
   raw=path.read_bytes()
   if hashlib.sha256(raw).hexdigest()!=proof['sha256']:raise ValueError('STALE_SOURCE: '+proof['path'])
   first,last=proof['lines'];excerpt='\n'.join(raw.decode('utf-8-sig').splitlines()[first-1:last]);text=normalize(excerpt)
   if excerpt.lstrip().startswith('--'):raise ValueError('Comment is not a declaration/registration')
   scope=observed['signature_scope'];symbol=observed['symbol']
   if 'registration' in scope:valid='Events.'+symbol+'.Add(' in text
   elif 'definition' in scope:
    name,args=observed['signature'].split('(',1);args=args.rstrip(')')
    valid=normalize('function '+observed['signature']) in text or normalize(name+'=function('+args+')') in text
   else:valid=symbol=='preAddCatDefs' and 'triggerEvent(' in text and symbol in excerpt
   if not valid:raise ValueError('Cited range does not support scoped observation: '+symbol)
 return {'status':'PASS','scope':'SOURCE_ONLY','observations':len(ledger['records']),'steam_build':ledger['steam_build'],'game_version':ledger['game_version'],'runtime_status':'NOT_TESTED','limitation':'Build value is the recorded provenance; verify installed app manifest separately. Matching source does not prove invocation or runtime semantics.'}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--game-root',required=True);args=parser.parse_args()
 try:print(json.dumps(verify(args.game_root),indent=2))
 except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(1,'Source evidence check failed: '+str(error)+'\n')
