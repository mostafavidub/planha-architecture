"""Native constructor129 packet -> geometry facts; no caller purpose/proof/profile mapping."""
import json,hashlib,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
ENGINE_SHA='894262559bb2fd822a9ea65876f68dee7844b197c57ae69832ec62d02b53403c'
SOURCE_PINS={'planha_general150_runtime_work/constructor129.py': 'cf94fe85957cb20e8d1ff6c5837f18a4d2e8e4ad442db42b67d91b3c7766f286', 'planha_general150_runtime_work/world_inventory125.py': '9b1847ddd82ec592b5aeef0a148d3f273077f6c7357969f5afd90a3be4319475', 'planha_general150_runtime_work/fixture_catalog114.json': 'fdfd29e5aa90f263ede216f7102d3bc2d242c0dc93058600ec2340f0f8c241e4'}

SOURCE_PINS['planha_general150_runtime_work/assemble114.py']='b12cf81eb0acdfd5c696445fe7821235012f589cac9477b865da89093c0b095e'

SOURCE_PINS['planha_general150_runtime_work/place_module116.py']='128e1545104de9dd3ae3c347c08e2d3f857bd0968dce4ea972a5157f43bfce6a'

SOURCE_PINS['planha_general150_runtime_work/place_module133.py']='a945f87b0ef909b166d35da2862251fe3063325c450990c4bde9ce24a38bc007'

SOURCE_PINS['planha_general150_runtime_work/place_kitchen117.py']='e3b8d024c50f6026dd143b8f39eb64035e2a756c68f6c8dd1e9900e207f9f0dc'

SOURCE_PINS['planha_general150_runtime_work/bedroom_module116.py']='21bcadf03beb91b9b78a85d2b87520b594c19dce28b932860d871744e4815789'

SOURCE_PINS['planha_general150_runtime_work/kitchen_module117.py']='d22cc81eee216181eedede9bb45ae4d6630da71a7e77681ab47ea0af8c295b19'

def verify_sources():
 for path,h in SOURCE_PINS.items():
  raw=(ROOT/path).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=h:raise ValueError('NATIVE_SCHEMA_SOURCE_CHANGED:'+path)
 raw=(HERE/'engine.py').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=ENGINE_SHA:raise ValueError('SEMANTIC_ENGINE_CHANGED')
 name='_semantic165_native_fixed';m=types.ModuleType(name);m.__file__=str(HERE/'engine.py');sys.modules[name]=m;exec(compile(raw,m.__file__,'exec'),m.__dict__);return m

def _evaluate_native_checked(packet,server_request):
 out={'schema':'NATIVE150_SEMANTIC_GEOMETRY_V2','status':'UNKNOWN','origin_verified':False,'constructor_replay':'REQUIRED_TRUSTED_BOUNDARY_NOT_EXECUTED','delivery_allowed':False,'frames':[],'issues':[]}
 try:
  g=verify_sources();e=g.e
  from host_bridge import load as load_host
  host_helper=load_host()
  if type(packet)is not dict or set(packet)!={'family','local_model','world_model','core','admission_claim'}or packet['admission_claim']is not False or packet['family']not in('FRONT_REAR','LEFT_RIGHT'):raise ValueError('CONSTRUCTOR129_PACKET_SCOPE_ONLY')
  if type(server_request)is not dict or set(server_request)!={'W','L','n','requested_count'}or type(server_request['n'])is not int or server_request['n']!=2:raise ValueError('SERVER_REQUEST_REQUIRED_N2')
  W,L=e.number(server_request['W']),e.number(server_request['L'])
  if not 5<=W<=45 or not 5<=L<=45:raise ValueError('REQUEST_DOMAIN')
  out['packet_digest']=e.digest(packet);out['program_digest']=e.digest(server_request);out['source_digest']=e.digest(SOURCE_PINS)
  profiles=e.load_source_profiles()
  from selected_profiles import registry,select_table
  profiles.update(registry());fixed_fixture_names={v['source_fixture_key']:k for k,v in profiles.items()}
  for frame in('local_model','world_model'):
   m=packet[frame]
   if type(m)is not dict or type(m.get('units'))is not list or sorted(u.get('id')for u in m['units'])!=['A','B']:raise ValueError('EXACT_NATIVE_UNITS_A_B')
   expected=[W,L,e.F(2)]if frame=='world_model'or packet['family']=='FRONT_REAR'else[L,W,e.F(2)]
   if type(m.get('inputs'))is not list or list(map(e.number,m['inputs']))!=expected:raise ValueError('FRAME_INPUT_DIMENSIONS')
   walls={k:e.rectangle(v)for k,v in m['walls'].items()};hosts={k:[v]for k,v in m['wall_hosts'].items()};globalregions={};fr={'frame':frame,'model_digest':e.digest(m),'rules':[],'unit_facts':[],'opening_facts':[],'unresolved_fixtures':[],'functional_subproofs':[]}
   capunits=[]
   for u in m['units']:
    uid=u['id'];rooms=g.rectmap(u['rooms']);own=g.rectangles(u['ownership'])
    for k,v in u['rooms'].items():globalregions[uid+'.'+k]=v
    payload={'ownership':u['ownership'],'walls':list(m['walls'].values()),'regions':u['rooms']}
    rr=g.evaluate('SPACE_ACCOUNTING',payload);fr['rules'].append({'unit':uid,**rr});fr['unit_facts'].append({'unit':uid,'ownership_rect_count':len(own),'room_ids':list(rooms),'fixture_ids':list(u['fixtures']),'wall_inventory_count':len(walls),'space_evidence_digest':rr.get('evidence_digest')})
    fixtures=[]
    for fid,r in u['fixtures'].items():
     rect=e.rectangle(r);suffix=fid.split('.')[-1]
     # Only source150 catalogue identity keys. Twin aliases/unknown types are not guessed.
     sid=fixed_fixture_names.get(fid,fixed_fixture_names.get(suffix))
     if fid=='dining_table'and (m.get('program',{}).get('capacity_profile')!='LEGACY_SOURCE_PROGRAM'or u.get('fixture_metadata',{}).get(fid,{}).get('kind')=='dining_table6'):
      selected=select_table(m,u);fr.setdefault('selected_source_profiles',[]).append(selected);sid=selected.get('source_id')if selected['status']=='SOURCE_PROFILE_SUBPROOF'else None
     containing=[k for k,rs in rooms.items()if g.outside([rect],rs)==0]
     if sid is None or len(containing)!=1:
      fr['unresolved_fixtures'].append({'unit':uid,'fixture':fid,'rect':list(map(str,rect)),'source_key_resolved':sid is not None,'geometric_containing_regions':containing,'reason':'SOURCE_TYPE_OR_UNIQUE_REGION_UNPROVEN'});continue
     expected=sorted(map(e.F,profiles[sid]['dimensions']));actual=sorted([rect[2]-rect[0],rect[3]-rect[1]])
     fr['functional_subproofs'].append({'unit':uid,'region':containing[0],'fixture':fid,'source_id':sid,'exact_dimensions_and_containment':actual==expected,'region_geometry_digest':e.digest(u['rooms'][containing[0]]),'fixture_geometry_digest':e.digest(r),'scope':'Fixed-source-sized physical fixture fits unique geometric region; not proof of operation, usable function or source origin','function_verdict':'UNKNOWN','missing':['SOURCE_ORIGIN','OPERATION_AND_ACCESS','REGION_PURPOSE_COMPLETENESS']})
     fixtures.append({'id':fid,'source_id':sid,'rect':r,'room_id':containing[0]})
    capunits.append({'id':uid,'ownership':u['ownership'],'rooms':u['rooms'],'fixtures':fixtures})
   cap=g.evaluate('ROOM_PROGRAM_CAPACITY',{'required_units':server_request['n'],'units':capunits});cap['proof_coverage']['missing'].append('NATIVE_FIXTURE_KEY_TO_ACTUAL_SOURCE_ORIGIN');fr['rules'].append(cap)
   from complexity import common_regions
   for k,v in common_regions(m.get('common_spaces',{})).items():
    if k in globalregions:raise ValueError('REGION_ID_COLLISION')
    globalregions[k]=v
   if type(m.get('openings'))is not list:raise ValueError('OPENINGS_LIST_REQUIRED')
   for op in m['openings']:
    if type(op)is not dict or not all(k in op for k in('id','rect','host_wall_id','connects')):raise ValueError('NATIVE_OPENING_FIELDS_REQUIRED')
    a=e.rectangle(op['rect']);host=op['host_wall_id'];exists=host in hosts;within=exists and g.outside([a],g.rectangles(hosts[host]))==0
    record={'id':op['id'],'host_id':host,'rect':op['rect'],'host_exists':exists,'aperture_in_host':within,'connects':op['connects']};fr['opening_facts'].append(record)
    host_result=host_helper.evaluate(m,op['id']);record['host_contract']=host_result
    checks=list(host_result['checks']);missing=list(host_result['missing'])
    unresolved=type(op['connects'])is not list or len(op['connects'])!=2 or any(k not in globalregions for k in op['connects'])
    if unresolved:missing.append('ACTUAL_CONNECTED_REGION_GEOMETRY')
    else:
     # Source host proof is computed above, never replace it with raw containment.
     checks.append(g.opening_region_adjacency(op['id'],op['rect'],op['connects'],globalregions))
    fr['rules'].append({'rule_id':'OPENINGS_REAL','opening_id':op['id'],'verdict':'FAIL'if any(c['verdict']=='FAIL'for c in checks)else'UNKNOWN','checks':checks,'host_relation_source':host_result,'proof_coverage':{'complete':False,'missing':missing},'delivery_allowed':False})
   if not m['openings']:fr['rules'].append({'rule_id':'OPENINGS_REAL','verdict':'UNKNOWN','reason':'EMPTY_OPENING_INVENTORY','delivery_allowed':False})
   if fr['unresolved_fixtures']:out['issues'].append({'frame':frame,'code':'INCOMPLETE_SOURCE_FIXTURE_MAPPING','count':len(fr['unresolved_fixtures'])})
   out['frames'].append(fr)
  out['status']='FAIL'if any(r['verdict']=='FAIL'for f in out['frames']for r in f['rules'])else'UNKNOWN'
 except Exception as ex:out['status']='UNKNOWN';out['issues'].append({'code':'MALFORMED_OR_UNSUPPORTED_NATIVE_EVIDENCE','detail':type(ex).__name__+':'+str(ex)})
 return out


