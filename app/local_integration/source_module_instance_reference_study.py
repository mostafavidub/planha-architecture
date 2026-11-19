"""Eight-module fixture/activity reference subset. Not whole-unit inventory.
Embedded source identity is not source authenticity. Dining/living and extra map
entries remain unverified. Metadata follows an explicit installer or XY-world source policy, not world heading.
"""
import copy
from source_module_floor_reference_study import assess as floor_assess,transformed
from source_wall_record_contract_study import need,rectangle
from declared_geometry_projection_study import digest
def assess(model,expected_model_digest,frame_mode):
 out={'schema':'MODULE_INSTANCE_REFERENCE_SUBSET_V1','state':'INVALID_MODULE_INSTANCE_SUBSET','model_digest':expected_model_digest,'accepted':False,'qualified':False,'origin_verified':False,'whole_inventory_verified':False,'physical_verified':False,'display_allowed':False,'delivery_allowed':False,'frame_mode':frame_mode,'frame_provenance_verified':False,'not_checked':['DINING_LIVING_AND_EXTRA_INSTANCES','MODULE_SOURCE_COMPLETENESS_AUTHENTICITY','EXTRA_ID_MAP_REFERENCES','ACTIVITY_ROUTES_AND_TARGETS','WORLD_HEADING_FROM_CANONICAL_METADATA']}
 try:
  need(type(frame_mode)is str and frame_mode in ('PRE_WORLD_INSTALLER','XY_SWAPPED_WORLD'),'EXPLICIT_FRAME_MODE')
  f=floor_assess(model,expected_model_digest);need(f['state']=='SOURCE_MODULE_FLOORS_AND_APRONS_BOUND_ONLY','MODULE_FLOOR_PREREQUISITE')
  units={u['id']:u for u in model['units']};seen={'fixtures':set(),'activities':set()};rows=[]
  for p in model['module_placements']:
   uid=p['unit_id'];u=units[uid];source=p['module']['unit'];ids=p['id_map'];bound={}
   for category in ('fixtures','activities'):
    src=source[category];actual=u[category]
    need(type(src)is dict and bool(src) and type(actual)is dict,'NONEMPTY_SOURCE_INSTANCE_MAP')
    refs=[]
    for sid,q in src.items():
     need(type(sid)is str and bool(sid) and sid in ids,'SOURCE_INSTANCE_ID')
     target=ids[sid];need(type(target)is str and bool(target) and target in actual,'TARGET_INSTANCE_REFERENCE')
     key=(uid,target);need(key not in seen[category],'DUPLICATE_UNIT_INSTANCE_BINDING');seen[category].add(key)
     need(transformed(q,p['transform'])==rectangle(actual[target]),'INSTANCE_GEOMETRY_BINDING')
     if category=='fixtures':
      sm=source['fixture_metadata'];am=u['fixture_metadata']
      need(type(sm)is dict and type(am)is dict and sid in sm and target in am,'FIXTURE_METADATA_REFERENCE')
      expected=copy.deepcopy(sm[sid]);need(type(expected)is dict,'SOURCE_METADATA_RECORD')
      if frame_mode=='XY_SWAPPED_WORLD':
       angle=expected.get('rotation_deg',0);need(type(angle)is int,'SOURCE_ROTATION_TYPE');expected['rotation_deg']=(90-angle)%180
      need(digest(expected)==digest(am[target]),'EXACT_SOURCE_METADATA_POLICY')
     refs.append({'source_id':sid,'target_id':target,'actual_value_digest':digest(actual[target])})
    bound[category]=refs
   rows.append({'unit':uid,'room':p['room_id'],'module_digest':p['module_hash'],'transform_digest':digest(p['transform']),'bindings':bound})
  need(digest(model)==expected_model_digest,'INPUT_MUTATION')
  out.update(state='MODULE_INSTANCE_REFERENCE_SUBSET_BOUND_ONLY',bindings=rows,fixture_binding_count=len(seen['fixtures']),activity_binding_count=len(seen['activities']),metadata_scope='installer exact source metadata or explicit XY policy (90-old)%180; axis footprint only, not world-facing heading or ergonomic approval')
 except (ValueError,TypeError,KeyError,IndexError,UnicodeError,OverflowError,RecursionError) as ex:out.update(error=str(ex),error_type=type(ex).__name__)
 return out
