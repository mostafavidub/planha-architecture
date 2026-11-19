"""Task4.3 one isolated bounded exploratory repair and fresh complete evaluation."""
import copy,json,math,os,signal,subprocess,sys,time,uuid,hashlib,inspect
from pathlib import Path
from front_rear_runtime_adapter import ROOT,ENGINE,ensure,transport,proposal_transport,digest,source_audit,packet_binding,preserve_report,verify_reports
from same_version_front_rear_contract import ENGINE_REVISION
from protected_repair_contract import freeze_parent,verify_child
from rejection_operator_selection import select
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
BUDGET=240
def save(path,obj):path.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False))
def one(root,name):
 fs=list(root.rglob(name));ensure(len(fs)==1,'EVIDENCE_UNIQUE:'+name);return json.loads(fs[0].read_text())
def candidate_transport(p):
 """Only source-declared four-seat geometric witness arrays extend original proposal boundary."""
 import numpy as np
 before=digest(p);q=copy.deepcopy(p);g=q.pop('independent_shared_group_study',None)
 q,receipt=proposal_transport(q);extra=[]
 def scalar(x,path):
  if type(x) is not np.float64:return x
  y=float(x);ensure(math.isfinite(y) and x.as_integer_ratio()==y.as_integer_ratio() and digest(x)==digest(y),'GROUP_SCALAR_EXACT')
  extra.append({'path':path,'source_type':'numpy.float64','ratio':[str(z) for z in y.as_integer_ratio()]});return y
 if g is not None:
  ensure(g['schema']=='V25_FOUR_SEAT_ENVELOPE_PROPOSAL_ONLY' and g['accepted'] is False and g['historical_shared_gate_marker'] is False,'GROUP_SOURCE_SCHEMA')
  seats={'sofa1_use','sofa2_use','chair1_use','chair2_use'}
  ensure(type(g['seat_uses']) is list and len(g['seat_uses'])==4 and set(g['seat_uses'])==seats,'GROUP_SEAT_SET')
  for key in ('envelope','body_witness'):
   ensure(type(g[key]) is list and len(g[key])==4,'GROUP_RECT')
   g[key]=[scalar(x,[key,i]) for i,x in enumerate(g[key])]
  if 'network_paths' in g:
   ensure(set(g['network_paths'])==seats,'GROUP_ROUTE_SET')
   for name,path in g['network_paths'].items():
    ensure(type(path) is list and len(path)==4,'GROUP_ROUTE_SHAPE')
    for i,pt in enumerate(path):
     ensure(type(pt) is list and len(pt)==2,'GROUP_POINT_SHAPE')
     path[i]=[scalar(x,['network_paths',name,i,j]) for j,x in enumerate(pt)]
  q['independent_shared_group_study']=g
 q,_=transport(q);ensure(digest(q)==before,'CANDIDATE_TRANSPORT_DIGEST')
 return q,{'base':receipt,'group_coordinate_conversions':extra,'before_digest':before,'after_digest':digest(q)}
def operator_transport(result):
 pin=digest(result);r=copy.deepcopy(result);receipts=[]
 for a in r['attempts']:
  a['proposal'],rec=candidate_transport(a['proposal']);receipts.append(rec)
 if r.get('child'):
  trace=r['child']['context']['construction_trace']
  for unit in ('A','B'):
   trace['proposals'][unit],rec=candidate_transport(trace['proposals'][unit]);receipts.append(rec)
 if r.get('child'):
  ensure(r['child']['packet']['family']=='FRONT_REAR','MODEL_NETWORK_TRANSPORT_FAMILY')
  p=r['child']['context']['construction_trace']['proposals']['A']
  for role in ('local_model','world_model'):
   m=r['child']['packet'][role]
   ensure(digest(m['proposal_network_paths'])==digest(p['network_paths']),'MODEL_PROPOSAL_NETWORK_SOURCE_BINDING')
   m['proposal_network_paths']=copy.deepcopy(p['network_paths'])
  receipts.append({'scope':'assemble114 root proposal_network_paths copied verbatim from proposalA, local/world only','source_binding':'exact digest equality to normalized source proposalA; no other model coordinate coercion'})
 r,_=transport(r);ensure(digest(r)==pin,'OPERATOR_TRANSPORT_DIGEST')
 return r,receipts
