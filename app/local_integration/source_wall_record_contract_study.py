"""Independent wall-record/alias contract study; never replaces a whole checker.
Source-derived field semantics: assemble114.wall, wall_union118.bind_physical_wall_union,
world_transform125.to_world. This is not proof of construction provenance.
"""
import copy,json,math,re
from fractions import Fraction as F
from declared_geometry_projection_study import SCHEMA as PROJECTION_SCHEMA,CONTRACT as PROJECTION_CONTRACT,rect as declared_rectangle,digest,scalar_text
SCHEMA='SOURCE_WALL_RECORD_REFERENCE_STUDY_V1'
ROOT_KEYS=set('schema contract_version inputs scope_declaration ordered_macro status accepted release_allowed profile program walls wall_hosts source_wall_hosts common_spaces openings concept_windows units room_metadata common_routes fixture_catalog_hash fixture_catalog fixture_catalog_digest openedge_assumptions route_failures proposal_network_paths network_scope logical_regions operations pending module_ports module_aprons module_placements quality_unverified source_geometry_contract physical_wall_network wall_finish_profile threshold_ownership spatial_accounting frame_binding125'.split())
NETWORK_KEYS=set('schema source_wall_hash solids source_aliases source_walls_preserved method faces finish_profile_status accepted'.split())
MAPS=('walls','wall_hosts','source_wall_hosts')
COVERED_PATHS=['root.walls','root.wall_hosts','root.source_wall_hosts','root.physical_wall_network.source_aliases']
OTHER_PATHS=['root.units[].rooms','root.units[].fixtures','root.units[].fixture_metadata','root.units[].activities','root.units[].routes','root.units[].route_targets','root.room_metadata','root.proposal_network_paths','root.module_aprons','root.wall_finish_profile']
def need(ok,reason):
 if not ok:raise ValueError(reason)
def clean(v,depth=0):
 need(depth<=100,'JSON_DEPTH')
 if type(v)is dict:
  need(all(type(k)is str for k in v),'JSON_KEY_TYPE')
  for x in v.values():clean(x,depth+1)
 elif type(v)is list:
  for x in v:clean(x,depth+1)
 else:need(type(v)in(str,int,float,bool,type(None)) and (type(v)is not float or math.isfinite(v)),'JSON_TYPE')
def coordinate(x):
 need(type(x)is str and len(x)<=128 and re.fullmatch(r'-?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)',x) is not None,'SOURCE_COORDINATE_STRING')
 return F(x)
def rectangle(q):
 need(type(q)is list and len(q)==4,'SOURCE_RECTANGLE')
 r=list(map(coordinate,q));need(r[0]<r[2] and r[1]<r[3],'SOURCE_RECTANGLE_EXTENT');return r
def mapping(v):
 need(type(v)is dict and 1<=len(v)<=2048,'NONEMPTY_RECTANGLE_MAP')
 for k,q in v.items():
  need(type(k)is str and re.fullmatch(r'[A-Za-z][A-Za-z0-9_.:-]{0,159}',k) is not None,'SOURCE_IDENTIFIER')
  rectangle(q)
def overlap(a,b):
 return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
def union_intervals(parts,x):
 ys=sorted((r[1],r[3]) for r in parts if r[0]<x<r[2]);out=[]
 for y,Y in ys:
  if out and y<=out[-1][1]:out[-1]=(out[-1][0],max(out[-1][1],Y))
  else:out.append((y,Y))
 return out
def same_union(a,b):
 xs=sorted({r[i] for r in a+b for i in (0,2)})
 return all(union_intervals(a,(x+X)/2)==union_intervals(b,(x+X)/2) for x,X in zip(xs,xs[1:]))
def wall_graph(walls,network):
 mapping(walls);need(type(network)is dict and set(network)==NETWORK_KEYS,'NETWORK_FIELDS')
 need(network['schema']=='EXACT_SOURCE_WALL_UNION118','NETWORK_SCHEMA')
 need(network['source_walls_preserved'] is True and network['accepted'] is False,'NETWORK_AUTHORITY')
 need(network['finish_profile_status']=='NOT_EVALUATED','FINISH_STATUS')
 need(all(type(network[k])is str and network[k] for k in ('method','faces')),'NETWORK_TEXT')
 need(type(network['source_wall_hash'])is str and network['source_wall_hash']==digest(walls),'SOURCE_WALL_DIGEST')
 solids=network['solids'];mapping(solids)
 need(set(solids)=={'physical_wall_'+str(i) for i in range(len(solids))},'SOLID_ID_INVENTORY')
 w={k:rectangle(q) for k,q in walls.items()};s={k:rectangle(q) for k,q in solids.items()}
 items=list(s.values())
 need(all(not overlap(a,b) for i,a in enumerate(items) for b in items[i+1:]),'SOLIDS_INTERIOR_OVERLAP')
 aliases=network['source_aliases'];need(type(aliases)is dict and set(aliases)==set(w),'SOURCE_ALIAS_KEYSET')
 for k,r in w.items():
  a=aliases[k];need(type(a)is list and a and all(type(x)is str for x in a),'ALIAS_REFERENCE_TYPE')
  need(len(a)==len(set(a)),'ALIAS_REFERENCE_DUPLICATE')
  need(set(a)<=set(s),'ALIAS_DANGLING')
  # Alias lists denote a set of material intersections; serialized order is not geometric.
  need(set(a)=={pid for pid,q in s.items() if overlap(r,q)},'ALIAS_INTERSECTION_SET')
 need(same_union(list(w.values()),items),'SOLID_UNION_MISMATCH')
 # No deleted/extra source record claim: entire source map is a separate provenance obligation.
 return {'source_wall_count':len(w),'physical_solid_count':len(s),'source_alias_count':len(aliases),'material_union_equal':True,'alias_reference_sets_exact':True,'source_wall_reconstruction':'union of referenced solid intersections clipped to each source rectangle, not whole referenced solids'}
