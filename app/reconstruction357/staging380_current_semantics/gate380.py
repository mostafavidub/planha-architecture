"""Pinned actual378 artifact authority; no new fresh execution or borrowed PASS."""
import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
D=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def load_inputs():
 out={}
 for k,s in json.loads((HERE/'inputs.json').read_text()).items():
  b=(W/s['path']).read_bytes()
  if hashlib.sha256(b).hexdigest()!=s['sha256']:raise ValueError('ACTUAL378_PIN:'+k)
  out[k]=json.loads(b)
 return out

def validate(record,fresh):
 pinned=load_inputs()
 if D(record)!=D(pinned['record'])or D(fresh)!=D(pinned['fresh']):raise ValueError('UNREGISTERED_CURRENT_ARTIFACT')
 c=record['candidate'];t=record['trace'];p=fresh['provenance'];m=c['model'];mh=D(m);raw=fresh['raw_report'];reg=fresh['expected_method_registry']
 fields={'input_record_digest':D(record),'outer_trace_digest':D(t),'candidate_digest':D(c),'packet_digest':D(c['packet']),'model_hash':mh,'candidate_id':record['candidate_id'],'run_id':t['run_id'],'raw':c['request']}
 if p.get('verified')is not True or any(p.get(k)!=v for k,v in fields.items()):raise ValueError('PROVENANCE_BINDING')
 if fresh['input_record_digest']!=D(record)or fresh['outer_trace_digest']!=D(t)or fresh['model_digest']!=mh or c['model_digest']!=mh or D(c['packet']['world_model'])!=mh:raise ValueError('CURRENT_MODEL_BINDING')
 if not fresh['fresh_checker_executed']or not fresh['source_unchanged']or not reg['built_before_evaluate']:raise ValueError('FRESH_NOT_EXECUTED')
 if raw['errors']or raw['pending']or raw['status']!='PASS_CONCEPT_SCOPED_REVIEW'or raw['model_hash']!=mh:raise ValueError('CURRENT_PHYSICAL_NOT_PASS')
 if record['test_only']is not False or fresh['test_only']is not False or t['schema']!='FINITE_PORTALS378_SOURCE_TRACE_V1':raise ValueError('SOURCE_FAMILY')
 old=json.loads((ROOT/'semantic_rules357/method_registry_source365.json').read_text())
 if reg['methods']!=old['methods']or reg['applicability']!=old['applicability']:raise ValueError('UNCHANGED_METHOD_KERNEL_REQUIRED')
 for n,h in reg['sources'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('CURRENT_SOURCE_CHANGED:'+n)
 return {'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':mh,'review_id':fresh['review_id'],'candidate_id':record['candidate_id'],'run_id':t['run_id'],'current_source_inventory_digest':D(reg['sources']),'test_only':False}

def views(record,fresh):
 b=validate(record,fresh);c=record['candidate'];t=record['trace']
 env={'schema':'CURRENT378_SEMANTIC380_VIEW','candidate_id':D(c),'raw':copy.deepcopy(c['request']),'packet':copy.deepcopy(c['packet']),'input_record_digest':D(record),'outer_trace_digest':D(t),'original_result_digest':D(fresh),'artifact_reassessment_only':True,'new_fresh_execution':False}
 res={'schema':'CURRENT378_SEMANTIC380_RESULT','candidate_digest':D(env),'raw_fresh_report':copy.deepcopy(fresh['raw_report']),'original_result_digest':D(fresh),'input_record_digest':D(record),'outer_trace_digest':D(t),'artifact_reassessment_only':True,'new_fresh_execution':False}
 return env,res,b

def validate_views(env,res):
 i=load_inputs();a,b,_=views(i['record'],i['fresh'])
 if D(env)!=D(a)or D(res)!=D(b):raise ValueError('CURRENT_VIEW_CHANGED')
