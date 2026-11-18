"""Current two-member selection is conditional on actual qualification proofs."""
import json,sys
from pathlib import Path
from guard387 import guard
from contract387 import validate_member_folder,digest,partial,clean,ROOT
P=Path(sys.argv[1]);expected=sys.argv[2];guard(expected)
PARENTS={'SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY'}
def qualifies(q):
 return q.get('qualified')is True and q.get('cohort_closed')is True and q.get('q12_verdict')=='PASS'and set(q.get('parent_verdicts',{}))==PARENTS and all(v=='PASS'for v in q['parent_verdicts'].values())and not q.get('missing')
inputs={k:validate_member_folder(P/k,expected,require_physical_pass=False)for k in('balanced','joint')};semantics={};members=[]
for kind,i in inputs.items():
 d=P/kind;s=json.loads((d/'semantics_supervision.json').read_text());r=json.loads((d/'semantics_worker_receipt.json').read_text());v=json.loads((d/'semantic.json').read_text())
 if not clean(s)or r.get('semantic_digest')!=digest(v)or r.get('record_digest')!=i['binding']['record_digest']or r.get('fresh_digest')!=i['binding']['fresh_digest']or r.get('run_id')!=P.name or r.get('kind')!=kind or v.get('binding')!=i['binding']:raise ValueError('CURRENT_SEMANTIC_RECEIPT:'+kind)
 semantics[kind]=v;members.append({'kind':kind,'binding':i['binding'],'model':i['record']['candidate']['model'],'physical_review_status':i['fresh']['raw_report']['status'],'errors':i['fresh']['raw_report']['errors'],'pending':i['fresh']['raw_report']['pending'],'original_pending':i['fresh']['raw_report'].get('original_pending',[]),'qualification':v.get('qualification',{'qualified':False,'missing':['SEMANTIC_PROOF_INCOMPLETE']}),'semantic_artifact_digest':digest(v)})
a,b=[inputs[k]for k in('balanced','joint')]
for key in('raw_digest','canonical_request_digest','received_digest','transport_body_sha256','program_digest','profile_digest','input_digest'):
 if a['binding'][key]!=b['binding'][key]:raise ValueError('SHARED_BRIEF_PROGRAM:'+key)
if a['binding']['candidate_id']==b['binding']['candidate_id']or a['binding']['review_id']==b['binding']['review_id']:raise ValueError('DISTINCT_MEMBER_IDENTITIES')
sys.path.insert(0,str(ROOT/'planha_general150_runtime_work'));sys.path.insert(0,str(ROOT/'staging367_pair_scope'))
from three_access_diversity133 import access_signature
from pair_scope import canonical_signature
sig={k:access_signature(i['record']['candidate']['model'])for k,i in inputs.items()};canonical={k:canonical_signature(v['signature'])for k,v in sig.items()};distinct=canonical['balanced']!=canonical['joint']
physical_pass=all(m['physical_review_status']=='PASS_CONCEPT_SCOPED_REVIEW'and m['errors']==[]and m['pending']==[]for m in members)
qualified=physical_pass and all(qualifies(m['qualification'])for m in members)and distinct
out=partial('COMPLETED_CURRENT_TWO_BUILDER_REVIEW',P.name);out.update(tested_branch_count=2,members=members,
 binding={'run_id':P.name,**{k:a['binding'][k]for k in('raw_digest','canonical_request_digest','received_digest','transport_body_sha256')}},
 semantic_state='PASS_SCOPED_CURRENT_SET'if qualified else'UNKNOWN_CURRENT_DEPENDENCIES',qualified_selected_set=qualified,request_fulfilled=qualified,
 scope='FIXED26X28_N2_COUNT2_REGISTERED_PROGRAM_FINITE_COHORT_CONCEPT_ONLY',global_domain_complete=False,technical_accepted=False,
 selected_set=[m['binding']for m in members]if qualified else[],qualified_selected_count=2 if qualified else 0,
 current_physical_pass_for_all_members=physical_pass,
 pair={'source_organization_distinct':distinct,'signatures':canonical,'witnesses':{k:v['witness']for k,v in sig.items()},'source_kernel':'three_access_diversity133.access_signature','does_not_substitute_member_quality':True},
 seal={'members':[{'binding_digest':digest(m['binding']),'semantic_digest':m['semantic_artifact_digest']}for m in members],'qualified':qualified,'run_id':P.name,'immutable_membership_digest':digest([m['binding']for m in members])})
guard(expected)
with(P/'result.json').open('x')as f:json.dump(out,f,ensure_ascii=False,indent=2)
