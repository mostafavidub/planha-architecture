"""358 source-bound intrinsic circulation inventory; necessity stays separate.
No old fresh reuse, whole-component role inferred from a label, or new admission.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import common
from common import digest,rows
from group_readsets365_v2 import build
from modules_spatial import rect,intersection,union_area,difference,source_sweeps
from wall_purpose import touches
from wall_origin365 import hall as bound_hall365
from unsupported_extent_causes357 import boundary_openings
ROOT=Path(__file__).resolve().parents[1]
def components(regions):
 left=set(range(len(regions)));out=[]
 while left:
  i=min(left);left.remove(i);ids=[i];todo=[i]
  while todo:
   a=todo.pop()
   for b in list(left):
    if touches(regions[a],regions[b])or intersection(regions[a],regions[b]):left.remove(b);ids.append(b);todo.append(b)
  out.append([regions[i]for i in ids])
 return out

def component_accounting(domain,required_paths,body,source_uses=()):
 if not required_paths:raise ValueError('REQUIRED_TARGET_INVENTORY_EMPTY')
 sweeps={k:source_sweeps(v,body)for k,v in required_paths.items()};out=[]
 for c in components(domain):
  served=[k for k,ss in sweeps.items()if any(intersection(a,b)for a in c for b in ss)];covered=[z for a in c for ss in sweeps.values()for b in ss if(z:=intersection(a,b))];uses=[z for a in c for b in source_uses if(z:=intersection(a,b))];rem=difference(c,covered+uses)
  out.append({'regions':[list(map(str,q))for q in c],'area_m2':str(union_area(c)),'required_targets_served':served,'actual_body_route_coverage_m2':str(union_area(covered)),'source_use_coverage_m2':str(union_area(uses)),'unsupported_margin_area_m2':str(union_area(rem)),'unsupported_margin_regions':[list(map(str,q))for q in rem],'verdict':'PASS_EXACT_REQUIRED_PATH_USE_COMPONENT'if served and not rem else'UNKNOWN_COMPONENT_WITHOUT_REQUIRED_TARGET'if not served else'UNKNOWN_MARGIN_OR_BLIND_APPENDAGE_REQUIRES_SOURCE_FUNCTION'})
 return out

def transverse_source_margin(domain,required_paths,body,max_clear_width):
 """Engineering operationalization of valid transverse margin, not tail use.
 Fill only a source corridor cross-section already traversed by a verified
 centerline; no longitudinal extension beyond actual swept body is created.
 """
 b=F(body);limit=F(max_clear_width);cover=[]
 if limit<b:raise ValueError('SOURCE_CORRIDOR_NARROWER_THAN_BODY')
 for q in domain:
  widths=(q[2]-q[0],q[3]-q[1])
  for path in required_paths.values():
   for a,z in zip(path,path[1:]):
    a,z=list(map(F,a)),list(map(F,z));axis=0 if a[1]==z[1]else 1 if a[0]==z[0]else None
    if axis is None:raise ValueError('ORTHOGONAL_SOURCE_ROUTE')
    normal=1-axis
    if not b<=widths[normal]<=limit or not q[normal]<=a[normal]<=q[normal+2]:continue
    lo=max(q[axis],min(a[axis],z[axis])-b/2);hi=min(q[axis+2],max(a[axis],z[axis])+b/2)
    if lo<hi:
     r=list(q);r[axis]=lo;r[axis+2]=hi;cover.append(tuple(r))
 return cover

def terminal_extensions(private,model,unit,paths,uses):
 """Detect source-rect terminal branches, not infer all unswept floor useless."""
 found=[];walls=list(map(rect,model['walls'].values()));sweeps=[sw for p in paths.values()for sw in source_sweeps(p,model['profile']['body_m'])]
 for q in private:
  long=0 if q[2]-q[0]>=q[3]-q[1]else 1;normal=1-long
  contacts=[b for b in private if b!=q and touches(q,b)]
  cuts=sorted({max(q[long],b[long])for b in contacts}|{min(q[long+2],b[long+2])for b in contacts})
  cuts=[x for x in cuts if q[long]<x<q[long+2]]
  if not cuts:continue
  for lo,hi in ((q[long],min(cuts)),(max(cuts),q[long+2])):
   a=list(q);a[long]=lo;a[long+2]=hi;a=tuple(a)
   if lo>=hi:continue
   openings=boundary_openings([a],walls)
   if not openings or any(o['axis']!=long for o in openings)or len({o['coordinate']for o in openings})!=1:continue
   actual_portals=[o['id']for o in model['openings']if intersection(a,rect(o['rect']))or touches(a,rect(o['rect']))]
   actual_uses=[x for x in uses if intersection(a,x)];actual_paths=[x for x in sweeps if intersection(a,x)]
   if actual_portals or actual_uses or actual_paths:continue
   if any(intersection(a,rect(u['geometry']))for u in found):continue
   found.append({'geometry':list(map(str,a)),'area_m2':str(union_area([a])),'source_private_rect':list(map(str,q)),'only_floor_connection':openings,'actual_portals':actual_portals,'actual_use_intersections':0,'actual_required_path_intersections':0,'classification':'UNTARGETED_TERMINAL_PRIVATE_EXTENSION_NECESSITY_OR_STAGING_ROLE_UNPROVEN','verdict':'UNKNOWN_NOT_PROVEN_USELESS','scope':'Exact three-sided solid boundary and one floor connection; no current source target/portal/activity/path witness. Generic maneuver/staging is not disproved; compare valid shortening alternative before hard rejection.'})
 return found

def evaluate(record,review):
 views=build(record,review,source_profile='SOURCE_BALANCED365');m=record['candidate']['model'];before=digest([record,review]);old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source365.json';req=rows(m,review['raw_report'])
 finally:common.REGISTRY_NAME=old
 deps=['body_route_sweeps','fixture_inventory_use','door_operation','private_grouping','circulation_functional_integrity','bath_service_operation','kitchen_essential_operation','partition_ledger','guest_living_route','guest_dining_route','serving_route']
 if any(req[k]['status']!='PASS_LIMITED'for k in deps):raise ValueError('FRESH_INTRINSIC_CIRCULATION_PREREQUISITE')
 origin={'raw':record['candidate']['request'],'packet':record['candidate']['packet'],'generation_context':record['candidate']['generation_context']};hall=bound_hall365(record)
 if hall is None:raise ValueError('SOURCE_HALL_ORIGIN_UNSUPPORTED')
 for wid,q in hall[0]['walls'].items():
  if rect(q)!=rect(m['walls'][wid]):raise ValueError('SOURCE_HALL_WALL_BINDING')
 h08=req['body_route_sweeps']['evidence']['witness']['routes'];out={'schema':'CIRCULATION_ROLE_BALANCED365_INTRINSIC_NOT_NECESSITY','model_hash':digest(m),'review_digest':digest(review),'record_digest':digest(record),'source_row_digests':{k:digest(req[k])for k in deps},'hall_origin':hall[1],'units':[],'parent_complete':False,'fresh_execution':False,'admission_allowed':False}
 for u in m['units']:
  uid=u['id'];paths={};inventory=[]
  for a,p in u['routes'].items():
   if a not in u['activities']:continue
   target=u['route_targets'].get(a)
   if target is None or list(map(F,p[-1]))!=list(map(F,target)):raise ValueError('ACTUAL_ROUTE_TARGET_BINDING')
   if not any(x['unit']==uid and x['route']==a and F(x['body_m'])==F(m['profile']['body_m'])for x in h08):raise ValueError('H08_REQUIRED_PATH_NOT_EXECUTED')
   paths[a]=p;inventory.append({'activity_id':a,'geometry':u['activities'][a],'target':target,'route_digest':digest(p)})
  if set(u['activities'])-set(paths):raise ValueError('SOURCE_ACTIVITY_ROUTE_INVENTORY_INCOMPLETE')
  scenario_rows=req['serving_route']['evidence']['witness']['routes']
  for name,path in u['scenario_routes'].items():
   if name not in ('guest_living','guest_dining','kitchen_to_dining_floor')or not any(r['unit']==uid and r['route']==name and F(r['body_width'])==F(m['profile']['body_m'])for r in scenario_rows):raise ValueError('SOURCE_SCENARIO_ROUTE_NOT_CHECKED')
   paths['scenario:'+name]=path;inventory.append({'scenario_route':name,'source_method':req['serving_route']['method'],'route_digest':digest(path)})
  uses=[rect(v)for v in u['fixtures'].values()]+[rect(v)for v in u['activities'].values()]
  for op in m['operations']['doors']:
   if not any(s.get('unit')==uid for s in op.get('states',[])):continue
   uses +=[rect(s['actor_rect'])for s in op['states']if s.get('unit')==uid]
   for s in op.get('continuous_actor_segments',[]):
    if s['unit']==uid:
     a,b=rect(s['actor_start']),rect(s['actor_end'])
     if a[0]==b[0]or a[1]==b[1]:uses.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
  private=list(map(rect,u['rooms']['private_circulation']));entry=list(map(rect,u['rooms']['entry_circulation']));margin=transverse_source_margin(private,paths,m['profile']['body_m'],record['trace']['proposal']['ordered_macro']['private_hall_clear_depth']);pc=component_accounting(private,paths,m['profile']['body_m'],uses+margin);ec=component_accounting(entry,paths,m['profile']['body_m'],uses)
  service=[]
  for p in m['module_placements']:
   if p['unit_id']!=uid or p['module']['schema']not in('BATHROOM_MODULE117','KITCHEN_MODULE117'):continue
   if digest(p['module'])!=p['module_hash']:raise ValueError('SERVICE_MODULE_HASH')
   from guest_closure import transformed_rect
   domains=[transformed_rect(q,p['transform'])for name,rs in p['module']['unit']['rooms'].items()if name!='public_access'for q in rs];keys=[p['id_map'][a]for a in p['module']['unit']['activities']];sp={k:paths[k]for k in keys if k in paths}
   covered=[z for q in domains for path in sp.values()for sw in source_sweeps(path,m['profile']['body_m'])if(z:=intersection(q,sw))];route_only=difference(covered,uses)
   declared={k:rs for k,rs in p['module']['unit']['rooms'].items()if k not in('public_access',p['room_id'])}
   service.append({'room':p['room_id'],'source_module_hash':p['module_hash'],'actual_service_required_targets':keys,'route_sweep_area_inside_service_m2':str(union_area(covered)),'route_only_after_actual_fixture_activity_deduction_m2':str(union_area(route_only)),'route_only_regions':[list(map(str,q))for q in route_only],'other_source_role_inventory':declared,'exclusive_service_circulation_status':'UNKNOWN_ROLE_EXCLUSIVITY_NOT_PROVEN_BY_ROOM_NAME_OR_ROUTE_ONLY_AREA','scope':'Route-only bookkeeping excludes fixture/activity/door actor use; full continuous kitchen/bath activity reservation must be reconciled before declaring exclusively circulation.'})
  out['units'].append({'unit':uid,'required_target_inventory':inventory,'untargeted_terminal_extensions':terminal_extensions(private,m,u,paths,uses),'private_margin_operationalization':{'basis':'SOURCE_TRANSVERSE_CLEAR_DEPTH_CROSS_SECTION_AROUND_REQUIRED_PATH_ONLY','source_max_clear_width_m':record['trace']['proposal']['ordered_macro']['private_hall_clear_depth'],'engineering_assumption':'Transverse floor around a verified traversal within the actual source corridor width is a supporting margin; no unsupported longitudinal tail is granted function.','regions':[list(map(str,q))for q in margin]},'private_circulation_components':pc,'entry_circulation_components':ec,'service_inventory':service})
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 from corridor_margin359 import prove as prove_margin
 for unit,row in zip(m['units'],out['units']):
  proof=prove_margin(record,unit,row['private_circulation_components'],req);row['source_connector_margin_proof']=proof
  row['intrinsic_private_role_status']='PASS_SCOPED_SOURCE_WHOLE_CONNECTOR_ROLE'if proof['all_residual_cells_source_bound']and not row['untargeted_terminal_extensions']else'UNKNOWN_SOURCE_COMPONENT_ROLE'
 out['necessity_comparison']='NOT_ASSESSED_HERE_REQUIRES_ELIGIBLE_FINITE_COMPARISON';out['status']='MEASURED_INTRINSIC_COMPONENT_PURPOSE_AND_EXPLICIT_GAPS';return out
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());v=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('circulation_role_actual365.json').write_text(json.dumps(o,indent=2));print([(u['unit'],[(k,[(c['area_m2'],c['unsupported_margin_area_m2'])for c in u[k]])for k in('private_circulation_components','entry_circulation_components')])for u in o['units']])
