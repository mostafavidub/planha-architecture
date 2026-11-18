"""Exact IR-P13 source-state reservations. No invented simultaneous scenarios.
All-reservations union is a conservative envelope, NOT a simultaneously usable
floor requirement. Source module operation/access evidence remains separate.
"""
import json,hashlib,time
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,difference,union_area
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def sweep(a,b):
 a,b=rect(a),rect(b)
 if (a[2]-a[0],a[3]-a[1])!=(b[2]-b[0],b[3]-b[1]):raise ValueError('NONRIGID_SOURCE_SWEEP')
 if a[0]!=b[0]and a[1]!=b[1]:raise ValueError('NONORTHOGONAL_SOURCE_SWEEP')
 return min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])
def operation_inventory(module):
 records=[];seen=set()
 def put(key,value,kind):
  if key in seen:raise ValueError('DUPLICATE_STATE_ID')
  seen.add(key);records.append({'id':key,'kind':kind,'rect':list(map(str,value))})
 def panel(p,prefix):
  closed,opened=rect(p['closed_panel']),rect(p['open_panel']);delta=tuple(map(F,p['translation']))
  if len(delta)!=2 or tuple(closed[i]+delta[i%2]for i in range(4))!=opened:raise ValueError('PANEL_MOTION_BINDING')
  put(prefix+'/panel/continuous',sweep(p['closed_panel'],p['open_panel']),'panel_continuous')
  states=p['states'];fractions={F(s['fraction'])for s in states}
  if not {F(0),F(1)}<=fractions:raise ValueError('ENDPOINT_STATES_REQUIRED')
  for i,s in enumerate(states):
   t=F(s['fraction'])
   if not 0<=t<=1 or rect(s['panel_rect'])!=tuple(closed[j]+delta[j%2]*t for j in range(4)):raise ValueError('STATE_PANEL_BINDING')
   put(prefix+'/state/'+str(i)+'/panel',rect(s['panel_rect']),'panel_state')
   put(prefix+'/state/'+str(i)+'/actor',rect(s['actor_rect']),'actor_state')
  segs=p['continuous_actor_segments']
  if not segs:raise ValueError('CONTINUOUS_ACTOR_INVENTORY')
  for i,s in enumerate(segs):
   if not 0<=F(s['t0'])<F(s['t1'])<=1:raise ValueError('SOURCE_TIME_RANGE')
   put(prefix+'/segment/'+str(i)+'/actor',sweep(s['actor_start'],s['actor_end']),'actor_continuous')
   # Zero-thickness hand trajectories are source reach witnesses, not invented
   # positive-area floor reservations. Existing operation gate checks their grip.
   if len(s['hand_start'])!=2 or len(s['hand_end'])!=2:raise ValueError('HAND_POINT_INVENTORY')
  return {'state_count':len(states),'continuous_segment_count':len(segs),'hand_geometry':'SOURCE_POINTS_NO_ADDED_AREA; ACTUAL_REACH_CHECK_SEPARATE'}
 summary=[];doors=module['operations']['doors'];closets=module['operations']['closets']
 if len({o['opening_id']for o in doors})!=len(doors):raise ValueError('DUPLICATE_DOOR')
 if len({(o['unit'],o['fixture_id'])for o in closets})!=len(closets):raise ValueError('DUPLICATE_CLOSET')
 for op in doors:
  if op['kind'] not in ('sliding_linear','pocket_source113'):raise ValueError('UNSUPPORTED_DOOR_MOTION')
  summary.append({'id':'door:'+op['opening_id'],**panel(op,'door:'+op['opening_id'])})
 for op in closets:
  prefix='closet:'+op['unit']+'.'+op['fixture_id'];panels=op['panels']
  if not panels or len({p['id']for p in panels})!=len(panels):raise ValueError('CLOSET_PANEL_INVENTORY')
  for i,r in enumerate(op['shell_rects']):put(prefix+'/shell/'+str(i),rect(r),'closet_shell')
  for p in panels:summary.append({'id':prefix+'/'+p['id'],**panel(p,prefix+'/'+p['id'])})
 return records,summary