def evaluate_native(packet,server_request):
 # Direct call has resource preflight but no hard time guarantee. Use run_bounded.
 from complexity import preflight
 try:bounds=preflight(packet)
 except Exception as ex:return {'status':'UNKNOWN','delivery_allowed':False,'issues':[{'code':'RESOURCE_PREFLIGHT_BLOCKED','detail':str(ex)}],'frames':[]}
 result=_evaluate_native_checked(packet,server_request);result['complexity']=bounds;return result

# 244 direct region-domain consumer. Called after the existing composition, using
# its ORIGINAL live fact; this does not execute composition or manufacture one.
CAPACITY244_SHA='25eb7203aba3969c44e3669f772233dc606ec990e05561b3c606310ad036fd47'
PRIVATE_USE244=frozenset(('SELECTED_PROGRAM_PRIVATE_MODULE_CLOSET_OPERATIONS_AND_SLEEP_ENDPOINTS','UNIT_ENTRY_TO_ALL_SOURCE_SLEEP_TARGETS_BODY_SWEEP'))

def attach_region_use(native,origin,converted,source_binding,capacity_fact,*,remaining_budget_seconds=10,cancel_token=None):
 import time,threading,math
 start=time.monotonic();event=threading.Event()if cancel_token is None else cancel_token
 out={'schema':'DIRECT_ROLE_DOMAIN244_PARTIAL','verdict':'UNKNOWN','regions':[],'units':[],'missing':[],'parent_complete':False,'delivery_allowed':False,'repair_authority':False,'full_useful_floor_verified':False}
 try:
  if type(event)is not threading.Event or type(remaining_budget_seconds)not in(int,float)or not math.isfinite(remaining_budget_seconds)or not 0<remaining_budget_seconds<=30:raise ValueError('SERVER_BUDGET')
  def tick():
   if event.is_set()or time.monotonic()-start>=remaining_budget_seconds:raise ValueError('DOMAIN244_RESOURCE_OR_CANCEL')
  tick();raw_budget=(HERE/'complexity.py').read_bytes()
  if hashlib.sha256(raw_budget).hexdigest()!='79d3501274bb26a7217e007df754610384339770c856fb8a693e10f826604cdf':raise ValueError('ROLE244_BUDGET_SOURCE_CHANGED')
  bm=types.ModuleType('_role244_budget');exec(compile(raw_budget,str(HERE/'complexity.py'),'exec'),bm.__dict__)
  bm.transport_shape(converted['packet'])
  cm=sys.modules.get('_capacity_composition215_v2');j=sys.modules.get('origin_join')
  if cm is None or hashlib.sha256(Path(cm.__file__).read_bytes()).hexdigest()!=CAPACITY244_SHA:raise ValueError('SAME_FIXED_CAPACITY_MODULE_REQUIRED')
  verified=cm.verify_fact(capacity_fact,origin,converted,source_binding)
  # verify_fact performs same-origin, issued identity, context/source/readset checks.
  g=verify_sources();e=g.e;packet=converted['packet'];expected=e.digest(packet)
  if native.get('packet_digest')!=expected:raise ValueError('NATIVE_PACKET_BINDING')
  frames=native.get('frames')
  if type(frames)is not list or len(frames)!=2 or {f.get('frame')for f in frames}!={'local_model','world_model'}:raise ValueError('NATIVE_FRAME_INVENTORY')
  bounds=[_preflight_roles244(packet[f],g.e,tick)for f in ('local_model','world_model')]
  if sum(b['estimated_work']for b in bounds)>4000000 or sum(b['rectangles']for b in bounds)>4000:raise ValueError('ROLE244_TWO_FRAME_AGGREGATE_BOUND')
  for frame in ('local_model','world_model'):
   tick();m=packet[frame];nr=next(f for f in frames if f['frame']==frame)
   if nr['model_digest']!=e.digest(m):raise ValueError('NATIVE_MODEL_BINDING')
   rows,unitrows=_role_domains244(m,g,verified,tick)
   out['regions'].extend(dict(x,frame=frame,model_digest=e.digest(m))for x in rows)
   out['units'].extend(dict(x,frame=frame,model_digest=e.digest(m))for x in unitrows)
  cm.verify_fact(capacity_fact,origin,converted,source_binding);tick()
  out['packet_digest']=expected;out['source_binding']=source_binding
  out['reused_scopes']=list(verified['resolved'])
  out['missing']=['SUPPORTING_FLOOR_EXTENT_AUTHORITY_NOT_GENERAL','FINAL_CIRCULATION_NECESSITY_NOT_PROVEN','LIVING_DINING_BATH_WHOLE_ROLE_USE_NOT_PROVEN','Q10_ARRIVAL_SEQUENCE_NOT_PROVEN']
 except (ValueError,KeyError,TypeError,AttributeError,IndexError,StopIteration,ZeroDivisionError,OverflowError,OSError)as exc:
  out['regions']=[];out['units']=[];out['missing'].append('ROLE244_UNVERIFIED:'+str(exc))
 native['region_use_coverage']=out
 return native

def _preflight_roles244(m,e,tick):
 """Bound all new readsets and reserve every union/overlay before evaluation.
 Engineering resource policy, never an architectural acceptance threshold.
 """
 stack=[m];nodes=0
 while stack:
  tick();v=stack.pop();nodes+=1
  if nodes>100000:raise ValueError('ROLE244_NODE_BOUND')
  if type(v)is dict:
   if len(v)>4000:raise ValueError('ROLE244_MAPPING_BOUND')
   for k,x in v.items():
    if type(k)is not str or len(k)>4096:raise ValueError('ROLE244_KEY_BOUND')
    stack.append(x)
  elif type(v)is list:
   if len(v)>4000:raise ValueError('ROLE244_LIST_BOUND')
   stack.extend(v)
  elif type(v)is str and len(v)>4096:raise ValueError('ROLE244_STRING_BOUND')
 units=m['units'];ps=m['module_placements']
 if type(units)is not list or not 1<=len(units)<=2 or type(ps)is not list or len(ps)>100:raise ValueError('ROLE244_INVENTORY_BOUND')
 rects=0;work=0
 def rs(v):
  nonlocal rects
  if type(v)is not list or len(v)>4000:raise ValueError('REGION244_BOUND')
  out=[]
  for r in v:
   tick();rects+=1
   if rects>4000:raise ValueError('ROLE244_AGGREGATE_RECT_BOUND')
   out.append(e.rectangle(r))
  return out
 def charge(qs):
  nonlocal work
  tick();xs={r[i]for r in qs for i in(0,2)};ys={r[i]for r in qs for i in(1,3)}
  work+=max(1,len(xs)-1)*max(1,len(ys)-1)*max(1,len(qs))
  if work>4000000:raise ValueError('ROLE244_AGGREGATE_WORK_BOUND')
 solids=rs(list(m['walls'].values()))
 for u in units:
  tick();own=rs(u['ownership']);rooms={k:rs(v)for k,v in u['rooms'].items()};domains=[]
  for p in ps:
   tick()
   if p['unit_id']!=u['id']:continue
   mod=p['module'];schema=mod.get('schema')
   if schema not in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118','KITCHEN_MODULE117'):continue
   mat=p['transform']['matrix'];tr=p['transform']['translation']
   if type(mat)is not list or len(mat)!=2 or any(type(r)is not list or len(r)!=2 for r in mat)or type(tr)is not list or len(tr)!=2:raise ValueError('D4_SCHEMA')
   a,b,c,d=[e.number(x)for row in mat for x in row];tx,ty=map(e.number,tr)
   if any(x not in(-1,0,1)for x in(a,b,c,d))or a*a+b*b!=1 or c*c+d*d!=1 or a*c+b*d!=0:raise ValueError('D4_ISOMETRY_REQUIRED')
   def tf(r):
    x,y,z,w=r;pts=[(a*i+b*j+tx,c*i+d*j+ty)for i,j in((x,y),(x,w),(z,y),(z,w))]
    return min(v[0]for v in pts),min(v[1]for v in pts),max(v[0]for v in pts),max(v[1]for v in pts)
   source={k:rs(v)for k,v in mod['unit']['rooms'].items()}
   for group in('fixtures','activities'):
    rs(list(mod['unit'][group].values()));rs(list(u[group].values()))
   parts=[tf(r)for r in source['kitchen'if schema=='KITCHEN_MODULE117'else'bed1']];actual=rooms[p['room_id']]
   # outside(parts,owner), outside(parts,actual), area(parts), outside(actual,parts).
   for q in(parts+own,parts+actual,parts,actual+parts):charge(q)
   domains.extend(parts)
  charge(own+solids+domains)
 return {'nodes':nodes,'rectangles':rects,'estimated_work':work}

