"""New finite-cohort derivation from unchanged joint367 proofs, never a reissued
SAME_INVOCATION receipt. Only cheap validation/comparison; no construction/fresh.

The conjunction extension is licensed by q04_closure367_v3.py:23-24. Downstream
positive dependency predicates are role_registry_final_joint367_v4.py:31-82;
service_criterion367_v4.py:17-36 retains its explicit AGAINST359 room scope.
All historical premises keep their original identities/digests and cohort scope.
"""
import ast,copy,hashlib,json,sys,types,uuid
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
D=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
PINS={
 'semantic_rules357/final_role_artifact_gate367.py':'3b23d391f1be295fcb5355e5e933194fded5252c45bd72e64d186159c557ff8b',
 'staging368_semantic_bridge/equivalence.py':'0287aa109152bdc408c0beb6fb5db6546af36848df148fa054ee7ae9d179eefa',
 'finite_comparison365/q04_closure365_v7.py':'c68b562e3ab14d6014cd711b2b880670a9c62f2fd7021aedee97a87f197ee002',
 'finite_comparison358/q04_closure359.py':'d8acbe42d3bfa2367be88296e6732a6f77ccee74d3ba7f0da33b0ebee08a15c0',
 'semantic_rules357/comparison_metrics.py':'952dbed32324f2d48d1428293bf68c438156801c70b9008168dea041f7365524',
 'semantic_rules357/role_registry_final_joint367_v4.py':'cddaa0a2c9da3e48ac0a13341c402d6eac8cbafaec6249959aa72f76a3acc78b',
 'semantic_rules357/role_dependency_seal367.py':'642164a2499b7e946643dcc364b7404f3cb7e89f4a9cb7e7a62982e906ffdd4a',
 'finite_comparison367/q04_closure367_v3.py':'a7ba944d29ffe4f63c920415a8efe78c2b402fdfc0562a0628b904fd4ea17c1d',
 'finite_comparison367/service_criterion367_v4.py':'cb2979bf3cf4c80f1ce9bd9dc587c6be44d89ac10b9deb042df4639e10b0ff65'}
RULES=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY')
GROUPS={'partition_ledger','door_operation','fixture_inventory_use','closet_operation','kitchen_essential_operation','bath_service_operation','program_functional_roles','privacy_scenarios','stored_living_network288'}
def _read(rel):return json.loads((ROOT/rel).read_text())
def _sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def _module(rel,name):
 p=ROOT/rel
 if _sha(p)!=PINS[rel]:raise ValueError('COMPOSITION_KERNEL_CHANGED:'+rel)
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def _comparison():
 # Complete unchanged metric module; only the exact named comparison functions.
 metrics=_module('semantic_rules357/comparison_metrics.py','_joint390_metrics')
 ns={'F':F,**{k:getattr(metrics,k)for k in('measure_model','route_metrics','rectangle_union_area')}}
 for rel,names in [('finite_comparison358/q04_closure359.py',{'dimensions'}),('finite_comparison365/q04_closure365_v7.py',{'objective','compare'})]:
  p=ROOT/rel
  if _sha(p)!=PINS[rel]:raise ValueError('COMPARISON_SOURCE_CHANGED')
  nodes=[n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)and n.name in names]
  if {n.name for n in nodes}!=names:raise ValueError('COMPARISON_FUNCTION_INVENTORY')
  exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
 return ns['compare']

def extension_condition(old_q04,rows):
 """Pure fail-closed conjunction. FALSE means witnessed non-dominance only."""
 if old_q04.get('verdict')!='PASS_SCOPED_FINITE_Q04_SOURCE_JOINT367'or old_q04.get('remaining')!=[]or old_q04.get('domain',{}).get('domain_closed')is not True:return False
 if len(rows)!=2 or {r.get('id')for r in rows}!={'finite_rank1','finite_rank2'}:return False
 for row in rows:
  c=row.get('comparison',{})
  if row.get('eligible')is not True or c.get('dominance')!='FALSE'or not c.get('strict_worse_witnesses'):return False
  if any(F(w['alternative'])<=F(w['current'])or F(w['alternative_increase'])!=F(w['alternative'])-F(w['current'])for w in c['strict_worse_witnesses']):return False
 return True

