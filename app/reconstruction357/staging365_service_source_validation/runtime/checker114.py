"""Independent rational geometry gates for GENERAL114. Never imports the producer.
Missing operational proof is NOT_EVALUATED, not a successful architectural plan.
Boundary contact is allowed; positive-area overlap is not. No daylight/legal claim.
"""
from fractions import Fraction
import hashlib,json
from pathlib import Path
from collections import Counter
F=lambda x:Fraction(str(x))
BODY=Fraction('0.7')
VERSION='GENERAL117_INDEPENDENT_CONCEPT_V1'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def rect(r):
 q=tuple(F(x) for x in r)
 if len(q)!=4 or q[0]>=q[2] or q[1]>=q[3]:raise ValueError('INVALID_RECTANGLE')
 return q
def intersects(a,b):return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
def encloses(a,b):return a[0]<=b[0] and a[1]<=b[1] and a[2]>=b[2] and a[3]>=b[3]
def covered(q,hosts):
 """Exact cell partition: holes cannot be silently replaced by a bounding box."""
 xs=sorted({q[0],q[2]}|{x for h in hosts for x in (h[0],h[2]) if q[0]<x<q[2]})
 ys=sorted({q[1],q[3]}|{y for h in hosts for y in (h[1],h[3]) if q[1]<y<q[3]})
 return all(any(h[0]<=a and b<=h[2] and h[1]<=c and d<=h[3] for h in hosts)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:]))
def sweeps(path,width=BODY):
 if not isinstance(path,list) or len(path)<2:raise ValueError('MISSING_ROUTE_PATH')
 p=[tuple(F(x)for x in point)for point in path];h=F(width)/2;out=[]
 for a,b in zip(p,p[1:]):
  if len(a)!=2 or len(b)!=2 or a==b or (a[0]!=b[0] and a[1]!=b[1]):raise ValueError('NON_ORTHOGONAL_OR_DEGENERATE_ROUTE')
  out.append((min(a[0],b[0])-h,min(a[1],b[1])-h,max(a[0],b[0])+h,max(a[1],b[1])+h))
 return out

def records(value):
 if isinstance(value,dict):return [dict(v,id=v.get('id',k)) for k,v in value.items()]
 if isinstance(value,list):return value
 raise ValueError('RECORD_COLLECTION_REQUIRED')
def rectangles(record):
 return [rect(r)for r in record['parts']]if 'parts'in record else [rect(record['rect'])]

def _evaluate_impl(model, *, workflow_context=None, comparison_only=False):
 errors=[];pending=[];counts={}
 def err(code,**data):errors.append(dict(code=code,**data))
 try:
  W,L,n=map(F,model['inputs']);frame=rect([0,0,W,L])
  if not 5<=W<=45 or not 5<=L<=45 or n!=2:err('INPUT_PROGRAM_DOMAIN')
  if model.get('contract_version')not in ('114-provisional-v1','115-provisional-v1'):err('UNSUPPORTED_CONSTRAINT_CONTRACT_VERSION')
  if F(model.get('profile',{}).get('body_m',0))!=BODY:err('MODEL_BODY_CONTRACT_BINDING')
  catalog=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text());catalog_hash=digest(catalog)
  source_path=Path(__file__).parent/catalog['source_file'];source_bytes=source_path.read_bytes();source=json.loads(source_bytes)
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
     source_path=Path(__file__).parent/'references/CAPACITY_PROGRAM118_SOURCE.json'
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
    from operation_check114 import pocket_host_geometry117
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
  from operation_check114 import check_operations
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
 from scope117 import reduce_scope117
 scope_doc=Path(__file__).parent/'references/CONCEPT_GATE_FA.md'
 if not scope_doc.is_file() or hashlib.sha256(scope_doc.read_bytes()).hexdigest()!='8804bca0ecb774c5186969f85c0d03b73766e23e20d30304b84f580c41a1d05e':
  report['errors'].append({'code':'CONCEPT_SCOPE_SOURCE_CHANGED'})
 report['scope_source']={'path':'references/CONCEPT_GATE_FA.md','sha256':'8804bca0ecb774c5186969f85c0d03b73766e23e20d30304b84f580c41a1d05e','source':'Pinned limited Concept contract from reference113, not technical approval'}
 report['nonleaf_interfaces']=[{'opening_id':o['id'],'kind':o.get('kind'),'hardware_status':'NOT_EVALUATED' if o.get('kind')=='core_access_interface' else 'NO_LEAF_SOURCE_ARCH'} for o in model.get('openings',[]) if o.get('kind') in ('core_access_interface','permanent_open_arch')]
 from q11_boundary118 import examine as examine_q11
 q11=examine_q11(model,workflow_context=workflow_context);report['errors'].extend(q11['errors']);report['pending'].extend(q11['pending']);report['q11_evidence']=q11['evidence']
 report['contract_addendum']='BLUEPRINT_Q11_MANDATORY_SOURCE_COMPLETENESS118_V1'
 from rule_contract118 import attach_rule_contract
 from named_checks118 import adapters_for_workflow,APPLICABILITY_ADAPTERS
 adapters=adapters_for_workflow(workflow_context)
 if comparison_only:
  adapters['long_corridor_necessity']=lambda m:{'status':'NOT_EVALUATED','witness':{'code':'EXCLUDED_FOR_NONCIRCULAR_COMPARISON','model_hash':digest(m)},'scope':'Internal comparison prerequisite only; Q04 not accepted or waived.'}
 return attach_rule_contract(model,reduce_scope117(report),trusted_evaluators=adapters,context={'stage':'concept_internal','batch_models':[model]},applicability_evaluators=APPLICABILITY_ADAPTERS)

def evaluate(model, *, workflow_context=None):
 return _evaluate_impl(model,workflow_context=workflow_context)

def evaluate_for_circulation_comparison(model, *, workflow_context=None):
 report=_evaluate_impl(model,workflow_context=workflow_context,comparison_only=True)
 remaining=[p for p in report['pending']if p!='RULE_NOT_EVALUATED:long_corridor_necessity']
 report['noncomparison_pending']=remaining
 report['excluded_requirements']=['long_corridor_necessity']
 report['comparison_scope']='All existing mandatory evaluations except explicitly unevaluated Q04, to avoid circular whole-alternative evaluation; not export admission.'
 report['status']='FAIL'if report['errors']else'NOT_EVALUATED'if remaining else'PASS_NONCIRCULAR_PHYSICAL_SCOPED'
 report.update(eligible_for_draft_export=False,draft_review_allowed=False,accepted=False,release=False,technical_accepted=False,public_release=False,all_rules_approved=False)
 return report

