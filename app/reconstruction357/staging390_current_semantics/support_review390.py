"""357 reconstructed same-fresh body support + actual functional instance cover.
This measures exact unresolved public extent, not automatic whole-role approval.
"""
from fractions import Fraction as F
import time
from common import rows,digest
from supporting_floor import analyze
from modules_spatial import rect,intersection,union_area,difference
from living_closure390 import evaluate as living
from door_reservations import derive as door_reservations

def evaluate(envelope,result,groups,seconds=20):
 start=time.monotonic();m=envelope['packet']['world_model'];out={'schema':'FUNCTIONAL_SUPPORT_BALANCED365_SAME_FRESH','model_hash':digest(m),'base_fresh_digest':digest(result),'rows':[],'parent_complete':False,'admission_allowed':False}
 try:
  if not 0<seconds<=30:raise ValueError('BOUNDED_BUDGET')
  req=rows(m,result['raw_fresh_report']);intr=living(envelope,result,groups,min(6,seconds))
  if intr['verdict']!='PASS_SCOPED_INTRINSIC_LIVING':raise ValueError('COMPLETE_SOURCE_SITTING_PREREQUISITE')
  for rid in('fixture_inventory_use','door_operation','partition_ledger','chair_capacity_movement'):
   if req[rid]['status']!='PASS_LIMITED':raise ValueError('SOURCE_FUNCTION:'+rid)
  out['source_function_rows']={k:digest(req[k])for k in('fixture_inventory_use','door_operation','partition_ledger','chair_capacity_movement')};out['intrinsic_closure_digest']=digest(intr)
  for u in m['units']:
   role=u['spatial_role_bindings']['living_activity_group'];anchors=[u['routes'][k][-1]for k in role['access_route_ids']]
   obs=list(m['walls'].values())+list(u['fixtures'].values())+[q for k,rs in u['rooms'].items()if k.startswith('bed')or k in('bath','kitchen','private_circulation')for q in rs]
   for op in m['operations']['doors']:obs.append(op['open_panel'])
   for op in m['operations']['kitchen']:
    if op['unit']==u['id']:obs+=op.get('motion_envelopes',[])
   for op in m['operations']['dining_chairs']:
    if op['unit']==u['id']:
     obs.append(op['occupied_body']);a,b=rect(op['closed_rect']),rect(op['open_rect']);obs.append(list(map(str,[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])))
   for seat in u['public_program']['capacity']['living_seats']:obs.append(seat['occupied_body'])
   remaining=seconds-(time.monotonic()-start)
   if remaining<=0:raise ValueError('SUPPORT_REVIEW_DEADLINE')
   r=analyze(u['ownership'],obs,anchors,m['profile']['body_m'],seconds=min(12,remaining))
   target=[rect(x)for x in u['rooms']['living']];body_support=[rect(x)for x in r.get('support_regions',[])];instances=[rect(u['fixtures'][k])for k in role['fixture_ids']]+[rect(u['activities'][k])for k in role['activity_ids']];operations=[]
   for op in m['operations']['doors']:
    if not any(st.get('unit')==u['id']for st in op.get('states',[])):continue
    for key in('closed_panel','open_panel','rail_envelope'):
     if key in op:operations.append(rect(op[key]))
    for st in op['states']:
     if st['unit']==u['id']:operations.append(rect(st['actor_rect']))
    for st in op.get('continuous_actor_segments',[]):
     if st['unit']!=u['id']:continue
     a,b=rect(st['actor_start']),rect(st['actor_end'])
     if a[0]==b[0]or a[1]==b[1]:operations.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
   for seat in u['public_program']['capacity']['living_seats']:operations.append(rect(seat['occupied_body']))
   for t in m['threshold_ownership']['allocations']:
    if t.get('owner')=='unit:'+u['id']:operations.append(rect(t['rect']))
   for opening in m['openings']:
    if any(x.startswith(u['id']+'.')for x in opening.get('connects',[])):operations.append(rect(opening['rect']))
   reservations=door_reservations(m,u['id']);pre_reservation=difference(target,body_support+instances+operations);unassigned=list(pre_reservation);reservation_ledger=[]
   for reservation in reservations:
    q=rect(reservation['region']);assigned=[z for a in unassigned if(z:=intersection(a,q))]
    if assigned:
     reservation_ledger.append({'source_reservation':reservation,'claimed_fragments':[list(map(str,z))for z in assigned],'claimed_area_m2':str(union_area(assigned)),'source_door_operation_row_digest':digest(req['door_operation']),'source_door_method':req['door_operation']['method']})
     unassigned=difference(unassigned,[q])
   operations += [rect(x['region'])for x in reservations]
   cover=body_support+instances+operations;rem=difference(target,cover);body_area=union_area([z for a in target for b in body_support if(z:=intersection(a,b))]);area=union_area(target);unresolved=union_area(rem)
   out['rows'].append({'unit':u['id'],'body_study':r,'public_domain_area_m2':str(area),'source_body_support_area_m2':str(body_area),'actual_fixture_activity_regions':[list(map(str,q))for q in instances],'actual_linear_operation_portal_regions':[list(map(str,q))for q in operations],'body_plus_source_function_coverage_m2':str(area-unresolved),'unresolved_area_m2':str(unresolved),'unresolved_regions':[list(map(str,q))for q in rem],'source_door_reservations':reservations,'reservation_purpose_ledger':reservation_ledger,'pre_reservation_unresolved_area_m2':str(union_area(pre_reservation)),'reservation_claimed_union_area_m2':str(union_area(pre_reservation)-union_area(unassigned)),'reservation_claims_disjoint_by_construction':True,'region_role_complete':False})
  out['status']='MEASURED_CURRENT_SOURCE_SUPPORT_NOT_FINAL_ROLE_APPROVAL';out['engineering_assumption']='Source-body-connected supporting floor can supplement complete source sitting/use bundle. Exclusive circulation, role allocation, unsupported pockets and author applicability remain separate. No conservative rotary bounding box is granted useful area.'
 except (ValueError,KeyError,TypeError,IndexError,AttributeError)as e:out['status']='UNKNOWN';out['missing']=[str(e)]
 out['elapsed_seconds']=time.monotonic()-start;return out
