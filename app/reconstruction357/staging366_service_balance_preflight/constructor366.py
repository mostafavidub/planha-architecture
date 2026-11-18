"""Independent SERVICE entry/portal constructor. No legacy context or verdict.
Original two-rectangle common tail retained; branch-end/notch changes unsupported
until independently integrated with own geometric guards. Never silently cut.
"""
from pathlib import Path
import json,hashlib,copy,sys
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'planha_general150_runtime_work'))
from contract114 import digest
from assemble366 import assemble
RECORD_SHA='8807b7f2e8ba841d8e1a38ba6787f72161c9d04f64d69e71112859be92976ad9'
SELECTION_SHA='37f3f3709776dfcae52087c4eeec67d509ca59a1fb97b1b6e0beafa39129168c'
def inputs():
 a=(ROOT/'staging365_service_grammar/candidate365.json').read_bytes();b=(HERE/'actual_selection366.json').read_bytes()
 if hashlib.sha256(a).hexdigest()!=RECORD_SHA or hashlib.sha256(b).hexdigest()!=SELECTION_SHA:raise ValueError('CONSTRUCTOR_INPUT_CHANGED')
 record=json.loads(a);result=json.loads(b)
 if result['status']!='NECESSARY_PARAMETER_SELECTION_ONLY' or result['source_unchanged']is not True:raise ValueError('SELECTION_INCOMPLETE')
 return record,result['selection']
def core_from(record,selection):
 base=record['candidate']['packet']['core'];core=copy.deepcopy(base)
 if base.get('physical_core_model'):raise ValueError('PHYSICAL_CORE_TRANSFORM_UNSUPPORTED')
 if len(base['lobby'])!=2:raise ValueError('SOURCE_TWO_RECT_CORE_ONLY')
 for uid in('A','B'):core['entry_centers'][uid][0]=selection['entry_x'][uid]
 core['service_balanced366']={**copy.deepcopy(selection),'source_base_core_digest':digest(base),'source_body_pose':'SOURCE_INSIDE_INSET_0.4_ALIGNED_WITH_CURRENT_PORTAL','tail_role':'UNRESOLVED_SOURCE_GEOMETRY_RETAINED','branch_end':'ORIGINAL_SOURCE146_RETAINED'}
 for name,w in [('stair',F('.9')),('lift',F('1.1'))]:
  r=list(map(F,core[name]));y=F(selection['portal_y'][name])
  if not r[1]+w/2<=y<=r[3]-w/2:raise ValueError('PORTAL_OUTSIDE_SOURCE_HOST')
 return core
def build():
 record,selection=inputs();before=digest(record);c=record['candidate'];core=core_from(record,selection);p=copy.deepcopy(record['trace']['proposal']);raw=copy.deepcopy(c['request'])
 if (p.get('ordered_macro')or{}).get('kind')!='PARALLEL_TWINS_BRANCH146':raise ValueError('SERVICE_BRANCH_PROFILE')
 model=assemble(F(raw['W']),F(raw['L']),core,p)
 original=c['model']
 for key in('inputs','program','profile'):
  if digest(model[key])!=digest(original[key]):raise ValueError('PROTECTED_'+key)
 for u in original['units']:
  v=next(x for x in model['units']if x['id']==u['id'])
  for key in('ownership','fixtures','activities'):
   if digest(v[key])!=digest(u[key]):raise ValueError('PROTECTED_'+u['id']+'_'+key)
 if digest(record)!=before:raise ValueError('BASELINE_MUTATED')
 return {'family':'FRONT_REAR','world_model':model,'local_model':copy.deepcopy(model),'core':core,'admission_claim':False}
def context(*args,**kwargs):raise ValueError('EXPLICIT_SERVICE_BALANCED366_REPLAY_REQUIRED')
