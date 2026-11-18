"""New reconstructed source profile, real checker; no semantic admission."""
import sys,json,hashlib,copy,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(HERE/'runtime'))
from contract114 import digest
from source_registry362 import resolve,verify_context

def inventory():
 roots=[HERE,BASE/'staging362_core_notch',BASE/'staging359_hall_clamp',BASE/'planha_general150_runtime_work']
 result={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for root in roots for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' and p.name not in ('frozen_sources.json',)}
 for name in ('staging358_comparative/row_candidate358.json','staging358_comparative/row_adapter358.py','staging358_comparative/row_body358.py'):
  baseline=BASE/name;result[name]=hashlib.sha256(baseline.read_bytes()).hexdigest()
 return result

def evaluate362(record,budget=90):
 if not 0<budget<=90:raise ValueError('BUDGET_SCOPE')
 start=time.monotonic();deadline=start+budget;before=inventory();input_hash=digest(record)
 context=resolve(copy.deepcopy(record),deadline);candidate=record['candidate'];model=copy.deepcopy(candidate['model'])
 from named_checks118 import adapters_for_workflow,APPLICABILITY_ADAPTERS
 from rule_contract118 import BUILTINS,_method
 callbacks=adapters_for_workflow(context)
 methods={k:_method(v) for k,v in {**callbacks,**BUILTINS}.items()}
 registry={'schema':'FIXED_SOURCE362_METHOD_REGISTRY','sources':before,'methods':methods,'applicability':{k:_method(v) for k,v in APPLICABILITY_ADAPTERS.items()},'built_before_evaluate':True}
 from checker114 import evaluate
 raw=evaluate(model,workflow_context=context)
 if not verify_context(model,context)['verified']:raise ValueError('POST_REVIEW_CONTEXT_INVALID_OR_EXPIRED')
 if raw.get('model_hash')!=digest(model):raise ValueError('RAW_MODEL_HASH')
 if before!=inventory() or input_hash!=digest(record):raise ValueError('SOURCE_OR_INPUT_CHANGED')
 return {'schema':'RECONSTRUCTED362_CORE_NOTCH_SOURCE_VALIDATION','raw_report':raw,'expected_method_registry':registry,'provenance':context._proof,'input_record_digest':input_hash,'outer_trace_digest':digest(record['trace']),'model_digest':digest(model),'fresh_checker_executed':True,'semantic_engine_executed':False,'accepted':False,'delivery_allowed':False,'seconds':time.monotonic()-start,'source_unchanged':True}
