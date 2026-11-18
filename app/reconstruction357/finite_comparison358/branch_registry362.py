"""Versioned actual producer domain; branch enumeration is not parent acceptance."""
from branch_registry359 import registry,callable_pointer
from active_dispatch_registry361 import build_active_registry
from build_ledger import ROOT,digest,json,hashlib,Path

def artifact(path):
 p=ROOT/path;return json.loads(p.read_text()),{'path':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def notch_lineage():
 old,op=artifact('staging360_core_notch/actual360.json');new,np=artifact('staging362_core_notch/actual362.json')
 of,ofp=artifact('review360_source_validation/result.json');nf,nfp=artifact('review362_source_validation/result.json')
 for r,f in ((old,of),(new,nf)):
  assert digest(r['candidate']['model'])==r['trace']['model_digest']==f['model_digest']==f['raw_report']['model_hash']
  assert f['input_record_digest']==digest(r)
 for k in ('raw','proposal','parent_record_digest','parent_model_digest'):
  assert digest(old['trace'][k])==digest(new['trace'][k]),k
 a=ROOT/'staging360_core_notch/core_variant360.py';b=ROOT/'staging362_core_notch/core_variant362.py'
 assert a.read_text().replace('360','362')==b.read_text(),'CORE_OPERATOR_CHANGED'
 for k in ('inputs','program','profile'):
  assert old['candidate']['model'][k]==new['candidate']['model'][k]
 assert old['candidate']['packet']['core']['notch360']==new['candidate']['packet']['core']['notch362']
 assert nf['fresh_checker_executed']and nf['source_unchanged']
 return {'branch_id':'CORE_SOUTH_LIFT_NOTCH_FIXED359_LINEAGE','same_parent_proposal_raw_and_exact_core_variant':True,'core_variant_only_version_tokens_changed':True,'source_variants':[callable_pointer('staging360_core_notch/core_variant360.py','derive'),callable_pointer('staging362_core_notch/core_variant362.py','derive')],'historical_attempt':{'record':op,'fresh':ofp,'model_digest':of['model_digest'],'raw_status':of['raw_report']['status'],'pending':of['raw_report'].get('pending',[]),'state':'SUPERSEDED_REPRESENTATION_ATTEMPT_NOT_AN_ACCEPTED_ALTERNATIVE','retained':True},'current_attempt':{'record':np,'fresh':nfp,'model_digest':nf['model_digest'],'raw_status':nf['raw_report']['status'],'errors':nf['raw_report'].get('errors',[]),'pending':nf['raw_report'].get('pending',[]),'state':'FRESH_EVALUATED_INTRINSIC_ELIGIBILITY_PENDING'},'representation_delta':'362 rebuild closes exact exposed boundary junction with notch_frame362.outer_right and source frame validator; original360 representation and its unknowns retained, not silently accepted or globally excluded.','source_delta':[callable_pointer('staging362_core_notch/notch_frame362.py','outer_right')],'parent_acceptance':False}

def build():
 r=registry();active=build_active_registry();notch=notch_lineage();branches=[]
 for b in r['branches']:
  if b['id']=='CORE_NOTCH360_FIXED_LINEAGE':branches.append(notch)
  elif b['id']!='LAYOUT_OTHER_SOURCE_TOPOLOGIES':branches.append(b)
 for row in active['branches']:
  q=dict(row);s=q['status'];solver=q['solver_status']
  q['terminal_search_state']=('RESTRICTED_MASTER_INFEASIBLE'if s=='NO_PROPOSAL_IN_THIS_RESTRICTED_MASTER'and solver==2 else 'SOURCE_PRIMITIVE_FIT_UNSUPPORTED'if s=='UNSUPPORTED_BUNDLE_FIT'else 'CONSTRUCTED_REQUIRES_BOUND_COMPARISON'if s=='PROPOSAL_ONLY'else 'UNRESOLVED')
  q['global_infeasibility']=False;branches.append(q)
 unknown=[x['id']for x in branches if x.get('terminal_search_state')=='UNRESOLVED']
 return {'schema':'SOURCE_BACKED_FINITE_BRANCH_REGISTRY362_V1','branches':branches,'active_dispatch_count':active['actual_active_branch_count'],'active_dispatch_enumeration_complete':not unknown,'unresolved_active_dispatch_ids':unknown,'notch_lineage':notch,'historical_not_active':active['historical_not_active'],'historical_exclusion_reason':active['historical_exclusion_reason'],'finite_domain_definition':'Exact source150 runtime tuple with original fixed input; registered fixed357/358/359 transformations; one source114 full-band ownership proof; one fixed359 south-lift-notch branch corrected360→362. No arbitrary continuous door/layout edits or historical files asserted exhausted.','restricted_search_terminal_meaning':'INFEASIBLE proves only the encoded restricted MILP. Unsupported fit proves only this source primitive at fixed frame. Neither establishes global layout impossibility.','branch_enumeration_closed':not unknown,'q04_comparison_closed':False,'remaining':['CURRENT362_INTRINSIC_GATE','CURRENT362_PURPOSE_AND_METRICS','PAIRWISE_SOURCE_FUNCTIONAL_OBJECTIVE_COMPARISON','INDEPENDENT_FINITE_DOMAIN_AUDIT'],'parent_acceptance':False,'global_optimum':False}
if __name__=='__main__':
 x=build();Path(__file__).with_name('branch_registry_actual362_v1.json').write_text(json.dumps(x,ensure_ascii=False,indent=2));print(x['active_dispatch_enumeration_complete'])
