"""Fixed-artifact IR-P13 paths via exact shared entry; no shortest-path claim."""
import json,hashlib,time
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,source_sweeps,intersection,union_area,difference
from bedroom_grouping358 import compare
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def point(p):
 if type(p)is not list or len(p)!=2 or any(type(x)not in(str,int)for x in p):raise ValueError('EXACT_POINT')
 return tuple(map(F,p))
def via_entry(bedpath,destination):
 if len(bedpath)<2 or not destination or point(bedpath[0])!=point(destination[0]):raise ValueError('SAME_ENTRY_ROOT_REQUIRED')
 return list(reversed(bedpath))+destination[1:]
def check_leg(path,body,floor,obstacles,deadline):
 collisions=[];uncovered=[]
 for i,s in enumerate(source_sweeps(path,body)):
  if time.monotonic()>deadline:raise ValueError('ROUTE_DEADLINE')
  if difference([s],floor):uncovered.append(i)
  for label,r in obstacles:
   if (q:=intersection(s,r)):collisions.append({'segment':i,'obstacle':label,'overlap':list(map(str,q))})
 return {'verdict':'PASS_SCOPED_TASK_PATH'if not collisions and not uncovered else'UNKNOWN_STORED_PATH_BLOCKED_NOT_INFEASIBLE','collisions':collisions,'uncovered':uncovered,'path_digest':digest(path)}
