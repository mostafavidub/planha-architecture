"""Independent raw physical core, explicitly incomplete without named/current gates.
All original raw-core checks retained; stricter5..25 and explicit new-schema adapters.
No scope reduction, pending removal, historical report filtering or delivery admission.
"""
import hashlib,json
from pathlib import Path
from collections import Counter
from checker114 import F,BODY,rect,intersects,encloses,covered,sweeps,records,rectangles,digest,check_whole_privacy117
from open_front_placement_check import check_module_placements
from open_front_kitchen_study import ENGINE
VERSION='OPEN_FRONT_RAW_PHYSICAL_CORE_STUDY_V1'
def assess(model, *, workflow_context=None, comparison_only=False):
 errors=[];pending=[];counts={}
 def err(code,**data):errors.append(dict(code=code,**data))
 try:
  W,L,n=map(F,model['inputs']);frame=rect([0,0,W,L])
  if not 5<=W<=25 or not 5<=L<=25 or n!=2:err('INPUT_PROGRAM_DOMAIN')
  if model.get('contract_version')not in ('114-provisional-v1','115-provisional-v1'):err('UNSUPPORTED_CONSTRAINT_CONTRACT_VERSION')
  if F(model.get('profile',{}).get('body_m',0))!=BODY:err('MODEL_BODY_CONTRACT_BINDING')
  catalog=json.loads((ENGINE/'fixture_catalog114.json').read_text());catalog_hash=digest(catalog)
  source_path=ENGINE/catalog['source_file'];source_bytes=source_path.read_bytes();source=json.loads(source_bytes)
  if hashlib.sha256(source_bytes).hexdigest()!='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4' or catalog['source_file_sha256']!=hashlib.sha256(source_bytes).hexdigest():err('IMMUTABLE_REFERENCE_FILE_CHANGED')
  for kind,spec in catalog['types'].items():
   source_q=rect(source['units'][0]['fixtures'][spec['source_fixture_key']])
   if (F(spec['width_m']),F(spec['depth_m']))!=(source_q[2]-source_q[0],source_q[3]-source_q[1]) or spec['scale_allowed']is not False:err('CATALOG_REFERENCE_SIZE_MISMATCH',kind=kind)
  if model.get('fixture_catalog_hash')!=catalog_hash:err('FIXTURE_CATALOG_BINDING')
  units=model['units'];walls={k:rect(v)for k,v in model['walls'].items()};owners={};fixtures=[]
  if len(units)!=2:err('UNIT_COUNT')
  for k,w in walls.items():
   if not encloses(frame,w):err('WALL_OUTSIDE_FRAME',wall=k)
  for u in units:
   uid=u['id'];owner=[rect(v)for v in u['ownership']];owners[uid]=owner
   for q in owner:
    if not encloses(frame,q):err('OWNERSHIP_OUTSIDE_FRAME',unit=uid)
   rooms={k:[rect(q)for q in v]for k,v in u['rooms'].items()}
   for k,rs in rooms.items():
    for r in rs:
     if not covered(r,owner):err('ROOM_OUTSIDE_OWNERSHIP',room=k)
   names=list(rooms)
   for i,a in enumerate(names):
    for b in names[i+1:]:
     if any(intersects(q,r)for q in rooms[a]for r in rooms[b]):err('ROOM_OVERLAP',rooms=[a,b])
   local={k:rect(v)for k,v in u['fixtures'].items()}
   for k,q in local.items():
    fixtures.append((uid,k,q))
    if not covered(q,owner):err('FIXTURE_OUTSIDE_OWNERSHIP',fixture=k)
    for wk,w in walls.items():
     if intersects(q,w):err('FIXTURE_WALL_COLLISION',fixture=k,wall=wk)
   routes=dict(u.get('routes',{}));routes.update(u.get('scenario_routes',{}))
   if not routes:pending.append('MISSING_BODY_ROUTES:'+uid)
   for rk,path in routes.items():
    for q in sweeps(path):
     if not covered(q,owner):err('BODY_OUTSIDE_OWNERSHIP',route=rk)
     for wk,w in walls.items():
      if intersects(q,w):err('BODY_WALL_COLLISION',route=rk,wall=wk)
     for fk,f in local.items():
      kind=u.get('fixture_metadata',{}).get(fk,{}).get('kind')
      source_task_exception=(kind=='shower_floor'and rk in('shower','shower_use'))or(kind=='WC_iranian'and rk=='WC_use')
      if not source_task_exception and intersects(q,f):err('BODY_FIXTURE_COLLISION',route=rk,fixture=fk)
   beds=[k for k in rooms if k.split('.')[-1].startswith('bed')]
   if not 1<=len(beds)<=4:err('BEDROOM_PROGRAM_COUNT',unit=uid)
   if F(model.get('program',{}).get('bedrooms_per_unit',0))!=len(beds):err('DECLARED_BEDROOM_PROGRAM_BINDING',unit=uid)
   metadata=u.get('fixture_metadata',{});inventory=Counter()
   for fk,q in local.items():
    md=metadata.get(fk,{});kind=md.get('kind');spec=catalog['types'].get(kind);inventory[kind]+=1
    if kind=='dining_table6':
     spec={'width_m':'2.2','depth_m':'1','allowed_plan_rotations_deg':[0,90,180,270]}
    if kind=='single_bed':
     spec={'width_m':'1.9','depth_m':'.9','allowed_plan_rotations_deg':[0,90,180,270]}
     source_path=ENGINE/'references/CAPACITY_PROGRAM118_SOURCE.json'
     if hashlib.sha256(source_path.read_bytes()).hexdigest()!='427cde4c55e57ea7c26ff52bb2651859750b93913cc86ecdf2751fad37566e8f':err('TWIN_SOURCE_CHANGED')
    if spec is None:err('UNKNOWN_FIXTURE_TYPE',fixture=fk);continue
    rotation=md.get('rotation_deg')
    if rotation not in spec['allowed_plan_rotations_deg']:err('FIXTURE_ROTATION',fixture=fk);continue
    expected=(F(spec['width_m']),F(spec['depth_m']))
    if rotation%180:expected=expected[::-1]
    if (q[2]-q[0],q[3]-q[1])!=expected:err('IMMUTABLE_FIXTURE_SIZE_CHANGED',fixture=fk)
   twin_rooms={p['room_id']for p in model.get('module_placements',[])if p.get('unit_id')==uid and p.get('module',{}).get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'}
   expected=Counter({k:1 for k in catalog['types']});expected['bed']=len(beds)-len(twin_rooms);expected['closet']=len(beds)
   if twin_rooms:expected['single_bed']=2*len(twin_rooms)
   roles=model.get('program',{}).get('sleep_roles')
   if roles is not None:
    actual_roles=['twin'if br in twin_rooms else'double'for br in sorted(beds)]
    if roles!=actual_roles:err('SLEEP_ROLE_MODULE_BINDING',unit=uid)
    if sorted(roles)==['double','twin','twin']:
     expected['armchair1']=2;expected['armchair2']=2
     if model['program'].get('design_occupants_per_unit')!=6:err('SIX_PERSON_PROGRAM_OCCUPANCY_BINDING',unit=uid)
   # Installed source dining inventory is independent of sleep occupancy.
   # No module means the legacy catalog inventory remains required.
   if u.get('dining_module_placement') is not None:
    try:
     from dining_inventory119 import counts as source_dining_counts
     dining_counts=source_dining_counts(u)
     if 'dining_table6'in dining_counts:expected.pop('dining_table',None)
     for kind,count in dining_counts.items():expected[kind]=count
    except (KeyError,ValueError,TypeError,IndexError)as ex:err('DINING_SOURCE_INVENTORY_BINDING',unit=uid,detail=str(ex))
   if inventory!=expected:err('FIXTURE_INVENTORY',unit=uid,expected=dict(expected),actual=dict(inventory))
   for br in beds:
    for kind in (('single_bed','closet')if br in twin_rooms else('bed','closet')):
     members=[fk for fk,q in local.items()if metadata.get(fk,{}).get('kind')==kind and covered(q,rooms[br])]
     if len(members)!=(2 if kind=='single_bed'else 1):err('BEDROOM_FIXTURE_MEMBERSHIP',room=br,kind=kind)
   if any(not covered(q,[r for rs in rooms.values()for r in rs]+list(walls.values())) for q in owner):err('UNACCOUNTED_OWNERSHIP_FLOOR',unit=uid)
  for i,(a,rs)in enumerate(owners.items()):
   for b,ss in list(owners.items())[i+1:]:
    if any(intersects(r,s)for r in rs for s in ss):err('UNIT_OWNERSHIP_OVERLAP',units=[a,b])
  for i,(u,k,q)in enumerate(fixtures):
   for v,j,r in fixtures[i+1:]:
    if intersects(q,r):err('FIXTURE_COLLISION',fixtures=[k,j])
  for op in model.get('openings',[]):
   q=rect(op['rect']);host_record=model.get('wall_hosts',{}).get(op.get('host_wall_id'));host=rect(host_record)if host_record is not None else walls.get(op.get('host_wall_id'))
   pocket_type=op.get('kind',op.get('operation_kind'))=='pocket_source113'
   if pocket_type:
    from open_front_operation_check import pocket_host_geometry117
    for code in pocket_host_geometry117(model,op,walls):err(code,opening=op['id'])
   elif host is None:pending.append('OPENING_UNCUT_HOST_BINDING_REQUIRED:'+op['id'])
   elif not encloses(host,q):err('OPENING_OUTSIDE_HOST',opening=op['id'])
   if host is not None and not pocket_type:
    pieces=[r for r in walls.values()if encloses(host,r)]+[rect(z['rect'])for z in model.get('openings',[])if z.get('host_wall_id')==op.get('host_wall_id')]
    if not covered(host,pieces):err('HOST_WALL_UNACCOUNTED_GAP',opening=op['id'])
    if any(intersects(q,w)for w in walls.values()):err('OPENING_NOT_ACTUALLY_CUT',opening=op['id'])
   vertical=(q[3]-q[1])>(q[2]-q[0]);axis=1 if vertical else 0
   low=q[axis]+BODY/2;high=q[axis+2]-BODY/2
   obstacles=list(walls.values())+[r for _,_,r in fixtures]
   values={low,high}
   for r in obstacles:
    values.update(v for v in (r[axis]-BODY/2,r[axis+2]+BODY/2)if low<=v<=high)
   ordered=sorted(values);values.update((a+b)/2 for a,b in zip(ordered,ordered[1:]))
   witness=False
   for t in values:
    if low>high or not low<=t<=high:continue
    crossing=(q[0]-BODY/2,t-BODY/2,q[2]+BODY/2,t+BODY/2)if vertical else(t-BODY/2,q[1]-BODY/2,t+BODY/2,q[3]+BODY/2)
    if encloses(frame,crossing)and not any(intersects(crossing,r)for r in obstacles):witness=True;break
   if not witness:err('NO_BODY_CROSSING_AT_ACTUAL_APERTURE',opening=op['id'])
  # Owner scope121: do not evaluate light, ventilation or required window inventory.
  # Preserve only geometry of window objects that actually exist in this model.
  for win in model.get('concept_windows',[]):
   q=rect(win['plan_rect']);host=walls.get(win.get('host_wall_id'))
   if host is None or not encloses(host,q):err('WINDOW_HOST_MISSING_OR_OUTSIDE',window=win['id'])
   if win.get('floor_portal')is not False or not 0<=F(win['sill_m'])<F(win['head_m']):err('WINDOW_HEIGHT_OR_FLOOR_PORTAL',window=win['id'])
  from open_front_operation_check import check_operations
  operation_owners=dict(owners)
  lobby=model.get('common_spaces',{}).get('lobby',[])
  if lobby:operation_owners['COMMON']=[rect(q)for q in lobby]
  oe,op=check_operations(model,operation_owners,walls,fixtures);errors.extend(oe);pending.extend(op)
  if model.get('module_placements')is not None:
   placement=check_module_placements(model);errors.extend(placement['errors']);pending.extend(placement['pending'])
  common=model.get('common_spaces',{});cr=model.get('common_routes',{})
  required={src+'_'+u['id']for src in ('stair','lift')for u in units}
  if set(cr)!=required:err('COMMON_ROUTE_INVENTORY')
  for name,path in cr.items():
   uid=name.rsplit('_',1)[-1];source=name.rsplit('_',1)[0]
   if source not in ('stair','lift')or uid not in owners:err('COMMON_ROUTE_UNKNOWN_ENDPOINT',route=name);continue
   core=rect(common[source]);start=tuple(F(v)for v in path[0])
   if not(core[0]<=start[0]<=core[2]and core[1]<=start[1]<=core[3]):err('COMMON_ROUTE_NOT_FROM_CORE',route=name)
   ownunit=next(u for u in units if u['id']==uid)
   entryparts=[rect(r)for r in ownunit['rooms'].get('entry_circulation',[])]
   end=tuple(F(v)for v in path[-1]);endbody=(end[0]-BODY/2,end[1]-BODY/2,end[0]+BODY/2,end[1]+BODY/2)
   if not covered(endbody,entryparts):err('COMMON_ROUTE_NOT_TO_REAL_ENTRY_FLOOR',route=name)
   for q in sweeps(path):
    if not encloses(frame,q):err('COMMON_BODY_OUTSIDE_FRAME',route=name)
    for wid,w in walls.items():
     if intersects(q,w):err('COMMON_BODY_WALL_COLLISION',route=name,wall=wid)
    for fu,fk,f in fixtures:
     if intersects(q,f):err('COMMON_BODY_FIXTURE_COLLISION',route=name,fixture=fk)
    for other,rs in owners.items():
     if other!=uid and any(intersects(q,r)for r in rs):err('COMMON_BODY_OTHER_UNIT',route=name,unit=other)
    for rkey,rs in ownunit['rooms'].items():
     if rkey not in ('entry_circulation','living') and any(intersects(q,rect(r))for r in rs):err('COMMON_BODY_PRIVATE_ROOM',route=name,room=rkey)
    othercore=rect(common['lift'if source=='stair'else'stair'])
    if intersects(q,othercore):err('COMMON_BODY_OTHER_CORE',route=name)
  if not cr:pending.append('COMMON_ROUTES_MISSING')
  if model.get('route_failures'):err('MISSING_REQUIRED_ACTIVITY_ROUTES',failures=model['route_failures'])
  for u in units:
   for target,point in u.get('route_targets',{}).items():
    path=u.get('routes',{}).get(target)
    if not path or tuple(map(F,path[-1]))!=tuple(map(F,point)):err('ROUTE_TARGET_BINDING',unit=u['id'],target=target)
   if set(u.get('activities',{}))!=set(u.get('route_targets',{})):err('ACTIVITY_ROUTE_INVENTORY',unit=u['id'])
  privacy=check_whole_privacy117(model);errors.extend(privacy['errors']);pending.extend(privacy['pending'])
  pending.extend(['VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED'])
  counts={'units':len(units),'fixtures':len(fixtures),'walls':len(walls),'windows':len(model.get('concept_windows',[]))}
 except (KeyError,ValueError,TypeError,IndexError,StopIteration,ZeroDivisionError)as e:err('MODEL_SCHEMA_OR_GEOMETRY_ERROR',detail=str(e))
 report={'checker_version':VERSION,'model_hash':digest(model),'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','errors':errors,'pending':sorted(set(pending)),'counts':counts,'privacy_evidence':locals().get('privacy',{}).get('evidence'),'placement_evidence':locals().get('placement'),'accepted':False,'release':False,'eligible_for_draft_export':not errors and not pending}
 report.update(eligible_for_draft_export=False,display_allowed=False,delivery_allowed=False,whole_physical_verified=False,
  missing_integrated_gates=['NAMED_RULE_CONTRACT','CURRENT_FUNCTIONAL_REQUIREMENTS','FULL_CURRENT_Q11'],
  scope='Raw physical core only. Existing capacity/quality pending retained. Supplemental boundary study is not full Q11. No historical report errors filtered.')
 return report