def child(directory,input_root,nonce):
 out={'schema':'BOUNDED_REPAIR_CHAIN_V1','nonce':nonce,'stage':'STARTED','stages':[],'reports':{},'report_digests':{},
  'generated_count':0,'verified_generated_count':0,'child_observed':False,'fresh_child_binding_verified':False,'parent_reused_as_child':False,
  'completed':False,'errors':[],**{k:False for k in AUTH}}
 live={};pins={};objects={};sourcepins=None;audit=None
 def checkpoint(stage):
  out['stage']=stage;out['stages'].append(stage);save(directory/'repair-progress.json',out)
 def unchanged():
  for name,(obj,h) in objects.items():ensure(digest(obj)==h,'REPAIR_OBJECT_MUTATION:'+name)
  verify_reports(live,pins);verify_reports(out['reports'],pins)
  if sourcepins is not None:
   from producer_provenance import require_unchanged
   require_unchanged(ROOT,sourcepins)
 def freeze(name,obj):objects[name]=(obj,digest(obj))
 def report(name,obj):
  preserve_report(out['reports'],live,pins,name,obj);out['report_digests']=copy.deepcopy(pins);unchanged()
 try:
  from producer_provenance import snapshot
  sourcepins=snapshot(ROOT,['app/local_integration/'+p for p in ('bounded_repair_chain.py','protected_repair_contract.py','rejection_operator_selection.py','explicit_pair_redirection.py','candidate/four_seat_group_candidate.py','front_rear_runtime_adapter.py','current_four_decision.py','current_programme_evaluator.py','source_guest_route_evaluator.py','source_living_evaluator.py','source_wall_function_evaluator.py')])
  audit=source_audit();out['source_snapshot']=sourcepins;checkpoint('SOURCES_VERIFIED')
  names=['request.json','runtime-bundle.json','child-complete.json','scheduler.json','decision.json']
  values=[one(input_root,n) for n in names];request,parent,oldchild,scheduler,decision=values
  ensure(digest(parent)=='ce47b8433c94aaf216c6fd0d67c8ca9bcc563466f85ba17d3bfdb1fa05d89234','PINNED_PARENT_RUNTIME')
  selection=one(input_root,'rejection-operator-selection.json');contract=one(input_root,'typed-repair-contract.json')
  ensure(digest(contract)=='64d7700851e02fb72cc9debe115783222b19671f9b37c24fa137ac9e97ee09b0','PINNED_PROTECTION_CONTRACT')
  freshselect=select(*values,{k:digest(v) for k,v in zip(('request','runtime','child','scheduler','decision'),values)})
  recorded=copy.deepcopy(selection);recorded.pop('actual_artifact_negative_tests',None)
  ensure(digest(freshselect)==digest(recorded),'FRESH_SELECTION_CHANGED')
  freshcontract=freeze_parent(selection,parent,expected_selection_digest=digest(selection),expected_runtime_digest=digest(parent))
  ensure(digest(freshcontract)==digest(contract),'FRESH_PROTECTION_CHANGED')
  freeze('parent',parent);freeze('selection',selection);freeze('contract',contract)
  out['parent_model_digest']=parent['model_digest'];out['parent_physical_report']=copy.deepcopy(parent['reports']['physical'])
  out['parent_physical_digest']=digest(out['parent_physical_report']);out['parent_attempt_id']=contract['parent_attempt_id']
  out['contract_digest']=digest(contract);checkpoint('PARENT_SELECTION_AND_PROTECTION_REVALIDATED')
  # Internal programme is derived from approved source-bound registry, not a public field.
  public=json.loads(bytes.fromhex(request['body_hex']));diagnostic={**public,'requested_count':1,'program':{'bedrooms_per_unit':2}}
  body=json.dumps(diagnostic,sort_keys=True).encode()
  from explicit_pair_redirection import redirect
  ensure(Path(inspect.getsourcefile(redirect)).resolve()==(ROOT/'app/local_integration/explicit_pair_redirection.py').resolve(),'REDIRECT_IMPORT')
  checkpoint('EXISTING_OPERATOR_STARTED')
  result=redirect(body,parent['packet']['world_model'],parent['context'])
  out['operator_returned']=True;out['operator_returned_raw_digest']=digest(result)
  out['child_observed']=result.get('child') is not None
  out['generated_count']=1 if out['child_observed'] else 0
  out['operator_attempts_constructed_models_observed']=sum(1 for a in result['attempts'] if a.get('model_digest'))
  out['generated_count_scope']='Observed selected child count before transport; verified_generated_count remains zero until complete fresh gates.'
  checkpoint('OPERATOR_RETURNED_TRANSPORT_NOT_VERIFIED')
  # Forensic JSON observation only: standard JSON transport can erase numpy scalar types.
  # This file is not an admitted typed model and may only be consumed after source-bound transport checks.
  save(directory/'operator-returned-observation.json',result)
  result,receipts=operator_transport(result);unchanged()
  check=copy.deepcopy(result);declared=check.pop('receipt_digest');ensure(digest(check)==declared,'OPERATOR_RECEIPT')
  out['operator_result_digest']=digest(result);out['operator_transport']=receipts
  out['operator_attempts_constructed_models_observed']=sum(1 for a in result['attempts'] if a.get('model_digest'))
  out['generated_count_scope']='Selected distinct child, not all exploratory candidates constructed inside the existing operator'
  save(directory/'operator-result.json',result);checkpoint('EXISTING_OPERATOR_RETURNED')
  if result['child'] is None:
   out.update(state='BOUNDED_SEARCH_NO_CHILD_NOT_INFEASIBLE',completed=True,generated_count=0)
  else:
   out['child_observed']=True;out['generated_count']=1
   selected=result['child'];packet,ctx=selected['packet'],selected['context']
   freeze('child_packet',packet);freeze('child_context',ctx)
   protected=verify_child(contract,digest(contract),packet,ctx)
   proposal=ctx['construction_trace']['proposals']['A'];raw=parent['binding']['raw']
   mh=packet_binding(packet,ctx,raw,proposal)
   ensure(mh==selected['model_digest'] and mh!=parent['model_digest'],'NEW_CHILD_REQUIRED')
   out.update(generated_count=1,child_model_digest=mh,fresh_child_binding_verified=True,protected_result=protected)
   checkpoint('CHILD_TYPED_BINDING_VERIFIED')
   import construction_replay127,evaluate_pair127,functional_review
   for mod,name,root in ((construction_replay127,'verify',ENGINE),(evaluate_pair127,'evaluate',ENGINE),(functional_review,'assess',ROOT/'app/local_integration')):
    ensure(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==(root/(mod.__name__+'.py')).resolve(),'FRESH_EVALUATOR_IMPORT')
   replay=construction_replay127.verify(packet['world_model'],ctx);report('replay',replay)
   ensure(replay['verified'] is True and replay['model_hash']==mh,'CHILD_REPLAY')
   checkpoint('CHILD_ORIGINAL_REPLAY')
   physical=evaluate_pair127.evaluate(packet,ctx);report('physical',physical)
   ensure(physical['model_hash']==mh and physical['accepted'] is False and physical['release'] is False,'CHILD_PHYSICAL_BINDING')
   checkpoint('CHILD_FULL_PHYSICAL')
   functional=functional_review.assess(packet['world_model'],physical,ENGINE_REVISION);report('functional',functional)
   ensure(functional['model_digest']==mh and functional['physical_review_digest']==digest(physical),'CHILD_FUNCTIONAL_BINDING')
   checkpoint('CHILD_ORIGINAL_FUNCTIONAL')
   bundle={'schema':'FRONT_REAR_ORIGINAL_RUNTIME_BUNDLE_V1','packet':copy.deepcopy(packet),'context':copy.deepcopy(ctx),
    'model_digest':mh,'binding':copy.deepcopy(parent['binding']),'reports':copy.deepcopy(out['reports']),'report_digests':copy.deepcopy(pins),
    'engine_revision':ENGINE_REVISION,'completed':True,'model_binding_verified':True,**{k:False for k in AUTH}}
   freeze('child_bundle',bundle);out['child_runtime_digest']=digest(bundle);save(directory/'child-runtime-bundle.json',bundle)
   from current_programme_evaluator import assess as programme
   from source_guest_route_evaluator import assess as guest
   from source_living_evaluator import assess as living
   from source_wall_function_evaluator import assess as walls
   assessments={}
   for cid,fn in [('CURRENT_PROGRAM_SUITABILITY',programme),('KITCHEN_GUEST_PATH_SEPARATION',guest),('CONTINUOUS_USEFUL_LIVING',living),('NONFUNCTIONAL_WALL_EXCLUSION',walls)]:
    value=fn(bundle);unchanged();assessments[cid]=copy.deepcopy(value);freeze(cid,value)
    save(directory/(cid+'.json'),value);checkpoint(cid)
   from current_four_decision import assemble
   d=assemble(bundle,assessments,{k:digest(v) for k,v in assessments.items()});unchanged()
   save(directory/'child-current-decision.json',d);out['current_decision']=copy.deepcopy(d['decision'])
   out['current_decision_digest']=digest(d);out['child_physical_status']=physical['status']
   out['child_pending_count']=len(physical['pending'])
   out.update(state='FRESH_CHILD_ALL_GATES_RECORDED_NOT_QUALIFIED',completed=True,verified_generated_count=1);checkpoint('CHILD_CURRENT_DECISION')
 except Exception as ex:
  out.update(state='REPAIR_CHAIN_FAILED_CLOSED',completed=False)
  out['errors'].append({'stage':out['stage'],'type':type(ex).__name__,'detail':str(ex)})
 finally:
  try:
   unchanged()
   ensure(audit is not None and sourcepins is not None,'INITIAL_SOURCE_AUDIT_NOT_ESTABLISHED')
   ensure(source_audit()==audit,'FINAL_SOURCE_AUDIT_CHANGED')
   out['source_integrity_verified']=True
  except Exception as ex:
   out.update(state='REPAIR_CHAIN_FAILED_CLOSED',completed=False,source_integrity_verified=False)
   out['errors'].append({'stage':'FINAL_INTEGRITY','type':type(ex).__name__,'detail':str(ex)})
  out['report_digests']=copy.deepcopy(pins)
  out['partial_evidence_scope']='Stage checkpoints retained. Existing operator has no per-variant callback; a hard kill during it may leave only OPERATOR_STARTED, not its in-memory attempts.'
  save(directory/'repair-complete.json',out)
 return out