check=evaluate

def check_module(module, _twin=False):
 """Private bedroom component only; never whole-model admission.
 Scope omission of kitchens/core/bath is explicit, not a whole-gate exemption.
 All operation witnesses are freshly evaluated against actual fragment geometry.
 """
 errors=[];pending=[];evidence={}
 def err(code,**data):errors.append(dict(code=code,**data))
 try:
  if module.get('schema')!=('PRIVATE_TWIN_ROOM_MODULE118'if _twin else'PRIVATE_ROOM_MODULE116'):err('MODULE_SCHEMA')
  if module.get('contract_version')!=('PRIVATE_TWIN_SOURCE_A9_V1'if _twin else'PRIVATE_ROOM_GEOMETRY_OPERATIONS_V1'):err('MODULE_CONSTRAINT_VERSION')
  program=module.get('input_program',{})
  if F(program.get('body_m',0))!=BODY or F(program.get('bedrooms',0))!=1:err('MODULE_PROGRAM_BODY_BINDING')
  binding=module.get('source_binding',{})
  producer_file=Path(__file__).with_name('twin_module118.py'if _twin else'bedroom_module116.py')
  if not producer_file.exists()or binding.get('producer_sha256')!=hashlib.sha256(producer_file.read_bytes()).hexdigest():err('MODULE_PRODUCER_SOURCE_CHANGED')
  if binding.get('fixture_source_sha256')!='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4':err('MODULE_REFERENCE_BINDING')
  placement=module.get('placement_contract',{})
  if placement.get('uniform_scale_allowed')is not False or placement.get('revalidate_after_placement')is not True:err('MODULE_PLACEMENT_CONSTRAINT_BINDING')
  unit=module['unit'];uid=unit['id'];owners={uid:[rect(r)for r in unit['ownership']]};walls={k:rect(r)for k,r in module['walls'].items()};bounds=rect(module['bounds'][0]if len(module['bounds'])==1 and isinstance(module['bounds'][0],list)else module['bounds'])
  rooms={k:[rect(r)for r in rr]for k,rr in unit['rooms'].items()};fixtures=[(uid,k,rect(r))for k,r in unit['fixtures'].items()]
  catalog=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text());source_bytes=(Path(__file__).parent/catalog['source_file']).read_bytes()
  if hashlib.sha256(source_bytes).hexdigest()!='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4':err('IMMUTABLE_REFERENCE_FILE_CHANGED')
  source=json.loads(source_bytes)
  if module.get('fixture_catalog_hash')!=digest(catalog):err('MODULE_FIXTURE_CATALOG_BINDING')
  kinds=[]
  for _,fid,q in fixtures:
   md=unit['fixture_metadata'][fid];kind=md['kind'];kinds.append(kind)
   if kind not in (('single_bed','closet')if _twin else('bed','closet')):err('UNEXPECTED_MODULE_FIXTURE',fixture=fid);continue
   if kind=='single_bed':
    source_path=Path(__file__).parent/'references/CAPACITY_PROGRAM118_SOURCE.json'
    if hashlib.sha256(source_path.read_bytes()).hexdigest()!='427cde4c55e57ea7c26ff52bb2651859750b93913cc86ecdf2751fad37566e8f':err('A9_SINGLE_BED_SOURCE_CHANGED')
    size=(F('1.9'),F('.9'));rot=md['rotation_deg']
   else:
    spec=catalog['types'][kind];sq=rect(source['units'][0]['fixtures'][spec['source_fixture_key']]);size=(sq[2]-sq[0],sq[3]-sq[1]);rot=md['rotation_deg']
   if rot not in (0,90,180,270):err('MODULE_FIXTURE_ORIENTATION',fixture=fid)
   if rot%180:size=size[::-1]
   if (q[2]-q[0],q[3]-q[1])!=size:err('MODULE_FIXTURE_RIGID_SIZE',fixture=fid)
   if not covered(q,owners[uid]):err('MODULE_FIXTURE_OUTSIDE_OWNER',fixture=fid)
   if any(intersects(q,w)for w in walls.values()):err('MODULE_FIXTURE_WALL_COLLISION',fixture=fid)
  if Counter(kinds)!=Counter({'single_bed':2,'closet':1}if _twin else{'bed':1,'closet':1}):err('MODULE_PRIVATE_FIXTURE_INVENTORY')
  if _twin:
   if set(k for k,v in unit['fixture_metadata'].items()if v['kind']=='single_bed')!={'bed1.bedA','bed1.bedB'}:err('TWIN_INSTANCE_ID_INVENTORY')
   required={'bed1.bedA_front','bed1.bedA_back','bed1.bedB_front','bed1.bedB_back','bed1.closet_front','bed1.changing'}
   if set(unit['activities'])!=required:err('TWIN_EACH_BED_ACTIVITY_INVENTORY')
   profile=module.get('sleep_profile',{})
   if profile.get('id')!='A9_F5_SINGLE_BED_0.9x1.9'or profile.get('source_sha256')!='427cde4c55e57ea7c26ff52bb2651859750b93913cc86ecdf2751fad37566e8f'or profile.get('source_line')!=378 or profile.get('scale_allowed')is not False or set(profile.get('target_fixture_ids',[]))!={'bed1.bedA','bed1.bedB'}:err('TWIN_SLEEP_PROFILE_BINDING')
   if binding.get('double_module_base_source_sha256')!=hashlib.sha256(Path(__file__).with_name('bedroom_module116.py').read_bytes()).hexdigest():err('TWIN_BASE_MODULE_SOURCE_CHANGED')
   for fid in('bed1.bedA','bed1.bedB'):
    bed=rect(unit['fixtures'][fid]);rotation=unit['fixture_metadata'][fid]['rotation_deg'];axis=1 if rotation%180==0 else 0
    low=list(bed);high=list(bed);low[axis+2]=bed[axis];low[axis]-=F('.9');high[axis]=bed[axis+2];high[axis+2]+=F('.9')
    actual={rect(unit['activities'][fid+'_front']),rect(unit['activities'][fid+'_back'])}
    if actual!={tuple(low),tuple(high)}:err('TWIN_BED_ACTIVITY_NOT_ACTUAL_ADJACENT_BAND',fixture=fid)

  for i,(_,fk,q)in enumerate(fixtures):
   for _,gk,r in fixtures[i+1:]:
    if intersects(q,r):err('MODULE_FIXTURE_COLLISION',fixtures=[fk,gk])
  for owner in owners[uid]:
   if not encloses(bounds,owner):err('MODULE_OWNERSHIP_OUTSIDE_BOUNDS')
   if not covered(owner,[q for rs in rooms.values()for q in rs]+list(walls.values())):err('MODULE_UNACCOUNTED_FLOOR')
  for rk,rs in rooms.items():
   if any(not covered(q,owners[uid])for q in rs):err('MODULE_ROOM_OUTSIDE_OWNERSHIP',room=rk)
   if any(intersects(q,w)for q in rs for w in walls.values()):err('MODULE_ROOM_FLOOR_WALL_OVERLAP',room=rk)
  names=list(rooms)
  for i,a in enumerate(names):
   for b in names[i+1:]:
    if any(intersects(q,r)for q in rooms[a]for r in rooms[b]):err('MODULE_ROOM_OVERLAP',rooms=[a,b])
  ports=module.get('external_ports',[])
  if not ports:pending.append('MODULE_EXTERNAL_PORT_MISSING')
  portcenters={tuple(map(F,p['center']))for p in ports}
  for p in ports:
   q=rect(p['rect']);c=tuple(map(F,p['center']))
   if not(q[0]<=c[0]<=q[2]and q[1]<=c[1]<=q[3]):err('MODULE_PORT_CENTER_NOT_IN_ACTUAL_PORT')
   if max(q[2]-q[0],q[3]-q[1])<BODY:err('MODULE_PORT_TOO_NARROW')
   matches=[o for o in module['openings']if o['id']==p.get('opening_id')]
   if len(matches)!=1:err('MODULE_PORT_APERTURE_BINDING')
   else:
    opening=matches[0];ap=rect(opening['rect'])
    if p.get('role_id')not in opening['connects']:err('MODULE_PORT_ROLE_NOT_CONNECTED')
    touches=(q[2]==ap[0]or q[0]==ap[2])and max(q[1],ap[1])<min(q[3],ap[3])or(q[3]==ap[1]or q[1]==ap[3])and max(q[0],ap[0])<min(q[2],ap[2])
    if not touches:err('MODULE_PORT_APPROACH_NOT_ADJACENT_TO_APERTURE')
   body=(c[0]-BODY/2,c[1]-BODY/2,c[0]+BODY/2,c[1]+BODY/2)
   if not covered(body,[q])or not covered(q,owners[uid]):err('MODULE_PORT_APPROACH_NOT_REAL_OWNED_FLOOR')
  targets=unit.get('route_targets',{});routes=unit.get('routes',{})
  if not targets or set(targets)!=set(unit.get('activities',{})) or set(routes)!=set(targets):err('MODULE_ACTIVITY_ROUTE_INVENTORY')
  for rk,path in routes.items():
   if tuple(map(F,path[0]))not in portcenters:err('MODULE_ROUTE_NOT_FROM_PORT',route=rk)
   if rk not in targets or tuple(map(F,path[-1]))!=tuple(map(F,targets[rk])):err('MODULE_ROUTE_TARGET_BINDING',route=rk)
   for q in sweeps(path):
    if not covered(q,owners[uid]):err('MODULE_ROUTE_OUTSIDE_OWNER',route=rk)
    if any(intersects(q,z)for z in list(walls.values())+[q for _,_,q in fixtures]):err('MODULE_BODY_OBSTACLE_COLLISION',route=rk)
  for op in module['openings']:
   q=rect(op['rect']);h=rect(module['wall_hosts'][op['host_wall_id']]);parts=[r for r in walls.values()if encloses(h,r)]+[rect(o['rect'])for o in module['openings']if o['host_wall_id']==op['host_wall_id']]
   if not encloses(h,q)or not covered(h,parts):err('MODULE_APERTURE_HOST_PARTITION',opening=op['id'])
   if any(intersects(q,w)for w in walls.values()):err('MODULE_APERTURE_NOT_CUT',opening=op['id'])
  fragment=dict(module);fragment['units']=[unit]
  from operation_check114 import check_operations
  oe,op=check_operations(fragment,owners,walls,fixtures,components=('doors','closets'));errors.extend(oe);pending.extend(op)
  try:
   from privacy116 import examine_module
   pr=examine_module(fragment);errors.extend(pr['errors']);pending.extend(pr['pending']);evidence['privacy']=pr['evidence']
  except ImportError:pending.append('MODULE_PRIVACY_CHECK_NOT_AVAILABLE')
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as ex:err('MODULE_SCHEMA_OR_GEOMETRY_ERROR',detail=str(ex))
 return {'checker_version':'PRIVATE_MODULE116_INDEPENDENT_V1','module_hash':digest(module),'status':'FAIL_MODULE'if errors else'NOT_EVALUATED_MODULE'if pending else'PASS_MODULE_SCOPED','errors':errors,'pending':sorted(set(pending)),'evidence':evidence,'whole_model_pass':False,'placement_revalidation_required':True,'accepted':False,'release':False,'eligible_for_draft_export':False,'scope':['One bedroom/closet/entry component','Kitchen,wet rooms,core,site and whole-plan quality are outside this module gate and remain mandatory in whole evaluation']}