def _intrinsic(record,fresh,intrinsic):
 e=intrinsic.get('evidence',{})
 if intrinsic.get('verdict')!='PASS'or intrinsic.get('eligible')is not True:raise ValueError('ADDED_MEMBER_INTRINSIC_UNKNOWN')
 rows=intrinsic.get('rows',[])
 if len(rows)!=18 or {r['id']for r in rows}!={f'B{i:02}'for i in range(1,19)} or any(r.get('verdict')!='PASS'for r in rows):raise ValueError('ADDED_MEMBER_18_ROWS')
 if e.get('record_digest')!=D(record)or e.get('new_result_digest')!=D(fresh)or e.get('model_digest')!=D(record['candidate']['model']):raise ValueError('INTRINSIC_CURRENT_TRIPLE')
 return D(intrinsic)

def _frozen_bytes(path):
 path=Path(path).resolve()
 if not path.is_relative_to(W):raise ValueError('OUTSIDE_FROZEN_WORKSPACE')
 files=json.loads((W/'review390_preaudit/source_freeze.json').read_text())['files'];matches={h for n,h in files.items()if(W/n).resolve()==path}
 if len(matches)!=1:raise ValueError('UNREGISTERED_FROZEN_AUTHORITY:'+str(path.relative_to(W)))
 data=path.read_bytes()
 if hashlib.sha256(data).hexdigest()!=next(iter(matches)):raise ValueError('FROZEN_AUTHORITY_CHANGED')
 return data

def _frozen_read(path):return json.loads(_frozen_bytes(path))

def execution_complete(supervision,state,unchanged):
 return supervision.get('reason')=='COMPLETED'and supervision.get('worker_returncode')==0 and supervision.get('worker_reaped')is True and supervision.get('cleanup_verified')is True and supervision.get('unresolved')==[] and state.get('state')=='COMPLETED'and state.get('cleanup_verified')is True and unchanged.get('verified')is True

def _rank2_authority(record,fresh):
 folder=W/'review384_actual_v1';sem=_frozen_read(folder/'result.json')
 supervision=_frozen_read(folder/'supervision.json');state=_frozen_read(folder/'state.json');pre=_frozen_read(folder/'preregistration.json');unchanged=_frozen_read(folder/'source_unchanged.json')
 if not execution_complete(supervision,state,unchanged):raise ValueError('RANK2_INTRINSIC_EXECUTION_NOT_VERIFIED')
 frozen=_frozen_bytes(W/'review384_preaudit/source_freeze.json')
 if hashlib.sha256(frozen).hexdigest()!=pre['freeze_sha256']:raise ValueError('RANK2_PREREGISTERED_FREEZE')
 for n,h in json.loads(frozen)['files'].items():
  if _sha(W/n)!=h:raise ValueError('RANK2_PREREGISTERED_SOURCE_CHANGED:'+n)
 path=ROOT/'staging384_rank2_semantics/gate384.py';data=_frozen_bytes(path)
 mod=types.ModuleType('_joint390_actual384_gate');mod.__file__=str(path)
 sys.path.insert(0,str(ROOT/'staging378_finite_portals'));exec(compile(data,str(path),'exec'),mod.__dict__)
 binding=mod.validate(record,fresh)
 if pre['binding']!=binding or sem['binding']!=binding:raise ValueError('RANK2_EXECUTION_SOURCE_BINDING')
 audit=_frozen_read(folder/'independent_audit.json')
 required={'rank2_binding','freeze','clean','intrinsic18','rank2_cohortbinding','rank0_coverage','retained_terminals','historical8','finite_q04','negative_witnesses','no_admission','wall_unknown_preserved'}
 if audit.get('schema')!='384_INDEPENDENT_POSTRUN_AUDIT'or audit.get('binding')!=binding or set(audit.get('checks',{}))!=required or any(v is not True for v in audit['checks'].values())or audit.get('raw_result_sha256')!=hashlib.sha256(_frozen_bytes(folder/'result.json')).hexdigest():raise ValueError('RANK2_INDEPENDENT_AUDIT_BINDING')
 if sem.get('schema')!='ACTUAL383_RANK2_INTRINSIC_AND_CURRENT379_FINITE_JOIN384'or sem.get('rank2_intrinsic_recomputed')is not True:raise ValueError('RANK2_384_AUTHORITY')
 return sem,{'independent_audit_digest':D(audit),'preregistration_digest':D(pre),'supervision_digest':D(supervision),'state_digest':D(state),'source_unchanged_digest':D(unchanged),'source_freeze_sha256':pre['freeze_sha256'],'binding':binding}

