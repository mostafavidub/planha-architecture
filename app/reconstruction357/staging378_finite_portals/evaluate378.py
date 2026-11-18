"""Fresh current-model review with derived source replay; no semantics reuse."""
import copy,hashlib,json,sys,time,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from source378 import inventory
sys.path.insert(0,str(HERE/'runtime'))
from contract114 import digest
from source_registry365 import resolve,verify_context
def module_origin_audit():
 import importlib
 critical=('named_checks118','source_registry365','source_identity365','notch_grammar365','q11_boundary118','core_circulation_scope118')
 rows=[]
 for name in critical:
  mod=importlib.import_module(name);actual=Path(mod.__file__).resolve();expected=(HERE/'runtime'/(name+'.py')).resolve()
  if actual!=expected:raise ValueError('CRITICAL_MODULE_ORIGIN:'+name)
  rows.append({'module':name,'path':str(actual.relative_to(ROOT)),'sha256':hashlib.sha256(actual.read_bytes()).hexdigest(),'relation':'CURRENT378_RUNTIME'})
 for name,mod in list(sys.modules.items()):
  if name in critical or not getattr(mod,'__file__',None):continue
  actual=Path(mod.__file__).resolve();expected=HERE/'runtime'/(name+'.py')
  if actual.is_relative_to(ROOT)and expected.is_file()and actual!=expected.resolve():
   if actual.read_bytes()!=expected.read_bytes():raise ValueError('CACHED_NONIDENTICAL_MODULE:'+name)
   rows.append({'module':name,'path':str(actual.relative_to(ROOT)),'sha256':hashlib.sha256(actual.read_bytes()).hexdigest(),'relation':'EXACT_BYTES_UNCHANGED_MODULE'})
 return rows
def registry_for(context):
 from named_checks118 import adapters_for_workflow,APPLICABILITY_ADAPTERS
 from rule_contract118 import BUILTINS,_method
 callbacks=adapters_for_workflow(context)
 return {'schema':'FINITE378_CURRENT_METHOD_REGISTRY','sources':inventory(),
    'methods':{k:_method(v)for k,v in {**callbacks,**BUILTINS}.items()},
    'applicability':{k:_method(v)for k,v in APPLICABILITY_ADAPTERS.items()},'built_before_evaluate':True}
def evaluate378(record,budget=90):
 if type(budget)not in(int,float) or not 0<budget<=90:raise ValueError('BUDGET_SCOPE')
 start=time.monotonic();origins=module_origin_audit();before=inventory();record_hash=digest(record)
 context=resolve(copy.deepcopy(record),start+budget);m=copy.deepcopy(record['candidate']['model'])
 registry=registry_for(context)
 from checker114 import evaluate
 module_origin_audit()
 raw=evaluate(m,workflow_context=context)
 origins=module_origin_audit()
 if not verify_context(m,context)['verified']:raise ValueError('CONTEXT_EXPIRED_OR_CHANGED')
 if raw.get('model_hash')!=digest(m):raise ValueError('CURRENT_REVIEW_MODEL')
 if before!=inventory() or digest(record)!=record_hash:raise ValueError('SOURCE_OR_INPUT_CHANGED')
 return {'schema':'FINITE378_CURRENT_SOURCE_VALIDATION','review_id':str(uuid.uuid4()),
   'module_origins':origins,'raw_report':raw,'expected_method_registry':registry,'provenance':context._proof,
   'input_record_digest':record_hash,'outer_trace_digest':digest(record['trace']),
   'model_digest':digest(m),'fresh_checker_executed':True,'source_unchanged':True,
   'semantic_engine_executed':False,'semantic_qualification':'UNKNOWN_NEW_GEOMETRY_NOT_REPROVEN',
   'prior_quality_certificates_reused':False,'test_only':record['test_only'],
   'accepted':False,'delivery_allowed':False,'seconds':time.monotonic()-start}
if __name__=='__main__':print(json.dumps(evaluate378(json.load(sys.stdin)),ensure_ascii=False))
