"""Postrun evidence audit plus explicit unchanged-author subset predicates.
Does not invoke semantic kernels or modify the original373 UNKNOWN output.
"""
import copy,hashlib,json,sys
from pathlib import Path
import psutil
P=Path(__file__).resolve().parent;W=P.parent;S=W/'reconstruction357/staging373_current_semantics';sys.path.insert(0,str(S))
from gate373 import load_inputs,validate,D
read=lambda p:json.loads(p.read_text())
original_sha=hashlib.sha256((P/'result.json').read_bytes()).hexdigest();r=read(P/'result.json');i=load_inputs();binding=validate(i['record'],i['fresh'],i['lineage']);F=read(W/'review373_preaudit/source_freeze.json');changed=[n for n,h in F['files'].items()if hashlib.sha256((W/n).read_bytes()).hexdigest()!=h]
s=read(P/'supervision.json');alive=[]
for t in s['tracked_processes']:
 try:
  if abs(psutil.Process(t['pid']).create_time()-t['create_time'])<.001:alive.append(t)
 except psutil.NoSuchProcess:pass
payload=read(P/'input_payload.json');pr=read(P/'preregistration.json')
checks={'full_frozen_sources_and_evidence_unchanged':not changed,'result_current_binding':r['binding']==binding,'payload_exact_current_inputs':all(payload[k]==i[k]for k in ('record','fresh','lineage')),'payload_bytes_unchanged':hashlib.sha256((P/'input_payload.json').read_bytes()).hexdigest()==pr['input_payload_sha256'],'supervision_clean':s['reason']=='COMPLETED'and s['worker_returncode']==0 and s['worker_reaped']and s['cleanup_verified']and not s['unresolved'],'tracked_worker_gone':not alive,'no_kernel_exceptions':r['errors']=={},'eleven_unique_parents':len(r['quality'])==11 and len({x['rule_id']for x in r['quality']})==11,'original_parent_unknown_preserved':all(x['verdict']=='UNKNOWN'for x in r['quality']),'no_old_proof_attestation':r['equivalence_attestation_used']is False and r['old_fixed_artifact_issuers_called']is False,'no_new_fresh':r['new_fresh_checker_executed']is False and r['fresh_review_reused_from372']is True}
e=r['evidence'];eb=r['evidence_bindings']
checks['all_evidence_outer_binding']=set(e)==set(eb)and all(all(eb[k].get(n)==v for n,v in binding.items())and eb[k]['evidence_digest']==D(v) for k,v in e.items())
checks['nine_prerequisites_recomputed_pass']=len(e['nine_prerequisites']['rows'])==9 and all(g['verdict']=='SCOPED_PASS'for g in e['nine_prerequisites']['rows'])
author=read(W/'reconstruction357/semantic_rules357/author_source.json');mapping=e['author_spatial_mapping'];mh=binding['model_digest']
checks['author_contract_unchanged']=hashlib.sha256((W/'owner_four_steps233.html').read_bytes()).hexdigest()==author['html_sha256']and hashlib.sha256((W/'recovered233_rendered/sections.json').read_bytes()).hexdigest()==author['sections_sha256']and mapping['source_html_sha256']==author['html_sha256']and mapping['extracted_sections_sha256']==author['sections_sha256']
checks['four_bound_proofs_computed']=all(x['proof_recomputed']and x['compute_status']=='BOUND_SCOPED_EVIDENCE_RETURNED'for x in r['quality']if x['rule_id']in ('OPENINGS_REAL','LIVING_USEFUL_CONTIGUITY','GUEST_ROUTE_INDEPENDENCE','KITCHEN_PROXIMITY'))
if not all(checks.values()):raise ValueError('AUDIT_BLOCKED:'+str(checks))
# These are the exact complete scoped parent conditions in pinned engine365_v3
# lines61-74, applied to new actual373 recomputation rather than old artifacts.
predicates={
 'OPENINGS_REAL':e['openings'].get('scope_complete')is True and e['openings'].get('codes')==[]and e['openings'].get('missing')==['INDEPENDENT_AUDIT_BEFORE_PARENT_ENABLE'],
 'LIVING_USEFUL_CONTIGUITY':mapping['rules']['Q02'].get('audit_recommendation')=='ELIGIBLE_CURRENT_PROFILE_PARENT_CLOSURE_PENDING_INDEPENDENT_AUDIT',
 'GUEST_ROUTE_INDEPENDENCE':mapping['rules']['Q06'].get('audit_recommendation')=='ELIGIBLE_CURRENT_PROFILE_PARENT_CLOSURE_PENDING_INDEPENDENT_AUDIT',
 'KITCHEN_PROXIMITY':e['kitchen'].get('verdict')=='PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS'and e['kitchen']['evidence'].get('model_hash')==mh}
scopes={
 'OPENINGS_REAL':'Source233 H08/H10/H11 opening-host, aperture, window geometry and required source operation profile only; no technical core or light/ventilation approval',
 'LIVING_USEFUL_CONTIGUITY':'Required source seating/use/access connected by verified source body sweeps; no whole residual-use or aesthetic optimum claim; R-LIV exact trigger N_A',
 'GUEST_ROUTE_INDEPENDENCE':'All four required source guest relations per unit, complete source private exclusion and conservative source kitchen operations; source open-transit profile only; H07 separate',
 'KITCHEN_PROXIMITY':'Q07 required source cooking-to-dining and living essential-use relations with protected guest/private access; sequential source operation profile; optional proximity ranking not claimed'}
quality=copy.deepcopy(r['quality'])
for q in quality:
 rid=q['rule_id']
 if predicates.get(rid):q.update(verdict='PASS',missing=[],scope=scopes[rid],source_closure_digest=D(e[q['evidence_key']]),contract_source_sha256=author['html_sha256'],basis='NEW373_RECOMPUTATION_PLUS_UNCHANGED_AUDITED_SCOPED_PARENT_PREDICATE')
engine=W/'reconstruction357/semantic_rules357/engine365_v3.py'
out={'schema':'373_POSTRUN_AUDITED_SUBSET','original373_result_sha256':original_sha,'original373_result_digest':D(r),'binding':binding,'quality':quality,'exact_predicates':predicates,'predicate_source':str(engine.relative_to(W)),'predicate_source_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'scope':'SCOPED_CURRENT372_ARTIFACT_ONLY; NOT_COMPLETE_QUALIFICATION','remaining_parent_rules':[q['rule_id']for q in quality if q['verdict']!='PASS'],'selected_set_rule':{'rule_id':'DISTINCTNESS_AND_FAIRNESS','verdict':'UNKNOWN','missing':['ACTUAL_NEW_MEMBER_SELECTION_PAIR_AND_Q12_NOT_ESTABLISHED']},'old_proof_pass_reused':False,'accepted':False,'delivery_allowed':False,'test_only':True}
(P/'audited_subset.json').write_text(json.dumps(out,indent=2));checks['original_result_still_immutable']=hashlib.sha256((P/'result.json').read_bytes()).hexdigest()==original_sha
(P/'independent_audit.json').write_text(json.dumps({'all_checks_passed':all(checks.values()),'checks':checks,'frozen_file_count':len(F['files']),'changed':changed,'tracked_alive':alive,'seconds':s['elapsed_seconds'],'subset_predicates':predicates},indent=2));print(json.dumps({'checks':checks,'subset_predicates':predicates,'remaining':out['remaining_parent_rules']},indent=2))