def sections(floor,obstacles):
 free=difference(floor,obstacles);axes={}
 for axis in (0,1):
  lo=min(r[axis]for r in floor);hi=max(r[axis+2]for r in floor)
  xs=sorted({lo,hi}|{r[j]for r in floor+obstacles for j in(axis,axis+2)if lo<r[j]<hi})
  slabs=[]
  for a,b in zip(xs,xs[1:]):
   mid=(a+b)/2;ivs=sorted((r[1-axis],r[3-axis])for r in free if r[axis]<mid<r[axis+2]);merged=[]
   for c,d in ivs:
    if merged and c<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],d)
    else:merged.append([c,d])
   slabs.append({'interval':list(map(str,(a,b))),'free_components':[list(map(str,x))for x in merged],'component_widths_m':[str(d-c)for c,d in merged]})
  axes[str(axis)]=slabs
 return {'free_area_m2':str(union_area(free)),'slabs':axes,'method':'EXACT_RECTANGLE_UNION_SUBTRACTION_AT_ALL_EDGE_BREAKPOINTS; ZERO_AREA_CONTACT_NOT_POSITIVE_FLOOR'}

def measure(module):
 u=module['unit'];floor=[rect(r)for r in u['rooms']['bed1']]
 static=[rect(r)for r in module['walls'].values()]+[rect(r)for r in u['fixtures'].values()]
 activity=[rect(r)for r in u['activities'].values()]
 records,inventory=operation_inventory(module)
 return {'module_digest':digest(module),'source_room_floor_m2':str(union_area(floor)),'after_wall_and_fixture_sections':sections(floor,static),'all_source_reservations_envelope':sections(floor,static+activity+[rect(r['rect'])for r in records]),'source_operation_inventory':inventory,'reservation_inventory':records,'activity_ids':sorted(u['activities']),'fixture_ids':sorted(u['fixtures']),'coverage':'ALL_DECLARED_SOURCE_DOOR_AND_CLOSET_ENDPOINT_PANEL_ACTOR_AND_CONTINUOUS_SWEEPS_PLUS_REQUIRED_ACTIVITIES','not_claimed':'NOT_SIMULTANEOUS_USE_REQUIREMENT; NOT_ALL_IMAGINABLE_JOINT_SCENARIOS; NOT_PATH_OR_CLEARANCE_ADMISSION'}