def check_module_placements(model):
 """Bind source components to actual whole-model geometry, then recheck local
 paths against ALL neighboring solids/fixtures. No placement receipt is trusted.
 """
 errors=[];pending=[];rows=[]
 def err(code,**kw):errors.append(dict(code=code,**kw))
 try:
  units={u['id']:u for u in model['units']};walls={k:rect(q)for k,q in model['walls'].items()};allfx=[(u['id'],k,rect(q))for u in model['units']for k,q in u['fixtures'].items()];seen=set();expected_ports=set()
  for rec in model.get('module_placements',[]):
   module=rec['module'];uid=rec['unit_id'];rid=rec['room_id'];key=(uid,rid);u=units[uid];mapping=rec['id_map'];t=rec['transform'];mat=[[F(x)for x in row]for row in t['matrix']];off=list(map(F,t['translation']))
   if key in seen:err('DUPLICATE_MODULE_PLACEMENT',unit=uid,room=rid)
   seen.add(key)
   from d4_contract125 import matrix as d4_matrix
   try:mat=d4_matrix(mat)
   except ValueError:err('MODULE_ISOMETRY_NOT_ALLOWED',unit=uid,room=rid);continue
   if rec['module_hash']!=digest(module):err('MODULE_SOURCE_HASH_MISMATCH',unit=uid,room=rid)
   if (model.get('ordered_macro')or{}).get('kind')in('TURN_T133','SIDECAR_T136','PARALLEL_TWINS_BRANCH146')and rid.startswith('bed'):
    from checker_source133 import examine as examine_rotation_source
    source=rec.get('rotation_source133',{});rr=examine_rotation_source(source)
    if rr['errors']or rr['pending']or source.get('base_module')!=module:err('ROTATION_SOURCE133_BINDING',unit=uid,room=rid)
   local=check_kitchen_module(module)if module.get('schema')=='KITCHEN_MODULE117'else check_bathroom_module(module)if module.get('schema')=='BATHROOM_MODULE117'else check_twin_module(module)if module.get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'else check_module(module);rows.append({'unit':uid,'room':rid,'module_hash':digest(module),'local_status':local['status']})
   if local['errors']:err('SOURCE_MODULE_RECHECK_FAILED',unit=uid,room=rid,errors=local['errors'])
   pending.extend('SOURCE_MODULE:'+str(p)for p in local['pending'])
   def pt(p):return tuple(sum(mat[i][j]*F(p[j])for j in(0,1))+off[i]for i in(0,1))
   def tr(q):
    q=rect(q);a=pt(q[:2]);b=pt(q[2:]);return(min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1]))
   def same(actual,expected,field):
    if actual!=expected:err('MODULE_PLACEMENT_PHYSICAL_BINDING',unit=uid,room=rid,field=field)
   for field in('walls','wall_hosts'):
    for k,q in module[field].items():
     target=mapping.get(k)
     same(rect(model[field][target])if target in model[field]else None,tr(q),field+'.'+k)
   same([rect(q)for q in u['rooms'][rid]],[tr(q)for q in module['unit']['rooms']['kitchen'if module.get('schema')=='KITCHEN_MODULE117'else'bath'if module.get('schema')=='BATHROOM_MODULE117'else'bed1']],'component_floor')
   apron=model.get('module_aprons',{}).get(uid+'.'+rid,[])
   same([rect(q)for q in apron],[tr(q)for q in module['unit']['rooms']['public_access']],'public_apron')
   from typed_public_access120 import parts as typed_public_parts
   private_module=module.get('schema')in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118')
   public_role=mapping.get('K.public_access')if module.get('schema')=='KITCHEN_MODULE117'else mapping.get('M.public_access',uid+'.public_access')if private_module else uid+'.public_access'
   allowed_roles={uid+'.public_access'}|({uid+'.kitchen_public_access'}if module.get('schema')=='KITCHEN_MODULE117'else{uid+'.private_access',uid+'.bedroom_public_access'}if private_module else set())
   if public_role not in allowed_roles:err('MODULE_PUBLIC_TYPE_NOT_ALLOWED',unit=uid,room=rid);public_role='INVALID'
   try:public=typed_public_parts(model,u,public_role)
   except ValueError as ex:err('MODULE_TYPED_PUBLIC_ROLE',unit=uid,room=rid,detail=str(ex));public=[]
   apron_host=list(public)
   if private_module and public_role==uid+'.private_access':
    # The source apron includes its own physical door-threshold strip; no
    # bedroom floor or unrelated aperture is added to the private approach.
    for source_opening in module['openings']:
     target=mapping[source_opening['id']]
     matches=[o for o in model['openings']if o['id']==target and public_role in o['connects']]
     if len(matches)==1 and rect(matches[0]['rect'])==tr(source_opening['rect']):apron_host.append(rect(matches[0]['rect']))
   for q in apron:
    if not covered(rect(q),apron_host):err('MODULE_APRON_NOT_REAL_PUBLIC_FLOOR',unit=uid,room=rid)
   for source_port in module['external_ports']:
    portid=mapping.get(source_port['id']);expected_ports.add(portid);matches=[z for z in model.get('module_ports',[])if z['id']==portid]
    if len(matches)!=1:err('MODULE_PLACED_PORT_INVENTORY',unit=uid,room=rid);continue
    actual=matches[0];same(rect(actual['rect']),tr(source_port['rect']),'port.rect');same(tuple(map(F,actual['center'])),pt(source_port['center']),'port.center')
    if actual['opening_id']!=mapping[source_port['opening_id']]or actual['role_id']!=mapping[source_port['role_id']]:err('MODULE_PLACED_PORT_ROLE_OPENING_BINDING',unit=uid,room=rid)
    c=pt(source_port['center']);body=(c[0]-BODY/2,c[1]-BODY/2,c[0]+BODY/2,c[1]+BODY/2)
    if not covered(body,public):err('PLACED_PORT_BODY_NOT_ON_PUBLIC_FLOOR',unit=uid,room=rid)
    if module.get('schema')=='KITCHEN_MODULE117':
     obstacles=list(walls.values())+[q for _,_,q in allfx]
     for op in model.get('operations',{}).get('dining_chairs',[]):
      if op.get('unit')!=uid:continue
      if op.get('occupied_body'):obstacles.append(rect(op['occupied_body']))
      if op.get('closed_rect')and op.get('open_rect'):
       a,b=rect(op['closed_rect']),rect(op['open_rect']);obstacles.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
     if any(intersects(body,z)for z in obstacles):err('KITCHEN_PORT_BODY_ACTUAL_OCCUPIED_COLLISION',unit=uid)
     if any(intersects(rect(a),z)for a in apron for z in obstacles):err('KITCHEN_APRON_ACTUAL_OCCUPIED_COLLISION',unit=uid)


   for k,q in module['unit']['fixtures'].items():
    target=mapping.get(k);same(rect(u['fixtures'][target])if target in u['fixtures']else None,tr(q),'fixture.'+k)
    if target in u['fixture_metadata']:
     source_md=module['unit']['fixture_metadata'][k];actual_md=u['fixture_metadata'][target]
     if actual_md['kind']!=source_md['kind']:err('MODULE_FIXTURE_KIND_BINDING',unit=uid,room=rid,fixture=target)
   for k,q in module['unit']['activities'].items():
    target=k.replace('bed1.',rid+'.');same(rect(u['activities'][target])if target in u['activities']else None,tr(q),'activity.'+k)
   for opening in module['openings']:
    target=mapping[opening['id']];matches=[o for o in model['openings']if o['id']==target]
    if len(matches)!=1:err('MODULE_OPENING_INVENTORY',unit=uid,room=rid);continue
    actual=matches[0];same(rect(actual['rect']),tr(opening['rect']),'opening.'+target)
    if actual['host_wall_id']!=mapping[opening['host_wall_id']]or actual['connects']!=[mapping.get(k,k)for k in opening['connects']]:err('MODULE_OPENING_ROLE_HOST_BINDING',opening=target)
   def compare_motion(source,actual,label):
    for field in('closed_panel','open_panel','pocket','rail_envelope'):
     if field in source:same(rect(actual[field]),tr(source[field]),label+'.'+field)
    same(tuple(map(F,actual['translation'])),tuple(sum(mat[i][j]*F(source['translation'][j])for j in(0,1))for i in(0,1)),label+'.translation')
    if 'open_transfer_points'in source:same([tuple(map(F,p))for p in actual['open_transfer_points']],[pt(p)for p in source['open_transfer_points']],label+'.open_transfer_points')
    for field in('states','continuous_actor_segments'):
     aa=actual.get(field,[]);ss=source.get(field,[])
     if len(aa)!=len(ss):err('MODULE_OPERATION_STATE_INVENTORY',field=label+'.'+field);continue
     for a,s in zip(aa,ss):
      for k in('panel_rect','actor_rect','actor_start','actor_end'):
       if k in s:same(rect(a[k]),tr(s[k]),label+'.'+field+'.'+k)
      for k in('hand_point','hand_start','hand_end'):
       if k in s:same(tuple(map(F,a[k])),pt(s[k]),label+'.'+field+'.'+k)
      for k in('fraction','t0','t1'):
       if k in s:same(F(a[k]),F(s[k]),label+'.'+field+'.'+k)
      if a.get('unit')!=uid or a.get('role_id')!=mapping.get(s.get('role_id'),s.get('role_id'))or a.get('side')!=s.get('side'):err('MODULE_OPERATION_ROLE_BINDING',field=label+'.'+field)
   for door in module['operations'].get('doors',[]):
    target=mapping[door['opening_id']];aa=[d for d in model.get('operations',{}).get('doors',[])if d['opening_id']==target]
    if len(aa)!=1:err('MODULE_DOOR_OPERATION_INVENTORY',opening=target)
    else:compare_motion(door,aa[0],target)
   for closet in module['operations'].get('closets',[]):
    target=mapping[closet['fixture_id']];aa=[d for d in model.get('operations',{}).get('closets',[])if d['unit']==uid and d['fixture_id']==target]
    if len(aa)!=1:err('MODULE_CLOSET_OPERATION_INVENTORY',fixture=target);continue
    actual=aa[0];same([rect(q)for q in actual['shell_rects']],[tr(q)for q in closet['shell_rects']],'closet.shells')
    if len(actual['panels'])!=len(closet['panels']):err('MODULE_CLOSET_HALF_INVENTORY',fixture=target)
    else:
     for s,a in zip(closet['panels'],actual['panels']):compare_motion(s,a,target+'.panel')
   for source_op in module.get('operations',{}).get('kitchen',[]):
    aa=[op for op in model.get('operations',{}).get('kitchen',[])if op['unit']==uid]
    if len(aa)!=1:err('MODULE_KITCHEN_OPERATION_INVENTORY',unit=uid);continue
    actual=aa[0];source_transform=source_op['canonical_transform'];cm=[[F(x)for x in row]for row in source_transform['matrix']];co=list(map(F,source_transform['translation']));expected_matrix=[[sum(cm[i][k]*mat[j][k]for k in(0,1))for j in(0,1)]for i in(0,1)];expected_offset=[co[i]-sum(expected_matrix[i][j]*off[j]for j in(0,1))for i in(0,1)]
    same([[F(x)for x in row]for row in actual['canonical_transform']['matrix']],expected_matrix,'kitchen.canonical_matrix');same(list(map(F,actual['canonical_transform']['translation'])),expected_offset,'kitchen.canonical_offset')
    same(tuple(map(F,actual['access_point'])),pt(source_op['access_point']),'kitchen.access')
    if actual['assumptions']!=source_op['assumptions']:err('MODULE_KITCHEN_MOTION_PARAMETER_BINDING',unit=uid)
   for source_role,region in module.get('logical_regions',{}).items():
    if 'parts'in region:
     target_role=mapping.get(source_role);actual_region=model.get('logical_regions',{}).get(target_role,{})
     same([rect(q)for q in actual_region.get('parts',[])],[tr(q)for q in region['parts']],'logical_region.'+source_role)
     if actual_region.get('unit')!=uid:err('MODULE_SERVICE_REGION_OWNER_BINDING',role=target_role)
   # Retained component paths remain usable after neighbor placement, independently
   # of the separately recomputed core-to-activity routes checked in evaluate().
   for rk,path in module['unit']['routes'].items():
    actualpath=[list(pt(p))for p in path]
    for q in sweeps(actualpath):
     if not covered(q,[rect(r)for r in u['ownership']]):err('PLACED_MODULE_ROUTE_OUTSIDE_OWNER',room=rid,route=rk)
     for wid,w in walls.items():
      if intersects(q,w):err('PLACED_MODULE_ROUTE_WALL_COLLISION',room=rid,route=rk,wall=wid)
     for fu,fk,f in allfx:
      own_service_exception=module.get('schema')=='BATHROOM_MODULE117'and fu==uid and ((rk=='WC_use'and fk==mapping.get('WC_iranian'))or(rk=='shower_use'and fk==mapping.get('shower_floor')))
      if not own_service_exception and intersects(q,f):err('PLACED_MODULE_ROUTE_FIXTURE_COLLISION',room=rid,route=rk,fixture=fu+'.'+fk)
  expected={(u['id'],k)for u in model['units']for k in u['rooms']if k.startswith('bed')or k in('kitchen','bath')}
  if seen!=expected:err('WHOLE_MODULE_BEDROOM_INVENTORY',expected=sorted(expected),actual=sorted(seen))
  actual_ports=[p['id']for p in model.get('module_ports',[])]
  if set(actual_ports)!=expected_ports or len(actual_ports)!=len(expected_ports):err('WHOLE_MODULE_PORT_INVENTORY')
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as ex:err('MODULE_PLACEMENT_SCHEMA_OR_GEOMETRY',detail=str(ex))
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':rows,'status':'FAIL_PLACEMENT'if errors else'NOT_EVALUATED_PLACEMENT'if pending else'PASS_PLACEMENT_SCOPED','whole_model_pass':False}

