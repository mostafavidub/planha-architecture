"""B02 conceptual face/layer accounting, not approval of construction systems.
Blueprint395-398/2053-2058 permits nominal10/20 or sensitivity15/25 with
explicit assumptions; unknown finish/material/tolerance is never numerical zero.
All offsets, boundaries and layer sums are verified against actual host geometry.
"""
from fractions import Fraction as F
from core_wall_audit118 import q

def examine(m):
 errors=[];pending=[];rows=[];hosts=m.get('wall_hosts',{});profiles=m.get('wall_finish_profile')
 if not isinstance(profiles,dict):return {'status':'NOT_EVALUATED','errors':[],'pending':['MISSING_PER_HOST_FINISHED_FACE_PROFILE'],'rows':[]}
 if set(profiles)!=set(hosts):errors.append('FINISH_PROFILE_HOST_INVENTORY')
 for hid,raw in hosts.items():
  if hid not in profiles:pending.append(hid+':PROFILE_MISSING');continue
  p=profiles[hid]
  try:
   host=q(raw);orientation=p['axis']['orientation'];axis=F(str(p['axis']['coordinate']));offs={k:F(str(p['offsets'][k]))for k in('minus','plus')};faces={k:F(str(p['faces'][k]))for k in('minus','plus')}
   if orientation not in('vertical','horizontal'):raise ValueError('UNSUPPORTED_AXIS')
   k=0 if orientation=='vertical'else 1;actual=(host[k],host[k+2]);thickness=actual[1]-actual[0]
   if offs['minus']<0 or offs['plus']<0:errors.append(hid+':NEGATIVE_FACE_OFFSET')
   if faces['minus']!=axis-offs['minus']or faces['plus']!=axis+offs['plus']:errors.append(hid+':AXIS_OFFSET_FACE_MISMATCH')
   if (faces['minus'],faces['plus'])!=actual:errors.append(hid+':FINISHED_FACES_NOT_ACTUAL_HOST')
   if offs['minus']+offs['plus']!=thickness:errors.append(hid+':OFFSET_TOTAL_NOT_PHYSICAL_THICKNESS')
   if not p.get('role')or not p.get('source_reference'):pending.append(hid+':ROLE_OR_SOURCE_MISSING')
   if p.get('role')in('source_bound_module_host','unknown','generic'):pending.append(hid+':WALL_FUNCTIONAL_ROLE_NOT_SPECIFIED')
   if p.get('layer_composition_status')!='DECLARED_LAYER_HYPOTHESIS_NOT_TECHNICALLY_VERIFIED':pending.append(hid+':LAYER_COMPOSITION_NOT_ESTABLISHED')
   if not p.get('layer_profile_source'):pending.append(hid+':LAYER_PROFILE_PROVENANCE_MISSING')
   finish=p.get('finish_by_side',{})
   for side in('minus','plus'):
    if finish.get(side)not in('MODELED_IN_LAYERS','EXPLICITLY_ABSENT_WITH_BASIS'):pending.append(hid+':FINISH_NOT_ESTABLISHED:'+side)
    elif finish[side]=='EXPLICITLY_ABSENT_WITH_BASIS'and not p.get('finish_absence_basis',{}).get(side):pending.append(hid+':FINISH_ABSENCE_WITHOUT_BASIS:'+side)
   if p.get('profile_kind')!='CONCEPT_SENSITIVITY_NOT_TECHNICAL':pending.append(hid+':PROFILE_NOT_THIS_DECLARED_CONCEPT_SCOPE')
   if p.get('system_verification')!='NOT_VERIFIED':errors.append(hid+':UNSUPPORTED_TECHNICAL_VERIFICATION_CLAIM')
   if p.get('construction_tolerance')!='UNKNOWN_NOT_ZERO':pending.append(hid+':CONSTRUCTION_TOLERANCE_MUST_REMAIN_EXPLICIT_UNKNOWN')
   layers=p.get('layers');sums={'minus':F(0),'plus':F(0)};ids=set();unknown=False
   order_counts={'minus':0,'plus':0};interfaces={'minus':axis,'plus':axis}
   for component,record in p.get('unmodeled_components',{}).items():
    if record.get('modeled_state')in('NOT_SPECIFIED','UNKNOWN'):pending.append(hid+':GEOMETRIC_COMPONENT_NOT_SPECIFIED:'+component)
    if record.get('numeric_zero_claimed')and record.get('modeled_state')in('NOT_SPECIFIED','UNKNOWN'):errors.append(hid+':UNKNOWN_COMPONENT_AS_ZERO:'+component)
   if not isinstance(layers,list)or not layers:pending.append(hid+':LAYER_RECORDS_MISSING');unknown=True;layers=[]
   for layer in layers:
    lid=layer.get('id');side=layer.get('side');value=layer.get('thickness_m');existence=layer.get('existence')
    if not lid or lid in ids:errors.append(hid+':LAYER_ID_MISSING_OR_DUPLICATED')
    ids.add(lid)
    if side not in sums:errors.append(hid+':LAYER_SIDE_UNKNOWN');continue
    if value is None or existence=='UNKNOWN':pending.append(hid+':LAYER_THICKNESS_OR_EXISTENCE_UNKNOWN:'+str(lid));unknown=True;continue
    t=F(str(value))
    if t<0:errors.append(hid+':NEGATIVE_LAYER')
    if t==0 and existence!='ABSENT':errors.append(hid+':UNKNOWN_OR_PRESENT_LAYER_AS_ZERO')
    if t>0 and existence not in('ASSUMED_PRESENT','PRESENT'):errors.append(hid+':POSITIVE_LAYER_WITHOUT_PRESENCE')
    if layer.get('status')!='CONCEPT_ASSUMPTION':pending.append(hid+':LAYER_ASSUMPTION_STATUS_MISSING')
    kind=layer.get('layer_type');description=str(layer.get('meaning',''))+' '+str(layer.get('id',''))
    if kind not in('core','cladding','finish','adhesive','insulation','membrane','air_cavity')or'aggregate'in description.lower():pending.append(hid+':ACTUAL_LAYER_TYPE_NOT_ESTABLISHED:'+str(lid))
    if not layer.get('material_model_or_concept_type')or not layer.get('thickness_basis'):pending.append(hid+':LAYER_TYPE_OR_THICKNESS_PROVENANCE_MISSING:'+str(lid))
    order_counts[side]+=1
    if layer.get('order_from_axis')!=order_counts[side]:errors.append(hid+':LAYER_ORDER_NOT_CONTIGUOUS:'+str(lid))
    try:
     inner=F(str(layer['inner_interface_coordinate']));outer=F(str(layer['outer_interface_coordinate']))
     if inner!=interfaces[side]or outer!=inner+(-t if side=='minus'else t):errors.append(hid+':LAYER_INTERFACE_NOT_ACTUAL_OFFSET:'+str(lid))
     interfaces[side]=outer
    except(KeyError,ValueError,TypeError,ZeroDivisionError):pending.append(hid+':LAYER_INTERFACES_MISSING:'+str(lid))
    sums[side]+=t
   if not unknown and sums!=offs:errors.append(hid+':LAYER_SUM_NOT_FINISHED_OFFSET')
   if not unknown and interfaces!=faces:errors.append(hid+':LAYER_OUTERMOST_INTERFACES_NOT_FINISHED_FACES')
   # A centered placement axis alone does not certify symmetric construction.
   if p.get('claims_symmetric_construction'):errors.append(hid+':SYMMETRIC_CONSTRUCTION_NOT_ESTABLISHED_BY_OFFSETS')
   rows.append({'host':hid,'role':p.get('role'),'orientation':orientation,'axis':str(axis),'offsets':{k:str(v)for k,v in offs.items()},'actual_faces':list(map(str,actual)),'finished_thickness_m':str(thickness),'layer_sums':{k:str(v)for k,v in sums.items()},'nominal_value_status':'DECLARED_CONCEPT_ASSUMPTION_ONLY','composition_status':p.get('layer_composition_status','NOT_ESTABLISHED'),'system_materials_installation':'NOT_VERIFIED','tolerance':'UNKNOWN_NOT_ZERO'})
  except(KeyError,ValueError,TypeError,ZeroDivisionError)as e:pending.append(hid+':FINISH_PROFILE_SCHEMA_OR_DATA:'+str(e))
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_CONCEPT_FACE_LAYER_GEOMETRY','errors':sorted(set(errors)),'pending':sorted(set(pending)),'rows':rows,'scope':'Axis, asymmetric offsets, ordered-side layer sums and actual modeled clear faces only. Assumed aggregate thickness is not a selected material system or manufacturer/structural/fire/acoustic/moisture/installation approval. Unknown technical layer composition and construction tolerance are not set to zero.'}