def _role_domains244(m,g,verified,tick):
 """Exact source room-floor D4 reconstruction; no room-label authority.
 Internal geometric kernel. Only attach_region_use supplies verified facts.
 """
 _preflight_roles244(m,g.e,tick)
 e=g.e;F=e.F;rows=[];unitrows=[];placements=m['module_placements']
 if type(placements)is not list or len(placements)>100:raise ValueError('PLACEMENT_INVENTORY_BOUND')
 def region(rs):
  if type(rs)is not list or len(rs)>4000:raise ValueError('REGION244_BOUND')
  return [e.rectangle(r)for r in rs]
 def encode(rs):return [list(map(str,r))for r in rs]
 def equal(a,b):return g.outside(a,b)==0 and g.outside(b,a)==0
 def overlay(own,solids,domains):
  groups=[own,solids]+[r for _,r in domains];qs=[r for group in groups for r in group]
  xs=sorted({r[i]for r in qs for i in(0,2)});ys=sorted({r[i]for r in qs for i in(1,3)})
  work=max(1,len(xs)-1)*max(1,len(ys)-1)*max(1,len(qs))
  if work>4000000:raise ValueError('ROLE244_OVERLAY_WORK_BOUND')
  def has(rs,x,y):return any(a<x<c and b<y<d for a,b,c,d in rs)
  cells=[];areas={}
  for a,c in zip(xs,xs[1:]):
   tick()
   for b,d in zip(ys,ys[1:]):
    x,y=(a+c)/2,(b+d)/2
    if not has(own,x,y):continue
    ids=tuple(k for k,r in domains if has(r,x,y))
    label='ACTUAL_SOLID_NOT_USEFUL_FLOOR'if has(solids,x,y)else'SOURCE_ROLE_DOMAIN_SUPPORT_UNPROVEN'if len(ids)==1 else'CONFLICTING_ROLE_EXTENTS'if ids else'NO_SOURCE_ROLE_EXTENT'
    cells.append({'rect':list(map(str,(a,b,c,d))),'classification':label,'role_ids':list(ids)})
    areas[label]=areas.get(label,F(0))+(c-a)*(d-b)
  return cells,{k:str(v)for k,v in areas.items()}
 if type(m['units'])is not list or not m['units'] or len({u['id']for u in m['units']})!=len(m['units']):raise ValueError('UNIT_DOMAIN_INVENTORY')
 for u in m['units']:
  tick();uid=u['id'];own=region(u['ownership']);domains=[];seen=set()
  for pl in placements:
   tick()
   if pl.get('unit_id')!=uid:continue
   mod=pl['module'];schema=mod.get('schema');room=pl['room_id'];rid=uid+'.'+room
   if rid in seen:raise ValueError('DUPLICATE_ROLE_DOMAIN')
   seen.add(rid)
   if schema not in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118','KITCHEN_MODULE117'):
    rows.append({'unit':uid,'role_id':rid,'domain_status':'UNKNOWN_UNSUPPORTED_SOURCE_ROLE','intrinsic_use_verdict':'UNKNOWN','useful_extent_verified':False});continue
   # Same JSON digest domain as source contract114, not an area-based inference.
   if pl['module_hash']!=e.digest(mod):raise ValueError('MODULE_HASH_BINDING')
   mat=pl['transform']['matrix'];tr=pl['transform']['translation']
   if type(mat)is not list or len(mat)!=2 or any(type(v)is not list or len(v)!=2 for v in mat):raise ValueError('D4_SCHEMA')
   aa,bb,cc,dd=[e.number(v)for row in mat for v in row]
   if aa*aa+bb*bb!=1 or cc*cc+dd*dd!=1 or aa*cc+bb*dd!=0 or any(v not in(-1,0,1)for v in(aa,bb,cc,dd)):raise ValueError('D4_ISOMETRY_REQUIRED')
   tx,ty=map(e.number,tr)
   def transform(r):
    a,b,c,d=e.rectangle(r);ps=[(aa*x+bb*y+tx,cc*x+dd*y+ty)for x,y in((a,b),(a,d),(c,b),(c,d))]
    return (min(x for x,y in ps),min(y for x,y in ps),max(x for x,y in ps),max(y for x,y in ps))
   sourcefloor=mod['unit']['rooms']['kitchen'if schema=='KITCHEN_MODULE117'else'bed1'];parts=[transform(r)for r in sourcefloor]
   actual=region(u['rooms'][room]);ids=pl['id_map']
   for group in('fixtures','activities'):
    for key,q in mod['unit'][group].items():
     tick();mapped=ids.get(key,key.replace('bed1.',room+'.'))
     if e.rectangle(u[group][mapped])!=transform(q):raise ValueError('ACTUAL_SOURCE_INSTANCE_GEOMETRY')
   if g.outside(parts,own)>0:raise ValueError('SOURCE_ROLE_DOMAIN_OUTSIDE_OWNER')
   contained=g.outside(parts,actual)==0
   if not contained:raise ValueError('SOURCE_ROLE_FLOOR_MISSING')
   # Full source floor (including valid margins), not only furniture footprints.
   # This is intrinsic domain authority, not proof all its excess is useful.
   required={'ESSENTIAL_KITCHEN_FRIDGE_DRAWER_SURFACE_OPERATIONS'}if schema=='KITCHEN_MODULE117'else PRIVATE_USE244
   domain_use=required<=set(verified['resolved'])
   domains.append((rid,parts))
   rows.append({'unit':uid,'role_id':rid,'source_schema':schema,'module_hash':pl['module_hash'],'source_parts':encode(parts),'source_area_m2':str(g.exact_area(parts)),'declared_extra_area_m2':str(g.outside(actual,parts)),'domain_status':'SOURCE_KITCHEN_ROOM_FLOOR_BOUND'if schema=='KITCHEN_MODULE117'else'SOURCE_PRIVATE_ROOM_FLOOR_BOUND','intrinsic_use_verdict':'PASS_LIMITED_SOURCE_SELECTED_INSTANCE_USE'if domain_use else'UNKNOWN','intrinsic_scope':'SOURCE_ESSENTIAL_KITCHEN_OPERATIONS_NOT_WHOLE_ACCESS'if schema=='KITCHEN_MODULE117'else'SOURCE_CLOSET_SLEEP_ENDPOINT_ENTRY_BODY_ACCESS_NOT_ALL_FLOOR_USE','required_missing':sorted(required-set(verified['resolved'])),'useful_extent_verified':False,'supporting_extent_status':'PARAMETRIC_ROOM_FLOOR_NOT_GENERAL_UTILITY_PROOF'})
  cells,areas=overlay(own,region(list(m['walls'].values())),domains)
  unitrows.append({'unit':uid,'cells':cells,'area_by_class_m2':areas,'all_non_solid_extent_functionally_unresolved':True,'scope':'SOURCE_ROLE_ALLOCATION_AND_BOUND_INTRINSIC_USE_NOT_FINAL_Q11'})
 return rows,unitrows

# 247: direct same-consumer, stored-route graph only. No route search or floor grant.
PUBLIC247_PATH='staging237_guest_routes/integrated.py'
PUBLIC247_SHA='1ee78349a1e79ca7ee3a38e006784ae6d9c54db7ef4e5ac4828229dbb6bff2da'
_SOURCE247={'public_program_audit118.py':'aa282091606bbdfc3cd91b58567d2757edb6f2959ce8c0fbc62d593af4f82c99'}
# Filled with literal pinned hashes before freeze, never runtime-discovered authority.

