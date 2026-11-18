"""Own SERVICE branch finite IR-P13 review; no inherited room equivalence."""
import json,hashlib,time
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent;ROOT=P.parent

def evaluate(record,result):
 out={'rule_id':'BEDROOM_GROUPING','verdict':'UNKNOWN','proofscopecomplete':False,'parent_initial':False,'live_authority':False,'delivery_allowed':False,'new_fresh_execution':False,'missing':[]}
 try:
  pins=json.loads((P/'bedroom_grouping_service365_pins.json').read_text())
  def check():
   for n,h in pins['files'].items():
    if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_OR_ARCHIVE_CHANGED:'+n)
  check()
  from eligibility_intrinsic_service365 import _loader
  load,_=_loader();common=load('common');digest=common.digest
  view=load('group_readsets_service365').build(record,result,source_profile='SOURCE_SERVICE365');m=view['envelope']['packet']['world_model'];raw=view['result']['raw_fresh_report'];rs=common.rows(m,raw)
  for key in ('private_grouping','fixture_inventory_use','door_operation','closet_operation','privacy_scenarios','body_route_sweeps'):
   r=rs[key];w=r['evidence']['witness']
   if r['status']!='PASS_LIMITED'or w.get('errors')or w.get('pending'):raise ValueError('SOURCE_CURRENT_ROOM_PROOF:'+key)
  bundle=load('closure_room_program_service365').bundle_inventory(m,rs)
  own=json.loads((P/'service365_private_actual_v2.json').read_text());routes=own['task_routes']
  if own['model_digest']!=digest(m):raise ValueError('OWN_PRIVATE_MODEL_BINDING')
  installed={(p['unit_id'],p['room_id']):p for p in m['module_placements']if p['room_id'].startswith('bed')}
  if len(installed)!=6 or len(own['rows'])!=6:raise ValueError('SIX_ROOMS_REQUIRED')
  for r in own['rows']:
   p=installed[(r['unit'],r['room'])]
   if r['module_digest']!=digest(p['module'])or r['sections']['module_digest']!=digest(p['module']):raise ValueError('OWN_SOURCE_SECTION_BINDING')
  if len(routes['units'])!=2 or any(len(u['pairs'])!=50 or any(q['verdict']!='PASS_SCOPED_JOINED_TASK_PATH'for q in u['pairs'])for u in routes['units']):raise ValueError('OWN_ALL_TASK_PATHS')
  local=json.loads((ROOT/'local_closet_counterfactual_service365/result.json').read_text());closets=[]
  if len(local['rows'])!=2:raise ValueError('TWO_SOURCE_TYPE_ALTERNATIVES')
  for row in local['rows']:
   rid='bed1'if row['room_type']=='double'else'bed2'if row['room_type']=='twin'else None
   if rid is None:raise ValueError('SOURCE_TYPE')
   h=digest(installed[('A',rid)]['module'])
   if row['derivation']['source_module_digest']!=h:raise ValueError('COUNTERFACTUAL_WRONG_MODULE')
   rays=[e for e in row['privacy_report']['errors']if e['code']=='PRIVATE_TARGET_VISIBLE']
   if not rays or any(e['witness']['state']!='fully_open'for e in rays):raise ValueError('ACTUAL_LOCAL_COUNTEREXAMPLE_REQUIRED')
   closets.append({'source_type':row['room_type'],'source_module_digest':h,'tested_longitudinal_counterexample_rays':rays,'chosen_transverse_reason':'CURRENT_SOURCE_USE_PRIVACY_PASS; TESTED_RIGID_LONGITUDINAL_ALTERNATIVE_BREAKS_BED_PRIVACY','remaining_unknown':row['privacy_report']['pending'],'not_claimed':'NOT_ALL_LONGITUDINAL_PLACEMENTS_INFEASIBLE; OLD_PATH_FAILURE_NOT_GLOBAL_COUNTERPROOF'})
  archive=json.loads((P/'bedroom_route_witness_actual358.json').read_text())['evidence']['members'];comparisons={};units=[]
  for name,a in archive.items():
   if a['program_digest']!=digest(m['program'])or a['profile_digest']!=digest(m['profile']):raise ValueError('ARCHIVE_PROGRAM_PROFILE')
   if set(a['vector'])!=set(routes['vector'])or any(p['verdict']!='PASS_SCOPED_JOINED_TASK_PATH'for u in a['units']for p in u['pairs']):raise ValueError('ARCHIVE_PATH_INVENTORY')
   comparisons[name]={'alternative_model_digest':a['model_digest'],'alternative_raw_digest':a['raw_digest'],'evidence_kind':'BYTE_PINNED_REVIEWED_HISTORICAL_PATH_ARCHIVE_NOT_LIVE_ELIGIBILITY','delta_paths_m':{k:str(F(routes['vector'][k])-F(a['vector'][k]))for k in routes['vector']},'delta_net_room_area_m2':{k:str(F(routes['net_bedroom_area_m2'][k])-F(a['net_bedroom_area_m2'][k]))for k in routes['net_bedroom_area_m2']}}
  for u in m['units']:
   uid=u['id'];alts={}
   for name,c in comparisons.items():
    paths={k:v for k,v in c['delta_paths_m'].items()if k.startswith(uid+'|')};areas={k:v for k,v in c['delta_net_room_area_m2'].items()if k.startswith(uid+'|')}
    alts[name]={'shorter':[k for k,v in paths.items()if F(v)<0],'longer':[k for k,v in paths.items()if F(v)>0],'all_path_deltas_m':paths,'all_room_area_deltas_m2':areas,'area_loss_disclosed':[k for k,v in areas.items()if F(v)<0],'is_nonshrink_repair':False,'averaging':False}
   units.append({'unit':uid,'alternatives':alts,'rationale':'Independent candidate retains same source assets/occupancy and usable private source topology; finite room-area/path tradeoff disclosed, not dominance over larger rooms.'})
  check();out.update(verdict='PASS_SCOPED_REVIEWED_TRADEOFF_PENDING_AUDIT',proofscopecomplete=True,evidence={'model_digest':digest(m),'record_digest':digest(record),'result_digest':digest(result),'bundle_digest':digest(bundle),'private_topology':rs['private_grouping']['evidence']['witness'],'own_sections':own['rows'],'own_task_paths':routes,'closet_rationale':closets,'comparisons':comparisons,'per_unit_tradeoffs':units},scope='IR-P13 FINITE OWN SERVICE BRANCH; SOURCE OPEN_TRANSIT TASKS; TWO LOCAL LONGITUDINAL PROBES; HISTORICAL SAME_PROGRAM PATH COMPARISON; NOT_GLOBAL_OPTIMUM_OR_NONSHRINK_REPAIR',missing=['INDEPENDENT_SCOPE_AUDIT_PENDING'])
 except(ValueError,KeyError,TypeError,IndexError,StopIteration)as e:out['missing']=[str(e)];out['proofscopecomplete']=False
 return out