def validate_model(m,deadline):
 body=F(m['profile']['body_m'])
 if body!=F('.7'):raise ValueError('SOURCE_BODY_PROFILE')
 unitrows=[];vector={};areas={}
 fixed=[('wall:'+k,rect(r))for k,r in m['walls'].items()]+[('open_panel:'+o['opening_id'],rect(o['open_panel']))for o in m['operations']['doors']]
 fixtures=[(u['id']+'.fixture:'+k,rect(r))for u in m['units']for k,r in u['fixtures'].items()]
 for u in m['units']:
  uid=u['id'];floor=[rect(r)for r in u['ownership']];routes=u['routes'];root=point(u['entry_point'])
  beds={k:p for k,p in routes.items()if k.startswith('bed')and k.endswith(('bed_front','bedA_front','bedB_front'))}
  required=['WC_front','shower_use','basin_front']+u['spatial_role_bindings']['living_activity_group']['access_route_ids']
  destinations={'entry':[u['entry_point']],**{k:routes[k]for k in required}}
  if len(required)!=len(set(required))or not beds:raise ValueError('TARGET_INVENTORY')
  allbed=[(k,rect(r))for k,rs in u['rooms'].items()if k.startswith('bed')for r in rs]
  otherowners=[('other_owner:'+v['id'],rect(r))for v in m['units']if v['id']!=uid for r in v['ownership']]
  otherprivate=[('private_other_unit:'+v['unit'],rect(r))for v in m['private_domains']if v['unit']!=uid for r in v['parts']]
  walls=[rect(r)for r in m['walls'].values()]
  for name,rs in u['rooms'].items():
   if name.startswith('bed'):areas[uid+'|'+name]=str(union_area(difference([rect(r)for r in rs],walls)))
  legs={};pairs=[]
  for b,path in beds.items():
   if point(path[0])!=root or point(path[-1])!=point(u['route_targets'][b]):raise ValueError('BED_ENDPOINT_BINDING')
   room=b.split('.')[0]
   obs=fixed+fixtures+otherowners+otherprivate+[('other_bedroom:'+k,r)for k,r in allbed if k!=room]
   legs['bed:'+b]=check_leg(path,body,floor,obs,deadline)
  for t,path in destinations.items():
   if point(path[0])!=root:raise ValueError('DESTINATION_ROOT')
   if t!='entry'and point(path[-1])!=point(u['route_targets'][t]):raise ValueError('DESTINATION_ENDPOINT_BINDING')
   fx=fixtures;exception=None
   if t=='shower_use':
    ps=[p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath']
    if len(ps)!=1:raise ValueError('SHOWER_MODULE_INVENTORY')
    p=ps[0]
    from guest_closure import transformed_rect
    if p['module_hash']!=digest(p['module'])or p['module']['schema']!='BATHROOM_MODULE117':raise ValueError('SHOWER_SOURCE')
    fid=p['id_map']['shower_floor']
    if rect(u['fixtures'][fid])!=transformed_rect(p['module']['unit']['fixtures']['shower_floor'],p['transform']):raise ValueError('SHOWER_FIXTURE_BINDING')
    if rect(u['activities'][t])!=transformed_rect(p['module']['unit']['activities'][t],p['transform']):raise ValueError('SHOWER_TASK_BINDING')
    exception=uid+'.fixture:'+fid;fx=[(k,r)for k,r in fixtures if k!=exception]
   obs=fixed+fx+otherowners+otherprivate+[('forbidden_bedroom:'+k,r)for k,r in allbed]
   # Entry pose checked as a degenerate orthogonal sweep, never omitted.
   q=path if len(path)>1 else path+path
   legs['destination:'+t]=check_leg(q,body,floor,obs,deadline);legs['destination:'+t]['task_only_exception']=exception
  for b,bp in beds.items():
   for t,dp in destinations.items():
    path=via_entry(bp,dp);length=sum(abs(a-b)for p,q in zip(path,path[1:])for a,b in zip(point(p),point(q)))
    ok=legs['bed:'+b]['verdict']=='PASS_SCOPED_TASK_PATH'and legs['destination:'+t]['verdict']=='PASS_SCOPED_TASK_PATH'
    key=uid+'|'+b+'|'+t;vector[key]=str(length)if ok else None
    pairs.append({'bed_target':b,'destination':t,'path':path,'length_m':str(length),'verdict':'PASS_SCOPED_JOINED_TASK_PATH'if ok else'UNKNOWN_LEG_UNPROVEN','leg_ids':['bed:'+b,'destination:'+t],'scenario':'SOURCE_BODY_0.7_OPEN_TRANSIT; NO_OTHER_BEDROOM_OR_OTHER_UNIT; SHOWER_FLOOR_EXCEPTION_ON_DESTINATION_LEG_ONLY'})
  unitrows.append({'unit':uid,'legs':legs,'pairs':pairs})
 return {'units':unitrows,'vector':vector,'net_bedroom_area_m2':areas,'scope':'CONCATENATED_EXISTING_SOURCE_PATHS_VIA_ENTRY_NOT_SHORTEST; NO_OCCUPIED_SEAT_OR_SIMULTANEOUS_KITCHEN_SCENARIO_CLAIM'}

def evaluate(seconds=30):
 out={'rule_id':'BEDROOM_GROUPING','verdict':'UNKNOWN','parent_initial':False,'live_authority':False,'delivery_allowed':False,'new_fresh_execution':False,'missing':[]}
 try:
  if type(seconds)not in(int,float)or not 0<seconds<=30:raise ValueError('BOUNDED_SECONDS')
  start=time.monotonic();deadline=start+seconds;pins=json.loads((HERE/'bedroom_route_witness358_pins.json').read_text())
  for n,h in pins['files'].items():
   if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_PIN:'+n)
  cohort=json.loads((HERE/'bedroom_grouping358_pins.json').read_text());members={}
  import eligibility_intrinsic357_v2 as old
  import eligibility_intrinsic358 as new
  for name,paths in cohort['members'].items():
   record=json.loads((ROOT/paths['record']).read_text());review=json.loads((ROOT/paths['review']).read_text())
   if name=='baseline351':record=record['selected'][0];review=review['central_fresh_reviews'][0]
   if name=='row358':load,_=new._loader();view=load('group_readsets358').build(record,review,source_profile='SOURCE358')
   else:profile='SOURCE351'if name=='baseline351'else'SOURCE_IDENTITY357';load,p=old._loader(profile);view=old._view(record,review,profile,load,p)
   m=view['envelope']['packet']['world_model'];raw=view['result']['raw_fresh_report'];rs=load('common').rows(m,raw)
   for k in('body_route_sweeps','private_grouping','door_operation','fixture_inventory_use'):
    if rs[k]['status']!='PASS_LIMITED'or rs[k]['evidence']['witness'].get('errors')or rs[k]['evidence']['witness'].get('pending'):raise ValueError('SOURCE_ROUTE_PREREQUISITE:'+k)
   eligibility=json.loads((ROOT/paths['eligibility']).read_text())
   if eligibility['verdict']!='PASS'or eligibility['evidence']['model_digest']!=digest(m):raise ValueError('MODEL_ELIGIBILITY')
   measured=validate_model(m,deadline);measured.update(model_digest=digest(m),raw_digest=digest(raw),program_digest=digest(m['program']),profile_digest=digest(m['profile']));members[name]=measured
  if len({v['program_digest']for v in members.values()})!=1 or len({v['profile_digest']for v in members.values()})!=1:raise ValueError('COHORT_PROGRAM_PROFILE')
  comparisons={};area_comparisons={}
  for name in('baseline351','translated357'):
   try:comparisons[name]=compare(members['row358']['vector'],members[name]['vector'])
   except ValueError as e:comparisons[name]={'verdict':'UNKNOWN','reason':str(e)};out['missing'].append('VALIDATED_TASK_ROUTE_COVERAGE:'+name)
   a=members['row358']['net_bedroom_area_m2'];b=members[name]['net_bedroom_area_m2']
   if set(a)!=set(b):raise ValueError('PROTECTED_ROOM_INVENTORY')
   area_comparisons[name]={k:{'selected':a[k],'alternative':b[k],'selected_minus_alternative':str(F(a[k])-F(b[k])),'no_shrink':F(a[k])>=F(b[k])}for k in a}
  local=json.loads((ROOT/'local_closet_counterfactual358/classified_result.json').read_text())
  reasons=[{'type':r['type'],'privacy_counterexample_count':len(r['independent_actual_privacy_counterexamples']),'scope':'ONLY_TESTED_LONGITUDINAL_PLACEMENT; OTHER_PLACEMENTS_UNASSESSED'}for r in local['cases']]
  out['evidence']={'members':members,'task_route_comparisons':comparisons,'protected_room_area_comparisons':area_comparisons,'local_closet_functional_reasons':reasons,'sections_reference':'local_closet_counterfactual358/result.json; limited reservation-union sections, not all joint door actor states','rationale_scope':'SOURCE_USABLE_BUNDLES_RETAINED; PRIVACY_COUNTEREXAMPLES_REJECT_TWO_TESTED_ALTERNATIVES; PER_UNIT_ROUTE_AND_ROOM_AREA_TRADEOFFS_NO_AVERAGING'}
  out['missing']+=['INDEPENDENT_SCOPE_AUDIT_BEFORE_PARENT_DECISION','OTHER_CLOSET_PLACEMENTS_AND_UNMODELED_JOINT_SCENARIOS_NOT_PROVEN']
  for n,h in pins['files'].items():
   if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED_AFTER')
  out['elapsed_seconds']=time.monotonic()-start
 except (ValueError,KeyError,TypeError,IndexError,StopIteration,ZeroDivisionError,FileNotFoundError)as e:out['missing'].append(str(e))
 return out
