"""Current-input semantic computation, no equivalence attestation or old issuer."""
import ast,copy,json,sys,time,types
from pathlib import Path
from gate373 import views,validate,D,HERE,ROOT
SEM=ROOT/'semantic_rules357'
RULES=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY')

def run(record,fresh,lineage):
 before=D([record,fresh,lineage]);env,res,binding=views(record,fresh,lineage)
 sys.path.insert(0,str(SEM))
 import common
 common.REGISTRY_NAME='method_registry_source365.json' # isolated373 process; unchanged methods verified by gate
 rs=common.rows(record['candidate']['model'],fresh['raw_report'])
 path=ROOT/'staging351_collision_lineage/fresh_bridge.py';code=path.read_text();mod=types.ModuleType('_semantic373_pinned351');mod.__file__=str(path);exec(compile(code,str(path),'exec'),mod.__dict__)
 contract,_=mod._group_sources285();mod._network_sources288()
 node=next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)and n.name=='source_groups285');source=ast.get_source_segment(code,node)
 body=source[source.index(" raw=result['raw_fresh_report']"):source.index(" _phase293('network.begin')")]
 fn="def predicates373(envelope,result,contract,methods):\n model=envelope['packet']['world_model'];mh=_digest_model282(model)\n"+body+" return summaries\n"
 ns=dict(mod.__dict__);exec(compile(fn,'<373_PINNED351_UNCHANGED_PREDICATES>','exec'),ns)
 rows=ns['predicates373'](env,res,contract,{k:fresh['expected_method_registry']['methods'][k]for k in mod.GROUP285_IDS})
 from network373 import evaluate as network
 net=network(env,res,rows,2);rows.append(net)
 groups={'schema':'CURRENT373_RECOMPUTED_GROUPS','model_hash':binding['model_digest'],'fresh_result_digest':D(res),'original_result_digest':D(fresh),'rows':rows,'review_verdict':'FAIL'if any(g['verdict']=='FAIL'for g in rows)else'UNKNOWN'if any(g['verdict']=='UNKNOWN'for g in rows)else'SCOPED_PASS'}
 evidence={'nine_prerequisites':groups};errors={}
 for name in ('living','guest','kitchen'):
  try:
   module=__import__(name+'_closure373');evidence[name]=module.evaluate(env,res,groups,seconds=8 if name!='living'else 6)
  except Exception as e:errors[name]=type(e).__name__+':'+str(e)
 try:
  from closure_openings import evaluate
  evidence['openings']=evaluate(record['candidate']['model'],fresh['raw_report'])
 except Exception as e:errors['openings']=type(e).__name__+':'+str(e)
 try:
  from closure_room_program365 import bundle_inventory
  evidence['room_bundle_inventory']=bundle_inventory(record['candidate']['model'],rs)
 except Exception as e:errors['room_bundle_inventory']=type(e).__name__+':'+str(e)
 try:
  from author233_spatial_mapping import evaluate
  evidence['author_spatial_mapping']=evaluate(env,evidence.get('living',{}),evidence.get('guest',{}))
 except Exception as e:errors['author_spatial_mapping']=type(e).__name__+':'+str(e)
 seams={
 'SPACE_ACCOUNTING':['CURRENT_ROLE_DAG_WHOLE_Q11_NOT_RECOMPUTED','CURRENT_EXPANDED_Q04_REQUIRED'],
 'CIRCULATION_NECESSITY':['q04_runner365.py_HARDCODES_OLD_INPUT','balanced365_extended_runner.py_HARDCODES_OLD_INPUT'],
 'COMMON_CORE_COMPACTNESS':['CURRENT_ROLE_DAG_COMMON_Q04_Q12_NOT_RECOMPUTED'],
 'PRIVACY_WITHOUT_FAKE_BAFFLE':['CURRENT_WALL_PURPOSE_Q04_WHOLE_ROLE_DEPENDENCIES_NOT_RECOMPUTED'],
 'SERVICE_COMPACTNESS':['service_runner365.py_HARDCODES_OLD_INPUT;CURRENT_SERVICE_PARTITION_COMPARISON_REQUIRED'],
 'BEDROOM_GROUPING':['bedroom_grouping365.py_FIXED_VIEW_GATE;CURRENT_TASK_ROUTE_FINITE_COMPARISON_REQUIRED'],
 'ROOM_PROGRAM_CAPACITY':['BUNDLE_INVENTORY_ONLY;FULL_ROOM_ACCESS_APPLICABILITY_CLOSURE_NOT_RECOMPUTED'],
 'OPENINGS_REAL':['CURRENT_SCOPED_OPENINGS_PROOF_INDEPENDENT_REVIEW_REQUIRED'],
 'LIVING_USEFUL_CONTIGUITY':['CURRENT_INTRINSIC_AND_AUTHOR_APPLICABILITY_PROOF_INDEPENDENT_REVIEW_REQUIRED'],
 'GUEST_ROUTE_INDEPENDENCE':['CURRENT_FOUR_RELATION_AND_AUTHOR_APPLICABILITY_PROOF_INDEPENDENT_REVIEW_REQUIRED'],
 'KITCHEN_PROXIMITY':['CURRENT_ESSENTIAL_RELATIONS_PROOF_INDEPENDENT_REVIEW_REQUIRED']}
 key_by_rule={'OPENINGS_REAL':'openings','LIVING_USEFUL_CONTIGUITY':'living','GUEST_ROUTE_INDEPENDENCE':'guest','KITCHEN_PROXIMITY':'kitchen'}
 quality=[]
 for rid in RULES:
  key=key_by_rule.get(rid);item=evidence.get(key,{})if key else {};local=item.get('evidence',{})
  local_model=local.get('model_hash',local.get('model_digest'))
  local_fresh=local.get('base_fresh_digest',local.get('fresh_digest',local.get('raw_digest')))
  computed=bool(key and key not in errors and local_model==binding['model_digest'] and local_fresh in (D(res),D(fresh['raw_report'])))
  quality.append({'rule_id':rid,'verdict':'UNKNOWN','missing':seams[rid],**binding,'proof_recomputed':computed,
   'compute_status':'BOUND_SCOPED_EVIDENCE_RETURNED'if computed else'FAILED_OR_UNBOUND_RETURN'if key else'NOT_IMPLEMENTED_CURRENT_INPUT',
   'evidence_key':key,'evidence_digest':D(item)if item else None,'no_old_parent_pass_reused':True})
 # Bind every raw evidence item, including partial/UNKNOWN output, without
 # asserting it is a complete proof. Local gates above determine compute status.
 evidence_bindings={k:{**binding,'evidence_digest':D(v),'view_result_digest':D(res),'recomputation_attempted':True}for k,v in evidence.items()}
 validate(record,fresh,lineage)
 if before!=D([record,fresh,lineage]):raise ValueError('INPUT_MUTATION')
 return {'schema':'CURRENT373_SEMANTIC_PROOF_CANDIDATES','binding':binding,'quality':quality,'evidence':evidence,'evidence_bindings':evidence_bindings,'errors':errors,'whole_parent_qualification':False,'semantic_prerequisites_recomputed':True,'fresh_review_reused_from372':True,'new_fresh_checker_executed':False,'old_fixed_artifact_issuers_called':False,'equivalence_attestation_used':False,'test_only':True,'accepted':False,'delivery_allowed':False}