def _stored_seat_graph247(model,unit,root,source,tick):
 """Internal kernel. Positive is a fixed conservative scenario, not general Q02.
 All graph edges are actual stored path subsegments; no invented connectors.
 Caller cannot submit an obstacle list or a graph.
 """
 # Closed bounded shape pass before Fraction parsing or any graph/union work.
 stack=[model];nodes=0
 while stack:
  tick();v=stack.pop();nodes+=1
  if nodes>100000:raise ValueError('GRAPH247_NODE_BOUND')
  if type(v)is dict:
   if len(v)>4000 or any(type(k)is not str or len(k)>4096 for k in v):raise ValueError('GRAPH247_MAPPING_BOUND')
   stack.extend(v.values())
  elif type(v)is list:
   if len(v)>4000:raise ValueError('GRAPH247_LIST_BOUND')
   stack.extend(v)
  elif type(v)is str and len(v)>4096:raise ValueError('GRAPH247_STRING_BOUND')
 F=source.F;body=F('.7');half=body/2
 if F(str(model['profile']['body_m']))!=body:raise ValueError('UNSUPPORTED_SOURCE_BODY_PROFILE')
 if 'source_geometry_contract'in model and F(str(model['source_geometry_contract']['body_m']))!=body:raise ValueError('UNSUPPORTED_SOURCE_BODY_PROFILE')
 owner=[source.q(r)for r in unit['ownership']];walls=[source.q(r)for r in model['walls'].values()]
 fixtures=[source.q(r)for u in model['units']for r in u['fixtures'].values()]
 cap=unit['public_program']['capacity'];seats=cap['living_seats'];uids=[r['fixture_id']for r in seats]
 if not seats or len(uids)!=len(set(uids)):raise ValueError('LIVING_INSTANCE_INVENTORY')
 expected={k for k,v in unit['fixture_metadata'].items()if v.get('kind')in('sofa1','sofa2','armchair1','armchair2')}
 if set(uids)!=expected:raise ValueError('LIVING_INSTANCE_INVENTORY')
 if len(seats)>64:raise ValueError('GRAPH247_INVENTORY_BOUND')
 obs=walls+fixtures;scenario=['STATIC_ACTUAL_SOLIDS','ALL_LIVING_AND_DINING_OCCUPIED','DINING_SOURCE_PULL_ENCLOSURES','SOURCE_KITCHEN_MOTION_ENCLOSURES','OPEN_DOOR_PANELS','EXPLICIT_PRIVATE_KITCHEN_EXCLUSION']
 for row in seats:
  q=source.q(row['occupied_body'])
  if (q[2]-q[0],q[3]-q[1])!=(body,body)or not source.covered(q,[source.q(unit['fixtures'][row['fixture_id']])]):raise ValueError('SOURCE_OCCUPIED_BODY_BINDING')
  obs.append(q)
 for op in model['operations']['dining_chairs']:
  if op['unit']!=unit['id']:continue
  a=source.q(op['closed_rect']);b=source.q(op['open_rect']);v=tuple(F(str(x))for x in op['translation'])
  if len(v)!=2 or v[0]*v[1]or sum(abs(x)for x in v)!=F('.4')or tuple(a[i]+v[i%2]for i in range(4))!=b:raise ValueError('SCENARIO_SOURCE_CHAIR_MOTION')
  obs.extend([source.q(op['occupied_body']),(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))])
 for op in model['operations'].get('doors',[]):obs.append(source.q(op['open_panel']))
 kitchens=[k for k in model['operations'].get('kitchen',[])if k.get('unit')==unit['id']]
 if len(kitchens)!=1 or not kitchens[0].get('motion_envelopes'):raise ValueError('SOURCE_KITCHEN_SCENARIO_INCOMPLETE')
 for op in kitchens:
  if F(str(op['assumptions']['body_m']))!=body:raise ValueError('SCENARIO_SOURCE_BODY_MISMATCH')
  obs.extend(source.q(r)for r in op['motion_envelopes'])
 obs.extend(source.q(r)for k,rs in unit['rooms'].items()if k.startswith('bed')or k in('bath','kitchen','private_circulation')for r in rs)
 obs.extend(source.q(r)for k,r in unit['activities'].items()if k.startswith('kitchen'))
 root=tuple(F(str(v))for v in root);paths={'guest_living':unit['scenario_routes']['guest_living']};targets={}
 if tuple(F(str(v))for v in paths['guest_living'][0])!=root:raise ValueError('SOURCE_ROOT_MISMATCH')
 for seat in seats:
  key=seat['access_activity_id'];p=unit['routes'][key];end=tuple(F(str(v))for v in p[-1]);q=(end[0]-half,end[1]-half,end[0]+half,end[1]+half)
  if not source.covered(q,[source.q(unit['activities'][key])])or source.hit(q,source.q(unit['fixtures'][seat['fixture_id']])):raise ValueError('SOURCE_STANDING_TARGET_BINDING')
  targets[seat['fixture_id']]=end;paths[key]=p
 segments=[]
 for name,p in paths.items():
  tick()
  if type(p)is not list or not 2<=len(p)<=256:raise ValueError('STORED_ROUTE_BOUND')
  for a,b in zip(p,p[1:]):
   a=tuple(F(str(v))for v in a);b=tuple(F(str(v))for v in b)
   if len(a)!=2 or len(b)!=2 or a==b or(a[0]!=b[0]and a[1]!=b[1]):raise ValueError('STORED_ROUTE_NOT_ORTHOGONAL')
   segments.append((a,b,name))
 if len(segments)>512 or len(obs)>4000 or len(segments)**2+len(segments)*max(1,len(obs))*max(1,len(owner))>4000000:raise ValueError('GRAPH247_WORK_BOUND')
 # Reserve exact source.covered grid scans before entering its nested loops.
 poses={'root':root,**{'target:'+k:p for k,p in targets.items()}}
 pose_rects={k:(p[0]-half,p[1]-half,p[0]+half,p[1]+half)for k,p in poses.items()}
 work=len(segments)**2+(len(segments)+len(pose_rects))*len(obs)
 # Include every stationary body in the same pre-work coverage budget.
 for sw in pose_rects.values():
  tick()
  xs={sw[0],sw[2]}|{r[i]for r in owner for i in(0,2)if sw[0]<r[i]<sw[2]}
  ys={sw[1],sw[3]}|{r[i]for r in owner for i in(1,3)if sw[1]<r[i]<sw[3]}
  work+=(len(xs)-1)*(len(ys)-1)*max(1,len(owner))
  if work>4000000:raise ValueError('GRAPH247_SOURCE_COVERAGE_WORK_BOUND')
 for a,b,_ in segments:
  tick();sw=(min(a[0],b[0])-half,min(a[1],b[1])-half,max(a[0],b[0])+half,max(a[1],b[1])+half)
  xs={sw[0],sw[2]}|{r[i]for r in owner for i in(0,2)if sw[0]<r[i]<sw[2]}
  ys={sw[1],sw[3]}|{r[i]for r in owner for i in(1,3)if sw[1]<r[i]<sw[3]}
  work+=(len(xs)-1)*(len(ys)-1)*max(1,len(owner))
  if work>4000000:raise ValueError('GRAPH247_SOURCE_COVERAGE_WORK_BOUND')
 blocked_poses=[]
 for name,sw in pose_rects.items():
  tick()
  if not source.covered(sw,owner)or any(source.hit(sw,o)for o in obs):blocked_poses.append(name)
 valid=[];blocked=[]
 for a,b,name in segments:
  tick();sw=(min(a[0],b[0])-half,min(a[1],b[1])-half,max(a[0],b[0])+half,max(a[1],b[1])+half)
  if not source.covered(sw,owner)or any(source.hit(sw,o)for o in obs):blocked.append({'route':name,'segment':[list(map(str,a)),list(map(str,b))],'reason':'FIXED_CONSERVATIVE_SCENARIO_NOT_CLEAR_NOT_GLOBAL_IMPOSSIBILITY'})
  else:valid.append((a,b,name))
 def on(p,a,b):return min(a[0],b[0])<=p[0]<=max(a[0],b[0])and min(a[1],b[1])<=p[1]<=max(a[1],b[1])and (a[0]==b[0]==p[0]or a[1]==b[1]==p[1])
 points={root,*targets.values()}
 for a,b,_ in valid:points.update((a,b))
 for i,(a,b,_)in enumerate(valid):
  tick()
  for c,d,_ in valid[i+1:]:
   if a[0]==b[0]and c[1]==d[1]:p=(a[0],c[1])
   elif a[1]==b[1]and c[0]==d[0]:p=(c[0],a[1])
   else:continue
   if on(p,a,b)and on(p,c,d):
    points.add(p)
    if len(points)>4096:raise ValueError('GRAPH247_POINT_BOUND')
 # Bound splitting adjacency separately before construction.
 if work+len(points)*max(1,len(valid))>4000000:raise ValueError('GRAPH247_SPLIT_WORK_BOUND')
 graph={p:set()for p in points}
 for a,b,_ in valid:
  tick();ps=sorted(p for p in points if on(p,a,b))
  for c,d in zip(ps,ps[1:]):graph[c].add(d);graph[d].add(c)
 seen=set()if 'root'in blocked_poses else{root};queue=list(seen)
 for a in queue:
  tick()
  for b in graph[a]:
   if b not in seen:seen.add(b);queue.append(b)
 missing=[k for k,p in targets.items()if p not in seen or 'target:'+k in blocked_poses]
 return {'unit':unit['id'],'verdict':'PASS_STORED_SOURCE_ROUTE_NETWORK_SCOPED'if not missing else'UNKNOWN','targets':{k:list(map(str,p))for k,p in targets.items()},'source_root':list(map(str,root)),'unconnected_stored_targets':missing,'blocked_stored_segments':blocked,'blocked_body_poses':blocked_poses,'scenario':scenario,'scenario_scope':'SUFFICIENT_COMMON_ENCLOSURE_PROFILE_NOT_NEW_SIMULTANEITY_REQUIREMENT','body_m':'0.7','global_path_completeness':False,'new_routes_generated':False,'whole_living_extent_verified':False,'repair_authority':False,'delivery_allowed':False}

