"""Independent source-construction/actual-use binding for real three-room halls.
No producer execution, solver or receipt-based PASS. This is a restricted method,
not an owner rule requiring three rooms, one hall, 1m depth or this arrangement.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
from frame_audit125 import digest,evaluate_core,equal,rectangle
from frame_circulation125 import same_union,rect
from private_binding121 import examine as private_use
from private_domain_inventory129 import examine as transport
SOURCE_SHA='7a8daecd2fa5b2dc1e6ddefc5f66e091b37a20e29930303a241d4fce18cc7229'

def rigid(r,T):
 M=[[F(str(v))for v in row]for row in T['matrix']]
 if len(M)!=2 or any(len(row)!=2 for row in M)or any(v not in(-1,0,1)for row in M for v in row)or any(sum(M[k][i]*M[k][j]for k in range(2))!=int(i==j)for i in range(2)for j in range(2)):raise ValueError('SOURCE_NON_D4')
 return rectangle(r,T)

def examine(world,local,core):
 if (local.get('ordered_macro')or{}).get('kind')=='PARALLEL_TWINS_BRANCH146':
  from private_branch_binding146 import examine as branch
  return branch(world,local,core)
 if (local.get('ordered_macro')or{}).get('kind')=='SIDECAR_T136':
  from private_sidecar_binding136 import examine as sidecar
  return sidecar(world,local,core)
 if (local.get('ordered_macro')or{}).get('kind')=='TURN_T133':
  from private_t_binding133 import examine as turn
  return turn(world,local,core)
 if (local.get('ordered_macro')or{}).get('kind')=='STAGGER_ACCESS132':
  from private_access_binding132 import examine as access
  return access(world,local,core)
 if (local.get('ordered_macro')or{}).get('kind')=='STAGGER132':
  from private_stagger_binding132 import examine as stagger
  return stagger(world,local,core)
 if (local.get('ordered_macro') or {}).get('kind')=='L3_EXPERIMENTAL131':
  from private_l3_binding131 import examine as l3
  return l3(world,local,core)
 errors=[];pending=[];verified={};witness={}
 try:
  if hashlib.sha256(Path(__file__).with_name('private_hall_producer121.py').read_bytes()).hexdigest()!=SOURCE_SHA:pending.append('PRIVATE_HALL_SOURCE_REVISION_UNREVIEWED')
  frame=evaluate_core(core);errors.extend('CORE:'+e for e in frame['errors']);T=core['world_from_local']
  binding=world['frame_binding125']
  if binding['local_model_hash']!=digest(local) or binding['core_contract_hash']!=digest(core) or not equal(binding['world_from_local'],T):errors.append('PRIVATE_HALL_ACTUAL_FRAME_HASH')
  if not equal(local['inputs'],core['solver_inputs'])or not equal(world['inputs'],core['physical_core_model']['inputs']):errors.append('PRIVATE_HALL_INPUT_FRAME')
  tr=transport(local,world);errors.extend(tr['errors']);pending.extend(tr['pending'])
  # Independently run actual enclosure/port/body-use and nonbed-path exclusion,
  # not merely the hall record label or its previous acceptance.
  for name,m in [('local',local),('world',world)]:
   r=private_use(m);errors.extend(name+':'+e for e in r['errors']);pending.extend(name+':'+e for e in r['pending']);witness[name+'_private_use']=r
  L=F(str(local['inputs'][1]));wall=F('.15');depth=F(1);half=F('.55');mapped=set()
  for u in local['units']:
   uid=u['id']
   if uid not in('A','B'):raise ValueError('UNSUPPORTED_UNIT')
   beds=[]
   for i in(1,2,3):
    rid='bed'+str(i);ps=[p for p in local['module_placements']if p['unit_id']==uid and p['room_id']==rid]
    if len(ps)!=1:raise ValueError('BEDROOM_SOURCE_INVENTORY')
    p=ps[0];s=p['module']
    if digest(s)!=p['module_hash']:errors.append(uid+':BEDROOM_SOURCE_HASH')
    if s['schema']not in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118'):pending.append(uid+':UNSUPPORTED_BEDROOM_SOURCE')
    expected=[rigid(r,p['transform'])for r in s['unit']['rooms']['bed1']]
    if not same_union(u['rooms'][rid],expected):errors.append(uid+':BEDROOM_SOURCE_FLOOR')
    if len(expected)!=1:raise ValueError('CURRENT_RECTANGULAR_ROOM_METHOD')
    x,y,X,Y=map(F,expected[0]);beds.append((x,y,X,Y)if uid=='A'else(x,L-Y,X,L-y))
   left=beds[0][0];right=beds[-1][2];front=beds[0][1];rear=max(r[3]for r in beds)+wall;back=rear+depth;cx=F(str(core['entry_centers'][uid][0]))
   if any(r[1]!=front for r in beds)or any(b[0]-a[2]!=F('1.3')for a,b in zip(beds,beds[1:])):pending.append(uid+':SOURCE_ORDERED_HALL_METHOD_UNSUPPORTED')
   formula={'left_return':[left-wall,rear,left,back+wall],'right_return':[right,rear,right+wall,back+wall],'back_left':[left,back,cx-half,back+wall],'back_right':[cx+half,back,right,back+wall]}
   for suffix,r in formula.items():
    key=uid+'.private_hall.'+suffix
    if uid=='B':r=[r[0],L-r[3],r[2],L-r[1]]
    wr=rigid(r,T);rect(wr)
    for fld in('walls','wall_hosts','source_wall_hosts'):
     if not equal(local[fld][key],r):errors.append('LOCAL_SOURCE_HALL:'+fld+':'+key)
     if not equal(world[fld][key],wr):errors.append('WORLD_SOURCE_HALL:'+fld+':'+key)
    verified[key]=list(map(str,wr))
  # Complete module wall binding prevents concealing an added wall under an ID
  # map; common wall union remains separately exact, not a name exemption.
  for p in world['module_placements']:
   if digest(p['module'])!=p['module_hash']:errors.append('MODULE_HASH')
   for k,r in p['module']['walls'].items():
    target=p['id_map'][k]
    if target in mapped or target in verified:errors.append('DUPLICATE_SOURCE_WALL_OWNER')
    mapped.add(target)
    if not equal(world['walls'][target],rigid(r,p['transform'])):errors.append('ACTUAL_MODULE_WALL:'+target)
  remaining=[r for k,r in world['walls'].items()if k not in mapped and k not in verified]
  if not same_union(remaining,list(core['physical_core_model']['walls'].values())):errors.append('UNCLASSIFIED_EXTRA_OR_MOVED_WALL')
 except(KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as e:errors.append('PRIVATE_HALL_SCHEMA:'+str(e))
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_SOURCE_BOUND_ACTUAL_PRIVATE_HALL_ONLY','errors':sorted(set(errors)),'pending':sorted(set(pending)),'boundary_wall_ids':sorted(verified)if not errors and not pending else[],'verified_wall_rects':verified if not errors and not pending else{},'witness':witness,'source_sha256':SOURCE_SHA,'accepted':False,'scope':'Exact reviewed hall construction from source-bound bedroom geometry, actual D4 and fresh private-domain use. No whole-plan/visibility/operations/capacity/Q11 optimality approval; no light or ventilation check.'}
