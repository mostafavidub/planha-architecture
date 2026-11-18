"""New357 v2 closed room-program join without parent reentry; no fresh execution or delivery authority."""
from pathlib import Path
import json,hashlib,time
from common import digest
from intrinsic_access365 import bound_rows,require_row,need,evaluate as access
from guest_closure390 import transformed_rect
from modules_spatial import rect,difference
from applicability import rliv_applicability
HERE=Path(__file__).resolve().parent;BASE=HERE.parent

def view_for(record,result,profile):
 need(profile=='SOURCE_BALANCED365','UNREGISTERED_PROFILE')
 from groups390 import build
 return build(record,result,source_profile=profile)

def bundle_inventory(m,rs):
 inv=require_row(rs,'fixture_inventory_use');cap=inv['capacity']['evidence'];placement=inv['source_placement']['evidence'];need(not inv['capacity']['errors']and not inv['capacity']['pending']and not inv['source_placement']['errors']and not inv['source_placement']['pending'],'SOURCE_CAPACITY_OR_PLACEMENT_PENDING')
 need(cap['model_hash']==digest(m)and cap['status']=='PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY','ACTUAL_CAPACITY_BINDING')
 for component in inv['fresh_functional_components']:need(component['status']=='PASS_LIMITED'and not component['witness'].get('errors')and not component['witness'].get('pending'),'FUNCTIONAL_COMPONENT_PENDING')
 roles=m['program']['sleep_roles'];need(roles==['double','twin','twin']and m['program']['bedrooms_per_unit']==3,'CURRENT_THREE_BEDROOM_SOURCE_PROGRAM_ONLY')
 need(m['program']['units']==len(m['units']),'UNIT_COUNT');placementkeys=[(p['unit'],p['room'])for p in placement];actualkeys=[(p['unit_id'],p['room_id'])for p in m['module_placements']];need(len(placementkeys)==len(set(placementkeys))and set(placementkeys)==set(actualkeys),'BIDIRECTIONAL_PLACEMENT_INVENTORY')
 closets=[(o['unit'],o['fixture_id'])for o in m['operations']['closets']];need(len(closets)==len(set(closets)),'DUPLICATE_CLOSET');requiredclosets=[];units=[]
 for u in m['units']:
  uid=u['id'];c=[c for c in cap['units']if c['unit']==uid];need(len(c)==1,'CAPACITY_UNIT_INVENTORY');c=c[0];need(c['residents_study']==m['program']['design_occupants_per_unit']==6,'CAPACITY_PROGRAM');need(all(type(c['actual_places'][k])is int and c['actual_places'][k]>=6 for k in('sleeping_places','dining_seats','living_seats')),'REQUIRED_PLACES')
  bednames=sorted(k for k in u['rooms']if k.startswith('bed'));need(bednames==['bed1','bed2','bed3'],'BEDROOM_INVENTORY');bundle=[]
  for room,role in zip(bednames,roles):
   ps=[p for p in m['module_placements']if p['unit_id']==uid and p['room_id']==room];need(len(ps)==1,'REQUIRED_BED_MODULE');p=ps[0];src=p['module'];need(p['module_hash']==digest(src),'MODULE_HASH');need(src['schema']==('PRIVATE_ROOM_MODULE116'if role=='double'else'PRIVATE_TWIN_ROOM_MODULE118'),'REQUIRED_ROLE_SOURCE_SCHEMA')
   witness=next(v for v in placement if(v['unit'],v['room'])==(uid,room));need(witness['module_hash']==p['module_hash']and witness['local_status']=='PASS_MODULE_SCOPED','FRESH_PLACEMENT_WITNESS')
   required=[p['id_map'][k]for k in src['unit']['fixtures']];need(len(required)==len(set(required))and set(required)=={k for k in u['fixtures']if k.startswith(room+'.')},'BIDIRECTIONAL_BED_FIXTURES')
   for k,r in src['unit']['fixtures'].items():need(rect(u['fixtures'][p['id_map'][k]])==transformed_rect(r,p['transform']),'EXACT_SOURCE_FIXTURE_TRANSFORM')
   for k,r in src['unit']['activities'].items():need(rect(u['activities'][p['id_map'][k]])==transformed_rect(r,p['transform']),'EXACT_SOURCE_ACTIVITY_TRANSFORM')
   expected=[transformed_rect(r,p['transform'])for r in src['unit']['rooms']['bed1']];actual=list(map(rect,u['rooms'][room]));need(not difference(actual,expected)and not difference(expected,actual),'SOURCE_CLOSED_BEDROOM_REGION')
   closet=p['id_map']['bed1.closet'];requiredclosets.append((uid,closet));need((uid,closet)in closets,'REQUIRED_CLOSET_OPERATION');bundle.append({'room':room,'role':role,'source_module_hash':p['module_hash'],'fixture_ids':required,'closed_region_source':'SOURCE_PRIVATE_ROOM_PLUS_FRESH_PLACEMENT_DOOR_OPERATION'})
  units.append({'unit':uid,'bedrooms':bundle,'capacity':c})
 need(set(closets)==set(requiredclosets),'EXTRA_OR_MISSING_CLOSET_OPERATION');return units