_PUBLIC_CALLS247={}
_PUBLIC_MAX247=16

def evaluate_public_guest247(origin,converted,source_binding,fresh,*,remaining_budget_seconds,cancel_token):
 """Replacement for the existing same-call 237 invocation, not an extra call.
 Internal worker API; no client report/receipt input. Returns original report.
 """
 m=sys.modules.get('_guest_routes237');j=sys.modules.get('origin_join')
 if m is None or hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()!=PUBLIC247_SHA:raise ValueError('FIXED_GUEST237_INSTANCE_REQUIRED')
 if j is None:raise ValueError('LIVE_ORIGIN_REQUIRED')
 j.verify_native_immutability(origin,converted,source_binding)
 if j.digest(fresh)!=origin._data['fresh_result_digest']:raise ValueError('NOT_SAME_FRESH_RESULT')
 if len(_PUBLIC_CALLS247)>=_PUBLIC_MAX247:raise ValueError('PUBLIC_CALL247_WORKER_LIFETIME_BOUND')
 result=m.evaluate(origin,converted,source_binding,fresh,remaining_budget_seconds=remaining_budget_seconds,cancel_token=cancel_token)
 j.verify_native_immutability(origin,converted,source_binding)
 if j.digest(fresh)!=origin._data['fresh_result_digest']:raise ValueError('FRESH_MUTATED')
 # Strong original-object references and immutable payload checksum, worker-local.
 _PUBLIC_CALLS247[id(result)]=(result,j.digest(result),origin,j.digest(converted),source_binding,j.digest(fresh),m)
 return result

def _verify_original_public247(j,m,origin,converted,source_binding,public_report,fresh):
 rec=_PUBLIC_CALLS247.get(id(public_report))
 if rec is None or rec[0]is not public_report or rec[2]is not origin or rec[6]is not m:raise ValueError('ORIGINAL_SAME_CALL_PUBLIC_REPORT_REQUIRED')
 if (rec[1],rec[3],rec[4],rec[5])!=(j.digest(public_report),j.digest(converted),source_binding,j.digest(fresh)):raise ValueError('PUBLIC_CALL247_PAYLOAD_OR_CONTEXT_CHANGED')
 return rec

def attach_living_network247(native,origin,converted,source_binding,capacity_fact,public_report,fresh,*,remaining_budget_seconds=10,cancel_token=None):
 import threading,time,math
 start=time.monotonic();event=cancel_token if cancel_token is not None else threading.Event()
 out={'schema':'STORED_LIVING_NETWORK247','verdict':'UNKNOWN','obligations':[],'missing':[],'whole_living_extent_verified':False,'parent_complete':False,'repair_authority':False,'delivery_allowed':False}
 try:
  if type(event)is not threading.Event or type(remaining_budget_seconds)not in(int,float)or not math.isfinite(remaining_budget_seconds)or not 0<remaining_budget_seconds<=30:raise ValueError('SERVER_BUDGET')
  def tick():
   if event.is_set()or time.monotonic()-start>=remaining_budget_seconds:raise ValueError('GRAPH247_CANCEL_OR_BUDGET')
  tick();cm=sys.modules.get('_capacity_composition215_v2');j=sys.modules.get('origin_join');m=sys.modules.get('_guest_routes237')
  if cm is None or hashlib.sha256(Path(cm.__file__).read_bytes()).hexdigest()!='25eb7203aba3969c44e3669f772233dc606ec990e05561b3c606310ad036fd47':raise ValueError('FIXED_CAPACITY246_INSTANCE_REQUIRED')
  verified=cm.verify_fact(capacity_fact,origin,converted,source_binding)
  if not {'SELECTED_PROGRAM_ACTUAL_SLEEP_DINING_LIVING_PLANAR_CAPACITY','ESSENTIAL_KITCHEN_FRIDGE_DRAWER_SURFACE_OPERATIONS'}<=set(verified['resolved']):raise ValueError('SOURCE_LIVING_CAPACITY_OR_KITCHEN_SCENARIO_WITNESS_MISSING')
  rec=_verify_original_public247(j,m,origin,converted,source_binding,public_report,fresh)
  if m is None or hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()!=PUBLIC247_SHA:raise ValueError('GUEST237_CODE_CHANGED')
  if j.digest(fresh)!=origin._data['fresh_result_digest']:raise ValueError('NOT_SAME_FRESH_RESULT')
  packet=converted['packet']
  if native.get('packet_digest')!=j.digest(packet):raise ValueError('NATIVE_PACKET_BINDING')
  frames=native.get('frames',[])
  if len(frames)!=2 or {f.get('frame')for f in frames}!={'local_model','world_model'}or any(f.get('model_digest')!=j.digest(packet[f['frame']])for f in frames):raise ValueError('NATIVE_MODEL_BINDING')
  if public_report.get('packet_hash')!=j.digest(packet)or public_report.get('source_binding')!=source_binding:raise ValueError('PUBLIC_MODEL_SOURCE_BINDING')
  obligations=public_report['obligations'];needed={(f,u,r)for f in('local_model','world_model')for u in('A','B')for r in('guest_living','guest_dining')}
  keys=[(x['frame'],x['unit'],x['route'])for x in obligations]
  if len(keys)!=len(needed)or set(keys)!=needed:raise ValueError('PUBLIC_SCOPE_INVENTORY')
  if any(x['verdict']!='PASS'or x['source_profile']!='SOURCE_PUBLIC118_BODY_POINT7'for x in obligations):raise ValueError('PUBLIC_SOURCE_ROUTE_SCOPE_UNVERIFIED')
  source_path=ROOT/'planha_general150_runtime_work/public_program_audit118.py';raw=source_path.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=_SOURCE247['public_program_audit118.py']:raise ValueError('SOURCE_PUBLIC_CHECKER_CHANGED')
  source=types.ModuleType('_source_public247');source.__file__=str(source_path);exec(compile(raw,str(source_path),'exec'),source.__dict__)
  for frame in('local_model','world_model'):
   model=packet[frame]
   if len(model['units'])!=2 or sorted(u['id']for u in model['units'])!=['A','B']:raise ValueError('GRAPH247_EXACT_AB_UNITS')
   for unit in model['units']:
    tick();row=next(x for x in obligations if(x['frame'],x['unit'],x['route'])==(frame,unit['id'],'guest_living'))
    result=_stored_seat_graph247(model,unit,row['source_root'],source,tick)
    out['obligations'].append(dict(result,frame=frame,model_hash=j.digest(model),source_public_hash=_SOURCE247['public_program_audit118.py']))
  cm.verify_fact(capacity_fact,origin,converted,source_binding)
  if j.digest(public_report)!=rec[1]or j.digest(fresh)!=rec[5]or source_path.read_bytes()!=raw:raise ValueError('SOURCE_OR_REPORT_CHANGED')
  tick();out['missing']=['WHOLE_LIVING_SUPPORTING_EXTENT_UNPROVEN','FINAL_Q11_CIRCULATION_NECESSITY_UNPROVEN']
  if any(x['verdict']=='UNKNOWN'for x in out['obligations']):out['missing'].append('STORED_ROUTE_NETWORK_INCOMPLETE_NOT_GLOBAL_INFEASIBILITY')
  out['scoped_network_complete']=all(x['verdict']=='PASS_STORED_SOURCE_ROUTE_NETWORK_SCOPED'for x in out['obligations'])
 except (ValueError,KeyError,TypeError,AttributeError,IndexError,ZeroDivisionError,StopIteration,OverflowError,OSError)as exc:
  out['obligations']=[];out['missing'].append('LIVING_NETWORK247_UNVERIFIED:'+str(exc));out['scoped_network_complete']=False
 native['living_network247']=out
 return native

