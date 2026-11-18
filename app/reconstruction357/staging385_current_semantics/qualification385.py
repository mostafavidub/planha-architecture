"""Exact scoped parent predicates from engine365_v3, with current evidence joins.
No heuristic promotion. Missing/unknown evidence stays unknown; source assumptions
and finite comparison limits are retained. Q14 is outside member qualification.
"""
from gate385 import D
RULES=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY')
HTML='046cb8490a0865b74a9f844fa7db513490c50393e21923d1aa458f846fa89108'
SECTIONS='98e39063ee7ba733335c450c7fb661b9939762873f19c788d1b0764cb2daf0e3'

def verify_joined_provenance(record,fresh,roles,joined):
 from frozen385 import module
 from gate385 import ROOT
 sealing=module(ROOT/'staging385_current_semantics/semantic_seal385.py','_current385_qualification_seal')
 dag=sealing.expected_dag();tools=sealing.dependency_tools();nodes=joined['nodes'];mh=D(record['candidate']['model'])
 tools.verify(nodes,dag)
 if joined['topological_order']!=tools.order(dag):raise ValueError('CURRENT_TOPOLOGICAL_ORDER')
 if joined['model_hash']!=mh or joined['record_digest']!=D(record)or joined['review_digest']!=D(fresh):raise ValueError('SEALED_ROLES_CURRENT_BINDING')
 if joined['input_roles_digest']!=D(roles)or joined['cohort_digest']!=D(roles['evidence']['cohort']):raise ValueError('SEALED_JOIN_INPUT_DIGESTS')
 q12=nodes['Q12_PER_UNIT'];deps=q12['sealed_dependency_digests'];required={'SOURCE_ROOM_USE','PUBLIC_SUPPORT','ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON'}
 if set(deps)!=required or set(q12['depends_on'])!=required or set(dag['Q12_PER_UNIT'])!=required:raise ValueError('EXACT_Q12_DEPENDENCY_INVENTORY')
 if any(deps[k]!=D(nodes[k])for k in required):raise ValueError('Q12_SEALED_DAG')
 balance=q12['balanced_common_access'];bh=D(balance)
 if balance['model_hash']!=mh or balance['record_digest']!=D(record)or balance['fresh_result_digest']!=D(fresh):raise ValueError('Q12_BALANCE_CURRENT_BINDING')
 if balance['verdict']!='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS'or not all(x['equal_fixed_source_metrics']for x in balance['comparisons']):raise ValueError('Q12_EXACT_BALANCE')
 import common
 rows=common.rows(record['candidate']['model'],fresh['raw_report']);room_roles=roles['evidence']['source_room_roles'];units=q12['evidence'];ids={u['id']for u in record['candidate']['model']['units']}
 if type(units)is not list or len(units)!=2 or len(ids)!=2 or {u['unit']for u in units}!=ids:raise ValueError('Q12_UNIT_INVENTORY')
 for u in units:
  if u['whole_unit_verdict']!='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW'or u['exact_pending']!=[]or u['balanced_access_digest']!=bh:raise ValueError('Q12_UNIT_PENDING_OR_BALANCE')
  if u['resolved_dependency_digests']!={k:deps[k]for k in('COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON')}:raise ValueError('Q12_UNIT_RESOLVED_DEPENDENCIES')
  expected_rooms=[r for r in room_roles if r['unit']==u['unit']]
  if not expected_rooms or D(u['source_room_roles'])!=D(expected_rooms):raise ValueError('Q12_CURRENT_SOURCE_ROOM_ROLES')
  if u['capacity_use_access_source_rows']!={k:D(rows[k])for k in sealing.CAPACITY}or any(rows[k]['status']!='PASS_LIMITED'for k in sealing.CAPACITY):raise ValueError('Q12_CURRENT_CAPACITY_USE_ACCESS_ROWS')
 return dag

