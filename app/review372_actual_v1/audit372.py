"""Post-run independent immutable evidence checks; no replay or reviewer execution."""
import json,hashlib,sys,collections
from pathlib import Path
import psutil
P=Path(__file__).resolve().parent;W=P.parent;A=W/'review369_current_family_actual_v1';S=W/'reconstruction357/staging372_route_aware_repair'
sys.path.insert(0,str(S))
from operator372 import digest,protected,rect,overlap
read=lambda p:json.loads(p.read_text())
F=read(W/'review372_preaudit/source_freeze.json');changed=[n for n,h in F['files'].items()if hashlib.sha256((W/n).read_bytes()).hexdigest()!=h]
checks={'all_frozen_sources_and_prior_evidence_unchanged':not changed}
prior=read(A/'fixture_record.json');before=read(A/'fresh_first.json');b=read(A/'fixture_binding.json');plan=read(P/'plan.json');result=read(P/'cycle_result.json')
checks.update(before_raw_carried_unchanged=plan['before_raw_report']==before['raw_report'],before_review_binding=plan['parent_fresh_digest']==digest(before) and plan['parent_binding']==b,prior_record_binding=plan['parent_record_digest']==digest(prior))
tracked=[]
for p in P.glob('*_supervision.json'):
 s=read(p);checks[p.stem+'_clean']=s['reason']=='COMPLETED'and s['worker_returncode']==0 and s['worker_reaped']and s['cleanup_verified']and not s['unresolved']
 for t in s['tracked_processes']:
  try:
   if abs(psutil.Process(t['pid']).create_time()-t['create_time'])<.001:tracked.append(t)
  except psutil.NoSuchProcess:pass
checks['tracked_processes_gone']=not tracked
out={'checks':checks,'changed_sources_or_evidence':changed,'frozen_file_count':len(F['files']),'tracked_remaining':tracked,'actual_operator':plan['operator'],'before_error_counts':dict(collections.Counter(e['code']for e in before['raw_report']['errors'])),'before_pending':before['raw_report']['pending'],'before_original_pending':before['raw_report']['original_pending'],'result_status':result['status']}
if (P/'fresh.json').exists():
 child=read(P/'repaired_record.json');after=read(P/'fresh.json');lineage=read(P/'reviewed_lineage.json');raw=after['raw_report']
 checks.update(protected_fields_equal=protected(prior)==protected(child),input_request_equal=prior['candidate']['request']==child['candidate']['request'],new_model=after['model_digest']!=before['model_digest'],new_review=after['review_id']!=before['review_id'],child_model_binding=after['model_digest']==digest(child['candidate']['model'])==raw['model_hash']==lineage['model_digest'],child_record_binding=after['input_record_digest']==digest(child)==lineage['record_digest'],lineage_parent_binding=lineage['parent_review_id']==before['review_id']and lineage['parent_fresh_digest']==digest(before)and lineage['parent_candidate_id']==b['candidate_id'],lineage_review_binding=lineage['review_id']==after['review_id']and lineage['fresh_digest']==digest(after),fresh_replayed=after['fresh_checker_executed']and after['provenance']['verified']and after['source_unchanged'],no_semantic_reuse=after['prior_quality_certificates_reused']is False,test_only=child['test_only']and after['test_only'],no_acceptance=not result['accepted']and not after['accepted']and not result['delivery_allowed'])
 pairs=plan['operator']['pair'];collisions=[u['id']for u in child['candidate']['model']['units']if overlap(rect(u['fixtures'][pairs[0]]),rect(u['fixtures'][pairs[1]]))]
 out.update(after_error_counts=dict(collections.Counter(e['code']for e in raw['errors'])),after_pending=raw['pending'],after_original_pending=raw['original_pending'],collision_units_remaining=collisions,parent_model_digest=before['model_digest'],current_model_digest=after['model_digest'],current_review_id=after['review_id'],current_candidate_id=lineage['candidate_id'],current_raw_status=raw['status'])
out['all_checks_passed']=all(checks.values())
(P/'independent_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