# 248 source-instance identity is not a catalog alias or capacity proof.
INSTANCE248_PINS={'twin_module118.py': '074c6f39f613977e0d7417a99f0d9682343d433713774faa7a18c85283e93260', 'bedroom_module116.py': '21bcadf03beb91b9b78a85d2b87520b594c19dce28b932860d871744e4815789', 'place_module116.py': '128e1545104de9dd3ae3c347c08e2d3f857bd0968dce4ea972a5157f43bfce6a', 'place_module133.py': 'a945f87b0ef909b166d35da2862251fe3063325c450990c4bde9ce24a38bc007', 'dining_module118.py': 'ec4ee12434adc5517c0407549374b138ea88d1e475ff13823e4c91a8a66ed7d7', 'dining_module121.py': '75a3a268e016898f7df9b925f863f056e9a6c4373a55d28d5243b6cf64027e22', 'dining_inventory119.py': '98b93deae20af0cd4b0a89102318b63736e2b0deb0231a48823d97b09a2d0288', 'assemble114.py': 'b12cf81eb0acdfd5c696445fe7821235012f589cac9477b865da89093c0b095e', 'typed_public_access120.py': 'ff381a06bf4272e75225ed898067d1818028a588fc72af37a86776332c1b2e3e', 'bedroom_approach_audit123.py': 'bd09ce5607e7065401a03e938b67c3114abdec9e10798182b4749e30c6f066c1', 'references/CAPACITY_PROGRAM118_SOURCE.json': '427cde4c55e57ea7c26ff52bb2651859750b93913cc86ecdf2751fad37566e8f', 'references/program6/proposal_metadata.json': 'ca992de5c7ee38a5d84addcdd8abd51ab2801317654f41ab2c9fe7522084c3c6', 'references/program6/chair_reference_model.json': '2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4', 'references/program6/assembly_AA-1924803-2.pdf': '24ad6e419508b4f8cb87d7f270e84df5deb5523f60e02098fab39759f8cb7d71'}
INSTANCE248_CLOSURE_SHA='6f1e6cb00b1fb2ce1bf65f24a019be9c38d58353e14e442cedd28d6a65d18802'

LIVING251_SOURCE_NAMES=('seating_binding142.py', 'seating_source142.py', 'assemble142.py', 'contract114.py', 'references/lr_option2_125x20_model.json')
INSTANCE248_PINS.update({'seating_binding142.py': 'fd34396fd1d94705aa149ac1583d377b830e7c34227b4d4b4c48ac5288ebeb52', 'seating_source142.py': '525610d31faf5f12b7787995536cafb71325ca6766ac6115bce093bf402419ce', 'assemble142.py': '62106191e06d8826de6ba76cab7b38be90c70fa28291f9e209e909b3bdbd9eb9', 'contract114.py': '8fa52a9d992cd078e7dd3356bab61de7b9687d60a4ae52fc403a3e0b2203dbcf', 'references/lr_option2_125x20_model.json': '2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4'})

def _capture_instances248(tick):
 raw=(ROOT/'staging246_kitchen_binding/source_closure.json').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=INSTANCE248_CLOSURE_SHA:raise ValueError('INSTANCE248_CLOSURE_DOCUMENT')
 pins=json.loads(raw);captured={}
 for name,h in pins.items():
  tick();data=(ROOT/'planha_general150_runtime_work'/name).read_bytes()
  if hashlib.sha256(data).hexdigest()!=h:raise ValueError('INSTANCE248_SOURCE_DRIFT:'+name)
  captured[name]=data
 if sum(map(len,captured.values()))>64000000:raise ValueError('INSTANCE248_CAPTURE_BOUND')
 for name,h in INSTANCE248_PINS.items():
  if name not in captured or hashlib.sha256(captured[name]).hexdigest()!=h:raise ValueError('INSTANCE248_FIXED_SOURCE:'+name)
 return captured

def _placed_instances248(model,g,tick,work=None):
 """Private pure bounded projection, not independently source-authoritative.
 Public entry requires live source replay/context + original verified fact.
 """
 e=g.e;rows=[];missing=[];work=[0]if work is None else work;units=model['units'];placements=model['module_placements']
 if type(units)is not list or len(units)>2 or len({u['id']for u in units})!=len(units)or type(placements)is not list or len(placements)>100:raise ValueError('INSTANCE248_INVENTORY_BOUND')
 def d4(t):
  mat=t['matrix'];tr=t['translation']
  if type(mat)is not list or len(mat)!=2 or any(type(r)is not list or len(r)!=2 for r in mat)or type(tr)is not list or len(tr)!=2:raise ValueError('INSTANCE248_D4_SHAPE')
  a,b,c,d=[e.number(x)for r in mat for x in r];tx,ty=map(e.number,tr)
  if any(x not in(-1,0,1)for x in (a,b,c,d))or a*a+b*b!=1 or c*c+d*d!=1 or a*c+b*d:raise ValueError('INSTANCE248_D4')
  def move(q):
   x,y,z,w=e.rectangle(q);ps=[(a*i+b*j+tx,c*i+d*j+ty)for i,j in((x,y),(x,w),(z,y),(z,w))];return min(x for x,y in ps),min(y for x,y in ps),max(x for x,y in ps),max(y for x,y in ps)
  return move
 for unit in units:
  uid=unit['id'];own=g.rectangles(unit['ownership']);claimed=set();expected_single=set()
  records=[]
  for p in placements:
   tick()
   if p.get('unit_id')!=uid:continue
   mod=p['module']
   if mod.get('schema')!='PRIVATE_TWIN_ROOM_MODULE118':continue
   if p['module_hash']!=e.digest(mod)or mod['source_binding']['producer_sha256']!=INSTANCE248_PINS['twin_module118.py']:raise ValueError('INSTANCE248_TWIN_SOURCE')
   profile=mod['sleep_profile'];keys={'bed1.bedA','bed1.bedB'}
   if profile['id']!='A9_F5_SINGLE_BED_0.9x1.9'or profile['source_file']!='references/CAPACITY_PROGRAM118_SOURCE.json'or profile['source_sha256']!=INSTANCE248_PINS[profile['source_file']]or set(profile['target_fixture_ids'])!=keys or sorted(map(e.number,profile['physical_size_m']))!=[e.F('.9'),e.F('1.9')]or profile['scale_allowed']is not False:raise ValueError('INSTANCE248_SINGLE_PROFILE')
   source=mod['unit']['fixtures'];ids=p['id_map']
   if not keys<=set(source)or not set(source)<=set(ids)or len({ids[k]for k in source})!=len(source):raise ValueError('INSTANCE248_TWIN_ID_MAP')
   move=d4(p['transform'])
   for key in keys:
    actual=ids[key];expected_single.add(actual)
    if mod['unit']['fixture_metadata'][key]['kind']!='single_bed':raise ValueError('INSTANCE248_TWIN_METADATA')
    records.append((actual,key,source[key],move,p['room_id'],'A9_F5_SINGLE_BED_0.9x1.9',[e.F('.9'),e.F('1.9')],p['module_hash'],'single_bed'))
  actual_single={k for k,v in unit['fixture_metadata'].items()if v.get('kind')=='single_bed'}
  if actual_single!=expected_single:raise ValueError('INSTANCE248_SINGLE_INVENTORY')
  p=unit.get('dining_module_placement')
  if p is None:missing.append(uid+':DINING_PLACEMENT_MISSING')
  else:
   mod=p['module'];schema=mod.get('schema');six=schema=='SIX_PLACE_PLANAR_SOURCE_STUDY_V1'
   if schema not in ('SIX_PLACE_PLANAR_SOURCE_STUDY_V1','DINING_CAPACITY_MODULE118_PROPOSAL'):raise ValueError('INSTANCE248_DINING_SCHEMA')
   keys={'table',*('chair_'+x for x in (('front_left','front_right','back_left','back_right','left','right')if six else('west','east','front','back')))}
   source=mod['fixtures'];ids=p['id_map'];seating=mod['seating'];n=6 if six else 4
   if p['module_hash']!=e.digest(mod)or set(source)!=keys or set(ids)!=keys or len(set(ids.values()))!=len(keys)or seating['requested_places']!=n or seating['distinct_chair_count']!=n:raise ValueError('INSTANCE248_DINING_INVENTORY')
   seats=seating['instances'];seatkeys=[x['fixture_id']for x in seats]
   if len(seatkeys)!=n or set(seatkeys)!=keys-{'table'}:raise ValueError('INSTANCE248_SEAT_INVENTORY')
   if six:
    binding=mod['source_binding']
    for key,name in [('metadata_sha256','references/program6/proposal_metadata.json'),('assembly_sha256','references/program6/assembly_AA-1924803-2.pdf'),('chair_source_sha256','references/program6/chair_reference_model.json')]:
     if binding[key]!=INSTANCE248_PINS[name]:raise ValueError('INSTANCE248_DINING_SOURCE_PROFILE')
    if binding['chair_source_fixture_key']!='dining_chair_front'or list(map(e.number,binding['table_fixed_dimensions_m']))!=[e.F('2.2'),e.F(1),e.F('.74')]:raise ValueError('INSTANCE248_DINING_PROFILE_DIMENSIONS')
   actual_dining={k for k,v in unit['fixture_metadata'].items()if v.get('kind')in('dining_table6','dining_table','dining_chair_front','dining_chair_back')}
   if actual_dining!=set(ids.values()):raise ValueError('INSTANCE248_DINING_EXTRA_OR_MISSING')
   move=d4(p['transform'])
   for key in sorted(keys):
    kind=('dining_table6'if six else'dining_table')if key=='table'else'dining_chair_front'if key in(('chair_front_left','chair_front_right','chair_left')if six else('chair_west','chair_front'))else'dining_chair_back'
    dims=([e.F(1),e.F('2.2')]if six else[e.F('.8'),e.F('1.2')])if key=='table'else[e.F('.5'),e.F('.5')]
    profile='SOURCE121_TABLE6'if key=='table'and six else'SOURCE118_TABLE4'if key=='table'else'SOURCE_REFERENCE_CHAIR_POINT5'
    records.append((ids[key],key,source[key],move,'dining',profile,dims,p['module_hash'],kind))
  if len(records)>64:raise ValueError('INSTANCE248_RECORD_BOUND')
  for actual,key,source_rect,move,room,profile,dims,mhash,kind in records:
   tick()
   if actual in claimed:raise ValueError('INSTANCE248_DUPLICATE_ACTUAL_ID')
   claimed.add(actual);r=e.rectangle(unit['fixtures'][actual]);s=e.rectangle(source_rect)
   if r!=move(source_rect)or unit['fixture_metadata'][actual]['kind']!=kind:raise ValueError('INSTANCE248_ACTUAL_SOURCE_BINDING')
   if sorted((s[2]-s[0],s[3]-s[1]))!=sorted(dims):raise ValueError('INSTANCE248_SOURCE_DIMENSIONS')
   regions=g.rectangles(unit['rooms'][room]);n=len(regions)+len(own)+2;work[0]+=8*n*n*max(1,n.bit_length())
   if work[0]>4000000:raise ValueError('INSTANCE248_CONTAINMENT_WORK_BOUND')
   inside=g.outside([r],regions)==0 and g.outside([r],own)==0
   rows.append({'unit':uid,'actual_fixture_id':actual,'source_fixture_key':key,'source_profile_id':profile,'source_module_hash':mhash,'role_id':uid+'.'+room,'actual_rect_digest':e.digest(unit['fixtures'][actual]),'region_digest':e.digest(unit['rooms'][room]),'proof_kind':'SOURCE_PLACED_INSTANCE_NOT_CATALOG_ALIAS','dimensions_exact':True,'contained':inside,'verdict':'PASS_LIMITED_DIMENSIONS_CONTAINMENT'if inside else'FAIL_SCOPED_CONTAINMENT','existing_category_inventory_complete':True,'operation_verified':False,'whole_quality':False,'repair_authority':False,'delivery_allowed':False})
  missing.append(uid+':LIVING_INSTANCE_SOURCE_BRANCH_NOT_IMPLEMENTED')
 return rows,missing