def rank0_mapping_check(coverage,old_members,baseline_record):
 required={'full_proposal','all_nonselector_core_fields','geometry_consumed_selector_fields','base_core_digest','ownership_family','exact_assembler_selector_readset'}
 if coverage.get('covered')is not True or set(coverage.get('checks',{}))!=required or any(v is not True for v in coverage['checks'].values()):raise ValueError('RANK0_FULL_SOURCE_COVERAGE')
 old=[r for r in old_members if r.get('id')=='balanced365']
 if len(old)!=1:raise ValueError('RANK0_OLD_BASELINE_INVENTORY')
 model=D(baseline_record['candidate']['model'])
 if coverage.get('baseline_model_digest')!=model or old[0].get('model_digest')!=model or old[0].get('record_digest')!=D(baseline_record):raise ValueError('RANK0_BASELINE_MODEL_RECORD_BINDING')
 if coverage.get('full_proposal_digest')!=D(baseline_record['trace']['proposal']):raise ValueError('RANK0_FULL_PROPOSAL_DIGEST')
 if coverage.get('assembler_source_digest')!=_sha(ROOT/'staging365_balanced_portals/assemble365.py')or coverage.get('core_source_digest')!=_sha(ROOT/'staging378_finite_portals/core378.py'):raise ValueError('RANK0_GEOMETRY_SOURCE_READSET')
 return {'verdict':'PASS_EXACT_RANK0_COVERAGE_BY_RETAINED_BALANCED365','coverage_digest':D(coverage),'baseline_model_digest':model,'baseline_record_digest':D(baseline_record),'all_geometry_predicates':copy.deepcopy(coverage['checks'])}

def _authority(bundle,rank,currentbinding):
 record=bundle['record'];fresh=bundle['fresh'];c=record['candidate'];t=record['trace'];mh=D(c['model']);proof=fresh['provenance']
 for k,v in {'input_record_digest':D(record),'outer_trace_digest':D(t),'model_digest':mh}.items():
  if fresh.get(k)!=v:raise ValueError('ADDED_MEMBER_FRESH:'+k)
 for k,v in {'input_record_digest':D(record),'outer_trace_digest':D(t),'model_hash':mh,'candidate_id':record['candidate_id'],'run_id':t['run_id'],'candidate_digest':D(c),'packet_digest':D(c['packet']),'raw':c['request']}.items():
  if proof.get(k)!=v:raise ValueError('ADDED_MEMBER_PROVENANCE:'+k)
 raw=fresh['raw_report']
 if proof.get('verified')is not True or not fresh.get('fresh_checker_executed')or not fresh.get('source_unchanged')or raw.get('model_hash')!=mh or raw.get('status')!='PASS_CONCEPT_SCOPED_REVIEW'or raw.get('errors')!=[]or raw.get('pending')!=[]:raise ValueError('ADDED_MEMBER_PHYSICAL_NOT_PASS')
 if t['selection_rank']!=rank or c['generation_context']['selection']!=t['enumeration'][rank]or record.get('test_only')is not False:raise ValueError('ADDED_MEMBER_RANK')
 for n,h in fresh['expected_method_registry']['sources'].items():
  if _sha(ROOT/n)!=h:raise ValueError('ADDED_MEMBER_SOURCE_CHANGED:'+n)
 if rank==1:
  if t['schema']!='FINITE_PORTALS378_SOURCE_TRACE_V1'or t['run_id']!=currentbinding['run_id']:raise ValueError('LIVE_RANK1_RUN')
  # Only the known server-owned member path, never a caller-provided proof path.
  folder=W/'review390_actual_v1/runs'/currentbinding['run_id']/'balanced'
  sem=json.loads((folder/'semantic.json').read_text());sup=json.loads((folder/'semantics_supervision.json').read_text())
  if not(sup.get('reason')=='COMPLETED'and sup.get('worker_returncode')==0 and sup.get('cleanup_verified')is True and sup.get('worker_reaped')is True and sup.get('unresolved')==[]):raise ValueError('LIVE_RANK1_SEMANTIC_RECEIPT')
  receipt=json.loads((folder/'semantics_worker_receipt.json').read_text())
  expected_receipt={'run_id':currentbinding['run_id'],'kind':'balanced','record_digest':D(record),'fresh_digest':D(fresh),'semantic_digest':D(sem),'source_guard_before_after':True}
  if any(receipt.get(k)!=v for k,v in expected_receipt.items()):raise ValueError('LIVE_RANK1_SEMANTIC_WORKER_BINDING')
  b=sem['binding']
  if any(b.get(k)!=v for k,v in {'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':mh,'run_id':currentbinding['run_id']}.items()):raise ValueError('LIVE_RANK1_SEMANTIC_BINDING')
  intrinsic=sem['roles']['evidence']['essential']['evidence']['intrinsic_eligibility']
 else:
  if t['schema']!='FINITE_PORTALS383_SOURCE_TRACE_V1':raise ValueError('RANK2_SOURCE')
  sem,execution_authority=_rank2_authority(record,fresh)
  intrinsic=sem['evidence']['rank2_intrinsic']
 if 'semantic'in bundle and D(bundle['semantic'])!=D(sem):raise ValueError('SUPPLIED_SEMANTIC_NOT_AUTHORITY_OUTPUT')
 if 'intrinsic'in bundle and D(bundle['intrinsic'])!=D(intrinsic):raise ValueError('SUPPLIED_INTRINSIC_NOT_AUTHORITY_OUTPUT')
 return {'semantic_result_digest':D(sem),'intrinsic_digest':_intrinsic(record,fresh,intrinsic),'model_digest':mh,'record_digest':D(record),'fresh_digest':D(fresh),'same_run':rank==1}

