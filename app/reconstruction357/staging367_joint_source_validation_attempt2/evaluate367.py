"""New reconstructed source profile, real checker; no semantic admission."""
import sys,json,hashlib,copy,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(HERE/'runtime'))
from contract114 import digest
from source_registry_joint367 import resolve,verify_context

def inventory():
 roots=[HERE,BASE/'staging367_service_joint_attempt2',BASE/'planha_general150_runtime_work']
 result={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for root in roots for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' and p.name not in ('frozen_sources.json',)}
 record=json.loads((BASE/'review367_joint_attempt2/actual367.json').read_text())
 for n,h in record['trace']['source_inventory'].items():
  actual=hashlib.sha256((BASE/n).read_bytes()).hexdigest()
  if actual!=h:raise ValueError('PRODUCER_SOURCE_DRIFT:'+n)
  result[n]=actual
 return result

def evaluate367(record,budget=90):
 if not 0<budget<=90:raise ValueError('BUDGET_SCOPE')
 start=time.monotonic();deadline=start+budget;before=inventory();input_hash=digest(record)
 context=resolve(copy.deepcopy(record),deadline);candidate=record['candidate'];model=copy.deepcopy(candidate['model'])
 from named_checks118 import adapters_for_workflow,APPLICABILITY_ADAPTERS
 from rule_contract118 import BUILTINS,_method
 callbacks=adapters_for_workflow(context)
 methods={k:_method(v) for k,v in {**callbacks,**BUILTINS}.items()}
 registry={'schema':'FIXED_JOINT_SOURCE367_METHOD_REGISTRY','sources':before,'methods':methods,'applicability':{k:_method(v) for k,v in APPLICABILITY_ADAPTERS.items()},'built_before_evaluate':True}
 from checker114 import evaluate
 raw=evaluate(model,workflow_context=context)
 if not verify_context(model,context)['verified']:raise ValueError('POST_REVIEW_CONTEXT_INVALID_OR_EXPIRED')
 if raw.get('model_hash')!=digest(model):raise ValueError('RAW_MODEL_HASH')
 if before!=inventory() or input_hash!=digest(record):raise ValueError('SOURCE_OR_INPUT_CHANGED')
 return {'schema':'JOINT367_SOURCE_VALIDATION','raw_report':raw,'expected_method_registry':registry,'provenance':context._proof,'input_record_digest':input_hash,'outer_trace_digest':digest(record['trace']),'model_digest':digest(model),'fresh_checker_executed':True,'semantic_engine_executed':False,'accepted':False,'delivery_allowed':False,'seconds':time.monotonic()-start,'source_unchanged':True}
