"""Two exact FRONT_REAR/P2 study inputs; no new constructor, fallback or authority."""
import copy,inspect
from pathlib import Path
from front_rear_runtime_adapter import (ROOT,AUTHORITY,CURRENT,ensure,transport,source_audit,
    proposal_transport,proposal_disposition,preserve_report,verify_reports,packet_binding)
from same_version_front_rear_contract import ENGINE_REVISION,digest
from producer_provenance import snapshot
import current_entry_boundary_x03 as boundary
import precision_boundary208 as precision
import source_fit_profile207 as fit
from core_choice_pair_study import bind_profile,bind_program

CASES=(('18.1','22.2'),('25','25'))
SCOPE='FRONT_REAR/P2 study: 18x20, 18.1x22.2, 25x25 (n2); 18x20 only (n1)'
ENTRY='SOURCE_FIT207_COMPACT_PAIR'

def guard():
 paths=['app/local_integration/'+n for n in ('parametric_pair_p04.py','precision_boundary208.py',
    'source_fit_profile207.py','core_choice_pair_study.py','producer_provenance.py')]
 for fn,name in ((precision.prepare,'precision_boundary208.py'),(precision.coordinate_receipt,'precision_boundary208.py'),
   (boundary.prepare,'current_entry_boundary_x03.py'),(boundary.propose_current,'current_entry_boundary_x03.py'),
   (boundary.construct_current,'current_entry_boundary_x03.py'),(fit.source_fit,'source_fit_profile207.py'),
   (bind_profile,'core_choice_pair_study.py'),(bind_program,'core_choice_pair_study.py')):
  ensure(Path(inspect.getsourcefile(fn)).resolve()==ROOT/'app/local_integration'/name,'P04_IMPORT_PATH')
 return {'local':snapshot(ROOT,paths),'boundary':boundary.source_snapshot()}

def prepare(body):
 exact=precision.prepare(body)
 raw=exact['raw']
 ensure(type(raw['n']) is int and raw['n']==2 and (raw['W'],raw['L']) in CASES,'P04_CASE_SCOPE')
 selected=boundary.prepare(ENTRY,body)
 ensure(digest(selected['raw'])==digest(raw) and digest(selected['envelope'])==digest(exact['envelope']),'P04_INPUT_BINDING')
 profile=selected['profile'];bind_profile(profile)
 contract={'schema':'P04_PARAMETRIC_STUDY_CONTRACT_V1','case':[raw['W'],raw['L'],2],
  'core_method':'FRONT_REAR_COMPACT118','family':'FRONT_REAR','programme':'PROGRAM_2BED_V1',
  'producer':'SOURCE_FIT207_COMPACT_PAIR','constructor':'CONSTRUCTOR127_COMPACT_PAIR',
  'engine_revision':ENGINE_REVISION,'variant':0,'organization_profile':'UNRESTRICTED',
  'topology':'SIDE_ROOTED_SERVICES','raw_ratios':exact['ratios'],**{k:False for k in AUTHORITY}}
 binding={'schema':'P04_PARAMETRIC_REQUEST_BINDING_V1','contract_digest':digest(contract),
  'contract':contract,'raw':raw,'envelope':exact['envelope'],'program_registry':profile,
  'program_registry_digest':digest(profile),'source_core_digest':digest(selected['core']),
  **{k:False for k in AUTHORITY}}
 return binding,selected['core']

