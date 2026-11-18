"""Current registered source role partition, never global exclusive-use proof.
Whole functional rooms include their validated margins. Entry is not itself a
nonservice label. All current declared task/operation roles are joined exactly.
"""
import json
from pathlib import Path
from common import digest
from modules_spatial import rect,intersection,difference,union_area,source_sweeps
from role_registry_joint367 import evaluate as roles
ROOT=Path(__file__).resolve().parents[1]
def clips(a,b):return[z for x in a for y in b if(z:=intersection(x,y))]
def linear(a,b):
 a,b=rect(a),rect(b)
 if a[2]-a[0]!=b[2]-b[0]or a[3]-a[1]!=b[3]-b[1]or(a[0]!=b[0]and a[1]!=b[1]):raise ValueError('UNSUPPORTED_NONLINEAR_OR_CHANGING_RECT')
 return(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))
def partition(entry,service,nonservice,inventory_complete):
 if not inventory_complete:raise ValueError('CLOSED_CURRENT_ROLE_INVENTORY_REQUIRED')
 s=clips(entry,service);n=clips(entry,nonservice);shared=clips(s,n);exclusive=difference(s,n);other=difference(n,s);unknown=difference(entry,s+n)
 if union_area(exclusive+shared+other+unknown)!=union_area(entry):raise ValueError('PARTITION_COVERAGE')
 return {'exclusive_current_profile_m2':str(union_area(exclusive)),'shared_current_profile_m2':str(union_area(shared)),'nonservice_current_profile_m2':str(union_area(other)),'unclassified_m2':str(union_area(unknown)),'regions':{k:[list(map(str,q))for q in v]for k,v in [('exclusive_current_profile',exclusive),('shared',shared),('nonservice',other),('unclassified',unknown)]}}
