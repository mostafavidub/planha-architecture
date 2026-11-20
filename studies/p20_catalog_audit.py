"""P20 inventory validator only. Never evaluates or qualifies a model."""
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json'
EXPECTED={
 'CURRENT_PROGRAM_SUITABILITY':{'P20_PROGRAM_IDENTITY','P20_PROGRAM_CAPACITY','P20_PROGRAM_ALTERNATIVES','P20_PROGRAM_QUALITY_FLOOR','P20_PROGRAM_PREFILTER','P20_PROGRAM_BUNDLE_USE','P20_PROGRAM_SERVICE_MINIMA'},
 'KITCHEN_GUEST_PATH_SEPARATION':{'P20_GUEST_FOUR_ROUTES','P20_GUEST_WORK_EXCLUSION','P20_GUEST_FIRST_LIVING','P20_GUEST_PRIVATE_ACCESS','P20_GUEST_KITCHEN_LABEL'},
 'CONTINUOUS_USEFUL_LIVING':{'P20_LIVING_SOURCE_SEATS','P20_LIVING_FLOOR_CONTINUITY','P20_LIVING_USEFUL_AREA','P20_LIVING_SHORTER_ALTERNATIVE','P20_LIVING_GROUP_USE'},
 'NONFUNCTIONAL_WALL_EXCLUSION':{'P20_WALL_SOURCE_INVENTORY','P20_WALL_VIEW_ONLY','P20_WALL_ALIAS_MATERIAL','P20_WALL_ALTERNATIVE','P20_WALL_PRIVACY_TARGETS','P20_CORE_ENGINEERING'}}
KINDS={'KNOWN_NECESSARY','COMPARATIVE_DUTY','CALIBRATION_OPEN','IMPLEMENTATION_OPEN','PROFILE_AND_EVIDENCE_OPEN','SCOPE_DISTINCTION','OUT_OF_SCOPE'}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
OPEN={'P20_OPEN_QUALITY_ANCHORS','P20_OPEN_EFFECTIVE_ACTIVITY_PROFILES','P20_OPEN_PROGRAMME_SELECTION','P20_OPEN_PRINCIPAL_GUEST_ORGANISATION','P20_OPEN_USEFUL_LIVING','P20_OPEN_PER_WALL_FUNCTION'}
RESULTS={'PASS_SCOPED','FAIL_SCOPED','INDETERMINATE','CONFLICT','NOT_EVALUATED','EVALUATION_ERROR','NOT_APPLICABLE','MEASURED_ONLY'}
def require(ok,code):
 if not ok:raise ValueError(code)
def gitblob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def validate(data,root=ROOT):
 require(type(data) is dict and data.get('schema')=='V25_CURRENT_FUNCTIONAL_CRITERIA_CATALOG_V2','CATALOG_SCHEMA')
 require(type(data.get('version')) is int and data['version']==2,'CATALOG_VERSION')
 require(all(data.get(k) is False for k in AUTH),'CATALOG_AUTHORITY')
 require(data.get('numeric_thresholds_added')==[],'UNAUTHORIZED_THRESHOLD')
 require(all(data.get('aggregate_policy',{}).get(k) is True for k in ('runtime_condition_result_is_not_aggregate_criterion','out_of_scope_is_not_pass','no_witness_is_not_global_infeasibility','known_violation_does_not_erase_unknown','classification_only_no_new_evaluator')),'AGGREGATE_POLICY')
 rows=data.get('criteria');require(type(rows) is list and len(rows)==4 and {r.get('id') for r in rows}==set(EXPECTED),'CRITERION_SET')
 aliases=data.get('source_aliases');require(type(aliases) is dict and bool(aliases),'SOURCE_ALIAS_SET')
 opens=data.get('open_decisions');require(type(opens) is list and len(opens)==6 and {r.get('id') for r in opens}==OPEN,'OPEN_DECISION_SET')
 for item in opens:
  require(item.get('implemented_by_this_task') is False and type(item.get('decision_needed')) is str and bool(item['decision_needed']),'OPEN_DECISION_CLAIM')
  require(type(item.get('criteria')) is list and bool(item['criteria']) and set(item['criteria'])<=set(EXPECTED),'OPEN_DECISION_CRITERIA')
 require(type(data.get('condition_result_vocabulary')) is dict and set(data['condition_result_vocabulary'])==RESULTS,'CONDITION_RESULT_VOCABULARY')
 seen=set();source_files={}
 for row in rows:
  require(row.get('current_state')=='UNKNOWN','CATALOG_IS_NOT_ASSESSMENT')
  refs=row.get('sources');require(type(refs) is list and bool(refs),'SOURCE_REQUIRED')
  allowed=set()
  for source in refs:
   require(set(source)=={'alias','label','locator_scope','source_kind'},'PUBLIC_SOURCE_FIELDS')
   require(source['alias'] in aliases and aliases[source['alias']]==source['label'] and source['source_kind']=='OWNER_REQUIREMENT','SOURCE_BINDING')
   allowed.add(source['alias'])
  conditions=row.get('conditions');require(type(conditions) is list and len(conditions)==len(EXPECTED[row['id']]) and {z.get('id') for z in conditions}==EXPECTED[row['id']],'CONDITION_SET')
  for condition in conditions:
   require(condition['id'] not in seen,'DUPLICATE_CONDITION');seen.add(condition['id'])
   require(condition.get('kind') in KINDS,'CONDITION_KIND')
   require(type(condition.get('source_refs')) is list and bool(condition['source_refs']) and set(condition['source_refs'])<=allowed,'UNSOURCED_CONDITION')
   require(condition.get('numeric_thresholds_added')==[],'UNAUTHORIZED_THRESHOLD')
   for key in ('requirement','required_witness','current_implementation','runtime_condition_result','implementation_gap','profile_or_calibration_gap','aggregate_effect'):
    require(type(condition.get(key)) is str and bool(condition[key].strip()),'CONDITION_FIELD:'+key)
   require(condition['aggregate_effect']=='No condition result grants aggregate PASS. Preserve known violations, missing evidence and out-of-scope separately.','CONDITION_PROMOTION')
  bindings=row.get('implementation_bindings')
  require(type(bindings) is list and len(bindings)==2,'IMPLEMENTATION_SET')
  require({b.get('family') for b in bindings}=={'FRONT_REAR_N2_SOURCE_P2','SINGLE_N1_P15_FIXED_18X20_P2'},'FAMILY_SET')
  for b in bindings:
   require(b.get('whole_criterion_pass_implemented') is False,'UNIMPLEMENTED_PASS')
   path=b.get('path');require(type(path) is str and path.startswith('app/local_integration/') and '..' not in path.split('/'),'IMPLEMENTATION_PATH')
   p=root/path;require(p.resolve().is_relative_to(root.resolve()),'IMPLEMENTATION_ESCAPE')
   raw=p.read_bytes();require(gitblob(raw)==b.get('git_blob'),'IMPLEMENTATION_CHANGED')
   names={n.name for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
   require(b.get('entry')=='assess' and b['entry'] in names,'ENTRYPOINT')
   source_files[path]=b['git_blob']
  require(bool(row.get('legacy_checker')),'HISTORICAL_MAPPING_REQUIRED')
 text=json.dumps(data,ensure_ascii=False)
 require('docs.google.com' not in text and 'document_id' not in text and 'revision_id' not in text,'PRIVATE_LOCATOR')
 return {'conditions':len(seen),'criteria':len(rows),'bound_evaluator_files':len(source_files),'geometry_executed':False,'qualified':False}
if __name__=='__main__':
 print(json.dumps(validate(json.loads(CATALOG.read_text())),sort_keys=True))