def check_kitchen_module(module):
 """Kitchen component geometry and freshly replayed essential113 motions.
 Permanent arch has no invented leaf; its physical aperture/body routes remain gates.
 """
 errors=[];pending=[];evidence={}
 def err(code,**kw):errors.append(dict(code=code,**kw))
 try:
  if module.get('schema')!='KITCHEN_MODULE117':err('KITCHEN_MODULE_SCHEMA')
  u=module['unit'];uid=u['id'];owner=[rect(q)for q in u['ownership']];walls={k:rect(q)for k,q in module['walls'].items()};bounds=rect(module['bounds'][0]if len(module['bounds'])==1 else module['bounds']);fx={k:rect(q)for k,q in u['fixtures'].items()}
  catalog=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text());sourcebytes=(Path(__file__).parent/catalog['source_file']).read_bytes();src=json.loads(sourcebytes)
  if hashlib.sha256(sourcebytes).hexdigest()!='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4'or module.get('fixture_catalog_hash')!=digest(catalog):err('KITCHEN_MODULE_FIXTURE_SOURCE_BINDING')
  producer=Path(__file__).with_name('kitchen_module117.py')
  if module.get('source_binding',{}).get('producer_sha256')!=hashlib.sha256(producer.read_bytes()).hexdigest():err('KITCHEN_MODULE_PRODUCER_SOURCE_CHANGED')
  if set(fx)!={'fridge','sink','prep','cooker'}:err('KITCHEN_MODULE_FIXTURE_INVENTORY')
  for k,q in fx.items():
   md=u['fixture_metadata'][k];sq=rect(src['units'][0]['fixtures'][k]);size=(sq[2]-sq[0],sq[3]-sq[1]);rot=md['rotation_deg']
   if rot not in(0,90,180,270):err('KITCHEN_FIXTURE_ROTATION')
   if rot%180:size=size[::-1]
   if (q[2]-q[0],q[3]-q[1])!=size or md['kind']!=k:err('KITCHEN_IMMUTABLE_FIXTURE_SIZE',fixture=k)
   if not covered(q,owner)or any(intersects(q,w)for w in walls.values()):err('KITCHEN_FIXTURE_FLOOR_OR_WALL',fixture=k)
  for i,(k,q)in enumerate(fx.items()):
   for j,r in list(fx.items())[i+1:]:
    if intersects(q,r):err('KITCHEN_FIXTURE_COLLISION',fixtures=[k,j])
  rooms={k:[rect(q)for q in rs]for k,rs in u['rooms'].items()}
  for k,rs in rooms.items():
   for q in rs:
    if not covered(q,owner)or any(intersects(q,w)for w in walls.values()):err('KITCHEN_ROOM_FLOOR_BINDING',room=k)
  for q in owner:
   if not encloses(bounds,q)or not covered(q,[r for rs in rooms.values()for r in rs]+list(walls.values())):err('KITCHEN_OWNERSHIP_ACCOUNTING')
  ports=module['external_ports'];centers={tuple(map(F,p['center']))for p in ports}
  for p in ports:
   q=rect(p['rect']);c=tuple(map(F,p['center']));body=(c[0]-BODY/2,c[1]-BODY/2,c[0]+BODY/2,c[1]+BODY/2);oo=[o for o in module['openings']if o['id']==p['opening_id']]
   if len(oo)!=1 or not covered(q,owner)or not covered(body,[q]):err('KITCHEN_PORT_BINDING')
   elif p['role_id']not in oo[0]['connects']:err('KITCHEN_PORT_ROLE_BINDING')
  for opening in module['openings']:
   q=rect(opening['rect']);host=rect(module['wall_hosts'][opening['host_wall_id']]);parts=[w for w in walls.values()if encloses(host,w)]+[rect(o['rect'])for o in module['openings']if o['host_wall_id']==opening['host_wall_id']]
   if opening.get('kind')!='permanent_open_arch'or opening.get('hardware')is not None:err('KITCHEN_ARCH_TYPE_NOT_SOURCE_PROFILE')
   if not encloses(host,q)or not covered(host,parts)or any(intersects(q,w)for w in walls.values()):err('KITCHEN_ACTUAL_ARCH_CUT')
  if set(u['routes'])!=set(u['route_targets']):err('KITCHEN_MODULE_ROUTE_INVENTORY')
  for k,path in u['routes'].items():
   if tuple(map(F,path[0]))not in centers or tuple(map(F,path[-1]))!=tuple(map(F,u['route_targets'][k])):err('KITCHEN_ROUTE_PORT_TARGET_BINDING')
   for q in sweeps(path):
    if not covered(q,owner)or any(intersects(q,w)for w in list(walls.values())+list(fx.values())):err('KITCHEN_MODULE_BODY_COLLISION')
  fragment=dict(module);fragment['units']=[u];ops=module.get('operations',{}).get('kitchen',[])
  if len(ops)!=1:pending.append('KITCHEN_MODULE_ACTUAL_OPERATION_MISSING')
  else:
   from operation_check114 import check_reference_kitchen117
   op=check_reference_kitchen117(fragment,ops[0]);errors.extend(op['errors']);pending.extend(op['pending']);evidence=op['evidence']
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as ex:err('KITCHEN_MODULE_SCHEMA_OR_GEOMETRY',detail=str(ex))
 return {'checker_version':'KITCHEN_MODULE117_INDEPENDENT_V1','module_hash':digest(module),'status':'FAIL_MODULE'if errors else'NOT_EVALUATED_MODULE'if pending else'PASS_MODULE_SCOPED','errors':errors,'pending':sorted(set(pending)),'evidence':evidence,'whole_model_pass':False,'eligible_for_draft_export':False,'accepted':False,'release':False}