def bind_result(result,nonce,operator,bundle=None,decision=None):
 ensure(result.get('nonce')==nonce and result.get('completed') is True and result.get('source_integrity_verified') is True,'CHILD_RECEIPT_COMPLETE')
 ensure(all(result.get(k) is False for k in AUTH),'CHILD_RECEIPT_AUTHORITY')
 ensure(result['state'] in ('BOUNDED_SEARCH_NO_CHILD_NOT_INFEASIBLE','FRESH_CHILD_ALL_GATES_RECORDED_NOT_QUALIFIED'),'CHILD_RECEIPT_STATE')
 ensure(digest(operator)==result['operator_result_digest'],'OPERATOR_FILE_DIGEST')
 original=copy.deepcopy(operator);declared=original.pop('receipt_digest');ensure(digest(original)==declared,'OPERATOR_FILE_RECEIPT')
 ensure(operator['parent_model_digest']==result['parent_model_digest'],'OPERATOR_PARENT')
 if result['state']=='BOUNDED_SEARCH_NO_CHILD_NOT_INFEASIBLE':
  ensure(type(result['generated_count']) is int and result['generated_count']==0 and type(result['verified_generated_count']) is int and result['verified_generated_count']==0 and result['fresh_child_binding_verified'] is False and result['child_observed'] is False,'NO_CHILD_COUNT_BINDING')
  ensure(operator['child'] is None and bundle is None and decision is None and 'current_decision' not in result,'NO_CHILD_EVIDENCE')
 else:
  ensure(type(result['generated_count']) is int and result['generated_count']==1 and type(result['verified_generated_count']) is int and result['verified_generated_count']==1 and result['child_observed'] is True and result['fresh_child_binding_verified'] is True,'CHILD_COUNT_BINDING')
  ensure(bundle is not None and decision is not None and operator['child'] is not None,'CHILD_FILES')
  mh=digest(bundle['packet']['world_model'])
  ensure(mh==result['child_model_digest']==bundle['model_digest']==operator['child']['model_digest'] and mh!=result['parent_model_digest'],'CHILD_MODEL_DISTINCT')
  ensure(digest(bundle)==result['child_runtime_digest'],'CHILD_RUNTIME_DIGEST')
  for k,r in bundle['reports'].items():ensure(digest(r)==bundle['report_digests'][k]==result['report_digests'][k] and digest(result['reports'][k])==digest(r),'CHILD_REPORT_BINDING')
  ensure(bundle['reports']['physical']['model_hash']==mh and bundle['reports']['replay']['verified'] is True,'CHILD_ORIGINAL_GATES')
  ensure(digest(decision)==result['current_decision_digest'] and decision['integrity_verified'] is True and decision['model_digest']==mh,'CHILD_DECISION_DIGEST')
  ensure(decision['physical_digest']==bundle['report_digests']['physical'] and digest(decision['decision'])==digest(result['current_decision']),'CHILD_DECISION_REPORT_BINDING')
  ensure(all(decision.get(k) is False and bundle.get(k) is False for k in AUTH),'CHILD_FILES_AUTHORITY')
 return True
