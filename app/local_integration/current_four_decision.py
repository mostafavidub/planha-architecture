"""Task3.6 same-model evidence decision. Four criteria are not the complete PRD."""
import copy,hashlib
from front_rear_runtime_adapter import ROOT,ensure,transport
from same_version_front_rear_contract import digest,ENGINE_REVISION
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
SCHEMAS={
 'CURRENT_PROGRAM_SUITABILITY':'CURRENT_PROGRAMME_SOURCE_EVALUATION_V1',
 'KITCHEN_GUEST_PATH_SEPARATION':'SOURCE_BOUND_FOUR_GUEST_ROUTES_V1',
 'CONTINUOUS_USEFUL_LIVING':'CURRENT_LIVING_SOURCE_EVIDENCE_V1',
 'NONFUNCTIONAL_WALL_EXCLUSION':'SOURCE_WALL_FUNCTION_EVIDENCE_V1'}
REQUIRED_SOURCES={
 'CURRENT_PROGRAM_SUITABILITY':{'app/local_integration/current_programme_evaluator.py','app/local_integration/program_profile_registry.py','specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json'},
 'KITCHEN_GUEST_PATH_SEPARATION':{'app/local_integration/source_guest_route_evaluator.py','app/local_integration/current_programme_evaluator.py','app/local_integration/kitchen_guest_review.py','app/local_integration/guest_four_route_diagnostic.py'},
 'CONTINUOUS_USEFUL_LIVING':{'app/local_integration/source_living_evaluator.py','app/local_integration/source_guest_route_evaluator.py','app/local_integration/living_connectivity_diagnostic.py','app/local_integration/fixed_route_clearance_diagnostic.py','app/local_integration/kitchen_guest_review.py'},
 'NONFUNCTIONAL_WALL_EXCLUSION':{'app/local_integration/source_wall_function_evaluator.py','app/local_integration/source_wall_counterfactual.py','app/local_integration/current_programme_evaluator.py'}}
def error_markers(value):
 found=[]
 def walk(v,path):
  if type(v) is dict:
   if v.get('state') in ('EVALUATOR_ERROR','UNKNOWN_EVALUATOR_OR_BINDING_ERROR'):found.append({'path':path,'reason':v['state']})
   if v.get('kind') in ('EVALUATOR_OR_SOURCE_BINDING_ERROR','INTEGRITY_ERROR'):found.append({'path':path,'reason':v['kind']})
   for k,x in v.items():
    if k not in ('original_physical_report','historical_physical_report','reports','replay'):walk(x,path+[k])
  elif type(v) is list:
   for i,x in enumerate(v):walk(x,path+[i])
 walk(value,[])
 if value.get('missing'):found.append({'path':['missing'],'reason':'MISSING_EVALUATOR_RESULT','details':value['missing']})
 if value.get('integrity_verified') is not True:found.append({'path':['integrity_verified'],'reason':'INTEGRITY_ERROR'})
 return found
def decide(physical,states):
 ensure(set(states)==set(SCHEMAS),'CRITERION_SET')
 ensure(all(s in ('PASS','FAIL','UNKNOWN','NOT_EVALUATED','EVALUATOR_ERROR') for s in states.values()),'CRITERION_STATE')
 blockers=[]
 if physical.get('errors') or physical.get('status')=='FAIL':blockers.append('PHYSICAL_FAIL')
 if any(s=='FAIL' for s in states.values()):blockers.append('CURRENT_NECESSARY_FAIL')
 if any(s=='EVALUATOR_ERROR' for s in states.values()):blockers.append('EVALUATOR_ERROR')
 if any(s=='UNKNOWN' for s in states.values()):blockers.append('CURRENT_UNKNOWN')
 if any(s=='NOT_EVALUATED' for s in states.values()):blockers.append('CURRENT_NOT_EVALUATED')
 if physical.get('pending'):blockers.append('PHYSICAL_PENDING')
 if physical.get('status')!='PASS_CONCEPT_SCOPED_REVIEW' and 'PHYSICAL_FAIL' not in blockers:blockers.append('PHYSICAL_NOT_VERIFIED')
 if physical.get('original_pending') or physical.get('not_evaluated'):blockers.append('HISTORICAL_UNRESOLVED_RETAINED')
 return {'state':'BLOCKED' if blockers else 'FOUR_CURRENT_CHECKS_COMPLETE_NOT_PRODUCT_QUALIFIED',
  'blockers':blockers,'current_four_conditions_complete':all(s=='PASS' for s in states.values()),
  'all_PRD_requirements_verified':False,**{k:False for k in AUTH}}