def evaluate():
 pins=json.loads((HERE/'bedroom_sections358_pins.json').read_text());out={'schema':'IRP13_SOURCE_STATE_SECTIONS358','parent_initial':False,'verdict':'UNKNOWN','fresh_or_solver':False,'delivery_allowed':False,'rows':[]}
 try:
  for f,h in pins['files'].items():
   if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED:'+f)
  record=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text());m=record['candidate']['model'];local=json.loads((ROOT/'local_closet_counterfactual358/result.json').read_text())
  start=time.monotonic()
  for r in local['rows']:
   room='bed1'if r['room_type']=='double'else'bed2';matches=[p for p in m['module_placements']if p['unit_id']=='A'and p['room_id']==room]
   if len(matches)!=1 or digest(matches[0]['module'])!=r['derivation']['source_module_digest']:raise ValueError('COUNTERFACTUAL_SOURCE_MODULE_BINDING')
   original=measure(matches[0]['module']);alternative=measure(r['counterfactual'])
   if len(original['reservation_inventory'])!=len(alternative['reservation_inventory'])or original['activity_ids']!=alternative['activity_ids']or original['fixture_ids']!=alternative['fixture_ids']:raise ValueError('TRANSFORM_INVENTORY_PRESERVATION')
   out['rows'].append({'type':r['room_type'],'original':original,'counterfactual':alternative,'independent_privacy_counterexamples':r['privacy_report']['errors'],'remaining_counterfactual_privacy_unknown':r['privacy_report']['pending'],'counterfactual_source_status':'TEST_ONLY_DERIVATION_NOT_PRODUCER_REPLAY'})
  # Explicit applicability to each of the six current rooms by actual module hash,
  # not transfer based on a room name or approximate dimensions.
  known={r['original']['module_digest']:r['type']for r in out['rows']};coverage=[]
  for p in m['module_placements']:
   if p['room_id'].startswith('bed'):
    h=digest(p['module']);coverage.append({'unit':p['unit_id'],'room':p['room_id'],'module_digest':h,'type':known.get(h),'covered':h in known})
  out['current_room_coverage']=coverage;out['source_state_sections_complete']=bool(coverage)and all(r['covered']for r in coverage)
  out['missing']=[]if out['source_state_sections_complete']else['CURRENT_ROOM_SOURCE_MODULE_NOT_IN_TWO_TYPE_SET']
  route=json.loads((HERE/'bedroom_route_witness_actual358.json').read_text());rv=route['evidence'];selected=rv['members']['row358']
  if selected['model_digest']!=digest(m):raise ValueError('ROUTE_MODEL_BINDING')
  raw=json.loads((ROOT/'review358_source_validation/result.json').read_text())['raw_report']
  if raw['model_hash']!=digest(m)or selected['raw_digest']!=digest(raw):raise ValueError('SAME_FRESH_SOURCE_BINDING')
  rs={r['requirement_id']:r for r in raw['rule_contract_evidence']['requirements']}
  if len(rs)!=len(raw['rule_contract_evidence']['requirements']):raise ValueError('DUPLICATE_SOURCE_ROW')
  for name in ('privacy_scenarios','fixture_inventory_use','private_grouping'):
   r=rs[name];w=r['evidence']['witness']
   if r['status']!='PASS_LIMITED'or w.get('errors')or w.get('pending'):raise ValueError('CURRENT_SOURCE_PROOF_UNRESOLVED:'+name)
  rationales=[]
  for unit in m['units']:
   uid=unit['id'];ur=next(v for v in selected['units']if v['unit']==uid)
   if not ur['pairs']or any(p['verdict']!='PASS_SCOPED_JOINED_TASK_PATH'for p in ur['pairs']):raise ValueError('TASK_PATH_COVERAGE')
   alternatives={}
   for name,c in rv['task_route_comparisons'].items():
    a={k:v for k,v in rv['protected_room_area_comparisons'][name].items()if k.startswith(uid+'|')}
    if len(a)!=m['program']['bedrooms_per_unit']or not all(v['no_shrink']for v in a.values()):raise ValueError('PROTECTED_ROOM_AREA')
    alternatives[name]={'shorter_paths':[k for k in c['better']if k.startswith(uid+'|')],'longer_paths':[k for k in c['worse']if k.startswith(uid+'|')],'protected_net_room_areas':a,'reason':'preserve source room area and usable bundle; retain these explicit route gains with disclosed route losses; no weighted compensation or global minimum claim'}
   rationales.append({'unit':uid,'current_source_bundle_privacy_and_private_topology':'SAME_MODEL_SOURCE_ROWS_PASS_LIMITED','validated_task_pairs':len(ur['pairs']),'alternatives':alternatives})
  if any(not r['independent_privacy_counterexamples']for r in out['rows']):raise ValueError('COUNTERFACTUAL_FUNCTIONAL_REASON_MISSING')
  out['per_unit_functional_rationale']=rationales
  out['finite_scope_evidence_ready_for_audit']=out['source_state_sections_complete']
  out['rationale']='IR-P13 finite source-profile evidence: exact net sections with source state inventory, actual usable bundles/closets/private topology, validated via-entry task routes and per-unit room-area tradeoffs, two independently witnessed longitudinal privacy failures. Not an exhaustive placement search or all-scenario certificate.' 
  out['model_digest']=digest(m);out['elapsed_seconds']=time.monotonic()-start
  for f,h in pins['files'].items():
   if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED_AFTER')
 except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError)as e:out['missing']=[str(e)];out['source_state_sections_complete']=False
 return out
