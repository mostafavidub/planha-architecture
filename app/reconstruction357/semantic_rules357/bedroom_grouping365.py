"""IR-P13 finite reviewed tradeoff on fixed SOURCE_BALANCED365 artifact, not optimum."""
import json,hashlib,time,types,builtins
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,intersection,difference,union_area
from bedroom_route_witness358 import validate_model
from bedroom_grouping358 import compare
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent


def _loader():
 pins=json.loads((HERE/'bedroom_grouping365_pins.json').read_text())['files'];loaded={}
 def load(name):
  if name in loaded:return loaded[name]
  key='semantic_rules357/'+name+'.py';data=(HERE/(name+'.py')).read_bytes()
  if hashlib.sha256(data).hexdigest()!=pins.get(key):raise ValueError('COMPONENT_CHANGED:'+name)
  module=types.ModuleType('_grouping362_'+name);module.__file__=str(HERE/(name+'.py'));loaded[name]=module
  def imp(n,g=None,l=None,fromlist=(),level=0):
   if level==0 and 'semantic_rules357/'+n+'.py' in pins:return load(n)
   return builtins.__import__(n,g,l,fromlist,level)
  module.__dict__['__builtins__']={**vars(builtins),'__import__':imp};exec(compile(data,module.__file__,'exec'),module.__dict__)
  if name=='common':module.REGISTRY_NAME='method_registry_source365.json'
  return module
 return load

def ownership_protection(new,old):
 if new['program']!=old['program']or new['profile']!=old['profile']:raise ValueError('PROTECTED_PROGRAM_PROFILE')
 if {u['id']for u in new['units']}!={u['id']for u in old['units']}or len(new['units'])!=len(old['units']):raise ValueError('PROTECTED_UNIT_INVENTORY')
 out=[]
 for u in old['units']:
  matches=[v for v in new['units']if v['id']==u['id']]
  if len(matches)!=1:raise ValueError('PROTECTED_UNIT_ID')
  a=list(map(rect,u['ownership']));b=list(map(rect,matches[0]['ownership']))
  if difference(a,b):raise ValueError('OWNERSHIP_AREA_LOST:'+u['id'])
  out.append({'unit':u['id'],'lost_area_m2':'0','added_area_m2':str(union_area(difference(b,a))),'criterion':'per-unit exact set containment, not equal area between units'})
 return out

def room_equivalence(new,old,section_rows):
 known={r['original']['module_digest']for r in section_rows};out=[]
 for p in new['module_placements']:
  if not p['room_id'].startswith('bed'):continue
  h=digest(p['module']);uid=p['unit_id'];rid=p['room_id'];matches=[q for q in old['module_placements']if q['unit_id']==uid and q['room_id']==rid]
  if len(matches)!=1 or h not in known or digest(matches[0]['module'])!=h or p['module_hash']!=h:raise ValueError('EXACT_SOURCE_ROOM_MODULE_REQUIRED')
  u=next(u for u in new['units']if u['id']==uid);v=next(u for u in old['units']if u['id']==uid)
  a=[rect(x)for x in u['rooms'][rid]];b=[rect(x)for x in v['rooms'][rid]]
  if difference(a,b)or difference(b,a):raise ValueError('WORLD_ROOM_FLOOR_CHANGED')
  def walls(m):return [z for q in m['walls'].values()for r in a if(z:=intersection(rect(q),r))]
  wa,wb=walls(new),walls(old)
  if difference(wa,wb)or difference(wb,wa):raise ValueError('ROOM_INTERIOR_PHYSICAL_WALLS_CHANGED')
  out.append({'unit':uid,'room':rid,'module_digest':h,'actual_world_floor_equal':True,'interior_physical_wall_union_equal':True})
 if len(out)!=new['program']['units']*new['program']['bedrooms_per_unit']:raise ValueError('ROOM_COVERAGE')
 return out

