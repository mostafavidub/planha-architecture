"""Task2.3 original FRONT_REAR runtime wiring; live invocation deferred to2.5."""
import copy,inspect,json,math,sys
from pathlib import Path
from public_wln_contract import parse_public,verify_public
from same_version_front_rear_contract import bind_request,digest,ENGINE_REVISION,FREEZE
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
AUTHORITY=('accepted','qualified','display_allowed','delivery_allowed')
CURRENT={'CURRENT_PROGRAM_SUITABILITY','KITCHEN_GUEST_PATH_SEPARATION','CONTINUOUS_USEFUL_LIVING','NONFUNCTIONAL_WALL_EXCLUSION'}
def ensure(ok,reason):
 if not ok:raise ValueError(reason)
def transport(value):
 """Only tuple-to-array JSON transport allowed; no scalar coercion."""
 changes=[]
 def visit(x,path):
  if type(x) is dict:
   ensure(all(type(k) is str for k in x),'TRANSPORT_KEY')
   return {k:visit(v,path+[k]) for k,v in x.items()}
  if type(x) in (list,tuple):
   if type(x) is tuple:changes.append(path)
   return [visit(v,path+[i]) for i,v in enumerate(x)]
  ensure(type(x) in (str,int,float,bool,type(None)),'TRANSPORT_TYPE')
  ensure(type(x) is not float or math.isfinite(x),'TRANSPORT_NONFINITE')
  return x
 out=visit(value,[])
 ensure(digest(out)==digest(value),'TRANSPORT_DIGEST_CHANGE')
 return out,{'tuple_paths':changes,'before_digest':digest(value),'after_digest':digest(out),'scope':'JSON tuple-to-array only; exact scalar types retained'}
def verify_reports(reports,pins):
 for key,h in pins.items():ensure(digest(reports[key])==h,'COMPLETED_REPORT_MUTATION:'+key)
def observed_digest(value):
 try:return digest(value)
 except Exception as ex:return 'UNHASHABLE_INTEGRITY_ERROR:'+type(ex).__name__
def observed_copy(value):
 try:
  out,_=transport(value)
  return out
 except Exception as ex:return {'unserializable_observation':type(ex).__name__}
def preserve_report(originals,live,pins,key,value):
 live[key]=value
 originals[key]=copy.deepcopy(value)
 pins[key]=digest(value)
def proposal_disposition(proposal):
 ensure(type(proposal) is dict,'PROPOSAL_OBJECT')
 status=proposal.get('status')
 allowed={'PROPOSAL_ONLY','SEARCH_TIMEOUT_NO_WITNESS','NO_PROPOSAL_IN_THIS_TOPOLOGY','NO_PROPOSAL_IN_THIS_PROGRAM','ROUNDED_PROPOSAL_REJECTED'}
 ensure(type(status) is str and status in allowed,'UNKNOWN_PRODUCER_STATUS')
 return status
def source_audit():
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
 from same_version_front_rear_contract import audit_sources
 result=audit_sources()
 from left_right_two_source_binding import source_state
 state=source_state()
 import constructor127,search114,construction_replay127,evaluate_pair127,functional_review
 pairs=[(constructor127,'frame'),(constructor127,'build'),(constructor127,'context'),(search114,'propose'),
  (construction_replay127,'verify'),(evaluate_pair127,'evaluate'),(functional_review,'assess')]
 for mod,name in pairs:
  root=ROOT/'app/local_integration' if mod is functional_review else ENGINE
  ensure(Path(mod.__file__).resolve()==(root/(mod.__name__+'.py')).resolve(),'MODULE_IMPORT')
  ensure(Path(inspect.getsourcefile(getattr(mod,name))).resolve()==(root/(mod.__name__+'.py')).resolve(),'CALLABLE_IMPORT')
 ensure(evaluate_pair127.verify is construction_replay127.verify,'PAIR_REPLAY_ALIAS')
 return {'api_audit':result,'engine_state':state}
