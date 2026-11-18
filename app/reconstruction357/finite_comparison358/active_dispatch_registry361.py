"""Read exact engine150 active schedule, not all files in runtime backup."""
from build_ledger import *
import ast

def build_active_registry():
 source=ROOT/'planha_general150_runtime_work/engine150.py';tree=ast.parse(source.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='runtime');loop=next(n for n in ast.walk(fn)if isinstance(n,ast.For)and isinstance(n.target,ast.Tuple)and [x.id for x in n.target.elts]==['organization','family']);domain=ast.literal_eval(loop.iter)
 oldpath=ROOT/'actual_run/actual_response.json';old=json.loads(oldpath.read_text());completedpath=Path(__file__).with_name('active_dispatch_actual361.json');completion=json.loads(completedpath.read_text())if completedpath.exists()else None
 states={(a['organization'],a['family']):{'source':'actual_run/actual_response.json#/attempts/'+str(i),'attempt':a}for i,a in enumerate(old['attempts'])}
 if completion:
  for i,a in enumerate(completion['completed_attempts']):states[(a['organization'],a['family'])]={'source':'finite_comparison358/active_dispatch_actual361.json#/completed_attempts/'+str(i),'attempt':a}
 rows=[]
 for org,family in domain:
  data=states[(org,family)];a=data['attempt'];rows.append({'id':org+'__'+family,'source_pointer':{'file':'planha_general150_runtime_work/engine150.py','lines':[loop.lineno,loop.end_lineno],'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},'selector':{'organization':org,'family':family,'program':['twin','twin','double']if org=='L3'else['double','twin','twin'],'profile':'source6person','raw':old['raw']},'evidence_pointer':data['source'],'status':a['status'],'reason':a.get('reason'),'solver_status':a.get('proposal',{}).get('solver_status'),'not_global_infeasibility':True,'candidate_model_digest':a.get('candidate',{}).get('model_digest'),'eligibility':a.get('eligibility','NOT_INFERRED_FROM_SEARCH_STATUS')})
 return {'schema':'SOURCE150_ACTIVE_DISPATCH_REGISTRY361','actual_active_branch_count':len(rows),'branches':rows,'source_callgraph':['staging351_collision_lineage/program_adapter.py → engine150.runtime','engine150.runtime schedule → per-organization propose → explicit source gates → constructor129.build/context → independent checker'],'historical_not_active':['private_mixed_source132 standalone','private_stagger_source132 standalone','unlisted constructor family/topology combinations'],'historical_exclusion_reason':'Not selected by this exact registered source150 runtime tuple; not claimed impossible or unusable globally','fallback_program_2_or1':'Different required bedroom program; not same-program Q04 comparator, not authorized program reduction as repair','raw_digest':digest(old['raw']),'baseline_actual_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'completed_actual_sha256':hashlib.sha256(completedpath.read_bytes()).hexdigest()if completion else None,'search_status_is_not_eligibility':True,'scope_closed_for_Q04':False}
if __name__=='__main__':
 x=build_active_registry();Path(__file__).with_name('active_dispatch_registry_actual361.json').write_text(json.dumps(x,ensure_ascii=False,indent=2));print(x['actual_active_branch_count'])