def _living_records251(converted,g,captured,tick):
 """Exact pinned source_records projection; no evidence/search/unit_geometry call.
 Pure internal helper is not origin authority; late entry checks same live context.
 """
 import ast,tempfile
 from decimal import Decimal,localcontext
 e=g.e;p=converted['packet'];t=converted['generation_context']['construction_trace'];proposal=t['proposal']
 if proposal.get('generation_method')!='SIDECAR_COMPACT_D4_GROUP142_LOCAL_WORLD_PENDING':return None
 if p['family']!='LEFT_RIGHT'or t['family']!='LEFT_RIGHT':raise ValueError('LIVING251_FAMILY')
 # contract114.digest uses canonical UTF8, not ASCII escaping.
 for key,hkey in [('local_model','local_model_hash'),('world_model','model_hash'),('core','core_hash')]:
  if e.digest(p[key])!=t[hkey]:raise ValueError('LIVING251_TRACE_HASH:'+key)
 if json.dumps(p['core']['world_from_local'],sort_keys=True,separators=(',',':'))!=json.dumps({'matrix':[[0,1],[1,0]],'translation':['0','0']},sort_keys=True,separators=(',',':')):raise ValueError('LIVING251_WORLD_TRANSFORM')
 for frame in ('local_model','world_model'):
  m=p[frame]
  if sorted(u['id']for u in m['units'])!=['A','B']or e.number(m['profile']['body_m'])!=e.F('.7')or e.number(m['source_geometry_contract']['body_m'])!=e.F('.7'):raise ValueError('LIVING251_PROFILE_OR_UNITS')
 for name in LIVING251_SOURCE_NAMES:
  if hashlib.sha256(captured[name]).hexdigest()!=INSTANCE248_PINS[name]:raise ValueError('LIVING251_SOURCE_CHANGED')
 # Exact source AST, limited to the raw-source reconstruction functions/constants.
 tree=ast.parse(captured['seating_binding142.py']);keep={'move_point','move_rect','source_records'};const={'IDS','MARKER','SPEC','SHA'}
 nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in keep or isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id in const for x in n.targets)]
 if {n.name for n in nodes if isinstance(n,ast.FunctionDef)}!=keep:raise ValueError('LIVING251_SOURCE_AST')
 st=ast.parse(captured['contract114.py']);sn=next(n for n in st.body if isinstance(n,ast.FunctionDef)and n.name=='S')
 with tempfile.TemporaryDirectory(prefix='living251_source_')as tmp:
  root=Path(tmp);ref=root/'references/lr_option2_125x20_model.json';ref.parent.mkdir();ref.write_bytes(captured['references/lr_option2_125x20_model.json'])
  ns={'F':e.F,'BODY':e.F('.7'),'Path':Path,'json':json,'hashlib':hashlib,'Decimal':Decimal,'localcontext':localcontext,'__file__':str(root/'seating_binding142.py')}
  exec(compile(ast.fix_missing_locations(ast.Module(body=[sn]+nodes,type_ignores=[])),'<PINNED_SOURCE_RECORDS251>','exec'),ns)
  tick();records,_=ns['source_records'](proposal);tick()
  if json.dumps(records,sort_keys=True,separators=(',',':'),default=ns['S'])!=json.dumps(proposal['compact_d4_sources142'],sort_keys=True,separators=(',',':')):raise ValueError('LIVING251_TYPED_SOURCE_RECORD')
 return {'records':records,'proposal_digest':e.digest(proposal),'length':e.number(p['local_model']['inputs'][1]),'move_rect':ns['move_rect'],'move_point':ns['move_point']}


def _living_rows251(model,frame,g,bound,tick,work):
 if bound is None:return [],[u['id']+':LIVING_SOURCE_BRANCH_UNSUPPORTED'for u in model['units']]
 e=g.e;rows=[];records=bound['records'];ids=set(records)
 for u in model['units']:
  uid=u['id'];matrix=((1,0),(0,1))if uid=='A'else((1,0),(0,-1));translation=(0,0)if uid=='A'else(0,bound['length'])
  def qmove(q):
   z=bound['move_rect'](q,matrix,translation)
   return bound['move_rect'](z,((0,1),(1,0)),(0,0))if frame=='world_model'else z
  def pmove(q):
   z=bound['move_point'](q,matrix,translation)
   return(z[1],z[0])if frame=='world_model'else z
  categories={'sofa1','sofa2','armchair1','armchair2'}
  actual={k for k,v in u['fixture_metadata'].items()if v.get('kind')in categories or k.startswith(('sofa','armchair'))}
  if actual!=ids or not ids<=set(u['fixtures']):raise ValueError('LIVING251_INSTANCE_INVENTORY')
  own=g.rectangles(u['ownership']);regions=g.rectangles(u['rooms']['living'])
  for name,r in records.items():
   tick();actual_rect=e.rectangle(u['fixtures'][name]);md=u['fixture_metadata'][name];dims=(e.F('2.2'),e.F('.9'))if name.startswith('sofa')else(e.F('.8'),e.F('.8'))
   # Size is derived independently from immutable reference via source record.
   source_dims=sorted((r['fixture'][2]-r['fixture'][0],r['fixture'][3]-r['fixture'][1]))
   angle=(90-r['rotation'])%180 if frame=='world_model'else r['rotation']
   if source_dims!=sorted(dims)or actual_rect!=qmove(r['fixture'])or md['kind']!=r['source_key']or type(md.get('walkable'))is not bool or md['walkable']is not False or e.number(md['rotation_deg'])!=angle or tuple(map(e.number,md['source_size_m']))!=dims:raise ValueError('LIVING251_ACTUAL_SOURCE_PROFILE')
   if e.rectangle(u['activities'][name+'_front'])!=qmove(r['reserved_activity'])or tuple(map(e.number,u['route_targets'][name+'_front']))!=pmove(r['target']):raise ValueError('LIVING251_ACTIVITY_TARGET')
   n=len(own)+len(regions)+2;work[0]+=8*n*n*max(1,n.bit_length())
   if work[0]>4000000:raise ValueError('LIVING251_CONTAINMENT_WORK_BOUND')
   inside=g.outside([actual_rect],regions)==0 and g.outside([actual_rect],own)==0
   rows.append({'unit':uid,'actual_fixture_id':name,'source_fixture_key':r['source_key'],'source_profile_id':'SOURCE142_REFERENCE_SEATING_D4','source_kind':'PROPOSAL_SOURCE_RECORD','source_proposal_digest':bound['proposal_digest'],'source_module_hash':bound['proposal_digest'],'role_id':uid+'.living','actual_rect_digest':e.digest(u['fixtures'][name]),'region_digest':e.digest(u['rooms']['living']),'proof_kind':'SOURCE_PLACED_INSTANCE_NOT_CATALOG_ALIAS','dimensions_exact':True,'contained':inside,'verdict':'PASS_LIMITED_DIMENSIONS_CONTAINMENT'if inside else'FAIL_SCOPED_CONTAINMENT','existing_category_inventory_complete':True,'operation_verified':False,'whole_quality':False,'repair_authority':False,'delivery_allowed':False})
 return rows,[]