def check_service_privacy117(model,unit):
 from privacy115 import separator,clear_witness
 errors=[];pending=[];rows=[];uid=unit['id'];walls={k:rect(q)for k,q in model['walls'].items()};targets={'WC_use':rect(unit['activities']['WC_use']),'shower_use':rect(unit['activities']['shower_use']),'shower_floor':rect(unit['fixtures']['shower_floor'])};floor=[rect(q)for q in unit['rooms']['bath']];openings=[o for o in model['openings']if uid+'.bath'in o['connects']];doors={o['opening_id']:o for o in model.get('operations',{}).get('doors',[])}
 if not openings:pending.append('SERVICE_PRIVACY_EXTERNAL_APERTURE_MISSING')
 for name,t in targets.items():
  if not covered(t,floor):errors.append({'code':'SERVICE_PRIVACY_TARGET_OUTSIDE_ACTUAL_FLOOR','target':name})
  for op in openings:
   ap=rect(op['rect']);face=None;ys=[q[1]for q in floor]+[q[3]for q in floor]
   # Necessary full inner boundary face, exactly as source113 wet-room proof.
   if ap[3]==min(ys) and t[1]>=ap[3]and covered((ap[0],ap[3],ap[2],ap[3]+F('.000001')),floor):face=(ap[0],ap[3],ap[2],ap[3])
   elif ap[1]==max(ys)and t[3]<=ap[1]and covered((ap[0],ap[1]-F('.000001'),ap[2],ap[1]),floor):face=(ap[0],ap[1],ap[2],ap[1])
   # Same necessary inner-face argument on X after a rigid D4 frame change.
   xs=[q[0]for q in floor]+[q[2]for q in floor]
   if face is None and ap[2]==min(xs) and t[0]>=ap[2] and covered((ap[2],ap[1],ap[2]+F('.000001'),ap[3]),floor):face=(ap[2],ap[1],ap[2],ap[3])
   elif face is None and ap[0]==max(xs) and t[2]<=ap[0] and covered((ap[0]-F('.000001'),ap[1],ap[0],ap[3]),floor):face=(ap[0],ap[1],ap[0],ap[3])
   if face is None:pending.append('SERVICE_PRIVACY_NECESSARY_BOUNDARY_FACE_NOT_BOUND:'+name);face=ap
   strict=next(({'wall':k,**p}for k,w in walls.items()if(p:=separator(face,t,w))),None);conditional=None if strict else next(({'wall':k,**p}for k,w in walls.items()if(p:=separator(face,t,w,True))),None)
   if op['id']not in doors:pending.append('SERVICE_PRIVACY_OPEN_STATE_MISSING:'+op['id'])
   witness=None
   if not strict and not conditional:
    obstacles=list(walls.values())+[rect(d['open_panel'])for d in doors.values()]+[rect(q)for q in unit['fixtures'].values()if not intersects(rect(q),t)]
    witness=clear_witness(ap,t,obstacles)
    if witness:errors.append({'code':'SERVICE_PRIVATE_TARGET_VISIBLE','opening':op['id'],'target':name,'witness':witness})
    else:pending.append('SERVICE_PRIVACY_ALL_RAYS_NOT_PROVEN:'+name)
   rows.append({'target':name,'opening':op['id'],'necessary_actual_boundary_face':list(map(str,face)),'strict':strict,'conditional_closed_boundary':conditional,'counterexample':witness})
 return {'errors':errors,'pending':pending,'evidence':rows}