def run(body,*,solver_seconds):
 """Explicit live API, not called by scheduler/UI. Requires external hard process timeout.
 No cancellation, waiting or hard-kill guarantee is implemented inside this function.
 """
 ensure(type(solver_seconds) in (int,float) and math.isfinite(solver_seconds) and 0<solver_seconds<=60,'SOLVER_BUDGET')
 envelope=parse_public(body);verify_public(body,envelope)
 binding=bind_request(body,envelope,'PROGRAM_2BED_V1')
 # Source approval and readiness are not inferred from legacy technical profile.
 binding_pin=digest(binding);raw=copy.deepcopy(binding['raw'])
 out={'schema':'FRONT_REAR_ORIGINAL_RUNTIME_BUNDLE_V1','status':'NOT_COMPLETED',
  'binding':binding,'stages':[],'reports':{},'errors':[],
  'fresh_model_executed':False,'completed':False,'production_supported':False,
  'solver_budget_seconds':solver_seconds,'outer_hard_timeout_required':True,
  **{k:False for k in AUTHORITY}}
 report_pins={};live_reports={};objects={};original_objects={};object_pins={};sources=None;state=None
 def freeze_object(k,v):
  objects[k]=v;object_pins[k]=digest(v);original_objects[k]=copy.deepcopy(v)
 def freeze_report(k,v):
  preserve_report(out['reports'],live_reports,report_pins,k,v)
 def unchanged():
  ensure(digest(binding)==binding_pin,'BINDING_MUTATION')
  for k,h in object_pins.items():ensure(digest(objects[k])==h,'OBJECT_MUTATION:'+k)
  verify_reports(out['reports'],report_pins)
  verify_reports(live_reports,report_pins)
  if sources is not None:
   from producer_provenance import require_unchanged
   require_unchanged(ROOT,sources)
  if state is not None:
   from left_right_two_source_binding import source_state
   from guard400 import guard
   ensure(source_state()==state and guard(FREEZE)==12991,'SOURCE_OR_GUARD_CHANGED')
 stage='source_audit'
 try:
  sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
  from producer_provenance import snapshot
  paths=['app/local_integration/'+f for f in ('front_rear_runtime_adapter.py','public_wln_contract.py','program_profile_registry.py','same_version_front_rear_contract.py','functional_review.py','guest_four_route_diagnostic.py','kitchen_guest_review.py','living_connectivity_diagnostic.py','review_cycle.py','producer_provenance.py','left_right_two_source_binding.py')]
  sources=snapshot(ROOT,paths)
  audit=source_audit();freeze_report('source_audit',audit);state=audit['engine_state']
  unchanged()
  import constructor127,search114,construction_replay127,evaluate_pair127,functional_review
  freeze_object('raw',raw);unchanged()
  stage='frame';core,_=constructor127.frame(raw,'FRONT_REAR');ensure(core is not None,'UNSUPPORTED_CURRENT_CORE_FIT');freeze_object('core',core);out['stages'].append(stage);unchanged()
  stage='proposal'
  proposal=search114.propose(core,2,time_limit=solver_seconds,variant=0,fixed_witness=None,diagnostic_capture=None,
   sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES',organization_profile='UNRESTRICTED')
  proposal,receipt=transport(proposal);freeze_object('proposal',proposal);freeze_report('proposal_transport',receipt)
  out['proposal']=copy.deepcopy(proposal);out['stages'].append(stage);unchanged()
  if proposal_disposition(proposal)!='PROPOSAL_ONLY':
   out.update(status='NO_PROPOSAL_IN_BOUNDED_ATTEMPT',completed=True,global_infeasibility_proven=False)
  else:
   from left_right_two_source_binding import proposal_check
   proposal_check(proposal)
   stage='constructor'
   packet=constructor127.build(raw,'FRONT_REAR',proposal,proposal)
   ctx=constructor127.context(raw,packet,{'A':proposal,'B':proposal})
   (packet,ctx),receipt=transport([packet,ctx])
   freeze_object('packet',packet);freeze_object('context',ctx);freeze_report('model_transport',receipt)
   model=packet['world_model'];mh=digest(model)
   ensure(digest(ctx['construction_trace']['raw'])==digest(raw),'TRACE_RAW')
   ensure(digest(ctx['construction_trace']['proposals'])==digest({'A':proposal,'B':proposal}),'TRACE_PROPOSALS')
   ensure(packet['family']=='FRONT_REAR' and packet['admission_claim'] is False,'PACKET_AUTHORITY')
   out.update(packet=copy.deepcopy(packet),context=copy.deepcopy(ctx),model_digest=mh,fresh_model_executed=True)
   out['stages'].append(stage);unchanged()
   stage='replay';replay=construction_replay127.verify(model,ctx);freeze_report('replay',replay);out['stages'].append(stage);unchanged()
   ensure(replay['verified'] is True and replay['model_hash']==mh,'REPLAY_FAILED')
   stage='physical';physical=evaluate_pair127.evaluate(packet,ctx);freeze_report('physical',physical);out['stages'].append(stage);unchanged()
   ensure(physical['model_hash']==mh,'PHYSICAL_MODEL')
   ensure(physical['accepted'] is False and physical['release'] is False,'PHYSICAL_AUTHORITY')
   # No error/pending merge, filtering, dedup or overwrite: full original report retained.
   stage='functional';current=functional_review.assess(model,physical,ENGINE_REVISION)
   freeze_report('functional',current);out['stages'].append(stage);unchanged()
   ensure(current['model_digest']==mh and current['physical_review_digest']==report_pins['physical'],'FUNCTIONAL_BINDING')
   ensure(current['source_revision']==ENGINE_REVISION,'FUNCTIONAL_SOURCE')
   ensure(all(current[k] is False for k in AUTHORITY),'FUNCTIONAL_AUTHORITY')
   current_ids=[r['id'] for r in current['requirements']]
   ensure(len(current_ids)==5 and set(current_ids)==CURRENT|{'INTERNAL_INSTANCE_CAPACITY'},'FUNCTIONAL_REQUIREMENTS')
   ensure(all(r['state']=='UNKNOWN' for r in current['requirements'] if r['id'] in CURRENT),'CURRENT_UNKNOWN_CHANGED')
   out.update(status='FULL_REPORTS_RETAINED_NOT_QUALIFIED',completed=True)
 except Exception as ex:
  out.update(status='RUNTIME_FAILED_CLOSED',completed=False)
  out['errors'].append({'stage':stage,'kind':'EVALUATOR_ERROR' if stage in ('physical','functional','replay') else 'RUNTIME_OR_BINDING_ERROR','type':type(ex).__name__,'detail':str(ex)})
 finally:
  try:unchanged()
  except Exception as ex:
   out.update(status='RUNTIME_FAILED_CLOSED',completed=False)
   out['errors'].append({'stage':'final_integrity','kind':'INTEGRITY_ERROR','type':type(ex).__name__,'detail':str(ex)})
  out['report_mutations']=[{'section':k,'original_digest':h,'observed_digest':observed_digest(live_reports[k]),'observed_report':observed_copy(live_reports[k])} for k,h in report_pins.items() if observed_digest(live_reports[k])!=h]
  out['object_integrity_verified']=all(observed_digest(objects[k])==h for k,h in object_pins.items())
  out['object_mutations']=[{'section':k,'original_digest':h,'observed_digest':observed_digest(objects[k]),'observed_object':observed_copy(objects[k])} for k,h in object_pins.items() if observed_digest(objects[k])!=h]
  out['forensic_notice']='Original packet/context/proposal/report copies are preserved; observed mutations are separate forensic diagnostics and never valid model evidence.'
  out.update(report_digests=copy.deepcopy(report_pins),object_digests=copy.deepcopy(object_pins),
   source_snapshot=sources,engine_revision=ENGINE_REVISION)
 return out
