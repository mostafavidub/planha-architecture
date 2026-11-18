"""IR-P13 bounded source-artifact comparison. No layout generation or authority."""
import json,hashlib,time
from pathlib import Path
from fractions import Fraction as F
from common import digest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
ASSUMPTION={'id':'ENG_ELONGATED_SOURCE_DEPTH_TRIAGE_V1','predicate':'long_side - short_side >= smallest required source closet depth','authority':'ENGINEERING_ASSUMPTION_NOT_OWNER_STANDARD','purpose':'conservative comparison trigger only, never a room rejection/aspect limit','unknown':'nonrectangular room, absent closet geometry or orientation evidence'}

def elongated(room,closets):
 if len(room)!=1 or not closets:raise ValueError('ELONGATED_TRIGGER_GEOMETRY_UNSUPPORTED')
 x,y,X,Y=map(F,room[0]);sides=(X-x,Y-y)
 if min(sides)<=0:raise ValueError('ROOM_EXTENT')
 depths=[]
 for c in closets:
  a,b,A,B=map(F,c)
  if min(A-a,B-b)<=0:raise ValueError('CLOSET_EXTENT')
  depths.append(min(A-a,B-b))
 depth=min(depths);return {'trigger':max(sides)-min(sides)>=depth,'long_side_m':str(max(sides)),'short_side_m':str(min(sides)),'source_closet_depth_m':str(depth),'assumption':ASSUMPTION['id']}

def compare(selected,alternative):
 if set(selected)!=set(alternative):raise ValueError('PAIR_INVENTORY_MISMATCH')
 better=[];worse=[];equal=[]
 for k in sorted(selected):
  if selected[k] is None or alternative[k] is None:raise ValueError('UNCONNECTED_STORED_NETWORK')
  a,b=F(selected[k]),F(alternative[k]);(better if a<b else worse if a>b else equal).append(k)
 return {'better':better,'worse':worse,'equal_count':len(equal),'dominates_on_these_routes_only':bool(better)and not worse,'tradeoff':bool(better and worse),'weighted_score':None}

