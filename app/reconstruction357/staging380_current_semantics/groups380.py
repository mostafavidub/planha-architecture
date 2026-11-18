"""Current378 views plus unchanged351 semantic predicates; no old artifact gate."""
import ast,copy,types
from gate380 import views,validate,D,ROOT
_CACHE=None
def build(record,new_result,seconds=8,source_profile='SOURCE_BALANCED365'):
 global _CACHE
 binding=validate(record,new_result)
 if _CACHE is not None:return copy.deepcopy(_CACHE)
 env,res,_=views(record,new_result)
 path=ROOT/'staging351_collision_lineage/fresh_bridge.py';code=path.read_text();mod=types.ModuleType('_semantic380_pinned351');mod.__file__=str(path);exec(compile(code,str(path),'exec'),mod.__dict__)
 contract,_=mod._group_sources285();mod._network_sources288()
 node=next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)and n.name=='source_groups285');s=ast.get_source_segment(code,node);body=s[s.index(" raw=result['raw_fresh_report']"):s.index(" _phase293('network.begin')")]
 ns=dict(mod.__dict__);exec(compile("def predicates380(envelope,result,contract,methods):\n model=envelope['packet']['world_model'];mh=_digest_model282(model)\n"+body+" return summaries\n",'<UNCHANGED351_SEMANTIC_PREDICATES>','exec'),ns)
 rows=ns['predicates380'](env,res,contract,{k:new_result['expected_method_registry']['methods'][k]for k in mod.GROUP285_IDS})
 from network380 import evaluate
 rows.append(evaluate(env,res,rows,min(seconds,2)))
 groups={'schema':'CURRENT380_RECOMPUTED_GROUPS','model_hash':binding['model_digest'],'fresh_result_digest':D(res),'original_result_digest':D(new_result),'rows':rows,'review_verdict':'FAIL'if any(g['verdict']=='FAIL'for g in rows)else'UNKNOWN'if any(g['verdict']=='UNKNOWN'for g in rows)else'SCOPED_PASS'}
 _CACHE={'envelope':env,'result':res,'groups':groups};return copy.deepcopy(_CACHE)
