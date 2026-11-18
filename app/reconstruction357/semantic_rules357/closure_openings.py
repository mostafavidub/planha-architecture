"""Rendered233 H08/H10/H11 evidence join. Not a fresh-run attestation.
Parent admission disabled pending independent audit and scenario closure.
No daylight/ventilation criterion; counts are inventories, never thresholds.
"""
from collections import Counter
from fractions import Fraction
from common import rows, digest
from pathlib import Path
import hashlib

SOURCE_SECTIONS={'H08':[211087,226320],'H10':[238554,252437],'H11':[252437,267506]}

def _rect(v):
 if type(v) is not list or len(v)!=4 or any(type(x) not in (int,str) for x in v):raise ValueError('EXACT_RECT_REQUIRED')
 q=tuple(Fraction(x) for x in v)
 if q[0]>=q[2] or q[1]>=q[3]:raise ValueError('NONPOSITIVE_RECT')
 return q

def _index(items,key):
 if type(items) is not list:raise ValueError('INVENTORY_LIST_REQUIRED')
 out={}
 for x in items:
  if type(x) is not dict or type(x.get(key)) is not str or not x[key] or x[key] in out:raise ValueError('INVALID_OR_DUPLICATE_ID')
  out[x[key]]=x
 return out

def _witness(rs,key):
 r=rs[key];w=r['evidence']['witness']
 if type(w) is not dict or type(w.get('errors')) is not list or type(w.get('pending')) is not list:raise ValueError('WITNESS_ERRORS_PENDING_REQUIRED')
 return r,w

# Exact audited implementation: check_operations checks every omitted opening
# through source_nonleaf117, and requires continuous actor/side/transfer proof.
# This is an implication of same-model executed evidence, NOT reexecution.
OPERATION_SOURCE_SHA='ac73b6a13c73f60c513de19c5faa60fb6a9f445e4ad4b2f836fd945df006ce6b'

def _scenario_join(model,rs):
 source=Path(__file__).resolve().parents[1]/'planha_general150_runtime_work/operation_check114.py'
 if hashlib.sha256(source.read_bytes()).hexdigest()!=OPERATION_SOURCE_SHA:raise ValueError('OPERATION_SEMANTICS_SOURCE_CHANGED')
 openings=_index(model['openings'],'id');doors=_index(model['operations']['doors'],'opening_id')
 r,w=_witness(rs,'door_operation');missing=[];inventory=[]
 passrow=r['status']=='PASS_LIMITED' and not w['errors'] and not w['pending']
 for oid,o in openings.items():
  if oid not in doors:
   # Discriminator is necessary only. Source checker supplies the stronger
   # transformed module/hash/geometry/role or core-boundary verification.
   supported=(o.get('kind')=='permanent_open_arch' and o.get('hardware') is None) or (oid in ('stair.entry','lift.entry') and o.get('kind')=='core_access_interface' and o.get('leaf_modeled') is False)
   if not supported:missing.append(oid+':NONLEAF_SOURCE_PROFILE_UNSUPPORTED')
   if not passrow:missing.append(oid+':NONLEAF_EXECUTED_PROOF_MISSING')
   inventory.append({'opening':oid,'type':'source_nonleaf117','executed_evidence_implication':bool(passrow and supported)})
   continue
  op=doors[oid];segments=op.get('continuous_actor_segments');states=op.get('states')
  if op.get('kind') not in ('sliding_linear','pocket_source113'):missing.append(oid+':OPERATION_PROFILE_UNSUPPORTED')
  if type(states)is not list or not {Fraction(0),Fraction(1)}<={Fraction(x['fraction']) for x in states}:missing.append(oid+':ENDPOINT_STATES_MISSING')
  if type(segments)is not list or not segments:missing.append(oid+':CONTINUOUS_TRAJECTORY_MISSING');segments=[]
  roles={x.get('role_id') for x in segments}
  if roles!=set(o['connects']):missing.append(oid+':BOTH_CONNECTED_ROLES_MISSING')
  # Multiple intervals on one role are legitimate, not duplicate targets.
  if len({digest(x) for x in segments})!=len(segments):missing.append(oid+':DUPLICATE_TRAJECTORY_RECORD')
  if op.get('kind')=='pocket_source113' and not op.get('open_transfer_points'):missing.append(oid+':OPEN_TRANSFER_MISSING')
  if not passrow:missing.append(oid+':EXECUTED_OPERATION_PROOF_MISSING')
  inventory.append({'opening':oid,'type':op.get('kind'),'roles':sorted(x for x in roles if isinstance(x,str)),'continuous_segments':len(segments),'source_profile_scope':'declared source operation, both sides, continuous actor and panel; not all imaginable joint states'})
 # Nonleaf kitchen exceptions rely on complete, same-model source placement.
 pr,pw=_witness(rs,'fixture_inventory_use');placement=pw.get('source_placement')
 if not isinstance(placement,dict) or placement.get('errors')!=[] or placement.get('pending')!=[] or not placement.get('evidence'):missing.append('SOURCE_MODULE_PLACEMENT_UNPROVEN')
 return {'inventory':inventory,'source_sha256':OPERATION_SOURCE_SHA,'method':r.get('method'),'readset_digest':digest({k:model[k] for k in ('openings','operations','module_placements','common_spaces','wall_hosts','walls','units','logical_regions')}),'source_pass_implication':passrow,'missing':missing}