def qualify(record,fresh,roles,joined):
 m=record['candidate']['model'];mh=D(m);b={'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':mh}
 if any(roles['binding'].get(k)!=v for k,v in b.items()):raise ValueError('CURRENT_ROLES_BINDING')
 e=roles['evidence'];essential=e['essential'];ev=essential['evidence'];results={k:'UNKNOWN'for k in RULES};reasons={};proofs={}
 for layer in (roles,essential):
  if any(layer['binding'].get(k)!=v for k,v in b.items()):raise ValueError('CURRENT_ESSENTIAL_BINDING')
  for name,value in layer['evidence'].items():
   p=layer['evidence_bindings'][name]
   if any(p.get(k)!=v for k,v in b.items())or p['evidence_digest']!=D(value):raise ValueError('CURRENT_EVIDENCE_BINDING:'+name)
 groups=ev['nine_prerequisites']
 if groups.get('review_verdict')!='SCOPED_PASS'or len(groups.get('rows',[]))!=9 or any(x.get('verdict')!='SCOPED_PASS'for x in groups['rows']):raise ValueError('NINE_CURRENT_PREREQUISITES')
 if any(v.get('codes',[None])[0:1]==['BINDING_OR_DISPATCH_BLOCKED']for name in ('base_modules_structure','base_modules_spatial','base_modules_comparison')for v in ev.get(name,{}).values()):raise ValueError('BASE_DISPATCH_BLOCKED')
 def apply(rule,fn,proof):
  try:
   if not fn():raise ValueError('EXACT_COMPLETE_PREDICATE_NOT_MET')
   results[rule]='PASS';proofs[rule]={'predicate_source':'semantic_rules357/engine365_v3.py','evidence_digest':D(proof),'model_digest':mh,'record_digest':D(record),'fresh_digest':D(fresh),'scope':'SCOPED_REGISTERED_CURRENT_SOURCE_ONLY'}
  except (KeyError,TypeError,ValueError,IndexError)as error:reasons[rule]=type(error).__name__+':'+str(error)
 opening=ev.get('openings',{})
 apply('OPENINGS_REAL',lambda:opening.get('scope_complete')is True and opening.get('codes')==[] and opening.get('missing')==['INDEPENDENT_AUDIT_BEFORE_PARENT_ENABLE'],opening)
 mapping=ev.get('author_mapping',{});closures=ev.get('primitive',{}).get('source_closures',{})
 for parent,rule,closure in [('LIVING_USEFUL_CONTIGUITY','Q02','living_closure'),('GUEST_ROUTE_INDEPENDENCE','Q06','guest_closure')]:
  apply(parent,lambda rule=rule: mapping['source_html_sha256']==HTML and mapping['extracted_sections_sha256']==SECTIONS and mapping['rules'][rule].get('audit_recommendation')=='ELIGIBLE_CURRENT_PROFILE_PARENT_CLOSURE_PENDING_INDEPENDENT_AUDIT',{'mapping':mapping,'closure':closures.get(closure)})
 kitchen=closures.get('kitchen_closure',{})
 apply('KITCHEN_PROXIMITY',lambda:kitchen.get('verdict')=='PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS'and kitchen.get('evidence',{}).get('model_hash')==mh,kitchen)
 room=ev.get('room_program',{})
 apply('ROOM_PROGRAM_CAPACITY',lambda:room.get('proofscopecomplete')is True and room.get('missing')==[] and room.get('evidence',{}).get('model_hash')==mh and room.get('evidence',{}).get('raw_hash')==D(fresh['raw_report']),room)
 grouping=ev.get('bedroom_grouping',{})
 apply('BEDROOM_GROUPING',lambda:grouping.get('verdict')=='PASS_SCOPED_REVIEWED_TRADEOFF'and grouping.get('proofscopecomplete')is True and grouping.get('missing')==[] and grouping['evidence']['model_digest']==mh and grouping['evidence']['raw_digest']==D(fresh['raw_report']),grouping)
 service=e.get('service',{})
 apply('SERVICE_COMPACTNESS',lambda:service.get('verdict')=='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'and service.get('source_profile')=='SOURCE_BALANCED365'and service.get('record_digest')==D(record)and service.get('fresh_result_digest')==D(fresh)and all(service[k].get('verdict')=='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'and service[k]['evidence'][1]['model_digest']==mh for k in('against362','against359')),service)
 if joined is not None:
  if any(joined['binding'].get(k)!=v for k,v in b.items()):raise ValueError('JOINED_CURRENT_BINDING')
  dag=verify_joined_provenance(record,fresh,roles,joined)
  expected_parent_deps={'SPACE_ACCOUNTING':dag['Q11_WHOLE_ROLE'],'CIRCULATION_NECESSITY':dag['Q04_COMPARISON'],'PRIVACY_WITHOUT_FAKE_BAFFLE':dag['Q05_PRIVACY'],'COMMON_CORE_COMPACTNESS':['COMMON_ROLE','Q11_WHOLE_ROLE','Q04_COMPARISON','Q12_PER_UNIT']}
  for rule in ('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','PRIVACY_WITHOUT_FAKE_BAFFLE','COMMON_CORE_COMPACTNESS'):
   proof=joined['parent_evidence'][rule];nodes=joined['nodes']
   def complete(proof=proof,rule=rule):
    if set(proof['required_dependency_nodes'])!=set(expected_parent_deps[rule])or set(proof['dependency_evidence_digests'])!=set(expected_parent_deps[rule]):raise ValueError('PARENT_COMPLETE_DEPENDENCY_INVENTORY')
    node=nodes[proof['closure_node']]
    return proof['verdict']=='PASS_SCOPED_INTERNAL_CURRENT_SOURCE'and proof['missing']==[] and proof['model_hash']==mh and proof['fresh_result_digest']==D(fresh)and proof['record_digest']==D(record)and proof['closure_evidence_digest']==D(node)and not node['blocking_dependencies']and all(h==D(nodes[dep])and nodes[dep]['status'].startswith('PASS_')and not nodes[dep]['blocking_dependencies']for dep,h in proof['dependency_evidence_digests'].items())
   apply(rule,complete,proof)
  q12=joined['nodes']['Q12_PER_UNIT'];q12_ok=q12['status']=='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW'and not q12['blocking_dependencies']
  if q12_ok:
   unit_ids={u['id']for u in m['units']};q12_ok={u['unit']for u in q12['evidence']}==unit_ids and all(u['whole_unit_verdict']==q12['status']and u['exact_pending']==[]for u in q12['evidence'])
 else:q12_ok=False
 cohort=e.get('cohort',{});closed=cohort.get('full_q04_closed')is True and cohort.get('remaining')==[] and cohort.get('verdict')=='PASS_SCOPED_DECLARED_FINITE_Q04'
 missing=[k+':'+reasons.get(k,'CURRENT_COMPLETE_PROOF_UNAVAILABLE')for k,v in results.items()if v!='PASS']
 if not q12_ok:missing.append('Q12_CURRENT_UNIT_QUALIFICATION_UNCLOSED')
 if not closed:missing.append('DECLARED_FINITE_COHORT_UNCLOSED')
 return {'qualified':not missing,'parent_verdicts':results,'q12_verdict':'PASS'if q12_ok else'UNKNOWN','cohort_closed':closed,'missing':missing,'parent_proofs':proofs,
         'model_digest':mh,'record_digest':D(record),'fresh_digest':D(fresh),'selection_set_qualification':False,'scope':'CURRENT_REGISTERED_FINITE_SOURCE_MEMBER_CONCEPT_ONLY_NOT_GLOBAL_OR_TECHNICAL_APPROVAL'}
