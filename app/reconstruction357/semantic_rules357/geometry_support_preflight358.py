"""Candidate geometry only. No prior fresh witness reused or implied."""
import json,time
from pathlib import Path
from common import digest
from supporting_floor import analyze
from modules_spatial import rect,intersection,union_area,difference
from door_reservations import derive
from unsupported_extent_causes357 import evaluate as causes

def evaluate(model,seconds=25):
 start=time.monotonic();o={'schema':'GEOMETRY_SUPPORT_PREFLIGHT358_NOT_FUNCTIONAL_REVIEW','model_hash':digest(model),'rows':[],'source_use_verified':False,'parent_complete':False,'admission_allowed':False,'fresh_execution':False}
 try:
  for u in model['units']:
   role=u['spatial_role_bindings']['living_activity_group'];anchors=[u['routes'][k][-1]for k in role['access_route_ids']];obs=list(model['walls'].values())+list(u['fixtures'].values())+[q for k,rs in u['rooms'].items()if k.startswith('bed')or k in('bath','kitchen','private_circulation')for q in rs]
   obs +=[op['open_panel']for op in model['operations']['doors']]
   for op in model['operations']['kitchen']:
    if op['unit']==u['id']:obs+=op.get('motion_envelopes',[])
   for op in model['operations']['dining_chairs']:
    if op['unit']==u['id']:
     obs.append(op['occupied_body']);a,b=rect(op['closed_rect']),rect(op['open_rect']);obs.append(list(map(str,[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])])))
   obs +=[seat['occupied_body']for seat in u['public_program']['capacity']['living_seats']]
   r=analyze(u['ownership'],obs,anchors,model['profile']['body_m'],seconds=min(12,seconds-(time.monotonic()-start)))
   target=list(map(rect,u['rooms']['living']));cover=list(map(rect,r.get('support_regions',[])))+[rect(u['fixtures'][k])for k in role['fixture_ids']]+[rect(u['activities'][k])for k in role['activity_ids']]
   for op in model['operations']['doors']:
    if not any(st.get('unit')==u['id']for st in op.get('states',[])):continue
    cover +=[rect(op[k])for k in('closed_panel','open_panel','rail_envelope')if k in op]+[rect(st['actor_rect'])for st in op['states']if st['unit']==u['id']]
    for st in op.get('continuous_actor_segments',[]):
     if st['unit']==u['id']:
      a,b=rect(st['actor_start']),rect(st['actor_end'])
      if a[0]==b[0]or a[1]==b[1]:cover.append((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])))
   cover +=[rect(s['occupied_body'])for s in u['public_program']['capacity']['living_seats']]+[rect(t['rect'])for t in model['threshold_ownership']['allocations']if t.get('owner')=='unit:'+u['id']]+[rect(op['rect'])for op in model['openings']if any(x.startswith(u['id']+'.')for x in op.get('connects',[]))]
   reservations=derive(model,u['id']);cover +=[rect(x['region'])for x in reservations];rem=difference(target,cover)
   o['rows'].append({'unit':u['id'],'body_geometry':r,'unresolved_area_m2':str(union_area(rem)),'unresolved_regions':[list(map(str,q))for q in rem],'candidate_declared_reservations':reservations,'functional_validity':'NOT_ASSESSED_REQUIRES_THIS_MODEL_FRESH'})
  o['status']='GEOMETRY_MEASURED_NOT_ACCEPTED';o['causes']=causes(model,o)
 except (ValueError,KeyError,TypeError,IndexError)as e:o.update(status='INCOMPLETE_GEOMETRY_STUDY',missing=[str(e)])
 return o
if __name__=='__main__':
 p=Path(__file__).resolve().parents[1];record=json.loads((p/'staging358_comparative/row_candidate358.json').read_text());o=evaluate(record['candidate']['model']);Path(__file__).with_name('geometry_support_preflight_actual358.json').write_text(json.dumps(o,indent=2));print(o['status'],[(r['unit'],r['unresolved_area_m2'])for r in o['rows']])
