"""Task1.5 evidence comparison only: no weights, Pareto claim or quality winner."""
import copy,hashlib
from fractions import Fraction as F
from front_rear_runtime_adapter import ROOT,transport
from same_version_front_rear_contract import digest,ENGINE_REVISION
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
DENOMINATORS=('gross_unit_ownership_union_m2','net_unit_ownership_minus_actual_wall_solids_m2')
def inventory(m):
 return [{'unit':u['id'],'items':{k:sorted([str(F(q[2])-F(q[0])),str(F(q[3])-F(q[1]))]) for k,q in u['fixtures'].items()}} for u in m['units']]
def compare(a,b,left,right,expected):
 a,_=transport(a);b,_=transport(b);left,_=transport(left);right,_=transport(right);expected,_=transport(expected)
 initial=digest([a,b,left,right,expected]);reasons=[];rows=[]
 producer=ROOT/'app/local_integration/programme_evidence_comparison.py';producer_hash=hashlib.sha256(producer.read_bytes()).hexdigest()
 out={'schema':'PROGRAMME_ALTERNATIVE_EVIDENCE_COMPARISON_V1','status':'NOT_COMPARABLE','quality_comparison':'UNRESOLVED_PROFILE',
  'observed_physical_reports':[copy.deepcopy(r.get('original_physical_report')) if type(r) is dict else None for r in (left,right)],'physical_report_model_digest_bindings':[False,False],
  'winner':None,'pareto_front':None,'quality_scores':None,'measurement_scope':'Metrics read from bound evaluator reports, not independently remeasured by this comparator','models':[digest(a),digest(b)],'reasons':reasons,'comparisons':rows,
  'comparison_source_snapshot':{'app/local_integration/programme_evidence_comparison.py':producer_hash},
  'scope':'Two existing same-request/programme models with equal source evaluator/scenario definitions; evidence deltas only, not programme suitability, ranking or all-PRD qualification.',
  **{k:False for k in AUTH}}
 def need(condition,reason):
  if not condition:reasons.append(reason)
 try:
  need(set(expected)=={'models','reports'},'RECEIPT_KEYS')
  need(expected.get('models')==[digest(a),digest(b)],'MODEL_RECEIPTS')
  need(expected.get('reports')==[digest(left),digest(right)],'REPORT_RECEIPTS')
  need(digest(a)!=digest(b),'DUPLICATE_MODEL_NOT_ALTERNATIVE')
  for k in ('inputs','program','profile','fixture_catalog_hash'):need(digest(a[k])==digest(b[k]),'MISMATCH_'+k.upper())
  need(digest(inventory(a))==digest(inventory(b)),'MISMATCH_FIXTURE_SOURCE_DIMENSIONS')
  need(left['schema']==right['schema']=='CURRENT_LIVING_SOURCE_EVIDENCE_V1','EVALUATOR_VERSION')
  need(digest(left['source_snapshot'])==digest(right['source_snapshot']),'EVALUATOR_SOURCE_MISMATCH')
  required={'app/local_integration/source_living_evaluator.py','app/local_integration/source_guest_route_evaluator.py','app/local_integration/living_connectivity_diagnostic.py','app/local_integration/fixed_route_clearance_diagnostic.py','app/local_integration/kitchen_guest_review.py'}
  need(set(left['source_snapshot'])==required,'EVALUATOR_SOURCE_SET')
  for path,h in left['source_snapshot'].items():
   need(path in required,'EVALUATOR_SOURCE_PATH')
   if path in required:need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,'EVALUATOR_SOURCE_CHANGED:'+path)
  for report_index,(m,r) in enumerate(((a,left),(b,right))):
   need(r['model_digest']==digest(m),'REPORT_MODEL')
   need(r['integrity_verified'] is True and not r.get('missing'),'REPORT_INTEGRITY')
   need(r['state']=='UNKNOWN','EXPECTED_SCOPED_UNKNOWN_EVALUATOR')
   need(r['replay']['verified'] is True and r['replay']['model_hash']==digest(m) and r['replay']['source_revision']==ENGINE_REVISION,'REPORT_REPLAY')
   need(digest(r['profile'])==digest(m['profile']),'REPORT_PROFILE')
   need(all(r.get(k) is False for k in AUTH),'REPORT_AUTHORITY')
   p=r['original_physical_report']
   bound=p['model_hash']==digest(m) and digest(p)==r['original_physical_digest']
   need(bound,'PHYSICAL_REPORT_BINDING');out['physical_report_model_digest_bindings'][report_index]=bound
   need(len(r['units'])==len(m['units']) and {u['unit'] for u in r['units']}=={u['id'] for u in m['units']},'UNIT_SET')
   for u in r['units']:
    for k in DENOMINATORS:need(k in u['area_accounting'] and F(u['area_accounting'][k])>0,'DENOMINATOR_DEFINITION_OR_VALUE')
    need(u['area_accounting']['verified_useful_living_area_m2'] is None,'UNSUPPORTED_USEFUL_AREA_CLAIM')
  if reasons:return out
  for u,v in zip(left['units'],right['units']):
   need(u['unit']==v['unit'],'UNIT_ORDER')
   ids=lambda z:[(e['fixture_id'],e['activity_id']) for e in z['actual_seat_endpoints']]
   need(ids(u)==ids(v),'TARGET_ACTIVITY_BINDING')
   need(len(u['studies'])==len(v['studies']),'SCENARIO_COUNT')
   for s,t in zip(u['studies'],v['studies']):
    need((s['domain'],s['anchor_fixture_id'],s['target_fixture_ids'])==(t['domain'],t['anchor_fixture_id'],t['target_fixture_ids']),'SCENARIO_TARGET_DOMAIN')
    need(len(s['routes'])==len(t['routes']),'ROUTE_TARGET_COUNT')
    for x,y in zip(s['routes'],t['routes']):
     need(x['target_fixture']==y['target_fixture'],'ROUTE_TARGET')
     need(x.get('body_m')==y.get('body_m')==str(F(a['profile']['body_m'])),'BODY_PROFILE')
     need(x['state'] in ('PASS_ACCESS_WITNESS_ONLY','NO_WITNESS_THIS_DOMAIN') and y['state'] in ('PASS_ACCESS_WITNESS_ONLY','NO_WITNESS_THIS_DOMAIN'),'ROUTE_ERROR_NOT_QUALITY')
     row={'unit':u['unit'],'domain':s['domain'],'target_fixture':x['target_fixture'],'left_state':x['state'],'right_state':y['state'],'comparison':'MISSING_WITNESS_NOT_NUMERIC_SUPERIORITY'}
     if x.get('path') and y.get('path') and x['state']==y['state']=='PASS_ACCESS_WITNESS_ONLY':
      row.update(comparison='SAME_DEFINED_METRICS_ONLY',left_length_m=x['length_m'],right_length_m=y['length_m'],
       right_minus_left_length_m=str(F(y['length_m'])-F(x['length_m'])),
       left_direction_changes=x['direction_changes_including_reversal'],right_direction_changes=y['direction_changes_including_reversal'])
     rows.append(row)
  if reasons:out['comparisons']=[];return out
  out['status']='COMPARABLE_SCOPED_EVIDENCE_NOT_QUALITY_RANKING'
  out['physical_statuses']=[r['original_physical_report']['status'] for r in (left,right)]
  out['physical_failure_preserved']=[bool(r['original_physical_report']['errors']) for r in (left,right)]
  out['original_physical_reports']=[copy.deepcopy(r['original_physical_report']) for r in (left,right)]
  out['report_digests']=[digest(left),digest(right)]
  out['denominator_semantics']=list(DENOMINATORS)
  out['source_snapshot']=copy.deepcopy(left['source_snapshot'])
  out['quality_gaps']=['No calibrated per-room/unit quality floors and acceptance anchors','No approved quality dimensions/directions/weights for Pareto','Route counts/lengths cannot turn physical FAIL or profile UNKNOWN into acceptance']
 except Exception as ex:
  reasons.append('COMPARISON_INPUT_OR_EVALUATOR_ERROR:'+type(ex).__name__+':'+str(ex));out['comparisons']=[];out['status']='NOT_COMPARABLE'
 finally:
  if digest([a,b,left,right,expected])!=initial:raise ValueError('COMPARISON_INPUT_MUTATION')
  if hashlib.sha256(producer.read_bytes()).hexdigest()!=producer_hash:raise ValueError('COMPARISON_PRODUCER_CHANGED')
  for path,h in left.get('source_snapshot',{}).items():
   if path in ('app/local_integration/source_living_evaluator.py','app/local_integration/source_guest_route_evaluator.py','app/local_integration/living_connectivity_diagnostic.py','app/local_integration/fixed_route_clearance_diagnostic.py','app/local_integration/kitchen_guest_review.py') and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=h:
    out['status']='NOT_COMPARABLE';out['comparisons']=[];reasons.append('SOURCE_CHANGED_DURING_COMPARISON')
 return out
