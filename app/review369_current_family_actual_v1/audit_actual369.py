import collections,hashlib,json,sys,zipfile
from pathlib import Path
import psutil
W=Path(__file__).resolve().parent.parent; P=Path(__file__).resolve().parent
sys.path.insert(0,str(W/'staging369_current_family_repair'))
from operator369 import digest,protected,rect,overlap
load=lambda p:json.loads(p.read_text())
freeze=W/'review369_current_family_preaudit/controlled_source_freeze.json'
F=load(freeze); changed=[n for n,h in F['files'].items() if hashlib.sha256((W/n).read_bytes()).hexdigest()!=h]
r=load(P/'fixture_record.json');f=load(P/'fresh_first.json');b=load(P/'fixture_binding.json');c=load(P/'cycle_result.json');t=r['trace'];pr=f['provenance'];raw=f['raw_report'];parent=load(W/'reconstruction357/staging369_controlled_cycle/parent368.json');req=load(W/'reconstruction357/staging369_controlled_cycle/request368.json')
checks={'freeze_hash':hashlib.sha256(freeze.read_bytes()).hexdigest()=='e13b3957bf7c66678e815060582b97b0224bf754cdc0233688a572cd4407676c','all10221_sources_unchanged':not changed,'immutable_embedded_parent':r['parent_record']==parent,'parent_binding':t['parent_record_digest']==digest(parent)==pr['parent_record_digest'],'raw_request_continuity':digest(r['candidate']['request'])==req['raw_digest'],'program_identity_ownership_preserved':protected(r)==protected(parent),'actual_current_model_changed':r['candidate']['model_digest']!=parent['candidate']['model_digest'],'fresh_current_model_binding':f['model_digest']==raw['model_hash']==digest(r['candidate']['model'])==b['model_digest'],'fresh_record_binding':f['input_record_digest']==digest(r)==b['record_digest']==pr['input_record_digest'],'fresh_review_binding':b['review_id']==f['review_id']==c['first_review_id'] and b['fresh_digest']==digest(f),'candidate_id_binding':b['candidate_id']==digest({'run_id':c['run_id'],'model_digest':f['model_digest'],'kind':'TEST_ONLY_DERIVED_BALANCED369'}),'provenance_verified':pr['verified'] is True,'registry_built_before_evaluate':f['expected_method_registry']['built_before_evaluate'] is True,'fresh_checker_executed':f['fresh_checker_executed'] is True,'no_prior_quality_reuse':f['prior_quality_certificates_reused'] is False,'test_only_inherited':r['test_only'] and f['test_only'] and c['test_only'],'repair_not_attempted':c['repair_attempted'] is False and c['fresh_count']==1,'strict_gate_blocked':c['status']=='STRICT_REJECTION_GATE_BLOCKED','raw_unknown_preserved':'VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED' in raw['original_pending'] and raw['not_evaluated']==raw['original_pending']}
collisions=[]
for u in r['candidate']['model']['units']:
 if overlap(rect(u['fixtures']['sofa1']),rect(u['fixtures']['armchair2'])):collisions.append(u['id'])
checks['declared_collision_real']='A' in collisions
alive=[];supervisions={}
for p in P.glob('*_supervision.json'):
 s=load(p);supervisions[p.name]=s
 checks[p.stem+'_clean']=s['cleanup_verified'] and s['worker_reaped'] and not s['unresolved'] and s['reason']=='COMPLETED' and s['worker_returncode']==0
 for x in s['tracked_processes']:
  try:
   proc=psutil.Process(x['pid'])
   if abs(proc.create_time()-x['create_time'])<0.001:alive.append(x)
  except psutil.NoSuchProcess:pass
checks['tracked_processes_gone']=not alive
with zipfile.ZipFile(W/'independent368actual/checkpoint368_actual_one_shot.zip')as z:
 checks['parent_matches_original_actual368']=json.loads(z.read('368_actual_evidence/program_receipts/bridge_run/balanced/constructed.json'))==parent
out={'all_checks_passed':all(checks.values()),'checks':checks,'source_count':len(F['files']),'changed_sources':changed,'tracked_processes_still_alive':alive,'collision_units':collisions,'error_codes':dict(collections.Counter(x['code']for x in raw['errors'])),'failed_rules':[x.get('requirement_id')for x in raw['errors']if x['code']=='RULE_FAILED'],'pending_count':len(raw['pending']),'original_pending':raw['original_pending'],'not_evaluated':raw['not_evaluated'],'run_id':c['run_id'],'parent_model_digest':parent['candidate']['model_digest'],'current_model_digest':f['model_digest'],'current_review_id':f['review_id'],'candidate_id':b['candidate_id'],'protected_snapshot_digest':digest(protected(r))}
(P/'independent_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert out['all_checks_passed']