def run(body,*,solver_seconds):
 ensure(type(solver_seconds) is int and 1<=solver_seconds<=30,'P04_SOLVER_BUDGET')
 bind,core=prepare(body)
 raw=bind['raw'];report_pins={};originals={};live={};objects={'raw':raw,'core':core}
 pins={k:digest(v) for k,v in objects.items()};bindpin=digest(bind)
 out={'schema':'FRONT_REAR_ORIGINAL_RUNTIME_BUNDLE_V1','binding':bind,'engine_revision':ENGINE_REVISION,
  'status':'NOT_COMPLETED','completed':False,'production_supported':False,'errors':[],'stages':[],
  'constructor_called':False,'construction_returned':False,'model_binding_verified':False,'fresh_model_executed':False,
  'solver_budget_seconds':solver_seconds,'reports':originals,'report_transports':{},**{k:False for k in AUTHORITY}}
 stage='source_audit'
 baseline=None
 def check():
  ensure(digest(bind)==bindpin and all(digest(objects[k])==h for k,h in pins.items()),'P04_INPUT_MUTATION')
  verify_reports(originals,report_pins);verify_reports(live,report_pins)
  ensure(baseline is not None and guard()==baseline,'P04_SOURCE_CHANGED')
 def keep(k,v):
  out['report_transports'][k]=preserve_report(originals,live,report_pins,k,v);check()
 try:
  baseline=guard();out['source_snapshot']=baseline
  audit=source_audit();keep('source_audit',audit)
  stage='proposal'
  result=boundary.propose_current(body,seconds=solver_seconds,variant=0)
  p,pr=proposal_transport(result);out['proposal']=copy.deepcopy(p);objects['proposal']=p;pins['proposal']=digest(p)
  keep('proposal_transport',pr);keep('coordinate_precision',precision.coordinate_receipt(result,p,pr))
  out['stages'].append(stage)
  if proposal_disposition(p)!='PROPOSAL_ONLY':
   out.update(status='NO_PROPOSAL_IN_BOUNDED_ATTEMPT',completed=True,global_infeasibility_proven=False)
   return out
  stage='source_fit'
  check_fit=fit.source_fit(p,core);keep('preconstruction_fit',check_fit)
  ensure(check_fit['proposal_digest']==pins['proposal'] and check_fit['core_digest']==pins['core'],'P04_FIT_BINDING')
  if check_fit['state']!='PASS_LIMITED_CONSTRAINTS':
   out.update(status='EXACT_FIT_REJECTED_NO_GLOBAL_INFEASIBILITY',completed=True,global_infeasibility_proven=False)
   return out
  stage='constructor';out['constructor_called']=True
  built=boundary.construct_current(body,{'A':p,'B':copy.deepcopy(p)})
  out.update(construction_returned=True,fresh_model_executed=True)
  (packet,ctx),receipt=transport([built['packet'],built['context']])
  objects.update(packet=packet,context=ctx);pins.update(packet=digest(packet),context=digest(ctx))
  model=packet['world_model'];bind_program(model,bind['program_registry'])
  ensure(digest(packet['core'])==bind['source_core_digest'],'P04_CORE_BINDING')
  mh=packet_binding(packet,ctx,raw,p)
  out.update(packet=copy.deepcopy(packet),context=copy.deepcopy(ctx),model_digest=mh,model_binding_verified=True)
  keep('model_transport',receipt);out['stages'].append(stage)
  import construction_replay127,evaluate_pair127,functional_review
  stage='replay';replay=construction_replay127.verify(model,ctx);keep('replay',replay)
  ensure(replay['verified'] is True and replay['model_hash']==mh,'P04_REPLAY_BINDING');out['stages'].append(stage)
  stage='physical';physical=evaluate_pair127.evaluate(packet,ctx);keep('physical',physical)
  ensure(physical['model_hash']==mh and physical['accepted'] is False and physical['release'] is False,'P04_PHYSICAL_BINDING')
  out['stages'].append(stage)
  stage='functional';functional=functional_review.assess(model,physical,ENGINE_REVISION);keep('functional',functional)
  ensure(functional['model_digest']==mh and functional['physical_review_digest']==report_pins['physical']
     and functional['source_revision']==ENGINE_REVISION and all(functional[k] is False for k in AUTHORITY)
     and {r['id'] for r in functional['requirements']}==CURRENT|{'INTERNAL_INSTANCE_CAPACITY'},'P04_FUNCTIONAL_BINDING')
  out['stages'].append(stage);out.update(status='FULL_REPORTS_RETAINED_NOT_QUALIFIED',completed=True)
 except Exception as ex:
  out.update(status='RUNTIME_FAILED_CLOSED',completed=False)
  out['errors'].append({'stage':stage,'kind':'RUNTIME_OR_BINDING_ERROR','type':type(ex).__name__,'detail':str(ex)})
 finally:
  try:
   check()
   ensure(source_audit()==audit,'P04_ENGINE_SOURCE_CHANGED')
   out['object_integrity_verified']=True
  except Exception as ex:
   out.update(status='RUNTIME_FAILED_CLOSED',completed=False,object_integrity_verified=False)
   out['errors'].append({'stage':'final_integrity','kind':'INTEGRITY_ERROR','type':type(ex).__name__,'detail':str(ex)})
  out.update(report_digests=copy.deepcopy(report_pins),object_digests=copy.deepcopy(pins))
 return out

def verify_completed(bundle):
 """Bind the persisted completed packet to the exact selected request and fit receipt."""
 bind=bundle['binding'];packet=bundle['packet'];proposal=bundle['proposal'];ctx=bundle['context']
 ensure(type(bundle.get('object_integrity_verified')) is bool and bundle['object_integrity_verified'],'P04_COMPLETED_INTEGRITY')
 ensure(bundle['source_snapshot']==guard() and bundle['engine_revision']==ENGINE_REVISION,'P04_COMPLETED_SOURCE')
 ensure(digest(packet['core'])==bind['source_core_digest'],'P04_COMPLETED_CORE')
 ensure(packet_binding(packet,ctx,bind['raw'],proposal)==bundle['model_digest'],'P04_COMPLETED_MODEL')
 report=bundle['reports']['preconstruction_fit']
 ensure(report['state']=='PASS_LIMITED_CONSTRAINTS' and report['proposal_digest']==digest(proposal)
    and report['core_digest']==bind['source_core_digest'],'P04_COMPLETED_FIT')
 verify_reports(bundle['reports'],bundle['report_digests'])
 ensure(set(bundle['reports'])==set(bundle['report_digests']) and {'physical','replay','functional'}<=set(bundle['reports']),'P04_COMPLETED_REPORTS')
 return True