def role_extension_predicates(oldrole,record,fresh,extension):
 """Recheck actual positive join predicates; preserve all historical receipts.
 This is a new proof-level join, not a new role geometry evaluation.
 """
 if extension.get('verdict')!='PASS_SCOPED_EXTENDED_FINITE_Q04_CONJUNCTION':raise ValueError('EXTENSION_NOT_CLOSED')
 n=oldrole['nodes'];mh=D(record['candidate']['model']);fh=D(fresh);rh=D(record)
 walls=n['WALL_PURPOSE']['evidence'];sourcewalls=walls['immutable_constructive_wall_evidence'];private=n['PRIVATE_CIRCULATION']
 if private['status']!='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE'or sourcewalls.get('unjoined_host_ids'):raise ValueError('WALL_INTRINSIC_PREMISE')
 need={}
 for row in sourcewalls['rows']:
  if row['verdict']=='UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY':
   if row['kind']!='EXECUTED_SOURCE_PRIVATE_ACCESS_BOUNDARY':raise ValueError('WALL_PENDING_KIND')
   need[row['wall_id']]=D(row)
  elif not row['verdict'].startswith('PASS_'):raise ValueError('UNRESOLVED_CONSTRUCTIVE_WALL')
 closed=walls['closed_hall_dependency_rows']
 if len(need)!=8 or len(closed)!=8 or {r['wall_id']:r['source_row_digest']for r in closed}!=need:raise ValueError('EXACT_WALL_SOURCE_ROWS')
 if any(r['verdict']!='PASS_SCOPED_SOURCE_PRIVATE_ACCESS_BOUNDARY_WITH_FINITE_NECESSITY'for r in closed):raise ValueError('OLD_HALL_JOIN_STATUS')
 if any(not n[d]['status'].startswith('PASS_')for d in n['Q11_WHOLE_ROLE']['depends_on']):raise ValueError('Q11_ALL_ROLE_DEPENDENCIES')
 privacy=next(r for r in fresh['raw_report']['rule_contract_evidence']['requirements']if r['requirement_id']=='privacy_scenarios')
 if privacy.get('model_hash')!=mh or privacy['status']!='PASS_LIMITED':raise ValueError('PRIVACY_CURRENT_ROW')
 balance=n['Q12_PER_UNIT']['balanced_common_access']
 if any(balance[k]!=v for k,v in [('model_hash',mh),('record_digest',rh),('fresh_result_digest',fh)])or balance['verdict']!='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS'or not all(c['equal_fixed_source_metrics']for c in balance['comparisons']):raise ValueError('EXACT_BALANCE_PREMISE')
 per=n['Q12_PER_UNIT']['evidence'];expected_units={u['id']for u in record['candidate']['model']['units']}
 if len(per)!=len(expected_units)or {u['unit']for u in per}!=expected_units:raise ValueError('PER_UNIT_INVENTORY')
 for unit in per:
  if unit['exact_pending']or not unit['whole_unit_verdict'].startswith('PASS_'):raise ValueError('PER_UNIT_PENDING')
  if set(unit['resolved_dependency_digests'])!={'COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON'}:raise ValueError('PER_UNIT_RESOLVED_INVENTORY')
  if any(v!=D(n[k])for k,v in unit['resolved_dependency_digests'].items()):raise ValueError('PER_UNIT_DEPENDENCY_HASH')
  if unit['balanced_access_digest']!=D(balance):raise ValueError('PER_UNIT_BALANCE_HASH')
 # Execute just the pure unchanged SERVICE reducer over its original exact
 # same-invocation receipts. Nothing is rewritten to a new freshness identity.
 svc=oldrole['service_compactness_evidence'];receipts=svc['invocation_receipts']
 rel='finite_comparison367/service_criterion367_v4.py';path=ROOT/rel
 if _sha(path)!=PINS[rel]:raise ValueError('SERVICE_REDUCER_CHANGED')
 names={'scoped_metric','reduce_bound'};nodes=[x for x in ast.parse(path.read_text()).body if isinstance(x,ast.FunctionDef)and x.name in names]
 if {x.name for x in nodes}!=names:raise ValueError('SERVICE_PURE_DECLARATIONS')
 ns={'F':F,'digest':D};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
 recalculated=ns['reduce_bound'](record,fresh,receipts['cost'],receipts['necessity'],receipts['functional_partition'])
 if any(D(svc[k])!=D(v)for k,v in recalculated.items()):raise ValueError('SERVICE_PURE_PREDICATES_CHANGED')
 if recalculated['remaining']or recalculated['verdict']!='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS':raise ValueError('SERVICE_REQUIRED_PREMISES')
 return {'verdict':'PASS_EXPLICIT_POSITIVE_DEPENDENCY_EXTENSION_PREDICATES','model_digest':mh,
  'source_predicates':{'wall_whole_privacy_q12':'role_registry_final_joint367_v4.py:31-82','service':'service_criterion367_v4.py:17-36','finite_conjunction':'q04_closure367_v3.py:23-24'},
  'exact_eight_hall_rows':need,'private_role_digest':D(private),'whole_role_dependencies':{d:D(n[d])for d in n['Q11_WHOLE_ROLE']['depends_on']},
  'privacy_row_digest':D(privacy),'balance_digest':D(balance),'per_unit_evidence_digest':D(per),'pure_service_reduction_digest':D(recalculated),
  'extension_digest':D(extension),'old_service_receipts_unchanged':True,'service_room_minimum_scope':'FIXED_AGAINST359_ONLY_NOT_NEW_GLOBAL_MINIMUM'}

