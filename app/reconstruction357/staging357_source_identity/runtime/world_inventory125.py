"""Fail-closed local/world schema binding. Independent of world_transform125.
Only this enumerated schema is supported. Derived ledgers require fresh gates.
"""
from copy import deepcopy
from pathlib import Path
import json,hashlib
from fractions import Fraction as F
from contract114 import digest,S
from d4_contract125 import matrix,compose,inverse
R=set('rect plan_rect closed_panel open_panel pocket rail_envelope panel_rect actor_rect actor_start actor_end closed_rect open_rect occupied_body standing_body closed_tray open_tray body_rect front_rect region'.split())
P=set('hand_point hand_start hand_end center hinge closed_actor open_actor open_access shelf_target held_target grip_closed grip_open storage_target workpoint access_point point target actor hand translation actor_offset_m normal front_normal'.split())
RL=set('shell_rects motion_envelopes regions parts'.split());PATH=set('path egress_route route open_transfer_points'.split())
TOP=set('schema contract_version inputs scope_declaration ordered_macro status accepted release_allowed profile program walls wall_hosts source_wall_hosts common_spaces openings concept_windows units room_metadata common_routes fixture_catalog_hash fixture_catalog fixture_catalog_digest openedge_assumptions route_failures proposal_network_paths network_scope logical_regions operations pending module_ports module_aprons module_placements quality_unverified source_geometry_contract physical_wall_network wall_finish_profile threshold_ownership spatial_accounting'.split())
def pt(p):return [S(F(str(p[1]))),S(F(str(p[0])))]
def rect(r):return [S(F(str(r[i])))for i in(1,0,3,2)]
def placement(t):
 m=compose([[0,1],[1,0]],t['matrix']);return dict(matrix=[[int(x)for x in row]for row in m],translation=pt(t['translation']))
def norm(v):
 if isinstance(v,dict):return {k:norm(x)for k,x in v.items()}
 if isinstance(v,list):return [norm(x)for x in v]
 if isinstance(v,(int,float,str))and not isinstance(v,bool):
  try:return F(str(v))
  except ValueError:pass
 return v

