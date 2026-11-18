"""Fixed359 lineage, one source-level core-notch rebuild; no solver/legacy context."""
import sys,json,copy,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;ROOT=BASE/'planha_general150_runtime_work';PARENT=BASE/'staging359_hall_clamp'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(PARENT));sys.path.insert(0,str(HERE))
from contract114 import digest
from constructor360 import build
LINEAGE=PARENT/'actual359.json'
LINEAGE_SHA='13aa33694b45bdc5dc04fe50251b2b867efa521da970fc639690d3975bb04d03'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory():
 files=[*ROOT.glob('*.py'),*ROOT.glob('*.json'),*(p for p in(ROOT/'references').rglob('*')if p.is_file()),*HERE.glob('*.py'),*(PARENT/n for n in('private_hall_producer359.py','clamp_geometry359.py','operation_reservations359.py')),LINEAGE]
 if sha(LINEAGE)!=LINEAGE_SHA:raise ValueError('FIXED359_LINEAGE_FILE')
 files += [BASE/n for n in json.loads(LINEAGE.read_text())['trace']['source_inventory']]
 return {str(p.relative_to(BASE)):sha(p)for p in sorted(set(files))}
def lineage():
 if sha(LINEAGE)!=LINEAGE_SHA:raise ValueError('FIXED359_LINEAGE_FILE')
 r=json.loads(LINEAGE.read_text());t=r['trace'];c=r['candidate']
 if t['schema']!='ROW_HALL_CLAMP359_SOURCE_TRACE_V1'or digest(c)!=t['candidate_digest']or digest(c['model'])!=t['model_digest']:raise ValueError('LINEAGE_BINDING')
 for name,h in t['source_inventory'].items():
  if sha(BASE/name)!=h:raise ValueError('LINEAGE_SOURCE_DRIFT:'+name)
 return r

def construct():
 old=lineage();before=inventory();raw=copy.deepcopy(old['trace']['raw']);p=copy.deepcopy(old['trace']['proposal']);packet=build(raw,'FRONT_REAR',p);m=packet['world_model'];prior=old['candidate']['model']
 for key in('inputs','profile','program'):
  if digest(m[key])!=digest(prior[key]):raise ValueError('PROTECTED_MODEL_FIELD:'+key)
 for key in('stair','lift'):
  if m['common_spaces'][key]!=prior['common_spaces'][key]:raise ValueError('PROTECTED_CORE_ASSET:'+key)
 for u in m['units']:
  v=next(v for v in prior['units']if v['id']==u['id'])
  for key in('fixtures','activities'):
   if digest(u[key])!=digest(v[key]):raise ValueError('PROTECTED_UNIT_ASSET:'+u['id']+':'+key)
  for name in v['rooms']:
   if name.startswith('bed')and u['rooms'][name]!=v['rooms'][name]:raise ValueError('PROTECTED_BEDROOM')
 context={'schema':'EXPLICIT360_CORE_NOTCH_CONTEXT','producer':'constructor360.build','parent_record_digest':digest(old),'parent_model_digest':digest(prior),'source_inventory':before,'core_variant':packet['core']['notch360'],'legacy_context_used':False,'functional_role_of_transferred_floor':'UNKNOWN','accepted':False}
 c={'request':raw,'request_digest':digest(raw),'packet':packet,'model':m,'model_digest':digest(m),'generation_context':context}
 if inventory()!=before:raise ValueError('SOURCE_DRIFT')
 t={'schema':'ROW_CORE_NOTCH360_SOURCE_TRACE_V1','raw':raw,'proposal':p,'parent_record_digest':digest(old),'parent_model_digest':digest(prior),'source_inventory':before,'candidate_digest':digest(c),'model_digest':digest(m),'solver_used':False,'accepted':False}
 return {'candidate':c,'trace':t,'accepted':False}
def replay(t):
 if t['schema']!='ROW_CORE_NOTCH360_SOURCE_TRACE_V1'or t['source_inventory']!=inventory():raise ValueError('SOURCE_TRACE_BINDING')
 r=construct()
 if r['trace']!=t:raise ValueError('EXACT_REPLAY_MISMATCH')
 return r
