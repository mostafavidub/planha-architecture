"""Fresh current-model review with derived source replay; no semantics reuse."""
import copy,hashlib,json,sys,time,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(HERE/'runtime'))
from contract114 import digest
from source_registry365 import resolve,verify_context
def inventory():
 base=json.loads((ROOT/'staging368_ui_api/source_manifest.json').read_text())['files']
 for name,want in base.items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=want:raise ValueError('BASE_SOURCE_CHANGED:'+name)
 new={str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
      for folder in (HERE,ROOT.parent/'staging369_current_family_repair')
      for p in folder.rglob('*') if p.is_file() and p.suffix in ('.py','.json') and '__pycache__'not in p.parts}
 return {'baseline368':base,'derived369':new}
def evaluate369(record,budget=90):
 if type(budget)not in(int,float) or not 0<budget<=90:raise ValueError('BUDGET_SCOPE')
 start=time.monotonic();before=inventory();record_hash=digest(record)
 context=resolve(copy.deepcopy(record),start+budget);m=copy.deepcopy(record['candidate']['model'])
 from named_checks118 import adapters_for_workflow,APPLICABILITY_ADAPTERS
 from rule_contract118 import BUILTINS,_method
 callbacks=adapters_for_workflow(context)
 registry={'schema':'DERIVED369_CURRENT_METHOD_REGISTRY','sources':before,
    'methods':{k:_method(v)for k,v in {**callbacks,**BUILTINS}.items()},
    'applicability':{k:_method(v)for k,v in APPLICABILITY_ADAPTERS.items()},'built_before_evaluate':True}
 from checker114 import evaluate
 raw=evaluate(m,workflow_context=context)
 if not verify_context(m,context)['verified']:raise ValueError('CONTEXT_EXPIRED_OR_CHANGED')
 if raw.get('model_hash')!=digest(m):raise ValueError('CURRENT_REVIEW_MODEL')
 if before!=inventory() or digest(record)!=record_hash:raise ValueError('SOURCE_OR_INPUT_CHANGED')
 return {'schema':'DERIVED369_CURRENT_SOURCE_VALIDATION','review_id':str(uuid.uuid4()),
   'raw_report':raw,'expected_method_registry':registry,'provenance':context._proof,
   'input_record_digest':record_hash,'outer_trace_digest':digest(record['trace']),
   'model_digest':digest(m),'fresh_checker_executed':True,'source_unchanged':True,
   'semantic_engine_executed':False,'semantic_qualification':'UNKNOWN_NEW_GEOMETRY_NOT_REPROVEN',
   'prior_quality_certificates_reused':False,'test_only':record['test_only'],
   'accepted':False,'delivery_allowed':False,'seconds':time.monotonic()-start}
if __name__=='__main__':print(json.dumps(evaluate369(json.load(sys.stdin)),ensure_ascii=False))