def examine(local,world,core):
 errors=[];unknown=[]
 is_l3=(local.get('ordered_macro')or{}).get('kind')=='L3_EXPERIMENTAL131'
 schema_path=Path(__file__).with_name('world_record_schema131.json'if is_l3 else'world_record_schema129.json')
 pin='6fa52b0efa87b75ff7d6bb241d944d74eb27eb754e2923817834d685d637fddb'if is_l3 else'59aac9a1e8b17caa40d16aca71a59c4281507b55abf56bb7efc48c5dea0d11ea'
 if (local.get('ordered_macro')or{}).get('kind')=='STAGGER_ACCESS132':
  schema_path=Path(__file__).with_name('world_record_schema132.json');pin='a159e2f354fe639d9d7189f4e7c1dd1b55a1a83dfd6102a735dae956501e32f2'
 if (local.get('ordered_macro')or{}).get('kind')=='TURN_T133':
  schema_path=Path(__file__).with_name('world_record_schema133.json');pin='a26381a2e538371ca3986f7138f03f9eb13e11076ddb20ca2608ff7ff0bbad83'
 if (local.get('ordered_macro')or{}).get('kind')=='SIDECAR_T136':
  schema_path=Path(__file__).with_name('world_record_schema136.json');pin='31d94841666ee1962d5a8abaa8401687f65b5fdefa7b248e8cdb210630c334bb'
 if (local.get('ordered_macro')or{}).get('kind')=='PARALLEL_TWINS_BRANCH146':
  schema_path=Path(__file__).with_name('world_record_schema147.json');pin='572665d0274e1c5f28a1a0767f8a5b38f1801dc79a4ef0880604639870c972dd'
 if hashlib.sha256(schema_path.read_bytes()).hexdigest()!=pin:
  return dict(errors=['RECORD_SCHEMA_SOURCE_CHANGED'],pending=[])
 record_schema=json.loads(schema_path.read_text())['records']
 def records(v,path='root',key=''):
  if key=='rotation_source133':
   from checker_source133 import examine as source_check
   r=source_check(v)
   if r['errors']or r['pending']:errors.append('INVALID_ROTATION_SOURCE133')
   return
  if key in ('module','source_contract'):return
  if isinstance(v,dict):
   keys=sorted(k for k in v if not(path=='root'and k=='frame_binding125'))
   if path=='root.physical_wall_network.solids':
    import re
    if any(not re.fullmatch(r'physical_wall_\d+',k)or not isinstance(z,list)or len(z)!=4 for k,z in v.items()):errors.append('UNKNOWN_PHYSICAL_SOLID_RECORD')
   elif path=='root.openedge_assumptions'and keys==['assessment','geometric_frame_transform','rights']:pass
   elif keys not in record_schema.get(path,[]):errors.append('UNKNOWN_RECORD_FIELDS:'+path)
   for k,z in v.items():
    if path=='root'and k=='frame_binding125':continue
    records(z,path+'.'+k,k)
  elif isinstance(v,list):
   for z in v:records(z,path+'[]')
 records(local)
 # Derived ledger dictionaries contain fresh coordinate-dependent IDs; their
 # original record shape is identical here and remains separately audited.
 records(world)
 def walk(x,key='',path=''):
  if key=='rotation_source133':
   from checker_source133 import examine as source_check
   r=source_check(x)
   if r['errors']or r['pending']:errors.append('INVALID_ROTATION_SOURCE133')
   return deepcopy(x)
  if key in ('module','source_contract'):return deepcopy(x)
  if isinstance(x,dict):
   if key in ('canonical_isometry','canonical_transform'):
    m=compose(x['matrix'],[[0,1],[1,0]])
    return dict(matrix=[[int(v)for v in row]for row in m],translation=deepcopy(x['translation']))
   d={k:walk(v,k,path+'.'+k)for k,v in x.items()}
   for k in('axis','front_axis'):
    if d.get(k)in('x','y'):d[k]={'x':'y','y':'x'}[d[k]]
   if d.get('orientation')in('horizontal','vertical'):d['orientation']={'horizontal':'vertical','vertical':'horizontal'}[d['orientation']]
   return d
  if isinstance(x,list):
   scalar=all(not isinstance(v,(dict,list))for v in x)
   if key in R and len(x)==4 and scalar:return rect(x)
   if key in P and len(x)==2 and scalar:return pt(x)
   if key in RL:return [rect(v)for v in x]
   if key in PATH:return [pt(v)for v in x]
   if scalar and len(x)in(2,4):
    try:
     [F(str(v))for v in x]
     if key not in ('angle_range_degrees','source_size_m','size_m','opaque_skin_m'):unknown.append(path)
    except ValueError:pass
   return [walk(v,'',path+'[]')for v in x]
  return deepcopy(x)
 try:
  current_top=TOP|({'private_domains'}if 'private_domains'in local else set())
  world_extra={'ordered_macro_coordinate_frame'}if local.get('ordered_macro')else set()
  if set(local)!=current_top:errors.append('LOCAL_SCHEMA_UNKNOWN_OR_MISSING:'+str(sorted(set(local)^TOP)))
  if set(world)!=current_top|{'frame_binding125'}|world_extra:errors.append('WORLD_SCHEMA_UNKNOWN_OR_MISSING')
  e=deepcopy(local)
  if 'private_domains'in local:
   from private_domain_inventory129 import examine as private_transport
   errors.extend(private_transport(local,world)['errors'])
   e['private_domains']=deepcopy(world['private_domains']) # compared independently above, not producer trusted
  if world.get('ordered_macro_coordinate_frame')!=('IMMUTABLE_LOCAL_CONSTRUCTION_PROPOSAL'if local.get('ordered_macro')else None):errors.append('ORDERED_MACRO_COORDINATE_FRAME')
  e['inputs']=[S(F(str(v)))for v in core['physical_core_model']['inputs'][:2]]+[2];e['schema']='GENERAL125_WORLD_FRAME_STUDY'
  if world['inputs']!=e['inputs']:errors.append('CANONICAL_API_INPUT_STRINGS')
  for k in ('walls','wall_hosts','source_wall_hosts'):e[k]={n:rect(r)for n,r in local[k].items()}
  e['common_spaces']={k:[rect(r)for r in v]if isinstance(v[0],list)else rect(v)for k,v in local['common_spaces'].items()}
  for k in ('common_routes','proposal_network_paths'):e[k]={n:[pt(p)for p in v]for n,v in local[k].items()}
  for k in ('openings','concept_windows','operations','module_ports','logical_regions','wall_finish_profile','threshold_ownership'):e[k]=walk(local[k],k,k)
  for w in e['concept_windows']:
   if 'destination'in w:w['destination']['edge']={'bottom':'left','top':'right','left':'bottom','right':'top'}.get(w['destination']['edge'],w['destination']['edge'])
  e['module_aprons']={k:[rect(r)for r in v]for k,v in local['module_aprons'].items()}
  for z in e['module_placements']:z['transform']=placement(z['transform'])
  for u in e['units']:
   u['ownership']=[rect(r)for r in u['ownership']];u['rooms']={k:[rect(r)for r in v]for k,v in u['rooms'].items()}
   for k in ('fixtures','activities'):u[k]={n:rect(r)for n,r in u[k].items()}
   for k in ('routes','scenario_routes'):u[k]={n:[pt(p)for p in v]for n,v in u[k].items()}
   u['route_targets']={n:pt(p)for n,p in u['route_targets'].items()};u['entry_point']=pt(u['entry_point'])
   for md in u['fixture_metadata'].values():md['rotation_deg']=(90-md.get('rotation_deg',0))%180
   u['dining_module_placement']['transform']=placement(u['dining_module_placement']['transform']);u['public_program']=walk(u['public_program'],'public_program','unit.public_program')
   u['spatial_role_bindings']=walk(u['spatial_role_bindings'],'spatial_role_bindings','unit.spatial_role_bindings')
   u['public_floor_classification']['route_geometry_hash']=digest({**u['routes'],**{'scenario:'+k:v for k,v in u['scenario_routes'].items()}})
  e['quality_unverified']=[s for s in e['quality_unverified']if 'ventilation'not in s and 'daylight'not in s]
  for k in current_top-{'private_domains','physical_wall_network','spatial_accounting','openedge_assumptions'}:
   a=deepcopy(e[k]);b=deepcopy(world[k])
   if k=='units':
    from geometry114 import cells
    for ua,ub in zip(a,b):
     for name in ua['spatial_role_bindings']:
      for item in (ua,ub):item['spatial_role_bindings'][name]['regions']=cells(item['spatial_role_bindings'][name]['regions'],[])
   if norm(a)!=norm(b):errors.append('WORLD_FIELD_BINDING:'+k)
  f=world['frame_binding125']
  for key,val in [('local_model_hash',digest(local)),('core_contract_hash',digest(core)),('world_from_local',core['world_from_local'])]:
   if f.get(key)!=val:errors.append('FRAME_CONTEXT_BINDING:'+key)
  if not f.get('not_a_receipt_of_whole_acceptance')or not f.get('rotation_deg_scope','').startswith('Axis footprint only')or not f.get('operation_angle_scope','').startswith('Kitchen angle ranges are source canonical'):errors.append('FRAME_SEMANTIC_SCOPE')
 except (KeyError,TypeError,ValueError,IndexError)as ex:errors.append('WORLD_BINDING_SCHEMA:'+str(ex))
 return dict(errors=errors,pending=['UNKNOWN_NUMERIC_FIELD:'+p for p in sorted(set(unknown))],model_hash=digest(world),local_model_hash=digest(local),derived_requirements=['fresh physical_wall_network','fresh spatial_accounting'],scope='Exact enumerated D4 fields; not whole admission; fixture rotation is axis only, operation angles canonical')
