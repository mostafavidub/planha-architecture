"""Explicit pinned372 stored-fresh authority; never a fabricated new fresh run."""
import hashlib,json,copy
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
D=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def load_inputs():
 spec=json.loads((HERE/'inputs.json').read_text());out={}
 for k,s in spec['inputs'].items():
  p=W/s['path'];b=p.read_bytes()
  if hashlib.sha256(b).hexdigest()!=s['sha256']:raise ValueError('PINNED372_BYTES_CHANGED:'+k)
  out[k]=json.loads(b)
 return out

def validate(record,fresh,lineage):
 pinned=load_inputs()
 if any(D(v)!=D(pinned[k])for k,v in [('record',record),('fresh',fresh),('lineage',lineage)]):raise ValueError('UNREGISTERED_CURRENT_ARTIFACT')
 if not pinned['audit']['all_checks_passed']or not pinned['comparison']['mechanics_success']:raise ValueError('CURRENT_REPAIR_NOT_VERIFIED')
 c=record['candidate'];m=c['model'];t=record['trace'];p=fresh['provenance'];raw=fresh['raw_report'];mh=D(m)
 if (fresh['input_record_digest']!=D(record)or fresh['outer_trace_digest']!=D(t)or fresh['model_digest']!=mh
  or p['model_hash']!=mh or p['input_record_digest']!=D(record)or p['candidate_digest']!=D(c)
  or p['packet_digest']!=D(c['packet'])or p['outer_trace_digest']!=D(t)or not p['verified']):raise ValueError('PROVENANCE_BINDING')
 if (lineage['record_digest']!=D(record)or lineage['model_digest']!=mh or lineage['review_id']!=fresh['review_id']or lineage['fresh_digest']!=D(fresh)):raise ValueError('LINEAGE_BINDING')
 if not fresh['fresh_checker_executed']or not fresh['source_unchanged']or not fresh['expected_method_registry']['built_before_evaluate']:raise ValueError('FRESH_NOT_EXECUTED')
 if raw['errors']or raw['pending']or raw['model_hash']!=mh or raw['status']!='PASS_CONCEPT_SCOPED_REVIEW':raise ValueError('CURRENT_SCOPED_REVIEW_NOT_PASS')
 reg=fresh['expected_method_registry'];old=json.loads((ROOT/'semantic_rules357/method_registry_source365.json').read_text())
 if reg['methods']!=old['methods']or reg['applicability']!=old['applicability']:raise ValueError('UNCHANGED_KERNEL_METHODS_REQUIRED')
 verify_sources(reg)
 if not(record['test_only']and fresh['test_only']and lineage['test_only']):raise ValueError('TEST_SCOPE')
 return {'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':mh,'review_id':fresh['review_id'],'candidate_id':lineage['candidate_id'],'test_only':True}

def views(record,fresh,lineage):
 binding=validate(record,fresh,lineage);c=record['candidate']
 env={'schema':'REGISTERED_DERIVED372_SEMANTIC373_VIEW','candidate_id':D(c),'raw':copy.deepcopy(c['request']),'packet':copy.deepcopy(c['packet']),'input_record_digest':D(record),'outer_trace_digest':D(record['trace']),'original_result_digest':D(fresh),'artifact_reassessment_only':True,'new_fresh_execution':False}
 res={'schema':'REGISTERED_DERIVED372_SEMANTIC373_RESULT','candidate_digest':D(env),'raw_fresh_report':copy.deepcopy(fresh['raw_report']),'original_result_digest':D(fresh),'input_record_digest':D(record),'outer_trace_digest':D(record['trace']),'artifact_reassessment_only':True,'new_fresh_execution':False}
 return env,res,binding

def validate_views(env,res):
 i=load_inputs();a,b,_=views(i['record'],i['fresh'],i['lineage'])
 if D(a)!=D(env)or D(b)!=D(res):raise ValueError('CURRENT_VIEW_CHANGED')

def verify_sources(reg):
 for root,key in ((ROOT,'baseline368'),(W,'derived369')):
  for n,h in reg['sources'][key].items():
   if hashlib.sha256((root/n).read_bytes()).hexdigest()!=h:raise ValueError('CURRENT_REGISTRY_SOURCE_CHANGED:'+n)
