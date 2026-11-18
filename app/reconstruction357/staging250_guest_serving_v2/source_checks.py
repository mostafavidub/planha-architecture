"""Fixed existing checker114 reuse. No producer build or whole-plan evaluate call."""
from pathlib import Path
import json,hashlib,tempfile,sys,threading,time,importlib
HERE=Path(__file__).resolve().parent;APP=HERE.parent/'planha_general150_runtime_work'
CLOSURE_SHA='6f1e6cb00b1fb2ce1bf65f24a019be9c38d58353e14e442cedd28d6a65d18802'
_LOCK=threading.RLock()
def capture(tick):
 raw=(HERE/'source_closure.json').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=CLOSURE_SHA:raise ValueError('CHECKER_CLOSURE_DOCUMENT_DRIFT')
 pins=json.loads(raw);out={}
 for n,h in pins.items():
  tick();data=(APP/n).read_bytes()
  if hashlib.sha256(data).hexdigest()!=h:raise ValueError('CHECKER_SOURCE_DRIFT:'+n)
  out[n]=data
 if sum(map(len,out.values()))>64000000:raise ValueError('SOURCE_COPY_RESOURCE_CAP')
 return out

def evaluate_models(packet,tick,world_witnesses):
 """Dedicated supervised worker only; scoped checks on both original models.
 Private temp source tree binds code AND data to same captured verified bytes.
 """
 captured=capture(tick);reports=[];names={Path(n).stem for n in captured if n.endswith('.py')and '/'not in n}
 with _LOCK,tempfile.TemporaryDirectory(prefix='bath189_')as tmp:
  root=Path(tmp)
  for n,b in captured.items():
   tick();p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  saved={n:sys.modules.get(n)for n in names};oldpath=list(sys.path)
  try:
   for n in names:sys.modules.pop(n,None)
   sys.path.insert(0,str(root));checker=importlib.import_module('checker114')
   from fractions import Fraction as F
   contract=importlib.import_module('contract114');frames=importlib.import_module('frame_contract125');audit=importlib.import_module('frame_audit125');entry=importlib.import_module('entry117');world=importlib.import_module('world_transform125')
   raw=packet['raw'];p=packet['packet'];W,L,n=contract.parse(raw)
   if n!=2:raise ValueError('N2_SOURCE_SCOPE')
   family=p['family']
   if family=='FRONT_REAR':core=contract.core_first(W,L)
   elif family=='LEFT_RIGHT':core=frames.local_core(W,L)
   else:raise ValueError('UNSUPPORTED_FAMILY')
   if core is None or not audit.equal(core,p['core']):raise ValueError('SOURCE_CORE_RECONSTRUCTION_MISMATCH')
   if family=='LEFT_RIGHT' and audit.evaluate_core(core)['errors']:raise ValueError('CORE_FRAME_UNVERIFIED')
   local=p['local_model'];uids=[u['id']for u in local['units']]
   if sorted(uids)!=['A','B']:raise ValueError('EXACT_AB_UNITS')
   roots={};expected_ops={};expected_openings={}
   for u in local['units']:
    uid=u['id'];owner=core.get('unit_ownership',{}).get(uid,[core['units'][uid]])
    if not audit.equal(u['ownership'],owner):raise ValueError('SOURCE_UNIT_OWNERSHIP')
    box=list(map(F,owner[0]));cx=F(core['entry_centers']['A'][0]);y=F(core['band'][1]);yt=F(core['band'][3]);lo,hi=(y-F('.15'),y)if uid=='A'else(yt,yt+F('.15'))
    roots[uid]=[cx,box[3]-F('.4')if uid=='A'else box[1]+F('.4')]
    opening={'id':uid+'.entry','rect':list(map(str,(cx-F('.65'),lo,cx+F('.65'),hi))),'host_wall_id':uid+'.unit_boundary','connects':['lobby',uid+'.entry_circulation'],'operation_kind':'sliding_study','operation_witness_status':'NOT_EVALUATED'}
    scratch={'openings':[opening]};entry.install(scratch);expected_openings[uid]=scratch['openings'][0];expected_ops[uid]=scratch['operations']['doors'][0]
   for frame in ('local_model','world_model'):
    tick();model=p[frame]
    if F(str(model.get('profile',{}).get('body_m','-1')))!=F('.7'):raise ValueError('UNSUPPORTED_SOURCE_BODY_PROFILE')
    if 'source_geometry_contract'in model and F(str(model['source_geometry_contract'].get('body_m','-1')))!=F('.7'):raise ValueError('SOURCE_GEOMETRY_BODY_PROFILE')
    swapped=family=='LEFT_RIGHT'and frame=='world_model';units=model['units']
    if sorted(u['id']for u in units)!=['A','B']:raise ValueError('FRAME_UNIT_INVENTORY')
    fixedwalls=[checker.rect(r)for r in model['walls'].values()];panels=[checker.rect(o['open_panel'])for o in model.get('operations',{}).get('doors',[])]
    allfixtures=[checker.rect(r)for u in units for k,r in u['fixtures'].items()if not u['fixture_metadata'].get(k,{}).get('walkable')]
    for u in units:
     uid=u['id'];entryroot=world.point(roots[uid])if swapped else list(map(str,roots[uid]));wantopening=world.geometry(expected_openings[uid])if swapped else expected_openings[uid];wantop=world.geometry(expected_ops[uid])if swapped else expected_ops[uid]
     opens=[o for o in model['openings']if o['id']==uid+'.entry'];ops=[o for o in model.get('operations',{}).get('doors',[])if o.get('opening_id')==uid+'.entry']
     if len(opens)!=1 or len(ops)!=1 or not audit.equal(opens[0],wantopening)or not audit.equal(ops[0],wantop):raise ValueError('SOURCE_ENTRY_INSTALLATION_BINDING')
     owner=[checker.rect(r)for r in u['ownership']];expected_owner=core.get('unit_ownership',{}).get(uid,[core['units'][uid]])
     if swapped:expected_owner=[world.rect(r)for r in expected_owner]
     if not audit.equal(u['ownership'],expected_owner):raise ValueError('FRAME_OWNERSHIP_BINDING')
     # This point is the fixed constructor root (assemble114:142), not copied from a route.
     from public_program_audit118 import sweeps as public_sweeps, q, hit, covered
     for name in ('guest_living','guest_dining'):
      tick();path=u.get('scenario_routes',{}).get(name)
      rec={'frame':frame,'unit':uid,'route':name,'source_root':list(map(str,entryroot)),'root_basis':'assemble114.py:142 fixed constructor entry point; not universal standing-region constraint','errors':[],'missing':[]}
      if type(path)is not list or not 2<=len(path)<=256:
       rec['missing'].append('REQUIRED_ROUTE_MISSING_OR_BOUND');reports.append(rec);continue
      if not audit.equal(path[0],entryroot):rec['errors'].append('SOURCE_ENTRY_ROOT_MISMATCH')
      dst=u.get('public_program',{}).get('destinations',{}).get(name)
      if type(dst)is not dict or dst.get('activity_id')not in u['activities'] or dst.get('fixture_id')not in u['fixtures']:
       rec['missing'].append('ACTUAL_TARGET_ROLE_BINDING');reports.append(rec);continue
      if name=='guest_living' and (dst['activity_id']!='sofa1_front' or dst['fixture_id']!='sofa1'):rec['missing'].append('LIVING_SOURCE_ROLE_UNSUPPORTED')
      if name=='guest_dining' and dst.get('binding')!='actual_dining_operation_standing_endpoint':rec['missing'].append('DINING_SOURCE_OPERATION_BINDING')
      try:pieces=public_sweeps(path)
      except (ValueError,TypeError,IndexError):rec['errors'].append('INVALID_ORTHOGONAL_PATH');reports.append(rec);continue
      private=[q(v)for key,rs in u['rooms'].items()if key.startswith('bed')or key=='bath'for v in rs]
      kitchen=[q(v)for v in u['rooms'].get('kitchen',[])]+[q(v)for key,v in u['activities'].items()if key.startswith('kitchen')]
      for piece in pieces:
       tick()
       if not covered(piece,owner):rec['errors'].append('BODY_OUTSIDE_OWNERSHIP')
       if any(hit(piece,v)for v in private):rec['errors'].append('BODY_CROSSES_PRIVATE_REGION')
       if any(hit(piece,v)for v in kitchen):rec['errors'].append('BODY_CROSSES_EXPLICIT_KITCHEN_WORK_REGION')
      rec['segments']=len(pieces);rec['body_m']='0.7';reports.append(rec)
   # One local direct source audit; world is consumed from the exact live fresh result.
   from public_program_audit118 import examine
   tick();local_public=examine(p['local_model']);tick()
   serving=[]
   source_hashes={'kitchen_module117.py':hashlib.sha256(captured['kitchen_module117.py']).hexdigest(),'fixture_reference':json.loads(captured['fixture_catalog114.json'])['source_file_sha256']}
   for frame in ('local_model','world_model'):
    for unit in p[frame]['units']:
     tick();serving.append(serving_binding250(p[frame],unit,frame,family=='LEFT_RIGHT'and frame=='world_model',tick,source_hashes))
   result={'serving':serving,'routes':reports,'local_public':local_public,'world_public':world_witnesses,'source_public_sha':__import__('hashlib').sha256(captured['public_program_audit118.py']).hexdigest(),'source_root_sha':__import__('hashlib').sha256(captured['assemble114.py']).hexdigest(),'local_source_calls':1,'world_source_calls':0}
   # Imported code/data cannot change between loading and its use.
   for n,b in captured.items():
    tick()
    if (root/n).read_bytes()!=b:raise ValueError('TEMP_CHECKER_TREE_MUTATION')
  finally:
   sys.path[:]=oldpath
   for n,old in saved.items():
    if old is None:sys.modules.pop(n,None)
    else:sys.modules[n]=old
  if capture(tick)!=captured:raise ValueError('CHECKER_SOURCE_CHANGED_DURING_RUN')
 return result


