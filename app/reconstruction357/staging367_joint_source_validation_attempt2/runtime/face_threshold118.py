"""Declared concept faces and source-referenced threshold ownership.
No selected material system, installed finish or tolerance is fabricated.
"""
from fractions import Fraction as F
from contract114 import S
from geometry114 import Q

def attach(m):
 profiles={}
 for hid,r in m['wall_hosts'].items():
  q=Q(r);ax=0 if q[2]-q[0]<=q[3]-q[1]else 1;lo,hi=q[ax],q[ax+2];mid=(lo+hi)/2;off=(hi-lo)/2
  if hid in('left','right','front','back'):role='exterior_envelope'
  elif hid.startswith('core.'):role='common_core_boundary'
  elif 'unit_shared_wing'in hid:role='interunit_boundary'
  elif 'unit_boundary'in hid:role='unit_to_common_boundary'
  elif '.bath.'in hid:role='wet_service_partition'
  elif '.kitchen.'in hid:role='kitchen_service_partition'
  elif '.bed'in hid:role='private_dry_partition'
  else:role='explicit_other_source_host'
  layers=[]
  for side in ('minus','plus'):
   if hi-lo<F('.1'):
    # This is an actual source pocket/opaque skin, not a conventional wall
    # silently assigned a zero unknown finish.
    layers.append({'id':side+'_source_skin','side':side,'thickness_m':S(off),'existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION','layer_role':'source_pocket_or_opaque_skin','material_hypothesis':'Source geometric opaque skin, material/product unverified','finish_decision':'No additional finish modeled in this declared source-skin study; not an unknown finish converted to zero.'})
   else:
    finish=F('.015')if role in('exterior_envelope','wet_service_partition','kitchen_service_partition')else F('.01')
    layers.append({'id':side+'_partition_body','side':side,'thickness_m':S(off-finish),'existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION','layer_role':'partition_body_segment','material_hypothesis':'Assumed non-loadbearing block partition body for concept comparison; block product, structure/fire/acoustics NOT_VERIFIED'})
    if role in('wet_service_partition','kitchen_service_partition'):
     layers.extend([{'id':side+'_waterproof_membrane','side':side,'thickness_m':'.002','existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION','layer_role':'wet_waterproofing_membrane','material_hypothesis':'2mm geometric waterproofing-layer study assumption; material, waterproofing performance and installation NOT_VERIFIED'},{'id':side+'_adhesive','side':side,'thickness_m':'.008','existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION','layer_role':'wet_finish_bedding','material_hypothesis':'8mm concept bedding/adhesive allowance, not installed product'},{'id':side+'_tile','side':side,'thickness_m':'.005','existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION','layer_role':'wet_surface_finish','material_hypothesis':'5mm concept surface tile study, not selected manufacturer'}])
    else:layers.append({'id':side+'_finish','side':side,'thickness_m':S(finish),'existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION','layer_role':'render_finish'if role=='exterior_envelope'else'dry_finish','material_hypothesis':'15mm render concept allowance'if role=='exterior_envelope'else'10mm dry plaster/lining concept allowance'})
  for side in ('minus','plus'):
   used=F(0);rank=0
   for layer in [z for z in layers if z['side']==side]:
    thickness=F(layer['thickness_m']);sign=-1 if side=='minus'else 1;rank+=1
    layer.update(order_from_axis=rank,inner_interface_coordinate=S(mid+sign*used),outer_interface_coordinate=S(mid+sign*(used+thickness)),source_reference='Declared concept hypothesis under B02, not a sourced product thickness')
    used+=thickness
  omitted={'thermal_insulation':{'modeled_state':'ABSENT_IN_THIS_CONCEPT_VARIANT','actual_building_state':'UNKNOWN'},'separate_cladding':{'modeled_state':'ABSENT_IN_THIS_CONCEPT_VARIANT','actual_building_state':'UNKNOWN'},'waterproofing_system':{'modeled_state':'ASSUMED_GEOMETRIC_2MM_MEMBRANE'if role in('wet_service_partition','kitchen_service_partition')else'NOT_APPLICABLE_TO_THIS_DRY_STUDY_FACE','performance':'NOT_VERIFIED','actual_building_state':'UNKNOWN','numeric_zero_claimed':False}}
  for layer in layers:
   layer['material_model_or_concept_type']=layer['material_hypothesis']
   layer['thickness_basis']=layer.get('source_reference','Explicit provisional concept geometry, not a selected technical system')
   layer['layer_type']={'partition_body_segment':'core','source_pocket_or_opaque_skin':'cladding','wet_finish_bedding':'adhesive','wet_surface_finish':'finish','wet_waterproofing_membrane':'membrane','render_finish':'finish','dry_finish':'finish'}[layer['layer_role']]
  profiles[hid]={'role':role,'profile_kind':'CONCEPT_SENSITIVITY_NOT_TECHNICAL','source_reference':'Blueprint B02 lines395-398/2053-2058 concept15/25 sensitivity; source-specific pocket/skin geometry retained','axis':{'orientation':'vertical'if ax==0 else'horizontal','coordinate':S(mid)},'offsets':{'minus':S(off),'plus':S(off)},'faces':{'minus':S(lo),'plus':S(hi)},'layers':layers,'layer_composition_status':'DECLARED_LAYER_HYPOTHESIS_NOT_TECHNICALLY_VERIFIED','layer_profile_source':'Internal explicit concept-comparison composition under Blueprint B02; numeric allowances are provisional design assumptions, not sourced product specifications','finish_by_side':{side:('EXPLICITLY_ABSENT_WITH_BASIS'if hi-lo<F('.1')else'MODELED_IN_LAYERS')for side in('minus','plus')},'finish_absence_basis':{side:'Thin source geometric pocket/opaque panel is modeled as the exposed skin in this concept variant; no additional finish selected; installed condition unknown.'for side in('minus','plus')},'unmodeled_components':omitted,'composition_authority':'Explicit internal concept comparison hypothesis, not owner-selected materials or approved technical system; actual installation remains unknown.','system_verification':'NOT_VERIFIED','construction_tolerance':'UNKNOWN_NOT_ZERO','material_and_installation':'NOT_SELECTED_NOT_VERIFIED','claims_symmetric_construction':False}
 m['wall_finish_profile']=profiles
 allocations=[]
 for o in m['openings']:
  oid=o['id']
  if oid not in('A.entry','B.entry','stair.entry','lift.entry'):continue
  q=Q(o['rect']);ax=0 if q[2]-q[0]<q[3]-q[1]else 1;mid=(q[ax]+q[ax+2])/2
  owners={'A.entry':['unit:A','common:lobby'],'B.entry':['common:lobby','unit:B'],'stair.entry':['common:stair','common:lobby'],'lift.entry':['common:lobby','common:lift']}[oid]
  for side,owner in zip(('minus','plus'),owners):
   r=list(q);r[ax+2 if side=='minus'else ax]=mid
   allocations.append({'opening_id':oid,'host_wall_id':o['host_wall_id'],'side':side,'owner':owner,'rect':list(map(S,r)),'reference_axis':{'orientation':'vertical'if ax==0 else'horizontal','coordinate':S(mid)},'area_m2':S((r[2]-r[0])*(r[3]-r[1])),'source_reference':'Blueprint line427: threshold floor divided by documented shared reference line; modeled clear portal, not fabricated frame subtraction','frame_basis':'Actual model opening aperture; installed frame/hardware tolerances not certified.'})
 m['threshold_ownership']={'schema':'PORTAL_REFERENCE_HALF_OWNERSHIP118','allocations':allocations,'physical_space':'actual modeled aperture floor only','does_not_change_room_or_unit_count':True,'installed_frame_not_certified':True}
 return m
