"""Run-specific semantic bridge for the closed fixed368 producer pipeline.
Internal callable only, in a separately pinned isolated worker after four real
source phases. No browser-supplied proof flags, paths or cached model output.
"""
import json,hashlib,copy,uuid,types,os,sys
from pathlib import Path
from equivalence import digest,compare,attest_proofs
from predicates import evaluate as current_predicates
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
REFERENCE_SHA='75c492c6622dd5db962ebed34fb81a1723c99b9c4459b244fc4528d6068aef72'

PIPELINE_PINS={'source_freeze.json':'0698f0958a23e2e882c60ff06e58490db01ed5fcaee084eb1d64318ff51046fa','pipeline.py':'084cbc912d68435de7614097001bf251fa3d6a123e5597d48932bfe60d9dc0c7','worker368.py':'21154e7037ccd648868d5a0a3367987c0e74a805179fd4abe1a6e83ebc9451de','model_binding368.py':'558f5f79923352268ce64c7ac80ba45ca13fba9d5b6e1daff65e3a524f8d7d84','request_contract368.py':'86a5f52df95cae6d56b3c8d8246d8ea14b1f0cc9ae1c61b7b6ac759530404fab'}
def verify_pipeline_sources():
 p=ROOT/'staging368_final_pipeline'
 for n,h in PIPELINE_PINS.items():
  if hashlib.sha256((p/n).read_bytes()).hexdigest()!=h:raise ValueError('PREREGISTERED_EXECUTION_SOURCE_CHANGED:'+n)
 for n,h in json.loads((p/'source_freeze.json').read_text())['files'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('PIPELINE_TRANSITIVE_SOURCE_CHANGED:'+n)

def _references():
 p=HERE/'reference_registry.json';b=p.read_bytes()
 if hashlib.sha256(b).hexdigest()!=REFERENCE_SHA:raise ValueError('PREREGISTERED_REFERENCE_CHANGED')
 reg=json.loads(b);cap={}
 for n,h in reg['sources'].items():
  data=(ROOT/n).read_bytes()
  if hashlib.sha256(data).hexdigest()!=h:raise ValueError('REFERENCE_SOURCE_POLICY_CHANGED:'+n)
  cap[n]=data;canon=os.path.relpath((ROOT/n).resolve(),ROOT.resolve())
  if canon in cap and cap[canon]!=data:raise ValueError('REFERENCE_ALIAS_CONFLICT')
  cap[canon]=data
 if digest(reg['sources'])!=reg['source_contract_cohort_policy_digest']:raise ValueError('POLICY_SUPERSET_DIGEST')
 return reg,cap

def _module(cap,path,name):
 mod=types.ModuleType(name);mod.__file__=str(ROOT/path);exec(compile(cap[path],str(ROOT/path),'exec'),mod.__dict__);return mod

def validate_execution(run_id,kind,envelope,record,fresh,binding,construct,review,supervisions,pipeline_receipt):
 # This content validation supplements, not replaces, trusted worker invocation.
 sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
 from request_contract368 import verify
 from model_binding368 import bind
 e=verify(envelope);actual=bind(envelope,record,kind,run_id)
 if actual!=binding:raise ValueError('RUN_CANDIDATE_BINDING_CHANGED')
 if pipeline_receipt.get('schema')!='FINAL_PIPELINE368_RUN'or pipeline_receipt.get('status')!='REVIEWED_NOT_QUALIFIED'or pipeline_receipt.get('generation_run_id')!=run_id:raise ValueError('FOUR_STAGE_PIPELINE_NOT_COMPLETED')
 expected={'canonical_request_digest':e['canonical_request_digest'],'raw_digest':e['raw_digest'],'received_digest':e['received_digest']}
 if any(pipeline_receipt.get(k)!=v for k,v in expected.items()):raise ValueError('PIPELINE_REQUEST_BINDING')
 matches=[m for m in pipeline_receipt['members']if m['kind']==kind]
 if len(matches)!=1 or matches[0]['construct']!=construct or matches[0]['review']!=review:raise ValueError('PIPELINE_PHASE_RECEIPT_BINDING')
 for phase,receipt in [('construct',construct),('review',review)]:
  if receipt.get('generation_run_id')!=run_id or receipt.get('binding')!=binding or receipt.get('run_specific_receipt')is not True or receipt.get('source_unchanged')is not True:raise ValueError('CURRENT_PHASE_RUN_BINDING:'+phase)
  if any(receipt.get(k)!=v for k,v in expected.items()):raise ValueError('CURRENT_PHASE_REQUEST_BINDING:'+phase)
  if receipt.get('source_record_digest')!=digest(record):raise ValueError('CURRENT_PHASE_RECORD_BINDING:'+phase)
  sup=supervisions[phase]
  if sup.get('reason')!='COMPLETED'or type(sup.get('worker_returncode'))is not int or sup['worker_returncode']!=0 or sup.get('cleanup_verified')is not True or sup.get('worker_reaped')is not True or sup.get('unresolved')!=[]:raise ValueError('CURRENT_PHASE_SUPERVISION:'+phase)
 if construct.get('phase')!='reconstructed_and_replayed'or construct.get('actual_construct_executed')is not True or construct.get('actual_replay_executed')is not True or construct.get('cached_model_returned')is not False:raise ValueError('REAL_CONSTRUCTION_REPLAY_REQUIRED')
 if review.get('phase')!='review_completed'or review.get('checker_executed')is not True or fresh.get('fresh_checker_executed')is not True:raise ValueError('REAL_CURRENT_CHECKER_REQUIRED')
 if review.get('fresh_result_digest')!=digest(fresh)or review.get('expected_registry_digest')!=digest(fresh['expected_method_registry']):raise ValueError('OWN_FRESH_REGISTRY_BINDING')
 rid=review['review_id']
 if str(uuid.UUID(rid))!=rid:raise ValueError('CANONICAL_REVIEW_UUID')
 return {'run_id':run_id,'candidate_id':binding['candidate_id'],'review_id':rid,'model_digest':binding['model_digest'],'record_digest':digest(record),'fresh_digest':digest(fresh),'packet_digest':binding['packet_digest'],'binding_digest':digest(binding),'construct_receipt_digest':digest(construct),'review_receipt_digest':digest(review),'supervision_digests':{k:digest(v)for k,v in supervisions.items()},**expected}

def decode_current_review(record,fresh,kind,reference_registry,cap):
 # Internal only: validate_execution and pinned isolated invocation precede this.
 # No old PASS equivalence is required to preserve a genuine current rejection.
 old=json.loads(cap[reference_registry['members'][kind]['paths']['fresh']])
 if fresh.get('expected_method_registry')!=old['expected_method_registry'] or fresh['expected_method_registry'].get('built_before_evaluate')is not True:raise ValueError('CURRENT_REJECTION_METHOD_REGISTRY')
 c=record['candidate'];p=fresh['provenance'];mh=digest(c['model'])
 if fresh.get('source_unchanged')is not True or fresh.get('model_digest')!=mh or fresh.get('input_record_digest')!=digest(record)or fresh.get('outer_trace_digest')!=digest(record['trace']):raise ValueError('CURRENT_REJECTION_ARTIFACT_BINDING')
 if p.get('verified')is not True or p['candidate_digest']!=digest(c)or p['packet_digest']!=digest(c['packet'])or p['model_hash']!=mh or p['raw']!=c['request']:raise ValueError('CURRENT_REJECTION_PROVENANCE')
 cm=_module(cap,'semantic_rules357/common.py','_current368_rejection_common');cm.REGISTRY_NAME='method_registry_source365.json'if kind=='balanced'else'method_registry_source367.json'
 raw=fresh['raw_report'];bound=cm.rows(c['model'],raw);errors=raw.get('errors');pending=raw.get('pending');status=raw.get('status')
 if type(errors)is not list or type(pending)is not list or status not in ('FAIL','NOT_EVALUATED','PASS_CONCEPT_SCOPED_REVIEW'):raise ValueError('UNSUPPORTED_CURRENT_REVIEW_SCHEMA')
 if status=='FAIL':
  if not errors:raise ValueError('FAIL_WITHOUT_SOURCE_ERRORS')
  for e in errors:
   if type(e)is not dict or type(e.get('code'))is not str or not e['code']:raise ValueError('UNSTRUCTURED_CURRENT_ERROR')
   if e['code']=='RULE_FAILED':
    row=bound.get(e.get('requirement_id'),{});ev=row.get('evidence',{})
    if row.get('status')!='FAIL'or ev.get('status')!='FAIL'or row.get('mandatory')is not True or ev.get('witness')!=e.get('witness'):raise ValueError('RULE_FAILED_WITHOUT_BOUND_WITNESS')
  return {'status':'REJECTED_UNSUPPORTED_REDESIGN','reasons':copy.deepcopy(errors),'pending':copy.deepcopy(pending),'supported_repair_operators':[],'model_digest':mh,'fresh_digest':digest(fresh),'scope':'Actual current physical/source rejection; no automatic repair operator registered for this fixed workflow.'}
 if errors:raise ValueError('NONFAIL_WITH_ERRORS')
 if status=='NOT_EVALUATED':return {'status':'UNKNOWN','reasons':['CURRENT_CHECKER_NOT_EVALUATED'],'pending':copy.deepcopy(pending),'supported_repair_operators':[],'model_digest':mh,'fresh_digest':digest(fresh)}
 if pending:raise ValueError('PASS_WITH_PENDING')
 return {'status':'PHYSICAL_SCOPED_REVIEW_COMPLETE','model_digest':mh,'fresh_digest':digest(fresh)}

def seal_current_dag(original_roles,run_binding,equivalence,groups,proofs):
 original=original_roles['nodes'];order=original_roles['topological_order'];dag={k:list(v['depends_on'])for k,v in original.items()};nodes={}
 # Retain old hashes; do not change the old proof's record/fresh identity.
 for k in order:
  deps=dag[k]
  if any(d not in nodes for d in deps):raise ValueError('CURRENT_DAG_ORDER')
  if k!='Q14_SELECTION_SET'and(not original[k]['status'].startswith('PASS_')or original[k]['blocking_dependencies']):raise ValueError('OLD_ROLE_NOT_CLOSED:'+k)
  nodes[k]={'status':'UNKNOWN_CURRENT_SET_NOT_ISSUED'if k=='Q14_SELECTION_SET'else'PASS_SCOPED_EQUIVALENT_SOURCE_ROLE_CURRENT_PREREQUISITES','original_node_digest':digest(original[k]),'run_binding_digest':digest(run_binding),'current_fresh_digest':run_binding['fresh_digest'],'reference_fresh_digest':equivalence['reference_fresh_digest'],'equivalence_digest':digest(equivalence),'current_groups_digest':digest(groups),'depends_on':deps,'sealed_dependency_digests':{d:digest(nodes[d])for d in deps}}
 oldq12=original['Q12_PER_UNIT'];units=[]
 for u in oldq12['evidence']:
  if u['exact_pending']:raise ValueError('REFERENCE_Q12_PENDING')
  units.append({'unit':u['unit'],'verdict':'PASS_SCOPED_PER_UNIT_Q12_CURRENT_EQUIVALENT_SOURCE','original_unit_evidence_digest':digest(u),'model_digest':run_binding['model_digest'],'run_id':run_binding['run_id'],'candidate_id':run_binding['candidate_id'],'review_id':run_binding['review_id'],'fresh_digest':run_binding['fresh_digest'],'missing':[],'current_role_node_digest':digest(nodes['Q12_PER_UNIT'])})
 verify_current_seals(nodes,order)
 return{'schema':'CURRENT368_ROLE_ATTESTATION_DAG','stage':'PRE_SELECTION_MEMBER_PREREQUISITES','nodes':nodes,'topological_order':order,'q12':units,'reference_roles_digest':digest(original_roles),'parent_attestation_digests':{x['rule_id']:digest(x)for x in proofs},'scope':'Current prerequisite/identity attestations with explicit equivalent-source proof reuse; original DAG and receipts retained unchanged.'}

def verify_current_seals(nodes,order):
 if len(set(order))!=len(nodes)or set(order)!=set(nodes):raise ValueError('CURRENT_DAG_NODE_INVENTORY')
 seen=set()
 for k in order:
  n=nodes[k]
  if any(d not in seen for d in n['depends_on']):raise ValueError('CURRENT_DAG_TOPOLOGY')
  if n['sealed_dependency_digests']!={d:digest(nodes[d])for d in n['depends_on']}:raise ValueError('CURRENT_DAG_STALE_SEAL')
  seen.add(k)
 return True

def qualify_run(run_folder,envelope,pipeline_receipt):
 caller_envelope=envelope;caller_pipeline=pipeline_receipt;input_digest=digest([envelope,pipeline_receipt]);envelope=copy.deepcopy(envelope);pipeline_receipt=copy.deepcopy(pipeline_receipt)
 folder=Path(run_folder).resolve();run_id=folder.name
 out={'schema':'CURRENT_RUN_SEMANTIC_QUALIFICATION368','status':'UNKNOWN','generation_run_id':run_id,'missing':[],'members':[],'accepted':False,'delivery_allowed':False,'global_domain_complete':False,'new_fresh_execution_by_bridge':False,'proof_mode':'CURRENT_FRESH_AND_NINE_PREDICATES_PLUS_EXPLICIT_EQUIVALENT_SOURCE_PROOF_REUSE'}
 try:
  if str(uuid.UUID(run_id))!=run_id or folder.parent!=(ROOT/'review368_runs').resolve():raise ValueError('FIXED_INTERNAL_RUN_DIRECTORY')
  verify_pipeline_sources();reg,cap=_references();issuer=_module(cap,'staging367_qualified_set/issuer.py','_reference368_issuer')
  outer_snapshots={n:hashlib.sha256((folder/n).read_bytes()).hexdigest()for n in ('request.json','result.json')}
  request=json.loads((folder/'request.json').read_text())
  if request!={'run_id':run_id,'envelope':envelope}:raise ValueError('RUN_REQUEST_ENVELOPE')
  if digest(json.loads((folder/'result.json').read_text()))!=digest(pipeline_receipt):raise ValueError('FIXED_PHYSICAL_PIPELINE_RECEIPT')
  if {m['kind']for m in pipeline_receipt['members']}!={'balanced','joint'}or len(pipeline_receipt['members'])!=2:raise ValueError('TWO_CURRENT_PHASE_MEMBERS')
  snapshots={};current=[]
  for kind in('balanced','joint'):
   d=folder/kind;names=('constructed','fresh','binding','construct_receipt','review_receipt','construct_supervision','review_supervision');vals={k:json.loads((d/(k+'.json')).read_text())for k in names};snapshots[kind]={k:digest(v)for k,v in vals.items()}
   r,f=vals['constructed'],vals['fresh'];rb=validate_execution(run_id,kind,envelope,r,f,vals['binding'],vals['construct_receipt'],vals['review_receipt'],{k:vals[k+'_supervision']for k in('construct','review')},pipeline_receipt)
   decoded=decode_current_review(r,f,kind,reg,cap)
   if decoded['status']!='PHYSICAL_SCOPED_REVIEW_COMPLETE':
    verify_pipeline_sources();_references()
    if any(hashlib.sha256((folder/n).read_bytes()).hexdigest()!=h for n,h in outer_snapshots.items()):raise ValueError('REJECTION_RUN_ARTIFACT_CHANGED')
    for seen,files in snapshots.items():
     for name,h in files.items():
      if digest(json.loads((folder/seen/(name+'.json')).read_text()))!=h:raise ValueError('REJECTION_MEMBER_ARTIFACT_CHANGED')
    if digest([caller_envelope,caller_pipeline])!=input_digest:raise ValueError('REJECTION_CALLER_MUTATION')
    out.update(status=decoded['status'],missing=decoded['reasons'],current_rejection={'kind':kind,'binding':rb,**decoded},supported_repair_operators=[]);return out
   paths=reg['members'][kind]['paths'];oldr,oldf,q,man=[json.loads(cap[paths[k]])for k in ('record','fresh','qualification','manifest')]
   member='balanced365'if kind=='balanced'else'joint367';issuer.verify_whole_dag(member,q,cap);issuer.validate_member(member,oldr,oldf,q,man)
   eq=compare(oldr,oldf,r,f);groups=current_predicates(r,f,kind,reg);proofs=attest_proofs(q['quality'],reg['members'][kind]['proof_maps'],eq,groups,rb,reg['source_contract_cohort_policy_digest'])
   oldroles=q['roles']if kind=='balanced'else q['source_closures']['final_role'];dag=seal_current_dag(oldroles,rb,eq,groups,proofs)
   quality=[{'rule_id':p['rule_id'],'verdict':'PASS','missing':[],'model_hash':rb['model_digest'],'run_id':run_id,'candidate_id':rb['candidate_id'],'review_id':rb['review_id'],'current_fresh_digest':rb['fresh_digest'],'source_closure':p,'scope':p['scope']}for p in proofs]
   current.append({'kind':kind,'binding':rb,'equivalence':eq,'current_groups':groups,'current_roles':dag,'quality':quality,'reference_qualification_digest':digest(q),'reference_model_only_used_as_comparison_oracle':True})
  if len({m['binding']['review_id']for m in current})!=2 or len({m['binding']['candidate_id']for m in current})!=2:raise ValueError('CURRENT_IDENTITIES_DISTINCT')
  # Source pair proof is invariant under identical full model/program/profile.
  # Recompute its actual source signature on the current records in next stage;
  # no fixed-set receipt alone qualifies these new run identities.
  if any(any(m['binding'][k]!=pipeline_receipt[k]for k in ('canonical_request_digest','raw_digest','received_digest'))for m in current):raise ValueError('SET_MEMBER_REQUEST_BINDING')
  pair=current_pair(folder,current,reg,cap)
  selected={'schema':'CURRENT_RUN_FIXED_TWO_MEMBER_SET368','generation_run_id':run_id,'canonical_request_digest':pipeline_receipt['canonical_request_digest'],'raw_digest':pipeline_receipt['raw_digest'],'normalized_raw_digest':pipeline_receipt['raw_digest'],'received_digest':pipeline_receipt['received_digest'],'requested_count':2,'qualified_selected_count':2,'members':[{'binding':m['binding'],'eleven_attestations_digest':digest(m['quality']),'q12_digest':digest(m['current_roles']['q12'])}for m in current],'pair':pair,'membership_authority':True,'membership_scope':'CURRENT_FIXED26X28_N2_COUNT2_CONCEPTUAL_SOURCE_ONLY','accepted':False,'delivery_allowed':False,'global_domain_complete':False}
  selected['set_digest']=digest(selected)
  for m in current:m['quality'].append({'rule_id':'DISTINCTNESS_AND_FAIRNESS','verdict':'PASS','missing':[],'model_hash':m['binding']['model_digest'],'run_id':run_id,'candidate_id':m['binding']['candidate_id'],'review_id':m['binding']['review_id'],'current_fresh_digest':m['binding']['fresh_digest'],'source_closure':{'current_set_digest':selected['set_digest'],'current_pair_digest':digest(pair),'independent_current_q12_digest':digest(m['current_roles']['q12'])},'scope':'Current fixed request/source-model pair and independently attested per-unit role evidence; not all-domain or delivery approval.'})
  for kind,files in snapshots.items():
   for name,h in files.items():
    if digest(json.loads((folder/kind/(name+'.json')).read_text()))!=h:raise ValueError('RUN_ARTIFACT_CHANGED_DURING_QUALIFICATION')
  for n,h in outer_snapshots.items():
   if hashlib.sha256((folder/n).read_bytes()).hexdigest()!=h:raise ValueError('RUN_REQUEST_OR_PIPELINE_RECEIPT_CHANGED')
  if digest([caller_envelope,caller_pipeline])!=input_digest:raise ValueError('CALLER_INPUT_MUTATION')
  verify_pipeline_sources();_references();out.update(status='QUALIFIED_FIXED_CURRENT_RUN',members=current,qualified_set=selected,canonical_request_digest=pipeline_receipt['canonical_request_digest'],raw_digest=pipeline_receipt['raw_digest'],received_digest=pipeline_receipt['received_digest'])
 except (ValueError,KeyError,TypeError,IndexError,OSError,OverflowError)as e:out['missing']=[str(e)];out['members']=[]
 return out

def current_pair(folder,members,registry,cap):
 import builtins
 rt=ROOT/'planha_general150_runtime_work';loaded={}
 def load(name):
  if name in loaded:return loaded[name]
  key='planha_general150_runtime_work/'+name+'.py'
  if key not in cap:raise ValueError('UNREGISTERED_CURRENT_PAIR_SOURCE:'+key)
  mod=types.ModuleType('_current368_pair_'+name);mod.__file__=str(ROOT/key);loaded[name]=mod
  def imp(n,g=None,l=None,fromlist=(),level=0):
   if level==0 and(rt/(n+'.py')).exists():return load(n)
   return builtins.__import__(n,g,l,fromlist,level)
  mod.__dict__['__builtins__']={**vars(builtins),'__import__':imp};exec(compile(cap[key],str(ROOT/key),'exec'),mod.__dict__);return mod
 algorithm=load('three_access_diversity133').access_signature
 canonical=_module(cap,'staging367_pair_scope/pair_scope.py','_current368_pair_normalizer').canonical_signature
 out=[];models=[]
 for member in members:
  r=json.loads((folder/member['kind']/'constructed.json').read_text());model=r['candidate']['model'];b=member['binding']
  if digest(model)!=b['model_digest']or digest(r)!=b['record_digest']:raise ValueError('CURRENT_PAIR_RUN_MODEL_BINDING')
  signature=algorithm(model);out.append({'kind':member['kind'],'generation_run_id':b['run_id'],'candidate_id':b['candidate_id'],'review_id':b['review_id'],'model_digest':digest(model),'current_fresh_digest':b['fresh_digest'],'source_signature':canonical(signature['signature']),'witness':signature['witness']});models.append(model)
 for k in('inputs','program','profile'):
  if digest(models[0][k])!=digest(models[1][k]):raise ValueError('CURRENT_PAIR_SHARED_'+k)
 if out[0]['source_signature']==out[1]['source_signature']:raise ValueError('CURRENT_PAIR_NOT_DISTINCT')
 return{'schema':'CURRENT368_SOURCE_ORGANIZATION_PAIR','members':out,'pair_count':1,'source_organization_distinct':True,'algorithm_source_digest':hashlib.sha256(cap['planha_general150_runtime_work/three_access_diversity133.py']).hexdigest(),'scope':'Current source port-normal organization signatures, D4/twin-swap invariant; no global architectural difference claim.'}
