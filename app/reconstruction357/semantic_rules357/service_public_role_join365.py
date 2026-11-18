"""Own-source role intersection: public support does not authorize entry-floor relabelling."""
import json
from pathlib import Path
from common import digest
from modules_spatial import rect,intersection,union_area,difference,source_sweeps
from guest_closure import transformed_rect
from reassess_spatial_service365 import evaluate as reassess
ROOT=Path(__file__).resolve().parents[1]
def clips(a,b):return [z for x in a for y in b if(z:=intersection(x,y))]
def classify_cells(residual,living,entry,body,instances,operations):
 if difference(residual,entry):raise ValueError('SERVICE_RESIDUAL_OUTSIDE_ACTUAL_ENTRY_DOMAIN')
 living_overlap=clips(residual,living);instance=clips(residual,instances);operation=clips(residual,operations)
 return {'route_only_residual_area_m2':str(union_area(residual)),'whole_actual_living_region_intersection_m2':str(union_area(living_overlap)),'body_connected_support_intersection_m2':str(union_area(clips(residual,body))),'actual_living_fixture_activity_intersection_m2':str(union_area(instance)),'actual_linear_operation_portal_intersection_m2':str(union_area(operation)),'remaining_without_independent_nonservice_use_m2':str(union_area(difference(residual,instance+operation))),'remaining_without_independent_nonservice_use_regions':[list(map(str,q))for q in difference(residual,instance+operation)],'verdict':'UNKNOWN_NON_SERVICE_FUNCTION_OR_NECESSITY_NOT_ESTABLISHED','exclusive_function_proven':False,'scope':'Living role-domain membership and verified source functional instances are separate from body reachability. No footprint tiling requirement and no automatic reclassification of empty floor.'}
def evaluate(record,review):
 spatial=reassess(record,review);m=record['candidate']['model'];out=[]
 if spatial['model_hash']!=digest(m)or spatial['raw_review_digest']!=digest(review):raise ValueError('OWN_SOURCE_REASSESSMENT_BINDING')
 for u in m['units']:
  uid=u['id'];p=next(p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath');source=p['module']
  if digest(source)!=p['module_hash']:raise ValueError('SOURCE_BATH_HASH')
  serviceids={p['id_map'][k]for k in source['unit']['activities']}
  if not serviceids<=set(u['routes']):raise ValueError('REQUIRED_SOURCE_SERVICE_ROUTE_INVENTORY')
  approach=[transformed_rect(q,p['transform'])for q in source['unit']['rooms']['public_access']];opening=next(o for o in m['openings']if o['id']==uid+'.bath');entry=list(map(rect,u['rooms']['entry_circulation']));bath=list(map(rect,u['rooms']['bath']))
  nonservice=[s for k,pth in u['routes'].items()if k not in serviceids for s in source_sweeps(pth,m['profile']['body_m'])]+[s for pth in u['scenario_routes'].values()for s in source_sweeps(pth,m['profile']['body_m'])]
  service=[s for k in serviceids for s in source_sweeps(u['routes'][k],m['profile']['body_m'])]
  if difference(entry,nonservice+service):raise ValueError('ACTUAL_ENTRY_ROUTE_INVENTORY_INCOMPLETE')
  residual=difference(entry,nonservice+bath+approach+[rect(opening['rect'])]);sr=next(r for r in spatial['support']['rows']if r['unit']==uid)
  ans=classify_cells(residual,list(map(rect,u['rooms']['living'])),entry,list(map(rect,sr['body_study']['support_regions'])),list(map(rect,sr['actual_fixture_activity_regions'])),list(map(rect,sr['actual_linear_operation_portal_regions'])))
  ans.update(unit=uid,service_target_ids=sorted(serviceids),source_module_digest=p['module_hash'],support_evidence_digest=digest(sr),actual_living_domain_digest=digest(u['rooms']['living']),residual_regions=[list(map(str,q))for q in residual]);out.append(ans)
 return {'schema':'SERVICE365_OWN_PUBLIC_ROLE_JOIN','model_digest':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'spatial_evidence_digest':digest(spatial),'units':out,'source_scope':'Q03 service role and Q04 circulation purpose remain separate from Q11 positive whole-functional living region. This is a measured gap, not an impossibility or uselessness verdict.','admission_allowed':False,'fresh_execution':False}
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());v=json.loads((ROOT/'review365_service_source_validation/result.json').read_text());print(json.dumps(evaluate(r,v),indent=2))
