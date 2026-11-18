"""Same-run internal semantic authority, never a client-supplied proof gate.
Configure once from a supervised balanced member folder; immutable snapshot plus
own current request/record/fresh/binding file hashes replace historical pins.
"""
import copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
D=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
_STATE=None

def _contract():
 sys.path.insert(0,str(ROOT/'staging390_form'))
 import contract390
 if Path(contract390.__file__).resolve()!=ROOT/'staging390_form/contract390.py':raise ValueError('CURRENT_CONTRACT_ORIGIN')
 return contract390

def configure(folder,expected_freeze):
 global _STATE
 from frozen390 import configure as freeze_configure
 freeze_configure(expected_freeze)
 if _STATE is not None:raise ValueError('SEMANTIC_CONTEXT_ALREADY_CONFIGURED')
 folder=Path(folder).resolve()
 if not folder.is_relative_to(W)or folder.name!='balanced':raise ValueError('INTERNAL_BALANCED_FOLDER_REQUIRED')
 # Includes whole source freeze, exact current source/member identity, and clean
 # construction/fresh/bind subprocess receipts. No caller artifact flags suffice.
 loaded=_contract().validate_member_folder(folder,expected_freeze,require_physical_pass=True)
 paths={'record':folder/'record.json','fresh':folder/'fresh.json','binding':folder/'binding.json','request':folder.parent/'request.json'}
 for k,p in paths.items():
  if D(json.loads(p.read_text()))!=D(loaded[k]):raise ValueError('TRANSPORT_FILE_SNAPSHOT:'+k)
 _STATE={'folder':folder,'expected_freeze':expected_freeze,'snapshot':copy.deepcopy(loaded),'paths':paths,'hashes':{k:hashlib.sha256(p.read_bytes()).hexdigest()for k,p in paths.items()}}
 return validate(loaded['record'],loaded['fresh'])

def _load_all():
 if _STATE is None:raise ValueError('INTERNAL_SAME_RUN_CONTEXT_REQUIRED')
 for k,p in _STATE['paths'].items():
  if hashlib.sha256(p.read_bytes()).hexdigest()!=_STATE['hashes'][k]:raise ValueError('CURRENT_MEMBER_FILE_CHANGED:'+k)
 return copy.deepcopy(_STATE['snapshot'])

def load_inputs():
 all=_load_all();return {k:all[k]for k in ('record','fresh')}

def validate(record,fresh):
 pinned=_load_all()
 if D(record)!=D(pinned['record'])or D(fresh)!=D(pinned['fresh']):raise ValueError('NOT_CURRENT_SUPERVISED_MEMBER')
 c=record['candidate'];t=record['trace'];p=fresh['provenance'];m=c['model'];mh=D(m);raw=fresh['raw_report'];reg=fresh['expected_method_registry']
 b=pinned['binding'];request=pinned['request']
 checked=_contract().validate_member(request,record,fresh,b,b['run_id'],kind='balanced')
 if checked!=b:raise ValueError('LIVE_MEMBER_BINDING_CHANGED')
 if raw['errors']or raw['pending']or raw['status']!='PASS_CONCEPT_SCOPED_REVIEW'or raw['model_hash']!=mh:raise ValueError('CURRENT_PHYSICAL_NOT_PASS')
 if record['test_only']is not False or fresh['test_only']is not False or t['schema']!='FINITE_PORTALS378_SOURCE_TRACE_V1':raise ValueError('BALANCED_SOURCE_FAMILY')
 old=json.loads((ROOT/'semantic_rules357/method_registry_source365.json').read_text())
 if reg['methods']!=old['methods']or reg['applicability']!=old['applicability']:raise ValueError('UNCHANGED_METHOD_KERNEL_REQUIRED')
 for n,h in reg['sources'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('CURRENT_SOURCE_CHANGED:'+n)
 return {'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':mh,'review_id':fresh['review_id'],'candidate_id':record['candidate_id'],'run_id':t['run_id'],
         'current_source_inventory_digest':D(reg['sources']),'request_envelope_digest':D(request),'form_binding_digest':D(b),'test_only':False,'authority':'SAME_RUN_SUPERVISED390_MEMBER'}

def views(record,fresh):
 b=validate(record,fresh);c=record['candidate'];t=record['trace']
 env={'schema':'CURRENT390_SEMANTIC_VIEW','candidate_id':D(c),'raw':copy.deepcopy(c['request']),'packet':copy.deepcopy(c['packet']),'input_record_digest':D(record),'outer_trace_digest':D(t),'original_result_digest':D(fresh),'artifact_reassessment_only':False,'new_fresh_execution':False,'same_pipeline_run':True}
 res={'schema':'CURRENT390_SEMANTIC_RESULT','candidate_digest':D(env),'raw_fresh_report':copy.deepcopy(fresh['raw_report']),'original_result_digest':D(fresh),'input_record_digest':D(record),'outer_trace_digest':D(t),'artifact_reassessment_only':False,'new_fresh_execution':False,'same_pipeline_run':True}
 return env,res,b

def validate_views(env,res):
 i=load_inputs();a,b,_=views(i['record'],i['fresh'])
 if D(env)!=D(a)or D(res)!=D(b):raise ValueError('CURRENT_VIEW_CHANGED')

def verify_end():
 i=_load_all()
 loaded=_contract().validate_member_folder(_STATE['folder'],_STATE['expected_freeze'],require_physical_pass=True)
 if any(D(loaded[k])!=D(i[k])for k in('record','fresh','binding','request')):raise ValueError('POST_SEMANTIC_AUTHORITY_CHANGED')
 return validate(i['record'],i['fresh'])