def assemble(bundle,assessments,expected_digests):
 bundle,_=transport(bundle);assessments,_=transport(assessments);expected_digests,_=transport(expected_digests)
 pin=digest([bundle,assessments,expected_digests]);mh=digest(bundle['packet']['world_model'])
 ensure(mh==bundle['model_digest'],'MODEL_DIGEST')
 physical=bundle['reports']['physical'];ph=digest(physical)
 ensure(physical['model_hash']==mh and ph==bundle['report_digests']['physical'],'PHYSICAL_BINDING')
 for k,r in bundle['reports'].items():ensure(digest(r)==bundle['report_digests'][k],'ORIGINAL_REPORT_BINDING')
 ensure(set(assessments)==set(SCHEMAS) and set(expected_digests)==set(SCHEMAS),'EXACT_FOUR_CRITERIA')
 reference_replay=bundle['reports']['replay']
 ensure(reference_replay['verified'] is True and reference_replay['source_revision']==ENGINE_REVISION and reference_replay['model_hash']==mh,'ORIGINAL_REPLAY_BINDING')
 rows=[];states={};sourcepins={}
 for cid,r in assessments.items():
  ensure(digest(r)==expected_digests[cid],'ASSESSMENT_DIGEST:'+cid)
  ensure(r['schema']==SCHEMAS[cid] and r['model_digest']==mh,'ASSESSMENT_MODEL_SCHEMA:'+cid)
  # Programme V1 lacks a criterion field; its unique versioned schema maps explicitly to this ID.
  ensure(r.get('criterion',cid if cid=='CURRENT_PROGRAM_SUITABILITY' else None)==cid,'ASSESSMENT_CRITERION')
  ensure(all(r.get(k) is False for k in AUTH),'ASSESSMENT_AUTHORITY')
  replay=r['reports']['replay'] if cid=='CURRENT_PROGRAM_SUITABILITY' else r['replay']
  ensure(digest(replay)==digest(reference_replay),'ASSESSMENT_REPLAY:'+cid)
  report=r['historical_physical_report'] if cid=='CURRENT_PROGRAM_SUITABILITY' else r['original_physical_report']
  declared=r['historical_physical_digest'] if cid=='CURRENT_PROGRAM_SUITABILITY' else r['original_physical_digest']
  ensure(declared==ph and digest(report)==ph,'ASSESSMENT_PHYSICAL:'+cid)
  snap=r['source_snapshot'];ensure(type(snap) is dict and set(snap)==REQUIRED_SOURCES[cid],'SOURCE_SNAPSHOT_REQUIRED_SET')
  for path,h in snap.items():
   ensure(type(path) is str and (path.startswith('app/local_integration/') or path.startswith('specs/')) and '..' not in path.split('/'),'SOURCE_PATH')
   actual=ROOT/path
   ensure(actual.resolve().is_relative_to(ROOT.resolve()),'SOURCE_PATH_ESCAPE')
   ensure(hashlib.sha256(actual.read_bytes()).hexdigest()==h,'SOURCE_SNAPSHOT_CHANGED:'+path)
   ensure(path not in sourcepins or sourcepins[path]==h,'SOURCE_CONFLICT');sourcepins[path]=h
  state=r['state'];ensure(state in ('PASS','FAIL','UNKNOWN','NOT_EVALUATED'),'RAW_CRITERION_STATE')
  errors=error_markers(r);effective='FAIL' if state=='FAIL' else 'EVALUATOR_ERROR' if errors else state;states[cid]=effective
  rows.append({'criterion':cid,'reported_state':state,'effective_state':effective,'evaluator_errors':errors,'assessment_digest':digest(r)})
 out={'schema':'SAME_MODEL_CURRENT_FOUR_DECISION_V1','model_digest':mh,'physical_digest':ph,'engine_revision':ENGINE_REVISION,
  'original_reports':copy.deepcopy(bundle['reports']),'original_report_digests':copy.deepcopy(bundle['report_digests']),
  'assessments':copy.deepcopy(assessments),'assessment_digests':copy.deepcopy(expected_digests),'criteria':rows,
  'decision':decide(physical,states),'source_snapshot':sourcepins,
  'scope':'Decision over four actual same-model current evidence reports plus retained original physical report. No error/pending suppression; no replacement of frozen gates; no claim of whole PRD or public delivery qualification.',
  **{k:False for k in AUTH}}
 if any(r['evaluator_errors'] for r in rows) and 'EVALUATOR_ERROR' not in out['decision']['blockers']:out['decision']['blockers'].append('EVALUATOR_ERROR')
 ensure(digest([bundle,assessments,expected_digests])==pin,'INPUT_MUTATION')
 for path,h in sourcepins.items():ensure(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,'SOURCE_CHANGED_DURING_DECISION')
 out['integrity_verified']=True
 return out
