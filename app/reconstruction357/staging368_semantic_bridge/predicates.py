"""Current nine predicates under new368 gate; never invokes old fixed-artifact gate.
Must run in an isolated pre-import-pinned bridge worker. Source kernels are
unchanged; only their pure predicate body is called after full readset validation.
"""
import ast,types,json,hashlib,copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SEM=ROOT/'semantic_rules357'
from equivalence import digest

def evaluate(record,fresh,kind,reference_registry,seconds=8):
 if kind not in('balanced','joint')or type(seconds)not in(int,float)or not 0<seconds<=10:raise ValueError('REGISTERED_KIND_AND_BUDGET')
 before_inputs=digest([record,fresh])
 # No acceptance flag from caller. Independently perform exact binding first.
 from equivalence import compare
 spec=reference_registry['members'][kind];oldr,oldf=[json.loads((ROOT/spec['paths'][k]).read_text())for k in ('record','fresh')];equivalent=compare(oldr,oldf,record,fresh)
 for n,h in reference_registry['sources'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('PREREGISTERED_SOURCE_CHANGED:'+n)
 sys.path.insert(0,str(SEM))
 def module(path,name):
  b=path.read_bytes();rel=str(path.relative_to(ROOT));pins=reference_registry['sources'];expected=pins.get(rel)
  if expected is None:
   matches=[v for k,v in pins.items()if(ROOT/k).resolve()==path.resolve()]
   if len(set(matches))!=1:raise ValueError('SOURCE_ALIAS_NOT_REGISTERED:'+rel)
   expected=matches[0]
  if hashlib.sha256(b).hexdigest()!=expected:raise ValueError('KERNEL_SOURCE_CHANGED:'+rel)
  m=types.ModuleType(name);m.__file__=str(path);exec(compile(b,str(path),'exec'),m.__dict__);return m
 cm=module(SEM/'common.py','_current368_common');cm.REGISTRY_NAME='method_registry_source365.json'if kind=='balanced'else'method_registry_source367.json';cm.rows(record['candidate']['model'],fresh['raw_report'])
 bridge=module(ROOT/'staging351_collision_lineage/fresh_bridge.py','_current368_source351')
 contract,_=bridge._group_sources285();bridge._network_sources288()
 c=record['candidate'];envelope={'schema':'CURRENT368_SEMANTIC_VIEW','candidate_id':digest(c),'raw':copy.deepcopy(c['request']),'packet':copy.deepcopy(c['packet']),'input_record_digest':digest(record),'outer_trace_digest':digest(record['trace']),'original_result_digest':digest(fresh),'artifact_reassessment_only':False,'new_fresh_execution':False}
 result={'schema':'CURRENT368_SEMANTIC_RESULT_VIEW','candidate_digest':digest(envelope),'raw_fresh_report':copy.deepcopy(fresh['raw_report']),'original_result_digest':digest(fresh),'input_record_digest':digest(record),'outer_trace_digest':digest(record['trace']),'artifact_reassessment_only':False,'new_fresh_execution':False}
 source=(ROOT/'staging351_collision_lineage/fresh_bridge.py').read_text();tree=ast.parse(source);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='source_groups285');text=ast.get_source_segment(source,node);body=text[text.index(" raw=result['raw_fresh_report']"):text.index(" _phase293('network.begin')")]
 fn="def current_predicates(envelope,result,contract,methods):\n model=envelope['packet']['world_model'];mh=_digest_model282(model)\n"+body+" return summaries\n";ns=dict(bridge.__dict__);exec(compile(fn,'<PREREGISTERED368_PURE_PREDICATES_FROM351>','exec'),ns)
 registry=fresh['expected_method_registry'];groups=ns['current_predicates'](envelope,result,contract,{k:registry['methods'][k]for k in bridge.GROUP285_IDS})
 network_name='network365'if kind=='balanced'else'network367';network=module(SEM/(network_name+'.py'),'_current368_'+network_name)
 # Deliberately do not invoke its old fixed-view evaluate() entrypoint. A new
 # current binding above authorizes this unchanged pure geometric kernel.
 ng=network._kernel(envelope,result,groups,min(seconds,2));groups.append(ng)
 if digest(result['raw_fresh_report'])!=digest(fresh['raw_report']):raise ValueError('CURRENT_RAW_MUTATED')
 if digest([record,fresh])!=before_inputs:raise ValueError('CURRENT_PREDICATE_INPUT_MUTATION')
 for n,h in reference_registry['sources'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('POST_PREDICATE_SOURCE_CHANGED:'+n)
 states=[x['verdict']for x in groups];verdict='FAIL'if'FAIL'in states else'UNKNOWN'if'UNKNOWN'in states else'SCOPED_PASS'
 return{'schema':'CURRENT368_NINE_SEMANTIC_PREREQUISITES','kind':kind,'model_hash':equivalent['model_digest'],'current_fresh_digest':digest(fresh),'current_record_digest':digest(record),'rows':groups,'review_verdict':verdict,'current_predicates_recomputed':True,'new_fresh_checker_executed_by_this_callback':False,'old_fixed_artifact_gate_invoked':False,'scope':'New gate plus unchanged pinned pure semantic/geometry kernels on current record and own fresh report; not a replay of cached group verdicts.'}
