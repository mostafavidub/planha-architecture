"""Concept finish-profile record and arithmetic binding, not technical approval.
Host-name role classification is the pinned source convention, not verified ownership.
Narrative strings are typed only; supplied geometry and hashes are not authenticity.
"""
from fractions import Fraction as F
from source_wall_record_contract_study import header,coordinate,rectangle,need
from declared_geometry_projection_study import digest
FIELDS=set('role profile_kind source_reference axis offsets faces layers layer_composition_status layer_profile_source finish_by_side finish_absence_basis unmodeled_components composition_authority system_verification construction_tolerance material_and_installation claims_symmetric_construction'.split())
BASE_LAYER=set('id side thickness_m existence status layer_role material_hypothesis order_from_axis inner_interface_coordinate outer_interface_coordinate source_reference material_model_or_concept_type thickness_basis layer_type'.split())
TYPES={'partition_body_segment':'core','source_pocket_or_opaque_skin':'cladding','wet_finish_bedding':'adhesive','wet_surface_finish':'finish','wet_waterproofing_membrane':'membrane','render_finish':'finish','dry_finish':'finish'}
def text(v):need(type(v)is str and bool(v),'TEXT_REQUIRED')
def role(hid):
 if hid in ('left','right','front','back'):return 'exterior_envelope'
 if hid.startswith('core.'):return 'common_core_boundary'
 if 'unit_shared_wing' in hid:return 'interunit_boundary'
 if 'unit_boundary' in hid:return 'unit_to_common_boundary'
 if '.bath.' in hid:return 'wet_service_partition'
 if '.kitchen.' in hid:return 'kitchen_service_partition'
 if '.bed' in hid:return 'private_dry_partition'
 return 'explicit_other_source_host'