def check_bathroom_module(module):
 errors=[];pending=[];evidence={}
 def err(code,**kw):errors.append(dict(code=code,**kw))
 try:
  if module.get('schema')!='BATHROOM_MODULE117':err('SERVICE_MODULE_SCHEMA')
  raw=Path(__file__).with_name('bathroom_source117.json').read_bytes();sourcehash=hashlib.sha256(raw).hexdigest()
  if sourcehash!='a31df1090677e03577f359b147052ca2cdf454863da00bdf663eafcc143e9428'or module['source_binding']['source_snapshot_sha256']!=sourcehash:err('SERVICE_SOURCE_BINDING')
  if module['source_binding']['producer_sha256']!=hashlib.sha256(Path(__file__).with_name('bathroom_module117.py').read_bytes()).hexdigest():err('SERVICE_PRODUCER_SOURCE_CHANGED')
  u=module['unit'];uid=u['id'];owner=[rect(q)for q in u['ownership']];walls={k:rect(q)for k,q in module['walls'].items()};fx={k:rect(q)for k,q in u['fixtures'].items()};rooms={k:[rect(q)for q in rs]for k,rs in u['rooms'].items()}
  catalog=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text())
  if module['fixture_catalog_hash']!=digest(catalog):err('SERVICE_FIXTURE_CATALOG_BINDING')
  if set(fx)!={'WC_iranian','shower_floor','basin'}:err('SERVICE_FIXTURE_INVENTORY')
  for k,q in fx.items():
   spec=catalog['types'][k];size=(F(spec['width_m']),F(spec['depth_m']));md=u['fixture_metadata'][k]
   if md['rotation_deg']%180:size=size[::-1]
   if md['rotation_deg']not in(0,90,180,270)or(q[2]-q[0],q[3]-q[1])!=size or md['kind']!=k:err('SERVICE_RIGID_FIXTURE_DIMENSION',fixture=k)
   if not covered(q,rooms['bath'])or any(intersects(q,w)for w in walls.values()):err('SERVICE_FIXTURE_FLOOR_WALL',fixture=k)
  for i,(k,q)in enumerate(fx.items()):
   for j,r in list(fx.items())[i+1:]:
    if intersects(q,r):err('SERVICE_FIXTURE_COLLISION',fixtures=[k,j])
  for k,rs in rooms.items():
   if any(not covered(q,owner)or any(intersects(q,w)for w in walls.values())for q in rs):err('SERVICE_ROOM_ACTUAL_FLOOR',room=k)
  if set(u['activities'])!={'WC_front','WC_use','shower_use','basin_front'}or set(u['routes'])!=set(u['activities'])or set(u['route_targets'])!=set(u['activities']):err('SERVICE_ACTIVITY_ROUTE_INVENTORY')
  centers={tuple(map(F,p['center']))for p in module['external_ports']}
  for k,path in u['routes'].items():
   if tuple(map(F,path[0]))not in centers or tuple(map(F,path[-1]))!=tuple(map(F,u['route_targets'][k])):err('SERVICE_ROUTE_ENDPOINT_BINDING',route=k)
   for q in sweeps(path):
    if not covered(q,owner)or any(intersects(q,w)for w in walls.values()):err('SERVICE_BODY_FLOOR_WALL',route=k)
    for fk,f in fx.items():
     if (k=='WC_use'and fk=='WC_iranian')or(k=='shower_use'and fk=='shower_floor'):continue
     if intersects(q,f):err('SERVICE_BODY_FIXTURE',route=k,fixture=fk)
  from operation_check114 import check_operations,pocket_host_geometry117
  for opening in module['openings']:
   for code in pocket_host_geometry117(module,opening,walls):err(code,opening=opening['id'])
  fragment=dict(module);fragment['units']=[u]
  oe,op=check_operations(fragment,{uid:owner},walls,[(uid,k,q)for k,q in fx.items()],components=('doors',));errors.extend(oe);pending.extend(op)
  pr=check_service_privacy117(fragment,u);errors.extend(pr['errors']);pending.extend(pr['pending']);evidence['privacy']=pr['evidence']
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as ex:err('SERVICE_MODULE_SCHEMA_OR_GEOMETRY',detail=str(ex))
 return {'checker_version':'SERVICE_MODULE117_INDEPENDENT_V1','module_hash':digest(module),'status':'FAIL_MODULE'if errors else'NOT_EVALUATED_MODULE'if pending else'PASS_MODULE_SCOPED','errors':errors,'pending':sorted(set(pending)),'evidence':evidence,'whole_model_pass':False,'eligible_for_draft_export':False,'accepted':False,'release':False}