def serving_binding250(model,unit,frame,swapped,tick,source_hashes):
 """Binding kernel only. Authority additionally requires evaluate's live replay join.
 No routing, source rebuilding, public examine, or geometry mutation here.
 """
 from fractions import Fraction as F
 from contract114 import digest
 from public_program_audit118 import q,covered,hit
 from typed_public_access120 import parts
 from world_transform125 import geometry as swap_geometry
 def number(v):
  if type(v)not in (str,int,F):raise ValueError('EXACT_SCALAR_TYPE_NO_BOOL_FLOAT')
  return F(v)
 uid=unit['id'];row={'frame':frame,'unit':uid,'route':'kitchen_to_dining_floor','scope':'SOURCE117_SERVING_START_PORT_OWNERSHIP_BINDING','errors':[],'missing':[],'binding_complete':False,'repair_authority':False}
 try:
  tick()
  if F(str(model['profile']['body_m']))!=F('.7'):raise ValueError('UNSUPPORTED_SOURCE_BODY_PROFILE')
  recs=[r for r in model['module_placements']if r['unit_id']==uid and r['room_id']=='kitchen']
  ops=[o for o in model['operations']['kitchen']if o['unit']==uid]
  if len(recs)!=1 or len(ops)!=1:raise ValueError('KITCHEN_SOURCE_INVENTORY')
  rec=recs[0];base=rec['module'];op=ops[0];sy=-1 if uid=='B'else 1
  collections=[model['walls'],model['wall_hosts'],model['module_ports'],model['module_placements'],unit['ownership'],unit['rooms'],unit['fixtures'],unit['activities'],base['walls'],base['wall_hosts'],base['unit']['fixtures'],base['unit']['activities']]
  if any(len(v)>4000 for v in collections)or sum(len(v)for v in unit['rooms'].values())>4000:raise ValueError('SERVING_READSET_BOUND')
  if base['schema']!='KITCHEN_MODULE117'or rec['module_hash']!=digest(base):raise ValueError('KITCHEN_MODULE_HASH_SCHEMA')
  if base['source_binding']['producer_sha256']!=source_hashes['kitchen_module117.py']or base['source_binding']['fixture_source_sha256']!=source_hashes['fixture_reference']:raise ValueError('KITCHEN_SOURCE_IDENTITY')
  if base['placement_contract']['allowed_transforms']!=['translation','axis_reflection']or base['placement_contract']['uniform_scale_allowed']is not False:raise ValueError('KITCHEN_SOURCE_TRANSFORM_CONTRACT')
  if base['input_program']['body_m']!='.7':raise ValueError('KITCHEN_SOURCE_BODY')
  tf=rec['transform'];want=[[0,sy],[1,0]]if swapped else[[1,0],[0,sy]]
  if set(tf)!={'matrix','translation'}or type(tf['matrix'])is not list or len(tf['matrix'])!=2 or any(type(v)is not list or len(v)!=2 for v in tf['matrix']):raise ValueError('KITCHEN_FRAME_D4_BINDING')
  if [[number(x)for x in v]for v in tf['matrix']]!=want or len(tf['translation'])!=2:raise ValueError('KITCHEN_FRAME_D4_BINDING')
  tr=list(map(number,tf['translation']))
  def pt(v):
   v=list(map(number,v));return tuple(sum(F(want[i][j])*v[j]for j in range(2))+tr[i]for i in range(2))
  def rr(v):
   a,b,c,d=map(number,v);ps=[pt(p)for p in ((a,b),(a,d),(c,b),(c,d))];return(min(p[0]for p in ps),min(p[1]for p in ps),max(p[0]for p in ps),max(p[1]for p in ps))
  prefix=uid+'.kitchen.';wm={k:prefix+k for k in base['walls']};hm={k:prefix+k for k in base['wall_hosts']}
  expected_map={**wm,**hm,'K.kitchen':uid+'.kitchen','K.public_access':uid+'.kitchen_public_access','K.kitchen.entry':prefix+'entry','K.port':prefix+'port','kitchen':'kitchen',**{k:k for k in base['unit']['fixtures']},**{k:k for k in base['unit']['activities']}}
  if rec['id_map']!=expected_map:raise ValueError('KITCHEN_INSTALLER_ID_ROLE_MAP')
  for kind,actual,mapping in [('walls',model['walls'],wm),('wall_hosts',model['wall_hosts'],hm)]:
   for k,v in base[kind].items():
    tick()
    if q(actual[mapping[k]])!=rr(v):raise ValueError('KITCHEN_ACTUAL_SOURCE_'+kind)
  for kind in ('fixtures','activities'):
   for k,v in base['unit'][kind].items():
    if q(unit[kind][k])!=rr(v):raise ValueError('KITCHEN_ACTUAL_SOURCE_'+kind)
  if [q(v)for v in unit['rooms']['kitchen']]!=[rr(v)for v in base['unit']['rooms']['kitchen']]:raise ValueError('KITCHEN_SOURCE_ROOM')
  ports=[p for p in model['module_ports']if p['id']==prefix+'port']
  if len(ports)!=1 or len(base['external_ports'])!=1:raise ValueError('KITCHEN_PORT_INVENTORY')
  bp=base['external_ports'][0];port=ports[0]
  expected_port=dict(bp,id=prefix+'port',opening_id=prefix+'entry',role_id=uid+'.kitchen_public_access',rect=list(map(str,rr(bp['rect']))),center=list(map(str,pt(bp['center']))))
  def equal(a,b,key=''):
   numeric=key in ('rect','center','body_width','matrix','translation')
   if type(a)is dict and type(b)is dict:return set(a)==set(b)and all(equal(a[k],b[k],k)for k in a)
   if type(a)is list and type(b)is list:return len(a)==len(b)and all(equal(x,y,key)for x,y in zip(a,b))
   if numeric:return number(a)==number(b)
   return type(a)is type(b)and a==b
  if not equal(port,expected_port):raise ValueError('KITCHEN_PORT_BINDING')
  source_open=base['openings'][0];opens=[o for o in model['openings']if o['id']==prefix+'entry']
  expected_open=dict(source_open,id=prefix+'entry',rect=list(map(str,rr(source_open['rect']))),host_wall_id=hm[source_open['host_wall_id']],connects=[expected_map[x]for x in source_open['connects']])
  if len(opens)!=1 or not equal(opens[0],expected_open):raise ValueError('KITCHEN_OPENING_BINDING')
  so=base['operations']['kitchen'][0]
  for field in ('profile','kind','source_contract','assumptions'):
   if op[field]!=so[field]:raise ValueError('KITCHEN_OPERATION_SOURCE_PROFILE')
  root=pt(so['workpoint']);access=pt(so['access_point'])
  act=q(unit['activities']['kitchen_work']);center=((act[0]+act[2])/2,(act[1]+act[3])/2)
  if root!=access or root!=center or tuple(map(number,op['workpoint']))!=root or tuple(map(number,op['access_point']))!=root:raise ValueError('KITCHEN_WORK_ACCESS_BINDING')
  # Canonical operation map is NOT the physical module placement map.
  local_t=tr[::-1]if swapped else tr
  canonical={'matrix':[[-1,0],[0,sy]],'translation':[str(local_t[0]),str(-local_t[1]if uid=='A'else local_t[1])]}
  if swapped:canonical=swap_geometry({'canonical_transform':canonical})['canonical_transform']
  if not equal(op['canonical_transform'],canonical)or not equal(op['canonical_isometry'],canonical):raise ValueError('KITCHEN_CANONICAL_BINDING')
  apron=[rr(v)for v in base['unit']['rooms']['public_access']]
  if [q(v)for v in model['module_aprons'][uid+'.kitchen']]!=apron:raise ValueError('KITCHEN_APRON_BINDING')
  # Source resolver validates source roles and opening-use, not room usefulness.
  roleparts=parts(model,unit,uid+'.kitchen_public_access',opening_id=prefix+'entry')
  owner=[q(v)for v in unit['ownership']];pc=pt(bp['center']);h=F('.35')
  footprints={'workpoint':(root[0]-h,root[1]-h,root[0]+h,root[1]+h),'port':(pc[0]-h,pc[1]-h,pc[0]+h,pc[1]+h)}
  queries=[(v,owner)for v in footprints.values()]+[(v,owner)for v in apron]+[(footprints['port'],roleparts)]
  rect_count=len(owner)+len(roleparts)+len(apron)+len(model['walls'])+sum(len(u['fixtures'])for u in model['units'])
  if rect_count>4000 or len(queries)>64:raise ValueError('SERVING_RECT_BOUND')
  work=0
  for r,regions in queries:
   tick();xs={r[0],r[2]}|{v[i]for v in regions for i in (0,2)if r[0]<v[i]<r[2]};ys={r[1],r[3]}|{v[i]for v in regions for i in (1,3)if r[1]<v[i]<r[3]}
   work+=(len(xs)-1)*(len(ys)-1)*max(1,len(regions))
  if work>2000000:raise ValueError('SERVING_COVERAGE_WORK_BOUND')
  row.update(binding_complete=True,source_root=list(map(str,root)),source_port=list(map(str,pc)),module_hash=rec['module_hash'],body_m='.7',role_id=uid+'.kitchen_public_access',model_hash=digest(model))
  for name,r in footprints.items():
   tick()
   if not covered(r,owner):row['errors'].append({'code':'SOURCE_BOUND_BODY_OUTSIDE_OWNERSHIP','pose':name,'body_rect':list(map(str,r))})
  for r in apron:
   tick()
   if not covered(r,owner):row['errors'].append({'code':'SOURCE_BOUND_APRON_OUTSIDE_OWNERSHIP','rect':list(map(str,r))})
  if not covered(footprints['port'],roleparts):row['missing'].append('PORT_NOT_ON_SOURCE_LOGICAL_ACCESS_VIEW')
  path=unit.get('scenario_routes',{}).get('kitchen_to_dining_floor')
  if not path:row['missing'].append('SERVING_ROUTE_NO_WITNESS_NOT_GLOBAL_INFEASIBILITY')
  elif tuple(map(number,path[0]))!=root:row['missing'].append('SERVING_SOURCE_START_MISMATCH')
  row['route_present']=bool(path)
  try:
   row['target_binding']=serving_target250(model,unit,swapped,tick);row['target_binding_complete']=True
  except (KeyError,TypeError,ValueError,IndexError,ZeroDivisionError,AttributeError)as ex:
   row['target_binding_complete']=False;row['missing'].append('SERVING_TARGET_UNPROVEN:'+str(ex))
 except (KeyError,TypeError,ValueError,IndexError,ZeroDivisionError,AttributeError)as e:
  row['binding_complete']=False;row['errors']=[];row['missing'].append('SERVING_BINDING_UNPROVEN:'+str(e))
 return row


