"""Source-profile conceptual clearance diagnostic, never generalized clear width."""
import sys,hashlib,json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'semantic_rules357'))
from modules_spatial import rect,difference,source_sweeps,intersection,digest
from comparison_metrics import route_metrics
from clearance_kernel import maximum_width

def entry_open_scenario(model):
 # Exact source-backed scenario, not simultaneous traversal during movement.
 # Entry actors/closed panels are not silently relabelled absent: their motions
 # remain separate source operation checks. This scenario is fully-open passage.
 panels=[];bindings=[]
 for uid in [u['id']for u in model['units']]:
  ops=[o for o in model['operations']['doors']if o['opening_id']==uid+'.entry']
  if len(ops)!=1:raise ValueError('ENTRY_OPERATION_UNIQUE')
  o=ops[0]
  if o['kind']!='sliding_linear':raise ValueError('UNSUPPORTED_ENTRY_OPERATION')
  closed,opened=rect(o['closed_panel']),rect(o['open_panel']);tx,ty=map(F,o['translation'])
  if (closed[0]+tx,closed[1]+ty,closed[2]+tx,closed[3]+ty)!=opened:raise ValueError('ENTRY_PANEL_TRANSLATION')
  states=[s for s in o['states']if F(s['fraction'])==1]
  if not states or any(rect(s['panel_rect'])!=opened for s in states):raise ValueError('SOURCE_OPEN_STATE_MISSING')
  panels.append({'id':uid+'.entry.FULLY_OPEN_PANEL','rect':list(map(str,opened))});bindings.append({'opening_id':o['opening_id'],'operation_digest':digest(o),'fraction':'1','open_state_digests':[digest(s)for s in states]})
 return panels,bindings

def model_route(model,route_id):
 src,uid=route_id.split('_');u=next(u for u in model['units']if u['id']==uid)
 if src not in ('stair','lift'):raise ValueError('SOURCE_ROUTE_ID')
 path=model['common_routes'][route_id];frame=[0,0,*model['inputs'][:2]];source=model['common_spaces'][src];forbidden=model['common_spaces']['lift'if src=='stair'else'stair'];body=F(model['profile']['body_m'])
 if body<=0:raise ValueError('PROFILE_BODY_REQUIRED')
 sourceports=[o for o in model['openings']if src in o['connects']and'lobby'in o['connects']];destports=[o for o in model['openings']if'lobby'in o['connects']and any(s.startswith(uid+'.')for s in o['connects'])]
 if len(sourceports)!=1 or len(destports)!=1:raise ValueError('UNIQUE_PORTAL_BINDING')
 domain=[rect(source)]+[rect(r)for r in model['common_spaces']['lobby']]+[rect(r)for key in ('entry_circulation','living')for r in u['rooms'][key]]+[rect(o['rect'])for o in sourceports+destports]
 complement=difference([rect(frame)],domain)
 obstacles=[{'id':'FLOOR_COMPLEMENT_'+str(i),'rect':list(map(str,r))}for i,r in enumerate(complement)]
 obstacles += [{'id':'WALL:'+i,'rect':r}for i,r in model['walls'].items()]
 obstacles += [{'id':'FIXTURE:'+v['id']+':'+i,'rect':r}for v in model['units']for i,r in v['fixtures'].items()]
 obstacles += [{'id':'OTHER_UNIT:'+v['id']+':'+str(i),'rect':r}for v in model['units']if v['id']!=uid for i,r in enumerate(v['ownership'])]
 obstacles.append({'id':'FORBIDDEN_CORE','rect':forbidden})
 panels,bindings=entry_open_scenario(model)
 # Match source starting and destination actor anchor obligations at profile size.
 sweeps=source_sweeps(path,body);h=body/2;first=list(map(F,path[0]));last=list(map(F,path[-1]));start=(first[0]-h,first[1]-h,first[0]+h,first[1]+h);end=(last[0]-h,last[1]-h,last[0]+h,last[1]+h)
 if difference([start],[rect(source)])or difference([end],[rect(r)for r in u['rooms']['entry_circulation']]):raise ValueError('SOURCE_POSE_ANCHOR')
 for p in sourceports+destports:
  if not any(intersection(r,rect(p['rect']))for r in sweeps):raise ValueError('PATH_ACTUAL_PORTAL_MISSING')
 static=maximum_width(path,frame,obstacles);opened=maximum_width(path,frame,obstacles+panels)
 limit=F(opened['max_axis_aligned_square_width_m']);epsilon=F(1,10**6)
 # Independent exact region verification at the algebraically derived bound.
 def sweep_valid(w):
  for s in source_sweeps(path,w):
   if difference([s],domain)or any(intersection(s,rect(o['rect']))for o in obstacles+panels):return False
  return True
 if not sweep_valid(limit)or sweep_valid(limit+epsilon):raise ValueError('CRITICAL_WIDTH_INDEPENDENT_RECHECK')
 q=route_metrics(path)
 return {'route_id':route_id,'actual_path':path,'source_domain_digest':digest([[str(v)for v in r]for r in domain]),'obstacle_inventory_digest':digest(obstacles),'obstacle_count':len(obstacles),'architectural_static_fixed_path_square_capacity':static,'fully_open_entry_passage_square_capacity':opened,'scenario_entry_bindings':bindings,'length_m':q['length'],'turns':q['direction_changes'],'profile_body_m':str(body),'profile_feasible_in_declared_scenario':limit>=body,'profile_scaled_width_margin':str((limit-body)/body),'critical_width_recheck':True,'epsilon_exact_m':str(epsilon),'at_bound_valid':True,'above_bound_invalid':True,'unassessed':['Other moving operation states not included in SOURCE_CORE_STATIC_PLUS_FULLY_OPEN_ENTRIES scenario','Hardware/technical stair-lift clearance outside Concept scope'],'not_claimed':['GENERAL_ARCHITECTURAL_CLEAR_WIDTH','BEST_ROUTE_CLEARANCE','ALL_OPERATION_STATES_FEASIBLE','BALANCE_ACCEPTANCE']}

