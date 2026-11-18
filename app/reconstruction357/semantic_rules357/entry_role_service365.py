"""Intrinsic source-declared access role and measured route-use classes.
No compactness/necessity comparison dependency and no claim about all possible uses.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
import common
from common import digest,rows
from group_readsets_service365 import build
from modules_spatial import rect,intersection,difference,union_area,source_sweeps
from guest_closure import transformed_rect
ROOT=Path(__file__).resolve().parents[1]
def clips(a,b):return[z for x in a for y in b if(z:=intersection(x,y))]
def partition(entry,service,nonservice,approach):
 unknown=difference(entry,service+nonservice)
 if unknown:raise ValueError('ENTRY_WITHOUT_CHECKED_REQUIRED_TRAVERSAL_STOP')
 s=clips(entry,service);n=clips(entry,nonservice);shared=clips(s,n);so=difference(s,n);no=difference(n,s);extra=difference(so,approach)
 if union_area(shared+so+no)!=union_area(entry):raise ValueError('ACCESS_ROLE_PARTITION_STOP')
 return {'whole_entry_area_m2':str(union_area(entry)),'current_source_service_only_route_area_m2':str(union_area(so)),'current_source_nonservice_only_route_area_m2':str(union_area(no)),'current_source_shared_route_area_m2':str(union_area(shared)),'service_only_outside_source_approach_m2':str(union_area(extra)),'service_only_outside_source_approach_regions':[list(map(str,q))for q in extra],'all_cells_required_traversal_bound':True,'classification_scope':'CURRENT_SOURCE_DECLARED_ROUTE_USE_CLASSES_NOT_EXCLUSIVITY_OF_ALL_POSSIBLE_FUNCTIONS'}
def evaluate(record,review):
 views=build(record,review,source_profile='SOURCE_SERVICE365');m=record['candidate']['model'];old=common.REGISTRY_NAME
 try:common.REGISTRY_NAME='method_registry_service365.json';req=rows(m,review['raw_report'])
 finally:common.REGISTRY_NAME=old
 deps=['body_route_sweeps','serving_route','fixture_inventory_use','bath_service_operation','door_operation','partition_ledger','circulation_functional_integrity']
 for k in deps:
  w=req[k]['evidence']['witness']
  if req[k]['status']!='PASS_LIMITED'or w.get('errors')or w.get('pending'):raise ValueError('CURRENT_FUNCTION_PREREQUISITE:'+k)
 out=[]
 for u in m['units']:
  uid=u['id'];body=F(m['profile']['body_m']);routes=u['routes'];scenario=u['scenario_routes']
  if set(routes)-set(u['activities'])!={'kitchen'}or routes['kitchen']!=routes['kitchen_work']or set(u['activities'])-set(routes):raise ValueError('UNKNOWN_SOURCE_ACTIVITY_ROUTE_INVENTORY_STOP')
  checked=req['body_route_sweeps']['evidence']['witness']['routes'];sc=req['serving_route']['evidence']['witness']['routes']
  for name in u['activities']:
   if not any(q['unit']==uid and q['route']==name and F(q['body_m'])==body for q in checked):raise ValueError('UNCHECKED_REQUIRED_ACTIVITY_STOP')
  for name in scenario:
   if not any(q['unit']==uid and q['route']==name and F(q['body_width'])==body for q in sc):raise ValueError('UNCHECKED_SOURCE_SCENARIO_STOP')
  if set(scenario)!={'guest_living','guest_dining','kitchen_to_dining_floor'}:raise ValueError('UNKNOWN_SOURCE_SCENARIO_INVENTORY_STOP')
  paths={**routes,**{'scenario:'+k:v for k,v in scenario.items()}}
  if u['public_floor_classification']['route_geometry_hash']!=digest(paths):raise ValueError('SOURCE_FINAL_FLOOR_ROUTE_HASH_STOP')
  swept=[q for p in paths.values()for q in source_sweeps(p,body)];owner=list(map(rect,u['ownership']));fixed=[rect(q)for name,rr in u['rooms'].items()if name not in('living','entry_circulation')for q in rr];walls=list(map(rect,m['walls'].values()));expected=difference(clips(owner,swept),fixed+walls);entry=list(map(rect,u['rooms']['entry_circulation']))
  if difference(entry,expected)or difference(expected,entry):raise ValueError('SOURCE_FINAL_ENTRY_CLASSIFICATION_STOP')
  p=next(p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath')
  if digest(p['module'])!=p['module_hash']:raise ValueError('SOURCE_SERVICE_MODULE_STOP')
  serviceids={p['id_map'][k]for k in p['module']['unit']['activities']};service=[q for k in serviceids for q in source_sweeps(routes[k],body)];nonservice=[q for k,pth in paths.items()if k not in serviceids for q in source_sweeps(pth,body)]
  approach=[transformed_rect(q,p['transform'])for q in p['module']['unit']['rooms']['public_access']]+[rect(next(o for o in m['openings']if o['id']==uid+'.bath')['rect'])]
  evidence=partition(entry,service,nonservice,approach);evidence.update(unit=uid,service_target_ids=sorted(serviceids),required_activity_ids=sorted(u['activities']),required_scenario_ids=sorted(scenario),source_route_geometry_hash=digest(paths),source_module_digest=p['module_hash'],source_whole_entry_domain_digest=digest(u['rooms']['entry_circulation']),verdict='PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE',necessity_verdict='NOT_ASSESSED_REQUIRES_INDEPENDENT_FINITE_COMPARISON');out.append(evidence)
 source=ROOT/'planha_general150_runtime_work/final_public_floor120.py';sha=hashlib.sha256(source.read_bytes()).hexdigest()
 if record['trace']['source_inventory'].get(str(source.relative_to(ROOT)))!=sha:raise ValueError('SOURCE_FLOOR_CONSTRUCTOR_PIN_STOP')
 return {'schema':'SERVICE365_INTRINSIC_ENTRY_ROLE_AND_CURRENT_ROUTE_USE_CLASSES','verdict':'PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE','model_digest':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'source_row_digests':{k:digest(req[k])for k in deps},'constructor':{'source':'final_public_floor120.py:rebuild','sha256':sha},'units':out,'engineering_scope':'The actual source entry domain is exactly its valid required/scenario body-path union outside other functional rooms and walls. This proves current access function, not optimal or necessary path cost, all possible multifunction, or global exclusive use. Source service-only area is a comparison cost input, not a zero-area acceptance condition.','compactness_verdict':'UNKNOWN_REQUIRES_FINITE_COMPARISON','admission_allowed':False,'fresh_execution':False}
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());v=json.loads((ROOT/'review365_service_source_validation/result.json').read_text());print(json.dumps(evaluate(r,v),indent=2))