def serving_target250(model,unit,swapped,tick):
 """Exact source dining destination projection; NO motion/examine rerun.
 Motion authority comes only from same-model public118 witness after it ran
 the explicit actual_dining_operation_standing_endpoint branch.
 """
 from fractions import Fraction as F
 from contract114 import digest
 from public_program_audit118 import q
 def num(v):
  if type(v)not in(str,int,F):raise ValueError('TARGET_EXACT_NUMBER_NO_BOOL_FLOAT')
  return F(v)
 dst=unit['public_program']['destinations']['kitchen_to_dining_floor']
 if type(dst)is not dict or dst.get('binding')!='actual_dining_operation_standing_endpoint':raise ValueError('SERVING_ACTUAL_DINING_BINDING_REQUIRED')
 p=unit['dining_module_placement'];m=p['module'];uid=unit['id'];sy=-1 if uid=='B'else 1
 six=m['schema']=='SIX_PLACE_PLANAR_SOURCE_STUDY_V1'
 if not six and m['schema']!='DINING_CAPACITY_MODULE118_PROPOSAL':raise ValueError('UNSUPPORTED_DINING_SOURCE')
 if p['module_hash']!=digest(m):raise ValueError('SERVING_DINING_MODULE_HASH')
 if len(m['fixtures'])>64 or len(m['seating']['instances'])>64:raise ValueError('SERVING_TARGET_BOUND')
 side='right'if six else'east';targetfixture='dining_chair_'+side;activity='dining_'+side
 if dst.get('fixture_id')!=targetfixture or dst.get('activity_id')!=activity:raise ValueError('SERVING_SOURCE_DESTINATION_ROLE')
 expected_ids={k:'dining_table'if k=='table'else'dining_'+k for k in m['fixtures']}
 if p['id_map']!=expected_ids or len(set(expected_ids.values()))!=len(expected_ids):raise ValueError('SERVING_DINING_INSTALLER_IDS')
 tf=p['transform'];mat=tf['matrix'];want=[[0,sy],[1,0]]if swapped else[[1,0],[0,sy]]
 if type(mat)is not list or len(mat)!=2 or any(type(r)is not list or len(r)!=2 for r in mat)or [[num(v)for v in r]for r in mat]!=want:raise ValueError('SERVING_DINING_FRAME_D4')
 if len(tf['translation'])!=2:raise ValueError('SERVING_DINING_TRANSLATION')
 tr=list(map(num,tf['translation']))
 def rr(r):
  a,b,c,d=map(num,r);points=[tuple(sum(want[i][j]*v[j]for j in range(2))+tr[i]for i in range(2))for v in ((a,b),(a,d),(c,b),(c,d))]
  return(min(v[0]for v in points),min(v[1]for v in points),max(v[0]for v in points),max(v[1]for v in points))
 for k,r in m['fixtures'].items():
  tick()
  if q(unit['fixtures'][expected_ids[k]])!=rr(r):raise ValueError('SERVING_ACTUAL_DINING_FIXTURE')
 seats=[s for s in m['seating']['instances']if s['fixture_id']=='chair_'+side]
 if len(seats)!=1:raise ValueError('SERVING_SEAT_INVENTORY')
 seat=seats[0];rise=seat['rise_transfer'];standing=rr(rise['standing_body'])
 if rise.get('other_seats_remain_occupied')is not True:raise ValueError('SERVING_SOURCE_OCCUPANCY_STATE')
 if (standing[2]-standing[0],standing[3]-standing[1])!=(F('.7'),F('.7')):raise ValueError('SERVING_SOURCE_BODY')
 if six:
  if num(m['assumptions']['body_m'])!=F('.7')or num(m['assumptions']['chair_pull_m'])!=F('.4'):raise ValueError('SERVING_DINING_SOURCE_PROFILE')
 elif num(rise['source_body_m'])!=F('.7'):raise ValueError('SERVING_DINING_SOURCE_PROFILE')
 if q(unit['activities'][activity])!=standing:raise ValueError('SERVING_ACTUAL_STANDING_ACTIVITY')
 end=((standing[0]+standing[2])/2,(standing[1]+standing[3])/2)
 ops=[o for o in model['operations']['dining_chairs']if o['unit']==uid and o['fixture_id']==targetfixture]
 if len(ops)!=1:raise ValueError('SERVING_CHAIR_OPERATION_INVENTORY')
 op=ops[0]
 if op['source_module_hash']!=p['module_hash']:raise ValueError('SERVING_CHAIR_SOURCE_HASH')
 for actual,src in [('closed_rect','closed_rect'),('open_rect','pulled_rect'),('occupied_body','occupied_body')]:
  if q(op[actual])!=rr(seat[src]):raise ValueError('SERVING_CHAIR_ACTUAL_STATE')
 a,b=rr(seat['closed_rect']),rr(seat['pulled_rect']);delta=(b[0]-a[0],b[1]-a[1])
 if tuple(map(num,op['translation']))!=delta or sum(abs(v)for v in delta)!=F('.4'):raise ValueError('SERVING_CHAIR_TRANSLATION')
 pb=rr(rise['pulled_occupied_body']);expected_egress=[((pb[0]+pb[2])/2,(pb[1]+pb[3])/2),end]
 if [tuple(map(num,v))for v in op['egress_route']]!=expected_egress:raise ValueError('SERVING_CHAIR_EGRESS_STATE')
 path=unit.get('scenario_routes',{}).get('kitchen_to_dining_floor')
 if path and tuple(map(num,path[-1]))!=end:raise ValueError('SERVING_ENDPOINT_NOT_SOURCE_STANDING_CENTER')
 return {'binding':'actual_dining_operation_standing_endpoint','fixture_id':targetfixture,'activity_id':activity,'module_hash':p['module_hash'],'seat_id':seat['id'],'standing_body':list(map(str,standing)),'source_endpoint':list(map(str,end)),'motion_recomputed':False,'motion_authority':'REQUIRES_SAME_PUBLIC118_EXPLICIT_BRANCH_WITNESS'}
