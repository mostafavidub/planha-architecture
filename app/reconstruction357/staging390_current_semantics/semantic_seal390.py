"""Canonical dependency/Q12 sealing using unchanged original issuer contracts.
Raw386 role join is retained separately. This derives no new geometric verdict.
"""
import ast,copy
from gate390 import D,ROOT
from frozen390 import bytes_for,module
CAPACITY=('fixture_inventory_use','body_route_sweeps','chair_capacity_movement','bath_service_operation','kitchen_essential_operation','guest_living_route','guest_dining_route','serving_route')

def expected_dag():
 base=ast.parse(bytes_for(ROOT/'semantic_rules357/role_registry_model365.py'))
 assignment=next(n for n in base.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='DAG'for t in n.targets));dag=ast.literal_eval(assignment.value)
 tree=ast.parse(bytes_for(ROOT/'semantic_rules357/role_registry_balanced365_expanded367_v3.py'));selected=[]
 for n in tree.body:
  if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='DAG'for t in n.targets):selected.append(n)
  elif isinstance(n,ast.AugAssign)and isinstance(n.target,ast.Subscript)and isinstance(n.target.value,ast.Name)and n.target.value.id=='DAG':selected.append(n)
  elif isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and isinstance(n.value.func.value,ast.Subscript)and isinstance(n.value.func.value.value,ast.Name)and n.value.func.value.value.id=='DAG':selected.append(n)
 if len(selected)!=3:raise ValueError('EXACT_FINAL_DAG_SOURCE_SHAPE')
 ns={'copy':copy,'ORIGINAL_DAG':dag};exec(compile(ast.Module(body=selected,type_ignores=[]),'<UNCHANGED_FINAL_DAG>','exec'),ns)
 return ns['DAG']

def dependency_tools():return module(ROOT/'semantic_rules357/role_dependency_seal367.py','_current390_unchanged_dependency_seal')

def seal_current(record,fresh,roles,joined):
 before=D([record,fresh,roles,joined]);mh=D(record['candidate']['model']);binding={'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':mh}
 for value in (roles,joined):
  if any(value['binding'].get(k)!=v for k,v in binding.items()):raise ValueError('CURRENT_SEAL_BINDING')
 for key,value in roles['evidence'].items():
  proof=roles['evidence_bindings'][key]
  if proof['evidence_digest']!=D(value)or any(proof.get(k)!=v for k,v in binding.items()):raise ValueError('CURRENT_ROLE_EVIDENCE:'+key)
 dag=expected_dag();out=copy.deepcopy(joined);nodes=out['nodes']
 if set(nodes)!=set(dag):raise ValueError('CURRENT_DAG_INVENTORY')
 # A seal never turns an UNKNOWN role into PASS. Missing constructive evidence
 # must remain a qualification blocker, not be synthesized as a dependency row.
 q12=nodes['Q12_PER_UNIT']
 if q12['status']!='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW':raise ValueError('Q12_NOT_READY_FOR_CANONICAL_SEAL')
 if any(not nodes[k]['status'].startswith('PASS_')for k in dag['Q12_PER_UNIT']):raise ValueError('Q12_REQUIRED_ROLE_NOT_PASS')
 import common
 current_rows=common.rows(record['candidate']['model'],fresh['raw_report'])
 for key in CAPACITY:
  if current_rows[key]['status']!='PASS_LIMITED':raise ValueError('CURRENT_UNIT_CAPACITY_USE_ACCESS:'+key)
 room_roles=roles['evidence']['source_room_roles'];expected_ids={u['id']for u in record['candidate']['model']['units']}
 if {u['unit']for u in q12['evidence']}!=expected_ids or len(q12['evidence'])!=len(expected_ids):raise ValueError('CURRENT_UNIT_INVENTORY')
 for unit in q12['evidence']:
  source=[r for r in room_roles if r['unit']==unit['unit']]
  if not source or any(not r['verdict'].startswith('PASS_')for r in source):raise ValueError('CURRENT_UNIT_SOURCE_ROOMS')
  unit['source_room_roles']=copy.deepcopy(source)
  unit['capacity_use_access_source_rows']={k:D(current_rows[k])for k in CAPACITY}
 tools=dependency_tools();nodes=tools.seal(nodes,dag)
 for unit in nodes['Q12_PER_UNIT']['evidence']:unit['dependency_digests']={k:D(nodes[k])for k in dag['Q12_PER_UNIT']}
 nodes=tools.seal(nodes,dag);tools.verify(nodes,dag)
 out.update(schema='CURRENT390_CANONICALLY_SEALED_ROLE_DAG',nodes=nodes,topological_order=tools.order(dag),model_hash=mh,record_digest=D(record),review_digest=D(fresh),raw_role_join_digest=D(joined),dependency_dag_source='UNMODIFIED_BALANCED365_EXPANDED367_V3_DAG',new_geometric_verdicts_added=False)
 for name,proof in out['parent_evidence'].items():
  if name=='DISTINCTNESS_AND_FAIRNESS':continue
  proof['unsealed_parent_evidence_digest']=D(joined['parent_evidence'][name])
  proof['closure_evidence_digest']=D(nodes[proof['closure_node']]);proof['dependency_evidence_digests']={k:D(nodes[k])for k in proof['required_dependency_nodes']}
 if D([record,fresh,roles,joined])!=before:raise ValueError('SEAL_INPUT_MUTATION')
 return out