def compose(currentrecord,currentfresh,currentbinding,currentgroups,equivalence,rank1_bundle,rank2_bundle):
 out={'schema':'JOINT390_EXPLICIT_FINITE_COHORT_CONJUNCTION_DERIVATION','qualified':False,'parent_verdicts':{r:'UNKNOWN'for r in RULES},'q12_verdict':'UNKNOWN','cohort_closed':False,'missing':[],
      'binding':copy.deepcopy(currentbinding),'new_role_geometry_executed':False,'old_same_invocation_receipts_reissued':False,'new_comparison_executed':False,'accepted':False,'delivery_allowed':False,'global_optimum':False}
 before=D([currentrecord,currentfresh,currentbinding,currentgroups,equivalence,rank1_bundle,rank2_bundle])
 try:
  for rel,h in PINS.items():
   if _sha(ROOT/rel)!=h:raise ValueError('COMPOSITION_SOURCE_CHANGED:'+rel)
  refpath=ROOT/'staging368_semantic_bridge/reference_registry.json'
  if _sha(refpath)!='75c492c6622dd5db962ebed34fb81a1723c99b9c4459b244fc4528d6068aef72':raise ValueError('OLD_REFERENCE_POLICY_CHANGED')
  ref=json.loads(refpath.read_text())
  for name,h in ref['sources'].items():
   if _sha(ROOT/name)!=h:raise ValueError('OLD_SOURCE_POLICY_CHANGED:'+name)
  if D(ref['sources'])!=ref['source_contract_cohort_policy_digest']:raise ValueError('OLD_POLICY_SUPERSET_DIGEST')
  spec=ref['members']['joint'];oldrecord=_read(spec['paths']['record']);oldfresh=_read(spec['paths']['fresh']);quality=_read(spec['paths']['qualification'])
  eqmod=_module('staging368_semantic_bridge/equivalence.py','_joint390_eq')
  actualeq=eqmod.compare(oldrecord,oldfresh,currentrecord,currentfresh)
  if actualeq!=equivalence:raise ValueError('SUPPLIED_EQUIVALENCE_MISMATCH')
  mh=D(currentrecord['candidate']['model'])
  for k,v in {'record_digest':D(currentrecord),'fresh_digest':D(currentfresh),'model_digest':mh,'kind':'joint'}.items():
   if currentbinding.get(k)!=v:raise ValueError('CURRENT_RUN_BINDING:'+k)
  rid=currentbinding['run_id']
  if str(uuid.UUID(rid))!=rid or currentbinding['candidate_id']!=D({'run_id':rid,'kind':'joint','model_digest':mh}):raise ValueError('CURRENT_CANDIDATE_IDENTITY')
  if D(quality)!=spec['reference_qualification_digest']:raise ValueError('OLD_QUALITY_DIGEST')
  # This validates old proofs at their ORIGINAL cohort scope only.
  transported=eqmod.attest_proofs(quality['quality'],spec['proof_maps'],actualeq,currentgroups,currentbinding,ref['source_contract_cohort_policy_digest'])
  gate=_module('semantic_rules357/final_role_artifact_gate367.py','_joint390_old_role_gate');oldrole=gate.evaluate(oldrecord,oldfresh)
  oldrole_base_digest=D(_read('final_role367_v4_supervised/actual.json'))
  old_q04=oldrole['service_compactness_evidence']['invocation_receipts']['necessity']
  hall=oldrole['nodes']['WALL_PURPOSE']['evidence']['closed_hall_dependency_rows']
  if len(hall)!=8 or len({r['wall_id']for r in hall})!=8 or any(r['verdict']!='PASS_SCOPED_SOURCE_PRIVATE_ACCESS_BOUNDARY_WITH_FINITE_NECESSITY'for r in hall):raise ValueError('OLD_EXACT8_WALL_JOIN')
  balance=oldrole['nodes']['Q12_PER_UNIT']['balanced_common_access']
  if balance['verdict']!='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS'or not all(c['equal_fixed_source_metrics']for c in balance['comparisons']):raise ValueError('OLD_EXACT_BALANCE')
  compare=_comparison();rows=[];m=currentrecord['candidate']['model']
  for rank,bundle in [(1,rank1_bundle),(2,rank2_bundle)]:
   authority=_authority(bundle,rank,currentbinding);alt=bundle['record']['candidate'];am=alt['model']
   if alt['request']!=currentrecord['candidate']['request']or any(am[k]!=m[k]for k in ('inputs','program','profile')):raise ValueError('ADDED_MEMBER_COMPARABILITY')
   rows.append({'id':'finite_rank'+str(rank),'eligible':True,'authority':authority,'comparison':compare(m,am)})
  out['new_comparison_executed']=True;out['added_members']=rows
  if not extension_condition(old_q04,rows):raise ValueError('ADDED_MEMBER_DOMINANCE_NOT_REFUTED')
  # No existing historical member, source366 conditional fact or failed attempt
  # is removed. Scope is only old declared finite domain UNION two finite ranks.
  old_ids=[r['id']for r in old_q04['cohort']['members']]
  rank2_sem,rank2_execution=_rank2_authority(rank2_bundle['record'],rank2_bundle['fresh'])
  rank0=rank0_mapping_check(rank2_sem['evidence']['cohort']['rank0_source_coverage'],old_q04['cohort']['members'],_read('staging365_balanced_portals/actual365.json'))
  extension={'rank0_mapping':rank0,'rank0_immutable384_result_digest':D(rank2_sem),'rank2_execution_authority':rank2_execution,'old_q04_digest':D(old_q04),'old_domain_digest':D(old_q04['domain']),'retained_old_member_ids':old_ids,'added_member_ids':[r['id']for r in rows],
    'additional_comparison_digests':{r['id']:D(r)for r in rows},'predicate':'OLD_Q04_PASS_AND_FOR_EACH_ADDED_ELIGIBLE_MEMBER_EXACT_COMPARE_DOMINANCE_FALSE',
    'source_predicate':'finite_comparison367/q04_closure367_v3.py:23-24','continuous_domain_exhaustiveness':False,'verdict':'PASS_SCOPED_EXTENDED_FINITE_Q04_CONJUNCTION'}
  # Historical gate has independently verified full old seals, exact8hall rows,
  # complete unit/parent inventories and immutable same-invocation receipts.
  # New certificates refer to those facts without rewriting their old digests.
  join_predicates=role_extension_predicates(oldrole,oldrecord,oldfresh,extension)
  certificate={}
  for rule in RULES:
   old=next(p for p in transported if p['rule_id']==rule)
   deps={'original_proof_digest':D(old),'exact_current_equivalence_digest':D(actualeq),'current_nine_digest':D(currentgroups),'cohort_extension_digest':D(extension),'immutable_old_role_digest':oldrole_base_digest,'positive_join_predicates_digest':D(join_predicates)}
   certificate[rule]={'verdict':'PASS_SCOPED_CURRENT_WITH_EXPLICIT_FINITE_EXTENSION','dependencies':deps,'dependency_seal':D(deps),'new_derivation':True,'historical_predicates_recomputed':False}
  per=oldrole['internal_per_unit_review']
  if per.get('missing')!=[]or not per.get('verdict','').startswith('PASS_')or any(u.get('exact_pending')for u in per['units']):raise ValueError('OLD_Q12_NOT_CLOSED')
  out.update(qualified=True,parent_verdicts={r:'PASS'for r in RULES},q12_verdict='PASS',q12_scoped_status='PASS_SCOPED_EXPLICIT_FINITE_EXTENSION',cohort_closed=True,certificates=certificate,cohort_extension=extension,
    positive_join_predicates=join_predicates,premises={'old_artifact_digest':oldrole_base_digest,'validated_artifact_gate_result_digest':D(oldrole),'old_service_receipts_digest':D(oldrole['service_compactness_evidence']),'old_q12_digest':D(per),'old_source_contract_cohort_policy_digest':ref['source_contract_cohort_policy_digest'],'old_proof_transports':transported,'current_equivalence':actualeq},
    scope='NEW_CONJUNCTION_DERIVATION_ON_EXACT_UNCHANGED_JOINT_MODEL_WITH_CURRENT9; OLD_ROLE_GEOMETRY_AND_AGAINST359_SERVICE_ROOM_COMPARISON_REUSED_EXPLICITLY; NOT_OLD_SAME_INVOCATION_REISSUE; Q14_SEPARATE')
 except Exception as error:out['missing'].append(type(error).__name__+':'+str(error))
 if before!=D([currentrecord,currentfresh,currentbinding,currentgroups,equivalence,rank1_bundle,rank2_bundle]):raise ValueError('COMPOSITION_INPUT_MUTATION')
 out['qualification']={k:copy.deepcopy(out[k])for k in ('qualified','parent_verdicts','q12_verdict','cohort_closed','missing')}
 out['qualification']['parent_verdicts11']=copy.deepcopy(out['parent_verdicts'])
 if 'q12_scoped_status'in out:out['qualification']['q12_scoped_status']=out['q12_scoped_status']
 return out

def load_rank2_bundle():
 """Only immutable384 registered inputs/output; no caller-selected paths."""
 inputs=_frozen_read(ROOT/'staging384_rank2_semantics/inputs.json');out={}
 for key in ('record','fresh'):
  p=W/inputs[key]['path'];data=_frozen_bytes(p)
  if hashlib.sha256(data).hexdigest()!=inputs[key]['sha256']:raise ValueError('RANK2_INPUT_SOURCE_PIN:'+key)
  out[key]=json.loads(data)
 sem,authority=_rank2_authority(out['record'],out['fresh'])
 out.update(semantic=sem,intrinsic=sem['evidence']['rank2_intrinsic'],execution_authority=authority)
 return out