def run(input_root):
 nonce=uuid.uuid4().hex;directory=ROOT/'repair-evidence'/nonce;directory.mkdir(parents=True,exist_ok=False)
 snapshot_paths=['app/local_integration/bounded_repair_chain.py']
 before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in snapshot_paths};audit=source_audit()
 receipt={'schema':'BOUNDED_REPAIR_PARENT_RECEIPT_V1','nonce':nonce,'shared_child_seconds':BUDGET,'budget_scope':'Repair existing loop plus all fresh gates inside one isolated child; parent source audits/setup excluded.',
  'source_snapshot':before,'head_sha':os.environ.get('GITHUB_SHA'),**{k:False for k in AUTH}}
 save(directory/'parent-start.json',receipt)
 started=time.monotonic();proc=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'--child',str(directory),str(input_root.resolve()),nonce],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True,cwd=ROOT)
 timeout=False;killed=False
 try:stdout,stderr=proc.communicate(timeout=BUDGET)
 except subprocess.TimeoutExpired:
  timeout=True
  try:os.killpg(proc.pid,signal.SIGKILL);killed=True
  except ProcessLookupError:pass
  stdout,stderr=proc.communicate()
 (directory/'stdout.txt').write_text(stdout);(directory/'stderr.txt').write_text(stderr)
 receipt.update(elapsed_seconds=time.monotonic()-started,timed_out=timeout,kill_sent=killed,wait_completed=proc.poll() is not None,returncode=proc.returncode)
 result=None
 if (directory/'repair-complete.json').exists():result=json.loads((directory/'repair-complete.json').read_text())
 receipt['child_receipt_verified']=False
 if not timeout and proc.returncode==0 and result:
  try:
   operator=json.loads((directory/'operator-result.json').read_text())
   bundle=json.loads((directory/'child-runtime-bundle.json').read_text()) if (directory/'child-runtime-bundle.json').exists() else None
   decision=json.loads((directory/'child-current-decision.json').read_text()) if (directory/'child-current-decision.json').exists() else None
   receipt['child_receipt_verified']=bind_result(result,nonce,operator,bundle,decision)
  except Exception as ex:receipt['receipt_error']={'type':type(ex).__name__,'detail':str(ex)}
 if result:
  receipt['observed_result_digest']=digest(result)
  if receipt['child_receipt_verified']:
   receipt.update(state=result['state'],generated_count=result['generated_count'],child_model_digest=result.get('child_model_digest'),current_decision=result.get('current_decision'))
  else:receipt['observed_unverified_state']=result.get('state')
 if not receipt['child_receipt_verified']:receipt['state']='TIMED_OUT_NOT_INFEASIBLE' if timeout else 'FAILED_OR_INCOMPLETE'
 receipt['source_integrity_verified']=source_audit()==audit and before=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in before}
 if not receipt['source_integrity_verified']:receipt['child_receipt_verified']=False;receipt['state']='SOURCE_INTEGRITY_FAILED_CLOSED'
 save(directory/'parent-receipt.json',receipt);return receipt
if __name__=='__main__':
 if len(sys.argv)==5 and sys.argv[1]=='--child':child(Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4])
 else:
  r=run(Path(sys.argv[1]));print(json.dumps(r,sort_keys=True))
  if not r['child_receipt_verified']:raise SystemExit(1)