def evaluate(record,review):
 from group_readsets362 import build
 before=digest([record,review]);build(record,review,source_profile='SOURCE362')
 req={r['requirement_id']:r for r in review['raw_report']['rule_contract_evidence']['requirements']}
 for name in ('core_concept','door_operation','wall_network','opening_hosts','partition_ledger'):
  r=req[name]
  if r['status']!='PASS_LIMITED'or r['evidence']['witness'].get('errors')or r['evidence']['witness'].get('pending'):raise ValueError('FRESH_SOURCE_REQUIREMENT:'+name)
 model=record['candidate']['model'];out=[model_route(model,k)for k in sorted(model['common_routes'])]
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'schema':'BALANCE363_EXACT_FIXED_PATH_SQUARE_CLEARANCE','verdict':'MEASURED_LIMITED_CONCEPT_PASSAGE_SCENARIO','model_digest':digest(model),'record_digest':digest(record),'fresh_result_digest':digest(review),'rows':out,'source_guard':'core_wall_audit118.core_concept same domain/blocked inventory plus bound fully-open entry panels','engineering_definition':'Largest axis-aligned square on entire fixed actual centerline; exact L-infinity distance to blocked-domain complement, including corners/endpoints; boundary contact without positive-area overlap allowed. Not universal clear width.','accepted':False,'balance_resolved':False,'new_fresh':False,'generation':False}

_evaluate=evaluate
def evaluate(record,review):
 try:return _evaluate(record,review)
 except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError)as e:
  return {'schema':'BALANCE363_EXACT_FIXED_PATH_SQUARE_CLEARANCE','verdict':'UNKNOWN','reason':type(e).__name__+':'+str(e),'accepted':False,'balance_resolved':False,'new_fresh':False,'generation':False}