def evaluate(record,result,source_profile='SOURCE_BALANCED365'):
 out={'rule_id':'ROOM_PROGRAM_CAPACITY','verdict':'UNKNOWN','parent_complete':False,'proofscopecomplete':False,'missing':[],'fresh_executed':False}
 try:
  view=view_for(record,result,source_profile);m=view['envelope']['packet']['world_model'];raw=view['result']['raw_fresh_report'];profile='BASE351'if source_profile=='SOURCE351'else source_profile;rs=bound_rows(m,raw,profile)
  authority=Path(__file__).resolve().parents[2]/'recovered233_rendered/sections.json';data=authority.read_bytes();need(hashlib.sha256(data).hexdigest()==SOURCE233_SHA,'AUTHOR233_SOURCE_PIN');sections=json.loads(data)['sections'];need(all(k in sections for k in('H12','H13','Q01')),'AUTHOR233_REQUIRED_SECTIONS')
  for key in('containment_all_entities','unit_independence','body_route_sweeps','fixture_inventory_use','closet_operation','program_functional_roles','bath_service_operation','kitchen_essential_operation','door_operation','private_grouping','zero_laundry'):require_row(rs,key)
  need(rs['zero_laundry']['evidence']['witness']['forbidden_entities']==[]and rs['zero_laundry']['evidence']['witness']['entity_count']>0,'LAUNDRY_PRESENT_OR_EMPTY_INVENTORY');units=bundle_inventory(m,rs)
  intrinsic=access(m,raw,profile);need(intrinsic['verdict']=='PASS_SCOPED_INTRINSIC_ACCESS','H07_OR_ARRIVAL_INCOMPLETE')
  from primitive390 import evaluate as primitive_evaluate
  quality=primitive_evaluate(m,raw,source_profile=source_profile,post_fresh={'envelope':view['envelope'],'result':view['result'],'groups':view['groups'],'seconds':10})
  closures=quality['source_closures'];need(closures['guest_closure']['verdict']=='PASS_SCOPED_FOUR_SOURCE_GUEST_RELATIONS','GUEST_ACCESS_REQUIRED');need(closures['kitchen_closure']['verdict']=='PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS','KITCHEN_USE_REQUIRED');need(closures['living_closure']['verdict']=='PASS_SCOPED_INTRINSIC_LIVING','LIVING_USE_REQUIRED')
  trigger=rliv_applicability(m);need(trigger['state']=='NOT_APPLICABLE','R_LIV_APPLICABLE_OR_SCOPE_UNKNOWN_REQUIRES_RATIO_AND_TWO_OPTIONS')
  out.update(verdict='PASS_SCOPED_ROOM_PROGRAM_PROOF_PENDING_AUDIT',proofscopecomplete=True,evidence={'model_hash':digest(m),'raw_hash':digest(raw),'source233_sha256':SOURCE233_SHA,'sections':['H12','H13','Q01'],'units':units,'intrinsic_access':intrinsic,'recomputed_closure_digests':{k:digest(v)for k,v in closures.items()},'r_liv':trigger},scope='CURRENT_TWO_UNIT_THREE_BEDROOM_SOURCE_PROGRAM_ONLY; OPTIONAL_FURNISHING_RANKING_UNASSESSED; NO_FULL_12_RULE_OR_DELIVERY_APPROVAL')
 except (ValueError,KeyError,TypeError,IndexError,StopIteration)as e:out['missing']=['ROOM_PROGRAM_CLOSURE:'+str(e)]
 return out

SOURCE233_SHA='98e39063ee7ba733335c450c7fb661b9939762873f19c788d1b0764cb2daf0e3'