def evaluate(seconds=30):
 out={'rule_id':'BEDROOM_GROUPING','verdict':'UNKNOWN','parent_initial':False,'parent_complete':False,'live_authority':False,'delivery_allowed':False,'new_fresh_execution':False,'assumption':ASSUMPTION,'missing':[]}
 try:
  if type(seconds)not in(int,float)or not 0<seconds<=30:raise ValueError('BOUNDED_SECONDS')
  start=time.monotonic();pins=json.loads((HERE/'bedroom_grouping358_pins.json').read_text())
  for name,sha in pins['files'].items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('PIN_CHANGED:'+name)
  import eligibility_intrinsic357_v2 as old
  import eligibility_intrinsic358 as new
  members={};profiles={};models={}
  for ident,meta in pins['members'].items():
   if time.monotonic()-start>=seconds:raise ValueError('COMPARISON_DEADLINE')
   data=json.loads((ROOT/meta['record']).read_text());review=json.loads((ROOT/meta['review']).read_text())
   record=data['selected'][0] if ident=='baseline351'else data
   review=review['central_fresh_reviews'][0]if ident=='baseline351'else review
   existing=json.loads((ROOT/meta['eligibility']).read_text())
   if existing.get('verdict')!='PASS' or len(existing.get('rows',[]))!=18 or any(r['verdict']!='PASS'for r in existing['rows']):raise ValueError('INTRINSIC_MINIMA_NOT_PROVEN:'+ident)
   if existing['evidence']['record_digest']!=digest(record)or existing['evidence']['new_result_digest']!=digest(review):raise ValueError('MODEL_SPECIFIC_ELIGIBILITY:'+ident)
   if ident=='row358':
    load,_=new._loader();view=load('group_readsets358').build(record,review,source_profile='SOURCE358')
   else:
    profile='SOURCE351'if ident=='baseline351'else'SOURCE_IDENTITY357';load,epins=old._loader(profile);view=old._view(record,review,profile,load,epins)
   model=view['envelope']['packet']['world_model'];raw=view['result']['raw_fresh_report'];rs=load('common').rows(model,raw)
   if existing['evidence']['model_digest']!=digest(model):raise ValueError('ELIGIBILITY_MODEL_MISMATCH')
   key=digest({'raw':{k:view['envelope']['raw'][k]for k in('W','L','n')},'program':model['program'],'profile':model['profile']})
   profiles[ident]=key;models[ident]=model
   w=rs['private_grouping']['evidence']['witness']
   if rs['private_grouping']['status']!='PASS_LIMITED'or w.get('errors')or w.get('pending'):raise ValueError('PRIVATE_GROUPING_UNPROVEN')
   if {u['unit']for u in w['units']}!={u['id']for u in model['units']}:raise ValueError('PRIVATE_UNIT_INVENTORY')
   bundle=load('closure_room_program'if ident!='row358'else'closure_room_program358').bundle_inventory(model,rs)
   matrix=load('route_matrix').evaluate(model,raw);vector={}
   for u in matrix['units']:
    expected={k for k in next(v for v in model['units']if v['id']==u['unit'])['routes']if k.startswith('bed')and k.endswith(('bed_front','bedA_front','bedB_front'))}
    if set(u['bed_targets'])!=expected:raise ValueError('ACTUAL_BED_TARGET_INVENTORY')
    for pair in u['pairs']:
     k=u['unit']+'|'+pair['bed_target']+'|'+pair['destination']
     if k in vector:raise ValueError('DUPLICATE_ROUTE_PAIR')
     vector[k]=pair['stored_network_length_m']
   members[ident]={'model_digest':digest(model),'raw_digest':digest(raw),'matrix':matrix,'vector':vector,'bundle_digest':digest(bundle),'topology_witness_digest':digest(w)}
  if len(set(profiles.values()))!=1:raise ValueError('SAME_PROGRAM_PROFILE_INPUT_REQUIRED')
  comparisons={i:compare(members['row358']['vector'],members[i]['vector'])for i in('baseline351','translated357')}
  roomrows=[]
  for p in models['row358']['module_placements']:
   if not p['room_id'].startswith('bed'):continue
   src=p['module']['unit'];floor=src['rooms']['bed1'];closets=[v for k,v in src['fixtures'].items()if k.endswith('closet')]
   row={'unit':p['unit_id'],'room':p['room_id'],'module_hash':p['module_hash'],'elongated':elongated(floor,closets)}
   # The source modules may have different envelopes. D4 or
   # translation of the entire bundle is NOT an independent closet alternative.
   hashes=[];orientations=[]
   for name,m in models.items():
    match=[q for q in m['module_placements']if q['unit_id']==p['unit_id']and q['room_id']==p['room_id']]
    if len(match)!=1:raise ValueError('BED_MODULE_INVENTORY')
    hashes.append(match[0]['module_hash'])
    unit=match[0]['module']['unit'];floor=unit['rooms']['bed1']
    if len(floor)!=1:raise ValueError('CLOSET_COMPARISON_ENVELOPE_UNSUPPORTED')
    a,b,A,B=map(F,floor[0]);longaxis=0 if A-a>B-b else 1 if B-b>A-a else None
    cs=[q for k,q in unit['fixtures'].items()if k.endswith('closet')]
    if len(cs)!=1:raise ValueError('CLOSET_ORIENTATION_INVENTORY')
    x,y,X,Y=map(F,cs[0]);closetaxis=0 if X-x>Y-y else 1 if Y-y>X-x else None
    orientations.append({'member':name,'source_room_envelope':floor,'source_closet':cs[0],'orientation':'UNRESOLVED'if None in(longaxis,closetaxis)else'TRANSVERSE_TO_LONG_AXIS'if longaxis!=closetaxis else'LONGITUDINAL_TO_LONG_AXIS','meaning':'relative axis evidence only; does not certify wall mounting or alternative feasibility'})
   row['same_internal_module_in_cohort']=len(set(hashes))==1
   row['member_source_orientations']=orientations
   row['closet_alternative_coverage']='UNKNOWN_NO_INDEPENDENT_TRANSVERSE_LONGITUDINAL_SOURCE_LAYOUT'if row['elongated']['trigger']else'NOT_TRIGGERED_BY_EXPLICIT_ENGINEERING_TRIAGE'
   roomrows.append(row)
  out.update(evidence={'members':members,'comparisons_selected_row358':comparisons,'rooms':roomrows,'same_program_profile_digest':next(iter(profiles.values())),'source_pin_digest':digest(pins)},scope='THREE_FIXED_SOURCE_PROGRAM_MEMBERS; EXACT_SHORTEST_STORED_ROUTE_UNION_NOT_GLOBAL_SHORTEST; TOPOLOGY_NOT_MINIMUM_CORRIDOR')
  if any(r['elongated']['trigger']for r in roomrows):out['missing'].append('SOURCE_ROOM_TRANSVERSE_VS_LONGITUDINAL_CLOSET_ALTERNATIVE_AND_NET_SECTION_COMPARISON')
  out['missing']+=['FUNCTIONAL_SELECTION_REASON_FOR_NONCOMPENSATORY_ROUTE_TRADEOFF','INDEPENDENT_AUDIT_BEFORE_PARENT_ENABLE']
  for name,sha in pins['files'].items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_CHANGED_DURING_COMPARISON')
  out['elapsed_seconds']=time.monotonic()-start
 except (ValueError,TypeError,KeyError,IndexError,StopIteration,ZeroDivisionError,FileNotFoundError)as e:out['missing'].append(str(e))
 return out
