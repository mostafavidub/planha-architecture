"""Explicit-two module room/apron reference contract. Not a whole floor checker.
Embedded module hashes establish supplied-content identity, not source authenticity.
Residual living, circulation, dining, ownership and physical usability remain separate.
"""
import copy
from fractions import Fraction as F
from source_wall_record_contract_study import header,clean,coordinate,rectangle,same_union,need
from declared_geometry_projection_study import matrix,digest,scalar_text
EXPECTED={'bed1':('PRIVATE_ROOM_MODULE116','bed1'),'bed2':('PRIVATE_TWIN_ROOM_MODULE118','bed1'),'bath':('BATHROOM_MODULE117','bath'),'kitchen':('KITCHEN_MODULE117','kitchen')}
PLACEMENT_FIELDS=set('module module_hash transform id_map unit_id room_id geometry_scope'.split())
ROOMS={'bed1','bed2','bath','kitchen','dining','living','entry_circulation'}
def parts(v):
 need(type(v)is list and bool(v),'NONEMPTY_FLOOR_PARTS');return [rectangle(q) for q in v]
def transformed(q,t):
 need(type(t)is dict and set(t)=={'matrix','translation'},'TRANSFORM_FIELDS');a=matrix(t['matrix'])
 need(type(t['translation'])is list and len(t['translation'])==2,'TRANSLATION_SHAPE');v=list(map(coordinate,t['translation']))
 x,y,X,Y=rectangle(q)
 ps=[[sum(F(a[i][j])*p[j] for j in (0,1))+v[i] for i in (0,1)] for p in ((x,y),(x,Y),(X,y),(X,Y))]
 return [min(p[0] for p in ps),min(p[1] for p in ps),max(p[0] for p in ps),max(p[1] for p in ps)]
def assess(model,expected_model_digest):
 out={'schema':'SOURCE_MODULE_FLOOR_REFERENCE_STUDY_V1','state':'INVALID_MODULE_FLOOR_CONTRACT','model_digest':expected_model_digest,'origin_verified':False,'whole_schema_verified':False,'physical_verified':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'not_checked':['LIVING_CIRCULATION_DINING_SEMANTICS','UNIT_OWNERSHIP_AND_ACCESS','MODULE_AUTHENTICITY_AND_INTERNAL_GATES','FIXTURES_ACTIVITIES_AND_OPERATIONS','EXTRA_ID_MAP_REFERENCES','WHOLE_EVALUATOR']}
 try:
  header(model,expected_model_digest)
  units={u['id']:u for u in model['units']}
  for u in units.values():
   need(type(u['rooms'])is dict and set(u['rooms'])==ROOMS,'EXPLICIT_TWO_ROOM_KEYS')
   for rs in u['rooms'].values():
    need(type(rs)is list,'ROOM_PARTS_TYPE')
    for q in rs:rectangle(q)
  ps=model['module_placements'];need(type(ps)is list and len(ps)==8,'EXPLICIT_TWO_MODULE_COUNT')
  keys=set();rows=[];aprons=model['module_aprons']
  need(type(aprons)is dict and set(aprons)=={uid+'.'+room for uid in ('A','B') for room in EXPECTED},'APRON_REFERENCE_KEYSET')
  for p in ps:
   need(type(p)is dict and set(p)==PLACEMENT_FIELDS,'PLACEMENT_FIELDS')
   uid,room=p['unit_id'],p['room_id']
   need(type(uid)is str and uid in units and type(room)is str and room in EXPECTED,'PLACEMENT_REFERENCE')
   need((uid,room)not in keys,'DUPLICATE_MODULE_INSTANCE');keys.add((uid,room))
   need(type(p['geometry_scope'])is str and p['geometry_scope'],'GEOMETRY_SCOPE')
   need(type(p['id_map'])is dict and all(type(k)is str and type(v)is str for k,v in p['id_map'].items()),'ID_MAP_TYPE')
   mod=p['module'];need(type(mod)is dict and mod.get('schema')==EXPECTED[room][0],'MODULE_ROLE_SCHEMA')
   need(type(p['module_hash'])is str and digest(mod)==p['module_hash'],'MODULE_DIGEST')
   floor=mod['unit']['rooms'][EXPECTED[room][1]];apron=mod['unit']['rooms']['public_access']
   parts(floor);parts(apron)
   expected=[transformed(q,p['transform']) for q in floor]
   actual=parts(units[uid]['rooms'][room]);need(same_union(expected,actual),'MODULE_ROOM_FLOOR_BINDING')
   expected_apron=[transformed(q,p['transform']) for q in apron];actual_apron=parts(aprons[uid+'.'+room])
   need(same_union(expected_apron,actual_apron),'MODULE_APRON_BINDING')
   rows.append({'unit':uid,'room':room,'source_room':EXPECTED[room][1],'module_digest':p['module_hash'],'transform_digest':digest(p['transform']),'room_value_digest':digest(units[uid]['rooms'][room]),'apron_value_digest':digest(aprons[uid+'.'+room]),'room_union_equal':True,'apron_union_equal':True})
  need(keys=={(uid,room) for uid in ('A','B') for room in EXPECTED},'MODULE_INSTANCE_INVENTORY')
  need(digest(model)==expected_model_digest,'INPUT_MUTATION')
  out.update(state='SOURCE_MODULE_FLOORS_AND_APRONS_BOUND_ONLY',bindings=rows,covered_paths=['root.units[].rooms: four installed module rooms only; remaining room lists typed only','root.module_aprons: exact eight explicit-two references'],source_content_authenticated=False)
 except (ValueError,TypeError,KeyError,IndexError,UnicodeError,OverflowError,RecursionError) as ex:out['error']=str(ex);out['error_type']=type(ex).__name__
 return out