def evaluate(model,raw_report):
 out={'verdict':'UNKNOWN','codes':[],'evidence':{},'missing':[], 'parent_initial':False,'accepted':False,'delivery_allowed':False,'fresh_execution_attested':False}
 try:
  rs=rows(model,raw_report)
  os=_index(model['openings'],'id');ws=_index(model['concept_windows'],'id')
  if set(os)&set(ws):raise ValueError('OPENING_WINDOW_ID_ALIAS')
  doors=_index(model['operations']['doors'],'opening_id')
  if not set(doors)<=set(os):raise ValueError('OPERATION_UNKNOWN_OPENING')
  clauses={};errors=[];missing=[]
  for name in ('opening_hosts','actual_opening_geometry','door_operation','closet_operation'):
   r,w=_witness(rs,name)
   clauses[name]={'status':r['status'],'errors':w['errors'],'pending':w['pending']}
   if w['errors']:
    if r['status']!='FAIL':raise ValueError('ROW_STATUS_ERRORS_CONTRADICTION')
    errors.append(name)
   elif w['pending'] or r['status']!='PASS_LIMITED':missing.append(name+':UNPROVEN')
  hw=_witness(rs,'opening_hosts')[1]
  hostrows=hw.get('openings')
  if type(hostrows)is not list:raise ValueError('HOST_INVENTORY_REQUIRED')
  oh=_index([r for r in hostrows if 'opening'in r],'opening')
  wh=_index([r for r in hostrows if 'window'in r],'window')
  if len(oh)+len(wh)!=len(hostrows) or set(oh)!=set(os) or set(wh)!=set(ws):raise ValueError('HOST_WITNESS_INVENTORY')
  for oid,o in os.items():
   _rect(o['rect']);links=o['connects']
   if type(links)is not list or len(links)!=2 or any(type(x)is not str or not x for x in links):raise ValueError('TWO_REGION_DATA_REQUIRED')
   if links[0]==links[1]:errors.append(oid+':IDENTICAL_CONNECTED_REGIONS')
   row=oh[oid]
   if row.get('host')!=o.get('host_wall_id') or row.get('regions')!=links:raise ValueError('HOST_READSET_MISMATCH')
   if row.get('crossing_found') is not True:missing.append(oid+':BODY_CROSSING_UNPROVEN')
  for wid,w in ws.items():
   hostid=w.get('host_wall_id')
   if wh[wid].get('host')!=hostid:raise ValueError('WINDOW_HOST_READSET_MISMATCH')
   if hostid not in model['walls']:missing.append(wid+':HOST_MISSING');continue
   a,b,c,d=_rect(w['plan_rect']);A,B,C,D=_rect(model['walls'][hostid])
   if not (A<=a<c<=C and B<=b<d<=D):errors.append(wid+':WINDOW_OUTSIDE_HOST')
   if w.get('floor_portal')is not False:errors.append(wid+':WINDOW_FLOOR_PORTAL')
   if not 0<=Fraction(w['sill_m'])<Fraction(w['head_m']):errors.append(wid+':VERTICAL_EXTENT')
  for kind,key in [('doors','opening_id'),('closets','fixture_id')]:
   ops=model['operations'][kind];actual=[x[key] for x in ops]
   w=_witness(rs,'door_operation' if kind=='doors' else 'closet_operation')[1]
   if w.get('operation_component')!=kind or Counter(w.get('actual_operation_ids',[]))!=Counter(actual):raise ValueError('OPERATION_WITNESS_INVENTORY:'+kind)
   if w.get('model_hash')!=digest(model):raise ValueError('OPERATION_MODEL_BINDING')
  # The source checker validates omitted doors using source_nonleaf117 and
  # source placement; this join does not reinterpret a mere leaf flag as proof.
  nonleaf=sorted(set(os)-set(doors))
  scenario=_scenario_join(model,rs)
  missing+=scenario['missing']
  out['scope_complete']=not errors and not missing
  missing+=['INDEPENDENT_AUDIT_BEFORE_PARENT_ENABLE']
  out['evidence']={'model_digest':digest(model),'raw_digest':digest(raw_report),'sections':SOURCE_SECTIONS,'source_rows':clauses,'scenario_join':scenario,'opening_ids':sorted(os),'window_ids':sorted(ws),'operated_opening_ids':sorted(doors),'source_nonleaf_candidates_not_new_proofs':nonleaf,'lighting_ventilation':'EXCLUDED','inventory_join':'BOUND_SCOPED' if not errors else 'BOUND_WITH_VIOLATION'}
  out['codes']=errors;out['missing']=sorted(set(missing));out['verdict']='FAIL' if errors else 'UNKNOWN'
 except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError,OverflowError) as ex:
  out['codes']=['BINDING_OR_DATA_UNAVAILABLE',str(ex)];out['missing']=['COMPLETE_SAME_MODEL_SOURCE_EVIDENCE']
 return out
