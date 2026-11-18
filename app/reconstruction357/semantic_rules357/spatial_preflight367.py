"""Source-joint367 read-only geometry inventory before its own fresh review.
Every result is diagnostic; no old source verdict or role closure is reused.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,intersection,difference,union_area,source_sweeps
from supporting_floor import analyze
from door_reservations import derive
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record):
 t=record['trace'];m=record['candidate']['model']
 if t['schema']!='SOURCE_SERVICE_JOINT367_TRACE_V1'or t['model_digest']!=digest(m)or t['candidate_digest']!=digest(record['candidate']):raise ValueError('JOINT367_BINDING')
 for p,h in t['source_inventory'].items():
  if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_DRIFT:'+p)
 data=(ROOT/'staging365_service_grammar/candidate365.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!='8807b7f2e8ba841d8e1a38ba6787f72161c9d04f64d69e71112859be92976ad9':raise ValueError('PARENT_RECORD')
 before=json.loads(data)
 if digest(before)!=t['parent_record_digest']:raise ValueError('PARENT_TRACE')
 bm=before['candidate']['model'];routes=[]
 for k,path in m['common_routes'].items():
  pts=[list(map(F,p))for p in path];length=sum(abs(a[0]-b[0])+abs(a[1]-b[1])for a,b in zip(pts,pts[1:]));dirs=[(1 if b[0]>a[0]else-1,0)if a[1]==b[1]else(0,1 if b[1]>a[1]else-1)for a,b in zip(pts,pts[1:])if a!=b];routes.append({'id':k,'length_m':str(length),'turns':sum(a!=b for a,b in zip(dirs,dirs[1:])),'path_digest':digest(path)})
 units=[]
 for u in m['units']:
  uid=u['id'];old=next(v for v in bm['units']if v['id']==uid);role=u['spatial_role_bindings']['living_activity_group'];anchors=[u['routes'][k][-1]for k in role['access_route_ids']]
  obs=list(m['walls'].values())+list(u['fixtures'].values())+[q for k,rs in u['rooms'].items()if k.startswith('bed')or k in('bath','kitchen','private_circulation')for q in rs]+[op['open_panel']for op in m['operations']['doors']]
  for op in m['operations']['kitchen']:
   if op['unit']==uid:obs+=op['motion_envelopes']
  for op in m['operations']['dining_chairs']:
   if op['unit']==uid:
    a,b=rect(op['closed_rect']),rect(op['open_rect']);obs +=[op['occupied_body'],list(map(str,(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))))]
  obs += [seat['occupied_body']for seat in u['public_program']['capacity']['living_seats']]
  body=analyze(u['ownership'],obs,anchors,m['profile']['body_m'],seconds=12)
  instances=[rect(u['fixtures'][k])for k in role['fixture_ids']]+[rect(u['activities'][k])for k in role['activity_ids']];ops=[]
  for op in m['operations']['doors']:
   if not op['opening_id'].startswith(uid+'.'):continue
   ops +=[rect(op[k])for k in ('closed_panel','open_panel','rail_envelope')if k in op]
   ops +=[rect(st['actor_rect'])for st in op['states']if st['unit']==uid]
   for st in op['continuous_actor_segments']:
    if st['unit']==uid:
     a,b=rect(st['actor_start']),rect(st['actor_end']);ops.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
  ops +=[rect(s['occupied_body'])for s in u['public_program']['capacity']['living_seats']]+[rect(x['rect'])for x in m['threshold_ownership']['allocations']if x.get('owner')=='unit:'+uid]
  ops +=[rect(o['rect'])for o in m['openings']if any(x.startswith(uid+'.')for x in o.get('connects',[]))]
  reservations=derive(m,uid);ops +=[rect(x['region'])for x in reservations]
  target=list(map(rect,u['rooms']['living']));rem=difference(target,list(map(rect,body.get('support_regions',[])))+instances+ops)
  units.append({'unit':uid,'protected_program_assets_equal':all(digest(u[k])==digest(old[k])for k in ('fixtures','fixture_metadata','activities','dining_module_placement','public_program')),'fixed_room_geometry_equal':{k:digest(u['rooms'][k])==digest(old['rooms'][k])for k in old['rooms']if k not in('living','entry_circulation','private_circulation')},'ownership_added_m2':str(union_area(list(map(rect,u['ownership'])))-union_area(list(map(rect,old['ownership'])))),'private_floor_m2':str(union_area(list(map(rect,u['rooms']['private_circulation'])))),'branch_end_wall':m['walls'][uid+'.private_branch146.branch_end'],'body_geometry_study':body,'public_target_area_m2':str(union_area(target)),'geometry_uncovered_area_m2':str(union_area(rem)),'geometry_uncovered_regions':[list(map(str,q))for q in rem],'own_fresh_functional_prerequisites':'NOT_YET_AVAILABLE_NO_ROLE_VERDICT'})
 return {'schema':'JOINT367_PRE_FRESH_SPATIAL_GEOMETRY_INVENTORY','model_digest':digest(m),'record_digest':digest(record),'common_lobby_regions':m['common_spaces']['lobby'],'common_lobby_area_m2':str(union_area(list(map(rect,m['common_spaces']['lobby'])))),'common_route_geometry':routes,'units':units,'required_new_helpers':['SOURCE_JOINT367 gate/method registry','Source367 constructor/notch/private-end wall origin adapter','Own COMMON route/entry-motion and clear-interior closure','Own living/guest/body/room functional prerequisites','Own private portal margin and service-entry role/cost','Own finite Q04/SERVICE and selected-set assessment'],'fresh_execution':False,'parent_complete':False,'admission_allowed':False,'scope':'Geometry and source identity only; even zero uncovered area is not a functional-role PASS without this model own fresh required checks.'}
if __name__=='__main__':print(json.dumps(evaluate(json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text())),indent=2))
