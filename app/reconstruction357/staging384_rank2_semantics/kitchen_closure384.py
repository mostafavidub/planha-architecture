"""New357 kitchen source-operation and endpoint closure, not parent Q07 approval.
No author233 applicability, ranking waiver, or historical353 verdict is assumed.
"""
import time
from fractions import Fraction as F
from common import rows,digest
from guest_closure384 import evaluate as guest,point
from modules_spatial import rect,intersection,union_area,source_sweeps
from comparison_metrics import route_metrics

def evaluate(envelope,result,groups,seconds=8):
 start=time.monotonic();out={'rule_id':'KITCHEN_PROXIMITY','verdict':'UNKNOWN','parent_complete':False,'evidence':{},'missing':[]}
 def need(ok,code):
  if not ok:raise ValueError(code)
 try:
  need(type(seconds)in(int,float)and 0<seconds<=10,'BOUNDED_BUDGET');before=digest([envelope,result,groups]);m=envelope['packet']['world_model'];rs=rows(m,result['raw_fresh_report']);h=digest(m)
  g=guest(envelope,result,groups,min(seconds,8));need(g['verdict']=='PASS_SCOPED_FOUR_SOURCE_GUEST_RELATIONS','SOURCE_GUEST_PRIVATE_RELATIONS')
  for name in('kitchen_essential_operation','serving_route','body_route_sweeps'):
   need(rs[name]['status']=='PASS_LIMITED'and rs[name]['evidence']['status']=='PASS_LIMITED','SOURCE_REQUIRED_SUBCONDITION:'+name)
  kw=rs['kitchen_essential_operation']['evidence']['witness'];sw=rs['serving_route']['evidence']['witness'];uids=[u['id']for u in m['units']]
  need(len(uids)==len(set(uids))and bool(uids),'UNIT_INVENTORY');need(kw['model_hash']==h and kw['operation_component']=='kitchen'and kw['errors']==[]and kw['pending']==[],'SOURCE_KITCHEN_OPERATION')
  need(set(kw['actual_operation_ids'])==set(uids)and len(kw['actual_operation_ids'])==len(uids),'OPERATION_ID_INVENTORY');need(sw['model_hash']==h and sw['status']=='PASS_PUBLIC_SCOPED'and sw['errors']==[]and sw['pending']==[],'SOURCE_SERVING')
  ops=m['operations']['kitchen'];need(len(ops)==len(uids)and {k['unit']for k in ops}==set(uids),'ACTUAL_KITCHEN_INVENTORY');body=F(m['profile']['body_m']);need(body==F('.7'),'CURRENT_REFERENCE113_BODY')
  measured=[]
  for u in m['units']:
   need(time.monotonic()-start<seconds,'CLOSURE_DEADLINE');uid=u['id'];op=next(k for k in ops if k['unit']==uid)
   need(op['profile']=='REFERENCE113_ESSENTIAL_KITCHEN_V1','SOURCE_KITCHEN_PROFILE');need(point(op['access_point'])==point(op['workpoint']),'SOURCE_WORKPOINT_ACCESS_BINDING')
   service=u['scenario_routes']['kitchen_to_dining_floor'];work=u['routes']['kitchen_work'];living=u['scenario_routes']['guest_living'];dining=u['scenario_routes']['guest_dining']
   need(point(service[0])==point(work[-1])==point(op['workpoint']),'SOURCE_KITCHEN_ORIGIN');need(point(work[0])==point(living[0])==point(u['entry_point']),'SOURCE_ENTRY_ROOT')
   need(u['public_program']['destinations']['kitchen_to_dining_floor']==u['public_program']['destinations']['guest_dining']and point(service[-1])==point(dining[-1]),'SOURCE_DINING_TARGET')
   sr=[r for r in sw['routes']if r['unit']==uid and r['route']=='kitchen_to_dining_floor'];need(len(sr)==1 and sr[0]['all_occupied_chair_motion_included']is True and F(sr[0]['body_width'])==body,'SOURCE_SERVING_SCENARIO')
   paths={'kitchen_to_dining':service,'kitchen_to_living_via_entry':list(reversed(work))+living[1:]};owner=[rect(r)for r in u['ownership']]
   obs=[('wall:'+k,rect(r))for k,r in m['walls'].items()]+[(v['id']+'.fixture:'+k,rect(r))for v in m['units']for k,r in v['fixtures'].items()]
   obs += [('door_open:'+o['opening_id'],rect(o['open_panel']))for o in m['operations']['doors']]
   obs += [('private:'+k,rect(r))for k,v in u['rooms'].items()if k.startswith('bed')or k in('private_circulation','bath')for r in v]
   for relation,path in paths.items():
    collisions=[]
    for i,s in enumerate(source_sweeps(path,body)):
     need(time.monotonic()-start<seconds,'CLOSURE_DEADLINE');need(union_area([z for r in owner if(z:=intersection(s,r))])==union_area([s]),'SOURCE_PATH_OWNERSHIP')
     for name,r in obs:
      if(z:=intersection(s,r)):collisions.append({'segment':i,'obstacle':name,'intersection':list(map(str,z))})
    measured.append({'unit':uid,'relation':relation,'metrics':route_metrics(path),'verdict':'PASS_SCOPED_PATH'if not collisions else'UNKNOWN_PATH_BLOCKED_NOT_GLOBAL_INFEASIBILITY','collisions':collisions,'scenario':'SOURCE_ESSENTIAL_SEQUENTIAL_USE; OPEN_TRANSIT_DOORS; SOURCE_SERVING_CHAIRS_CHECK_SEPARATE','body_m':str(body)})
  need(digest([envelope,result,groups])==before,'INPUT_MUTATION');rows(m,result['raw_fresh_report']);ready=all(r['verdict']=='PASS_SCOPED_PATH'for r in measured)
  out.update(verdict='PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS'if ready else'UNKNOWN',evidence={'model_hash':h,'fresh_digest':digest(result),'source_guest_closure_digest':digest(g),'row_hashes':{k:digest(rs[k])for k in('kitchen_essential_operation','serving_route','body_route_sweeps')},'relations':measured},missing=['AUTHOR233_ESSENTIAL_SCOPE_AND_COMPARATIVE_APPLICABILITY_AUDIT_PENDING']if ready else['ACTUAL_KITCHEN_RELATION_CLOSURE_INCOMPLETE'],scope='REFERENCE113_ESSENTIAL_OPERATION_AND_SOURCE_ENDPOINT_RELATIONS_ONLY',optional_ranking={'disposition':'UNASSESSED_AUTHOR233_PENDING','not_claimed':'NO_GLOBAL_PROXIMITY_OPTIMUM_OR_WAIVER'})
 except(ValueError,KeyError,TypeError,IndexError,StopIteration)as e:out['missing']=['CLOSURE_BLOCKED:'+str(e)]
 out['elapsed_seconds']=time.monotonic()-start;return out