def nonservice_inventory(m,u,serviceids):
 uid=u['id'];out={};body=m['profile']['body_m']
 bath=next(p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath');bathdoors={bath['id_map'][x['id']]for x in bath['module']['openings']}
 if set(u['rooms'])!={'bed1','bed2','bed3','bath','kitchen','dining','private_circulation','entry_circulation','living'}:raise ValueError('UNCLASSIFIED_ROOM_ROLE')
 if set(m['operations'])!={'doors','closets','kitchen','dining_chairs'}:raise ValueError('UNCLASSIFIED_OPERATION_KIND')
 for k,v in u['rooms'].items():
  if k not in('bath','entry_circulation'):out['whole_room:'+k]=list(map(rect,v))
 for k,v in u['activities'].items():
  if k not in serviceids:out['activity:'+k]=[rect(v)]
 paths={**u['routes'],**{'scenario:'+k:v for k,v in u['scenario_routes'].items()}}
 for k,v in paths.items():
  if k not in serviceids:out['required_path:'+k]=list(source_sweeps(v,body))
 for op in m['operations']['doors']:
  if op['opening_id'] in bathdoors:continue
  if not any(t.get('unit')==uid for t in op['states']):continue
  qs=[linear(op['closed_panel'],op['open_panel']),rect(op['rail_envelope'])]
  qs +=[rect(t['actor_rect'])for t in op['states']if t.get('unit')==uid]
  qs +=[linear(t['actor_start'],t['actor_end'])for t in op['continuous_actor_segments']if t.get('unit')==uid]
  out['door_operation:'+op['opening_id']]=qs
 for op in m['operations']['closets']:
  if op['unit']!=uid:continue
  qs=list(map(rect,op['shell_rects']))
  for p in op['panels']:
   qs +=[linear(p['closed_panel'],p['open_panel']),rect(p['rail_envelope'])]+[rect(t['actor_rect'])for t in p['states']]+[linear(t['actor_start'],t['actor_end'])for t in p['continuous_actor_segments']]
  out['closet_operation:'+op['fixture_id']]=qs
 for op in m['operations']['kitchen']:
  if op['unit']==uid:
   if not op['motion_envelopes']:raise ValueError('KITCHEN_ENVELOPES_MISSING')
   out['kitchen_operation']=list(map(rect,op['motion_envelopes']))
 for op in m['operations']['dining_chairs']:
  if op['unit']==uid:out['dining_operation:'+op['fixture_id']]=[rect(op['occupied_body']),linear(op['closed_rect'],op['open_rect'])]+list(source_sweeps(op['egress_route'],body))
 for p in u['public_program']['capacity']['living_seats']:out['living_occupied:'+p['id']]=[rect(p['occupied_body'])]
 # Whole source rooms already include fixture footprints; keep standalone
 # actual fixtures explicitly, with source bath IDs excluded.
 bath=next(p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath');bathfixtures={bath['id_map'][k]for k in bath['module']['unit']['fixtures']}
 for k,q in u['fixtures'].items():
  if k not in bathfixtures:out['fixture:'+k]=[rect(q)]
 return out

def evaluate(record,review):
 before=digest([record,review]);m=record['candidate']['model'];out={'schema':'JOINT367_CLOSED_CURRENT_SOURCE_SERVICE_ROLE_PARTITION','model_digest':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'verdict':'UNKNOWN','remaining':[],'global_exclusive_function_m2':None,'units':[],'accepted':False,'new_fresh_execution':False}
 try:
  registry=roles(record,review)
  for node in('SOURCE_ROOM_USE','PUBLIC_SUPPORT','PRIVATE_CIRCULATION','COMMON_ROLE','ENTRY_CIRCULATION'):
   if not registry['nodes'][node]['status'].startswith('PASS_'):raise ValueError('CURRENT_ROLE_PREREQUISITE:'+node)
  for u in m['units']:
   uid=u['id'];p=next(p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath');ids={p['id_map'][k]for k in p['module']['unit']['activities']}
   if not ids<=set(u['activities']):raise ValueError('SERVICE_TASK_INVENTORY')
   entry=list(map(rect,u['rooms']['entry_circulation']));service=[q for k in ids for q in source_sweeps(u['routes'][k],m['profile']['body_m'])];inventory=nonservice_inventory(m,u,ids);nonservice=[q for v in inventory.values()for q in v]
   part=partition(entry,service,nonservice,True)
   prior=next(x for x in registry['nodes']['ENTRY_CIRCULATION']['evidence']['units']if x['unit']==uid)
   part.update(unit=uid,service_target_ids=sorted(ids),source_bath_module_hash=p['module_hash'],whole_entry_area_m2=str(union_area(entry)),route_only_measurement_m2=prior['current_source_service_only_route_area_m2'],route_only_outside_approach_m2=prior['service_only_outside_source_approach_m2'],nonservice_inventory={k:{'regions':[list(map(str,q))for q in v],'geometry_digest':digest([list(map(str,q))for q in v]),'service_path_intersection_m2':str(union_area(clips(clips(entry,service),v)))}for k,v in inventory.items()})
   if part['unclassified_m2']!='0':out['remaining'].append(uid+':UNCLASSIFIED_CURRENT_ROLE_CELLS')
   out['units'].append(part)
  out['role_prerequisite_digests']={k:digest(registry['nodes'][k])for k in('SOURCE_ROOM_USE','PUBLIC_SUPPORT','PRIVATE_CIRCULATION','COMMON_ROLE','ENTRY_CIRCULATION')}
  out['verdict']='PASS_SCOPED_CURRENT_SOURCE_ROLE_PARTITION'if not out['remaining']else'UNKNOWN'
 except (ValueError,KeyError,TypeError,IndexError)as e:out['remaining'].append(str(e))
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 out['scope']='Exclusive only among this fixed registered source room/task/scenario/operation inventory. Whole operational room margins retained; entry label and body reachability are not nonservice roles. Includes source bath approach. Kitchen conservative motion envelopes may only reduce the exclusive metric. Not global exclusive use, necessity or wholequality.'
 return out
if __name__=='__main__':
 r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('service_role_inventory_joint_actual367.json').write_text(json.dumps(o,indent=2));print(o['verdict'],o['remaining'],[(x['unit'],x['exclusive_current_profile_m2'])for x in o['units']])
