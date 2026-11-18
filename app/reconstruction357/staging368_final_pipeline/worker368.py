"""Fresh process per source phase. Verify complete closure before project import."""
import sys,json,hashlib,time,uuid,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
manifest,expected,folder,kind,phase,budget=sys.argv[1:];manifest=Path(manifest);folder=Path(folder);budget=float(budget)
def failure_hook(t,e,tb):
 (folder/(phase+'_error.json')).write_text(json.dumps({'error':type(e).__name__+':'+str(e),'traceback':''.join(traceback.format_exception(t,e,tb)),'accepted':False},indent=2))
 sys.__excepthook__(t,e,tb)
sys.excepthook=failure_hook
if hashlib.sha256(manifest.read_bytes()).hexdigest()!=expected:raise ValueError('EXTERNAL_FREEZE_ANCHOR')
frozen=json.loads(manifest.read_text())
def check():
 for n,h in frozen['files'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_DRIFT:'+n)
check()
sys.path.insert(0,str(HERE))
from request_contract368 import digest,verify
from model_binding368 import bind
request=json.loads((folder.parent/'request.json').read_text());envelope=request['envelope'];run_id=request['run_id'];e=verify(envelope);start=time.monotonic()
if kind not in ('balanced','joint')or phase not in('construct','review'):raise ValueError('CLOSED_STAGE_INVENTORY')
if phase=='construct':
 producer=ROOT/('staging365_balanced_portals'if kind=='balanced'else'staging367_service_joint_attempt2');sys.path.insert(0,str(producer))
 if kind=='balanced':
  import adapter365 as source
  parent=source.lineage();raw=parent['trace']['raw']
 else:
  import joint367 as source
  parent=source.original();raw=parent['candidate']['request']
 if digest(raw)!=e['raw_digest']:raise ValueError('CALLER_SOURCE_REQUEST_MISMATCH_BEFORE_CONSTRUCT')
 record=source.construct();bound=bind(envelope,record,kind,run_id)
 replay=source.replay(record['trace'])
 if digest(replay)!=digest(record):raise ValueError('ACTUAL_REPLAY_RECORD_MISMATCH')
 (folder/'constructed.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));(folder/'binding.json').write_text(json.dumps(bound,indent=2))
 out={'phase':'reconstructed_and_replayed','binding':bound,'source_record_digest':digest(record),'source_parent_digest':digest(parent),'actual_construct_executed':True,'actual_replay_executed':True,'cached_model_returned':False,'new_fresh':False}
else:
 record=json.loads((folder/'constructed.json').read_text());bound=bind(envelope,record,kind,run_id)
 if digest(bound)!=digest(json.loads((folder/'binding.json').read_text())):raise ValueError('RUN_CANDIDATE_CHANGED')
 path=ROOT/('staging365_balanced_source_validation'if kind=='balanced'else'staging367_joint_source_validation_attempt2');sys.path.insert(0,str(path))
 if kind=='balanced':
  from evaluate365 import evaluate365 as evaluate
 else:
  from evaluate367 import evaluate367 as evaluate
 fresh=evaluate(record,min(90,budget))
 if fresh.get('fresh_checker_executed')is not True or fresh.get('source_unchanged')is not True or fresh.get('expected_method_registry',{}).get('built_before_evaluate')is not True or fresh.get('provenance',{}).get('verified')is not True:raise ValueError('ACTUAL_CHECKER_OR_REGISTRY_NOT_PROVEN')
 if fresh['raw_report'].get('model_hash')!=bound['model_digest']:raise ValueError('RAW_REVIEW_MODEL_BINDING')
 for n,h in fresh['expected_method_registry']['sources'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('EXPECTED_METHOD_SOURCE_DRIFT:'+n)
 if fresh.get('model_digest')!=bound['model_digest']or fresh.get('input_record_digest')!=digest(record)or fresh.get('outer_trace_digest')!=digest(record['trace']):raise ValueError('CURRENT_REVIEW_BINDING')
 (folder/'fresh.json').write_text(json.dumps(fresh,ensure_ascii=False,indent=2))
 out={'phase':'review_completed','binding':bound,'review_id':str(uuid.uuid4()),'fresh_result_digest':digest(fresh),'source_record_digest':digest(record),'checker_executed':fresh.get('fresh_checker_executed')is True,'expected_registry_digest':digest(fresh['expected_method_registry']),'fresh_artifact':'fresh.json','source_profile':('SOURCE_BALANCED365'if kind=='balanced'else'SOURCE_JOINT367'),'accepted':False,'delivery_allowed':False,'semantic_qualification':'NOT_EXECUTED_RUN_SPECIFIC_PROOF_REQUIRED','repair_authority':False}
check();out.update(generation_run_id=run_id,canonical_request_digest=e['canonical_request_digest'],raw_digest=e['raw_digest'],received_digest=e['received_digest'],seconds=time.monotonic()-start,source_unchanged=True,run_specific_receipt=True)
(folder/(phase+'_receipt.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'kind':kind,'phase':out['phase'],'seconds':out['seconds']}))