def pair(v):need(type(v)is dict and set(v)=={'minus','plus'},'SIDE_KEYSET')
def assess(model,expected_model_digest):
 out={'schema':'CONCEPT_FINISH_RECORD_REFERENCE_STUDY_V1','state':'INVALID_FINISH_RECORD','model_digest':expected_model_digest,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'origin_verified':False,'technical_system_verified':False,'whole_schema_verified':False,'not_checked':['NARRATIVE_SOURCE_AUTHENTICITY','HOST_OPENING_AND_OWNERSHIP_RELATIONS','ACTUAL_MATERIAL_INSTALLATION','WHOLE_PHYSICAL_EVALUATOR']}
 try:
  header(model,expected_model_digest)
  hosts=model['wall_hosts'];profiles=model['wall_finish_profile']
  need(type(hosts)is dict and bool(hosts) and type(profiles)is dict and set(hosts)==set(profiles),'PROFILE_HOST_KEYSET')
  rows=[];conflicts=[]
  for hid,raw in hosts.items():
   text(hid);q=rectangle(raw);ax=0 if q[2]-q[0]<=q[3]-q[1] else 1
   lo,hi=q[ax],q[ax+2];mid=(lo+hi)/2;off=(hi-lo)/2;r=role(hid);thin=hi-lo<F('.1');wet=r in ('wet_service_partition','kitchen_service_partition')
   p=profiles[hid];need(type(p)is dict and set(p)==FIELDS,'PROFILE_FIELDS')
   need(p['role']==r and p['profile_kind']=='CONCEPT_SENSITIVITY_NOT_TECHNICAL','CONCEPT_ROLE')
   for key in ('source_reference','layer_profile_source','composition_authority'):text(p[key])
   need(p['layer_composition_status']=='DECLARED_LAYER_HYPOTHESIS_NOT_TECHNICALLY_VERIFIED' and p['system_verification']=='NOT_VERIFIED' and p['construction_tolerance']=='UNKNOWN_NOT_ZERO' and p['material_and_installation']=='NOT_SELECTED_NOT_VERIFIED' and p['claims_symmetric_construction'] is False,'TECHNICAL_AUTHORITY')
   need(type(p['axis'])is dict and set(p['axis'])=={'orientation','coordinate'},'AXIS_FIELDS')
   need(p['axis']['orientation']==('vertical' if ax==0 else 'horizontal') and coordinate(p['axis']['coordinate'])==mid,'HOST_AXIS')
   for name in ('faces','offsets','finish_by_side','finish_absence_basis'):pair(p[name])
   need(coordinate(p['faces']['minus'])==lo and coordinate(p['faces']['plus'])==hi,'HOST_FACES')
   need(all(coordinate(v)==off for v in p['offsets'].values()),'HOST_OFFSETS')
   need(all(v==('EXPLICITLY_ABSENT_WITH_BASIS' if thin else 'MODELED_IN_LAYERS') for v in p['finish_by_side'].values()),'FINISH_STATE')
   for v in p['finish_absence_basis'].values():text(v)
   layers=p['layers'];need(type(layers)is list and bool(layers),'LAYERS')
   ids=set()
   for z in layers:
    need(type(z)is dict and set(z)==BASE_LAYER|({'finish_decision'} if thin else set()),'LAYER_FIELDS')
    text(z['id']);need(z['id']not in ids,'DUPLICATE_LAYER_ID');ids.add(z['id'])
    need(z['side'] in ('minus','plus') and z['existence']=='ASSUMED_PRESENT' and z['status']=='CONCEPT_ASSUMPTION','LAYER_ASSUMPTION')
    for key in ('material_hypothesis','source_reference','material_model_or_concept_type','thickness_basis'):text(z[key])
    if thin:text(z['finish_decision'])
   expected_roles=['source_pocket_or_opaque_skin'] if thin else ['partition_body_segment']+(['wet_waterproofing_membrane','wet_finish_bedding','wet_surface_finish'] if wet else ['render_finish' if r=='exterior_envelope' else 'dry_finish'])
   for side,sign in (('minus',-1),('plus',1)):
    ls=[z for z in layers if z['side']==side]
    need([z['layer_role']for z in ls]==expected_roles,'LAYER_ROLE_SEQUENCE')
    expected_thickness=[off] if thin else ([off-F('.015'),F('.002'),F('.008'),F('.005')] if wet else [off-(F('.015') if r=='exterior_envelope' else F('.01')),F('.015') if r=='exterior_envelope' else F('.01')])
    used=F(0)
    for rank,z in enumerate(ls,1):
     thick=coordinate(z['thickness_m']);need(thick>0,'POSITIVE_LAYER_THICKNESS');need(thick==expected_thickness[rank-1],'SOURCE_CONCEPT_ALLOWANCE')
     need(type(z['order_from_axis'])is int and z['order_from_axis']==rank,'LAYER_ORDER')
     need(z['layer_type']==TYPES[z['layer_role']],'LAYER_TYPE')
     need(coordinate(z['inner_interface_coordinate'])==mid+sign*used and coordinate(z['outer_interface_coordinate'])==mid+sign*(used+thick),'LAYER_INTERFACE')
     used+=thick
    need(used==off,'LAYER_SUM_TO_HOST_FACE')
   omitted=p['unmodeled_components'];need(type(omitted)is dict and set(omitted)=={'thermal_insulation','separate_cladding','waterproofing_system'},'UNMODELED_FIELDS')
   for key in ('thermal_insulation','separate_cladding'):
    need(omitted[key]=={'modeled_state':'ABSENT_IN_THIS_CONCEPT_VARIANT','actual_building_state':'UNKNOWN'},'ABSENCE_NOT_ACTUAL_ZERO')
   w=omitted['waterproofing_system']
   need(type(w)is dict and set(w)=={'modeled_state','performance','actual_building_state','numeric_zero_claimed'},'WATERPROOFING_FIELDS')
   need(w['modeled_state']==('ASSUMED_GEOMETRIC_2MM_MEMBRANE' if wet else 'NOT_APPLICABLE_TO_THIS_DRY_STUDY_FACE') and w['performance']=='NOT_VERIFIED' and w['actual_building_state']=='UNKNOWN' and w['numeric_zero_claimed'] is False,'UNKNOWN_PRESERVATION')
   if thin and wet:conflicts.append({'host_id':hid,'code':'SOURCE_PROFILE_SEMANTIC_CONFLICT','detail':'Source declares a 2mm membrane in unmodeled components but its thin-wet profile contains only source skin','state':'UNKNOWN'})
   rows.append({'host_id':hid,'host_digest':digest(raw),'profile_digest':digest(p),'geometry_and_layer_chain_bound':True})
  need(digest(model)==expected_model_digest,'INPUT_MUTATION')
  out.update(state='CONCEPT_PROFILE_GEOMETRY_BOUND_WITH_SOURCE_CONFLICT' if conflicts else 'CONCEPT_PROFILE_GEOMETRY_BOUND_ONLY',bindings=rows,source_semantic_conflicts=conflicts,profile_semantics_verified=False,covered_path='root.wall_finish_profile')
 except (ValueError,TypeError,KeyError,IndexError,UnicodeError,OverflowError,RecursionError) as ex:out.update(error=str(ex),error_type=type(ex).__name__)
 return out