def check_whole_privacy117(model):
 """Every actual bedroom target and actual wet-room target, fresh whole walls.
 Bedroom adapter changes names only; wet rooms use source113 necessary boundary
 face, with strict vs closed-boundary certificates retained explicitly.
 """
 from copy import deepcopy
 from privacy116 import examine_module
 errors=[];pending=[];rows=[]
 public=[rect(r)for u in model['units']for k,rs in u['rooms'].items()if not k.startswith('bed')and k!='bath'for r in rs]
 for value in model.get('common_spaces',{}).values():public.extend([rect(q)for q in value]if isinstance(value[0],list)else[rect(value)])
 for u in model['units']:
  uid=u['id'];beds=[k for k in u['rooms']if k.startswith('bed')]
  if not beds:errors.append({'code':'WHOLE_PRIVACY_BED_INVENTORY_EMPTY','unit':uid})
  for room in beds:
   target=uid+'.'+room;ops=[o for o in model['openings']if target in o['connects']];ids={o['id']for o in ops};view={'schema':'PRIVATE_ROOM_MODULE116','walls':deepcopy(model['walls']),'openings':deepcopy(ops),'operations':{'doors':[deepcopy(o)for o in model.get('operations',{}).get('doors',[])if o['opening_id']in ids]}}
   for op in view['openings']:op['connects']=[uid+'.bed1'if role==target else role for role in op['connects']]
   fixtures={v['id']+'.'+k:q for v in model['units']for k,q in v['fixtures'].items()}
   actual_beds={k:q for k,q in u['fixtures'].items()if k.startswith(room+'.')and u['fixture_metadata'].get(k,{}).get('kind')in('bed','single_bed')}
   view['schema']='PRIVATE_TWIN_ROOM_MODULE118'if any(u['fixture_metadata'][k]['kind']=='single_bed'for k in actual_beds)else'PRIVATE_ROOM_MODULE116'
   for k,q in actual_beds.items():fixtures.pop(uid+'.'+k,None);fixtures[k]=q
   view['unit']={'id':uid,'rooms':{'bed1':deepcopy(u['rooms'][room]),'public_access':[[str(x)for x in q]for q in public]},'fixtures':fixtures,'activities':{'bed1.changing':u['activities'][room+'.changing']}}
   closet_id=room+'.closet'
   view['operations']['closets']=[deepcopy(o)for o in model.get('operations',{}).get('closets',[])if o.get('unit')==uid and o.get('fixture_id')==closet_id]
   view['unit']['fixtures'].pop(uid+'.'+closet_id,None)
   view['unit']['fixtures'][closet_id]=deepcopy(u['fixtures'][closet_id])
   view['unit']['fixture_metadata']={k:deepcopy(u['fixture_metadata'][k])for k in [closet_id,*actual_beds]}
   result=examine_module(view);errors.extend({'unit':uid,'room':room,**e}for e in result['errors']);pending.extend(uid+'.'+room+':'+p for p in result['pending']);rows.append({'unit':uid,'room':room,'kind':'full_actual_aperture_strict_bedroom','evidence':result['evidence']})
  if 'bath'not in u['rooms']:errors.append({'code':'WHOLE_PRIVACY_BATH_MISSING','unit':uid});continue
  result=check_service_privacy117(model,u);errors.extend({'unit':uid,**e}for e in result['errors']);pending.extend(uid+':'+p for p in result['pending']);rows.append({'unit':uid,'room':'bath','kind':'actual_necessary_inner_boundary_face','evidence':result['evidence']})
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':{'whole_model_hash':digest(model),'targets':rows,'status':'FAIL_SCOPED'if errors else'NOT_EVALUATED'if pending else'PASS_SCOPED_PRIVACY','closed_boundary_means':'Non-strict opaque boundary/tangency convention, NEVER a closed-door assumption','accepted':False}}


def check_twin_module(module):
 """Both source-sized single beds, all instance access/targets; no double-bed substitution."""
 return check_module(module,_twin=True)