def _logical_access248(model,g,captured,tick,stats=None):
 """Use exact existing source resolver; logical views never enter partition rooms.
 Dedicated supervised worker; captured private import tree restored on exit.
 """
 import tempfile,importlib
 rows=[];stats={}if stats is None else stats;stats['resolver_calls']=0;names={Path(n).stem for n in captured if n.endswith('.py')and '/'not in n}
 with tempfile.TemporaryDirectory(prefix='logical248_')as tmp:
  root=Path(tmp)
  for name,data in captured.items():
   tick();p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  saved={n:sys.modules.get(n)for n in names};oldpath=list(sys.path)
  try:
   for name in names:sys.modules.pop(name,None)
   sys.path.insert(0,tmp);resolver=importlib.import_module('typed_public_access120')
   cache={};units={u['id']:u for u in model['units']}
   if len(model['openings'])>100:raise ValueError('LOGICAL248_OPENING_BOUND')
   for opening in model['openings']:
    tick();connects=opening['connects']
    if type(connects)is not list or len(connects)!=2:raise ValueError('LOGICAL248_CONNECTS')
    views={};missing=[]
    for role in connects:
     if role in model.get('logical_regions',{}):
      uid=model['logical_regions'][role].get('unit');key=(uid,role)
      if role==str(uid)+'.private_access':
       missing.append(role+':PRIVATE_ROLE_CACHE_EQUIVALENCE_NOT_IMPLEMENTED');continue
      if role in (str(uid)+'.bedroom_public_access',str(uid)+'.kitchen_public_access'):
       source_role='M.public_access'if role.endswith('.bedroom_public_access')else'K.public_access';allowed=[]
       for placement in model.get('module_placements',[]):
        if placement.get('unit_id')!=uid or placement.get('id_map',{}).get(source_role)!=role:continue
        allowed.extend(placement['id_map'][o['id']]for o in placement['module']['openings']if source_role in o['connects'])
       actual_ids=[o['id']for o in model['openings']if role in o['connects']]
       if len(allowed)!=len(set(allowed))or len(actual_ids)!=len(set(actual_ids))or set(allowed)!=set(actual_ids)or opening['id']not in allowed:raise ValueError('LOGICAL248_COMPLETE_OPENING_CONTEXT')
      elif role!=str(uid)+'.public_access':
       missing.append(role+':UNSUPPORTED_LOGICAL_ROLE');continue
      if key not in cache:
       try:
        stats['resolver_calls']+=1;cache[key]=('RESOLVED',resolver.parts(model,units[uid],role,opening['id']))
       except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as exc:cache[key]=('UNKNOWN',str(exc))
      status,value=cache[key]
      if status=='RESOLVED':views[role]=[list(map(str,r))for r in value]
      else:missing.append(role+':'+value)
     elif '.'in role and role.split('.',1)[0]in units:
      uid,name=role.split('.',1)
      if name in units[uid]['rooms']:views[role]=units[uid]['rooms'][name]
      else:missing.append(role+':PHYSICAL_ROOM_MISSING')
     elif role in model.get('common_spaces',{}):
      v=model['common_spaces'][role];views[role]=v if role=='lobby'else[v]
     else:missing.append(role+':ROLE_UNSUPPORTED')
    if not any(r in model.get('logical_regions',{})for r in connects):continue
    result=g.opening_region_adjacency(opening['id'],opening['rect'],connects,views)if not missing and len(views)==2 else None
    rows.append({'opening_id':opening['id'],'proof_kind':'EXACT_TYPED_PUBLIC_ACCESS120_RESOLVER','logical_views_digest':g.e.digest(views),'partition_rooms_unchanged':True,'adjacency':result,'missing':missing,'verdict':'UNKNOWN'if result is None else result['verdict'],'repair_authority':False,'delivery_allowed':False})
   for name,data in captured.items():
    tick()
    if (root/name).read_bytes()!=data:raise ValueError('LOGICAL248_TEMP_SOURCE_DRIFT')
  finally:
   sys.path[:]=oldpath
   for name,mod in saved.items():
    if mod is None:sys.modules.pop(name,None)
    else:sys.modules[name]=mod
 return rows


def attach_source_instances248(native,origin,converted,source_binding,capacity_fact,*,remaining_budget_seconds=10,cancel_token=None):
 import time,threading,math
 start=time.monotonic();event=threading.Event()if cancel_token is None else cancel_token
 out={'schema':'PLACED_SOURCE_INSTANCES248_PARTIAL','verdict':'UNKNOWN','rows':[],'logical_access':[],'source_access_recheck':[],'missing':[],'parent_complete':False,'repair_authority':False,'delivery_allowed':False}
 try:
  if type(event)is not threading.Event or type(remaining_budget_seconds)not in(int,float)or not math.isfinite(remaining_budget_seconds)or not 0<remaining_budget_seconds<=30:raise ValueError('INSTANCE248_BUDGET')
  def tick():
   if event.is_set()or time.monotonic()-start>=remaining_budget_seconds:raise ValueError('INSTANCE248_CANCEL_OR_BUDGET')
  j=sys.modules['origin_join'];cm=sys.modules['_capacity_composition215_v2']
  if hashlib.sha256(Path(cm.__file__).read_bytes()).hexdigest()!=CAPACITY244_SHA:raise ValueError('INSTANCE248_FACT_MODULE')
  cm.verify_fact(capacity_fact,origin,converted,source_binding);tick();g=verify_sources();packet=converted['packet']
  if native.get('packet_digest')!=j.digest(packet):raise ValueError('INSTANCE248_PACKET_BINDING')
  frames=native['frames']
  if type(frames)is not list or len(frames)!=2 or {r['frame']for r in frames}!={'local_model','world_model'}:raise ValueError('INSTANCE248_FRAME_INVENTORY')
  bounds=[_preflight_roles244(packet[f],g.e,tick)for f in ('local_model','world_model')]
  if sum(x['estimated_work']for x in bounds)>4000000 or sum(x['rectangles']for x in bounds)>4000:raise ValueError('INSTANCE248_AGGREGATE_BOUND')
  captured=_capture_instances248(tick);work=[0];j.verify_native_immutability(origin,converted,source_binding)
  living=_living_records251(converted,g,captured,tick)
  for frame in ('local_model','world_model'):
   tick();m=packet[frame];mh=j.digest(m)
   if next(r for r in frames if r['frame']==frame)['model_digest']!=mh:raise ValueError('INSTANCE248_MODEL_BINDING')
   rows,missing=_placed_instances248(m,g,tick,work)
   lr,lm=_living_rows251(m,frame,g,living,tick,work);rows.extend(lr);missing=[x for x in missing if not x.endswith(':LIVING_INSTANCE_SOURCE_BRANCH_NOT_IMPLEMENTED')]+lm
   stats={'frame':frame,'scope':'ACTUAL_SOURCE_ACCESS_RECHECK_NOT_LOOKUP_ONLY'};phase=sys.modules.get('phase_journal');stamp=time.monotonic()
   if phase is not None:phase.emit('actual_source_access_recheck248_'+frame,'START')
   failed=True
   try:
    logical=_logical_access248(m,g,captured,tick,stats);failed=False
   finally:
    stats['elapsed_seconds']=time.monotonic()-stamp;out['source_access_recheck'].append(stats)
    if phase is not None:phase.emit('actual_source_access_recheck248_'+frame,'ERROR'if failed else'END')
   out['rows'].extend(dict(r,frame=frame,model_digest=mh)for r in rows);out['logical_access'].extend(dict(r,frame=frame,model_digest=mh)for r in logical);out['missing'].extend(frame+':'+x for x in missing)
  cm.verify_fact(capacity_fact,origin,converted,source_binding)
  j.verify_native_immutability(origin,converted,source_binding)
  if _capture_instances248(tick)!=captured:raise ValueError('INSTANCE248_SOURCE_MUTATION')
  out.update(packet_digest=j.digest(packet),source_binding=source_binding,source_inventory_digest=j.digest(INSTANCE248_PINS))
 except (KeyError,ValueError,TypeError,AttributeError,IndexError,StopIteration,ZeroDivisionError,OverflowError,OSError)as ex:
  out['rows']=[];out['logical_access']=[];out['missing'].append('INSTANCE248_UNVERIFIED:'+str(ex))
 native['placed_instance_coverage248']=out
 return native
