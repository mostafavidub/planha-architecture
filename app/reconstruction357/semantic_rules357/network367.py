"""Own-source367 stored network reassessment, never live/fresh authority."""
import json,hashlib,types,copy
from pathlib import Path
from common import digest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
MANIFEST_SHA='60d316ccb86467520a387de92707e4eaccb8d2fa9491d564b72d2ac86e82f2a5'
def manifest():
 data=(HERE/'network367_manifest.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!=MANIFEST_SHA:raise ValueError('NETWORK367_MANIFEST_CHANGED')
 return json.loads(data)
def sources():
 m=manifest();captured={}
 for n,h in m['sources'].items():
  data=(ROOT/n).read_bytes()
  if hashlib.sha256(data).hexdigest()!=h:raise ValueError('NETWORK367_SOURCE_CHANGED:'+n)
  captured[n]=data
 return captured

def evaluate(envelope,result,prerequisites,seconds):
 try:
  m=manifest()
  if envelope.get('schema')!='REGISTERED_SOURCE_JOINT367_VIEW' or result.get('schema')!='REGISTERED_SOURCE_JOINT367_RESULT_VIEW':raise ValueError('NETWORK367_PROFILE')
  if [digest(envelope),digest(result),digest(prerequisites)]!=m['view_digests']:raise ValueError('NETWORK367_FIXED_ARTIFACT_PREREQUISITES_BINDING')
  before=digest([envelope,result,prerequisites]);out=_kernel(envelope,result,prerequisites,seconds)
  if before!=digest([envelope,result,prerequisites]):raise ValueError('NETWORK367_INPUT_MUTATED')
  out['source_profile']='SOURCE_JOINT367';out['artifact_reassessment_only']=True;out['new_fresh_execution']=False
  out['source_pins_digest']=digest(m['sources']);return out
 except(ValueError,KeyError,TypeError,FileNotFoundError)as e:return {'requirement_id':'stored_living_network288','verdict':'UNKNOWN','reason':str(e),'artifact_reassessment_only':True,'new_fresh_execution':False,'repair_authority':False}

def _kernel(envelope,result,prerequisites,remaining_seconds):
 """Same live-Origin callsite only. Reuse exact graph247; no checker/issuer."""
 import ast,time
 from fractions import Fraction as F
 from decimal import Decimal,localcontext
 start=time.monotonic();captured=sources()
 out={'requirement_id':'stored_living_network288','verdict':'UNKNOWN','scope':'GUEST_ROOT_TO_ALL_STORED_LIVING_STANDING_TARGETS_ONLY','rows':[],'repair_authority':False,'whole_living_extent_verified':False,'whole_Q11_IRP12':False,'source_pins_digest':digest(manifest()['sources'])}
 def tick():
  if type(remaining_seconds)not in(int,float)or remaining_seconds<=0 or time.monotonic()-start>=min(2,remaining_seconds):raise ValueError('NETWORK288_REMAINING_DEADLINE')
 def funcs(name,names,ns,constants=False):
  raw=captured[name];tree=ast.parse(raw);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in names or constants and isinstance(n,ast.Assign)and all(isinstance(t,ast.Name)and t.id.endswith('_KEYS')for t in n.targets)]
  if {n.name for n in nodes if isinstance(n,ast.FunctionDef)}!=set(names):raise ValueError('NETWORK288_SOURCE_FUNCTION_MISSING')
  exec(compile(ast.Module(body=nodes,type_ignores=[]),str(ROOT/name),'exec'),ns)
  return ns
 try:
  tick()
  if any(r['verdict']!='SCOPED_PASS'for r in prerequisites):raise ValueError('NETWORK288_SAMEFRESH_PREREQUISITES_UNPROVEN')
  pkt=envelope['packet'];model=pkt['world_model'];core=pkt['core'];family=pkt['family'];mh=digest(model)
  # Core is part of Origin267 trace and independently verified constructor replay.
  ns={'F':F,'Decimal':Decimal,'localcontext':localcontext,'deepcopy':copy.deepcopy}
  funcs('planha_general150_runtime_work/contract114.py',['S'],ns)
  funcs('planha_general150_runtime_work/public_program_audit118.py',['q','hit','covered'],ns)
  ns['Q']=ns['q'];funcs('staging367_service_joint_attempt2/entry367.py',['install'],ns)
  funcs('planha_general150_runtime_work/world_transform125.py',['point','rect','geometry','canonical','placement'],ns,True)
  funcs('staging251_geometry/native_adapter.py',['_stored_seat_graph247'],ns)
  if family not in('FRONT_REAR','LEFT_RIGHT'):raise ValueError('NETWORK288_UNSUPPORTED_FRAME')
  swapped=family=='LEFT_RIGHT'
  if swapped and core.get('world_from_local')!={'matrix':[[0,1],[1,0]],'translation':['0','0']}:raise ValueError('NETWORK288_FRAME_BINDING')
  units=model['units']
  if sorted(u['id']for u in units)!=['A','B']:raise ValueError('NETWORK288_UNIT_INVENTORY')
  rows=result['raw_fresh_report']['rule_contract_evidence']['requirements']
  w=next(r for r in rows if r['requirement_id']=='program_functional_roles')['evidence']['witness']
  ce=w['actual_capacity']['evidence'];pub=w['public_scenarios']['evidence']
  if ce.get('status')!='PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY'or ce.get('model_hash')!=mh or pub.get('status')!='PASS_PUBLIC_SCOPED'or pub.get('model_hash')!=mh:raise ValueError('NETWORK288_SOURCE_CAPACITY_PUBLIC_STATUS')
  if sorted(x['unit']for x in ce['units'])!=['A','B']:raise ValueError('NETWORK288_CAPACITY_UNIT_INVENTORY')
  for u in units:
   tick();uid=u['id'];owner=core.get('unit_ownership',{}).get(uid,[core['units'][uid]])
   wantowner=[ns['rect'](r)for r in owner]if swapped else owner
   eq=lambda a,b:digest(a)==digest(b)
   # Numeric representation equality is source rational, never trimming identifiers.
   if [ns['q'](r)for r in u['ownership']]!=[ns['q'](r)for r in wantowner]:raise ValueError('NETWORK288_CORE_OWNERSHIP')
   cx=F(core['entry_centers'][uid][0]);y=F(core['band'][1]);yt=F(core['band'][3]);box=list(map(F,owner[0]));lo,hi=(y-F('.15'),y)if uid=='A'else(yt,yt+F('.15'))
   root=[F(ns['S'](z)) for z in (cx,box[3]-F('.4')if uid=='A'else box[1]+F('.4'))]
   opening={'id':uid+'.entry','rect':[ns['S'](z)for z in (cx-F('.65'),lo,cx+F('.65'),hi)],'host_wall_id':uid+'.unit_boundary','connects':['lobby',uid+'.entry_circulation'],'operation_kind':'sliding_study','operation_witness_status':'NOT_EVALUATED'}
   scratch={'openings':[opening]};ns['install'](scratch,core['service_balanced367']['slide_direction'])
   wantopen=scratch['openings'][0];wantop=scratch['operations']['doors'][0]
   if swapped:root=ns['point'](root);wantopen=ns['geometry'](wantopen);wantop=ns['geometry'](wantop)
   # Source strings can be decimal or rational; structural numeric comparison.
   def same(a,b):
    if type(a)is dict:return type(b)is dict and set(a)==set(b)and all(same(a[k],b[k])for k in a)
    if type(a)is list:return type(b)is list and len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    if type(a)is str and type(b)is str:
     try:return F(a)==F(b)
     except(ValueError,ZeroDivisionError):return a==b
    return type(a)is type(b)and a==b
   opens=[o for o in model['openings']if o['id']==uid+'.entry'];ops=[o for o in model['operations']['doors']if o.get('opening_id')==uid+'.entry']
   if len(opens)!=1 or len(ops)!=1 or not same(opens[0],wantopen)or not same(ops[0],wantop):raise ValueError('NETWORK288_SOURCE_ENTRY_INSTALLATION')
   cap=u['public_program']['capacity'];seats=cap['living_seats'];crow=next(x for x in ce['units']if x['unit']==uid)
   if crow['living_occupied_instances']!=len(seats)or crow['actual_places']['living_seats']!=sum(s['places']for s in seats):raise ValueError('NETWORK288_CAPACITY_INVENTORY')
   source=types.SimpleNamespace(**ns);row=ns['_stored_seat_graph247'](model,u,root,source,tick)
   row['model_hash']=mh;out['rows'].append(row)
  out['verdict']='SCOPED_PASS'if all(r['verdict']=='PASS_STORED_SOURCE_ROUTE_NETWORK_SCOPED'for r in out['rows'])else'UNKNOWN'
  out['reason']=None if out['verdict']=='SCOPED_PASS'else'STORED_NETWORK_INCOMPLETE_NOT_GLOBAL_INFEASIBILITY'
 except(ValueError,KeyError,TypeError,IndexError,StopIteration,ZeroDivisionError,OverflowError)as exc:
  out['reason']='NETWORK288_UNVERIFIED:'+str(exc)
 if sources()!=captured:raise ValueError('NETWORK288_SOURCE_MUTATION')
 return out
