"""Rendered233 H08/H10/H11 evidence join. Not a fresh-run attestation.
Parent admission disabled pending independent audit and scenario closure.
No daylight/ventilation criterion; counts are inventories, never thresholds.
"""
from collections import Counter
from fractions import Fraction
from common import rows, digest

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
  missing+=['COMPLETE_SOURCE_SCENARIO_AND_NONLEAF_PLACEMENT_CLOSURE','INDEPENDENT_AUDIT_BEFORE_PARENT_ENABLE']
  out['evidence']={'model_digest':digest(model),'raw_digest':digest(raw_report),'sections':SOURCE_SECTIONS,'source_rows':clauses,'opening_ids':sorted(os),'window_ids':sorted(ws),'operated_opening_ids':sorted(doors),'source_nonleaf_candidates_not_new_proofs':nonleaf,'lighting_ventilation':'EXCLUDED','inventory_join':'BOUND_SCOPED' if not errors else 'BOUND_WITH_VIOLATION'}
  out['codes']=errors;out['missing']=sorted(set(missing));out['verdict']='FAIL' if errors else 'UNKNOWN'
 except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError,OverflowError) as ex:
  out['codes']=['BINDING_OR_DATA_UNAVAILABLE',str(ex)];out['missing']=['COMPLETE_SAME_MODEL_SOURCE_EVIDENCE']
 return out