def evaluate(record,result,seconds=15):
 out={'rule_id':'BEDROOM_GROUPING','verdict':'UNKNOWN','parent_initial':False,'proofscopecomplete':False,'live_authority':False,'delivery_allowed':False,'new_fresh_execution':False,'missing':[]}
 try:
  if type(seconds)not in(int,float)or not 0<seconds<=15:raise ValueError('BOUNDED_SECONDS')
  start=time.monotonic();pins=json.loads((HERE/'bedroom_grouping365_pins.json').read_text())
  for f,h in pins['files'].items():
   if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_PIN:'+f)
  load=_loader();view=load('group_readsets365_v2').build(record,result,source_profile='SOURCE_BALANCED365');m=view['envelope']['packet']['world_model'];raw=view['result']['raw_fresh_report'];rs=load('common').rows(m,raw)
  for k in('private_grouping','privacy_scenarios','fixture_inventory_use','door_operation','body_route_sweeps'):
   r=rs[k];w=r['evidence']['witness']
   if r['status']!='PASS_LIMITED'or w.get('errors')or w.get('pending'):raise ValueError('SOURCE_ROOM_PREREQUISITE:'+k)
  bundle=load('closure_room_program365').bundle_inventory(m,rs)
  sections=json.loads((HERE/'bedroom_sections_actual358.json').read_text())
  if not sections.get('finite_scope_evidence_ready_for_audit')or sections.get('missing'):raise ValueError('SECTIONS_EVIDENCE_UNRESOLVED')
  old=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text())['candidate']['model'];equivalence=room_equivalence(m,old,sections['rows'])
  previous=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text())['candidate']['model'];protected=ownership_protection(m,previous)
  current=validate_model(m,time.monotonic()+min(10,seconds-(time.monotonic()-start)))
  if any(p['verdict']!='PASS_SCOPED_JOINED_TASK_PATH'for u in current['units']for p in u['pairs']):raise ValueError('CURRENT_BALANCED365_TASK_PATH_UNPROVEN')
  stored=json.loads((HERE/'bedroom_route_witness_actual358.json').read_text())['evidence']['members'];comparisons={};rationales=[]
  for name,alternative in stored.items():
   if alternative['program_digest']!=digest(m['program'])or alternative['profile_digest']!=digest(m['profile']):raise ValueError('COHORT_PROGRAM_PROFILE')
   if any(p['verdict']!='PASS_SCOPED_JOINED_TASK_PATH'for u in alternative['units']for p in u['pairs']):raise ValueError('ALTERNATIVE_TASK_PATH_UNPROVEN')
   comparisons[name]=compare(current['vector'],alternative['vector'])
  for unit in m['units']:
   uid=unit['id'];byalternative={}
   for name,c in comparisons.items():
    alt=stored[name]['net_bedroom_area_m2'];areas={}
    for k,v in current['net_bedroom_area_m2'].items():
     if not k.startswith(uid+'|'):continue
     areas[k]={'selected_m2':v,'alternative_m2':alt[k],'delta_m2':str(F(v)-F(alt[k])),'no_shrink':F(v)>=F(alt[k])}
    if len(areas)!=m['program']['bedrooms_per_unit']or not all(v['no_shrink']for v in areas.values()):raise ValueError('PROTECTED_ROOM_AREA_REDUCED')
    byalternative[name]={'shorter_paths':[k for k in c['better']if k.startswith(uid+'|')],'longer_paths':[k for k in c['worse']if k.startswith(uid+'|')],'protected_net_room_areas':areas,'policy':'reviewed finite preference tradeoff; no average, no no-worse-all-routes claim'}
   rationales.append({'unit':uid,'alternatives':byalternative,'source_bundle_privacy_private_topology':'CURRENT_BALANCED365_BOUND_SOURCE_ROWS_AND_BUNDLE','closet_selection_reason':'two source-rigid longitudinal placements have independently audited direct privacy counterexamples; keep current transverse source construction in this finite comparison'})
  out.update(verdict='PASS_SCOPED_REVIEWED_TRADEOFF',proofscopecomplete=True,evidence={'model_digest':digest(m),'raw_digest':digest(raw),'record_digest':digest(record),'result_digest':digest(result),'current_task_routes':current,'room_section_equivalence':equivalence,'section_source_model_digest':sections['model_digest'],'bundle_digest':digest(bundle),'ownership_protection_vs359':protected,'comparisons':comparisons,'per_unit_functional_rationale':rationales,'section_artifact_digest':digest(sections)},scope='IR-P13_FINITE_SOURCE_PROFILE: baseline351/translated357/row358/current_balanced365 plus two tested closet counterfactuals; SOURCE0.7_OPEN_TRANSIT; exact source-state net sections; reviewed tradeoffs NOT DOMINANCE/GLOBAL_OPTIMUM/ALL_PLACEMENTS/ALL_JOINT_SCENARIOS')
  for f,h in pins['files'].items():
   if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED_AFTER')
  out['elapsed_seconds']=time.monotonic()-start
 except (ValueError,KeyError,TypeError,IndexError,StopIteration,ZeroDivisionError,FileNotFoundError)as e:out['verdict']='UNKNOWN';out['proofscopecomplete']=False;out['missing']=[str(e)]
 return out