def header(model,expected_model_digest):
 clean(model)
 need(type(expected_model_digest)is str and re.fullmatch(r'[0-9a-f]{64}',expected_model_digest) is not None,'EXPECTED_DIGEST_TYPE')
 need(digest(model)==expected_model_digest,'MODEL_DIGEST_MISMATCH')
 need(type(model)is dict and set(model)==ROOT_KEYS,'ROOT_FIELDS')
 need(model['schema']=='GENERAL125_WORLD_FRAME_STUDY','WORLD_SCHEMA')
 need(model['accepted'] is False and model['release_allowed'] is False,'MODEL_AUTHORITY')
 need(model['ordered_macro'] is None,'UNSUPPORTED_ORDERED_FAMILY')
 ins=model['inputs'];need(type(ins)is list and len(ins)==3 and type(ins[2])is int and ins[2]==2,'INPUT_SCOPE')
 need(all(F(5)<=coordinate(x)<=F(25) for x in ins[:2]),'INPUT_RANGE')
 us=model['units'];need(type(us)is list and len(us)==2 and all(type(u)is dict for u in us),'UNIT_RECORDS')
 need([u.get('id') for u in us]==['A','B'],'UNIT_IDENTITY')
 p=model['program'];need(type(p)is dict and type(p.get('units'))is int and p['units']==2 and type(p.get('bedrooms_per_unit'))is int and p['bedrooms_per_unit']==2 and p.get('sleep_roles')==['double','twin'],'PROGRAM_SCOPE')
def projection(model):
 # Explicit per-value linkage; no recursive numeric guessing or unknown-field skipping.
 records=[]
 for field in MAPS:
  for k,q in model[field].items():
   canonical=[scalar_text(v) for v in rectangle(q)];declared_rectangle(canonical)
   records.append({'namespace_hint_by_source_id':k.split('.')[0] if k.split('.')[0] in ('A','B') else 'COMMON','ownership_attribution_verified':False,'source_record_id':k,'source_field':field,'source_path':[field,k],'source_value_digest':digest(q),'canonical_rectangle':canonical})
 return {'schema':'WALL_RECTANGLE_SOURCE_BINDING_V1','records':records,'model_digest':digest(model),'role':'rectangle','projection_contract_schema':PROJECTION_SCHEMA,'projection_contract_digest':digest(PROJECTION_CONTRACT),'canonicalization':'source decimal strings only; exact rational value retained, lexical form may change','not_complete_geometry_projection':True}
def assess(model,expected_model_digest):
 out={'schema':SCHEMA,'state':'INVALID_WALL_RECORD_CONTRACT','covered_paths':COVERED_PATHS,'not_checked_paths':OTHER_PATHS,'root_keyset_checked':False,'origin_verified':False,'source_inventory_completeness_verified':False,'whole_schema_verified':False,'physical_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
 try:
  header(model,expected_model_digest);out['root_keyset_checked']=True
  for field in MAPS:mapping(model[field])
  result=wall_graph(model['walls'],model['physical_wall_network'])
  bound=projection(model)
  need(digest(model)==expected_model_digest,'INPUT_MUTATION')
  out.update(state='WALL_RECORD_REFERENCE_AND_MATERIAL_UNION_VALID_ONLY',model_digest=expected_model_digest,wall_graph=result,projection=bound,projection_digest=digest(bound),scope='Exact typed source-shaped wall maps and independent material/alias graph only; root digest is identity, not authentication. Hosts are typed rectangles, not verified opening-host coverage. No old checker error is removed.')
 except (ValueError,TypeError,KeyError,IndexError,UnicodeError,RecursionError,OverflowError) as ex:out['error']=str(ex);out['error_type']=type(ex).__name__
 return out
