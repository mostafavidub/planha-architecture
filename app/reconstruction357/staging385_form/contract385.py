"""Two closed source builders; only trusted same-run files supply proof material."""
import sys,uuid,hashlib,copy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from request_contract368 import parse_json,verify,digest
KINDS=('balanced','joint')
def bind_member(envelope,record,fresh,run_id,kind,review_id):
 verify(envelope)
 if kind not in KINDS or str(uuid.UUID(run_id))!=run_id or str(uuid.UUID(review_id))!=review_id:raise ValueError('KIND_OR_RUN_REVIEW_UUID')
 c=record['candidate'];t=record['trace'];m=c['model'];mh=digest(m);p=fresh['provenance']
 if c['request']!=envelope['normalized_raw']or c['request_digest']!=envelope['raw_digest']or digest(c['request'])!=envelope['raw_digest']:raise ValueError('COMMON_REQUEST')
 if c['model_digest']!=mh or t['model_digest']!=mh or t['candidate_digest']!=digest(c)or digest(c['packet']['world_model'])!=mh:raise ValueError('SOURCE_MODEL_BINDING')
 for k,v in {'input_record_digest':digest(record),'outer_trace_digest':digest(t),'model_digest':mh}.items():
  if fresh.get(k)!=v:raise ValueError('CURRENT_FRESH_BINDING:'+k)
 for k,v in {'input_record_digest':digest(record),'outer_trace_digest':digest(t),'candidate_digest':digest(c),'packet_digest':digest(c['packet']),'model_hash':mh,'raw':c['request']}.items():
  if p.get(k)!=v:raise ValueError('CURRENT_PROVENANCE:'+k)
 if p.get('verified')is not True or fresh.get('fresh_checker_executed')is not True or fresh.get('source_unchanged')is not True or fresh['expected_method_registry'].get('built_before_evaluate')is not True or fresh['raw_report']['model_hash']!=mh:raise ValueError('CURRENT_REVIEW_AUTHORITY')
 reg=fresh['expected_method_registry']
 for name,h in reg['sources'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('REVIEW_SOURCE_CHANGED:'+name)
 if kind=='balanced':
  sys.path.insert(0,str(ROOT/'staging379_form'))
  from contract379 import bind
  b=bind(envelope,record,fresh,run_id)
  if review_id!=fresh['review_id']:raise ValueError('BALANCED_REVIEW_ID')
  cid=b['candidate_id'];dispatch=b['dispatch']
 else:
  from model_binding368 import bind
  b=bind(envelope,record,'joint',run_id);cid=b['candidate_id']
  if t['schema']!='SOURCE_SERVICE_JOINT367_TRACE_V1' or fresh['schema']!='JOINT367_SOURCE_VALIDATION':raise ValueError('JOINT_SOURCE_SCHEMA')
  registry=json.loads((ROOT/'semantic_rules357/method_registry_source367.json').read_text())
  if reg['methods']!=registry['methods']or reg['applicability']!=registry['applicability']:raise ValueError('JOINT_CURRENT_METHOD_REGISTRY')
  raw=fresh['raw_report'];dispatch={'repair_attempted':False,'reason':'UNSUPPORTED_REPAIR_REASON'if raw['errors']else'UNKNOWN_PENDING_REVIEW'if raw['pending']else'NO_CURRENT_REJECTION_SCOPED_PHYSICAL_ONLY'if raw['status']=='PASS_CONCEPT_SCOPED_REVIEW'else'UNKNOWN_REVIEW_STATUS','errors':raw['errors'],'pending':raw['pending'],'original_pending':raw.get('original_pending',[]),'accepted':False}
 return {'kind':kind,'run_id':run_id,'candidate_id':cid,'review_id':review_id,'record_digest':digest(record),'fresh_digest':digest(fresh),'model_digest':mh,
         'raw_digest':envelope['raw_digest'],'canonical_request_digest':envelope['canonical_request_digest'],'received_digest':envelope['received_digest'],'transport_body_sha256':envelope['transport_body_sha256'],
         'program_digest':digest(m['program']),'profile_digest':digest(m['profile']),'input_digest':digest(m['inputs']),'dispatch':dispatch}

def validate_member(envelope,record,fresh,binding,run_id,kind='balanced'):
 actual=bind_member(envelope,record,fresh,run_id,kind,binding['review_id'])
 if actual!=binding:raise ValueError('MEMBER_BINDING_CHANGED')
 return actual

def clean(s):return s.get('reason')=='COMPLETED'and s.get('worker_returncode')==0 and s.get('cleanup_verified')is True and s.get('worker_reaped')is True and s.get('unresolved')==[]
def validate_member_folder(folder,expected,require_physical_pass=True):
 from guard385 import guard
 guard(expected);folder=Path(folder);kind=folder.name
 if kind not in KINDS:raise ValueError('MEMBER_FOLDER_KIND')
 read=lambda p:json.loads(p.read_text())
 envelope=read(folder.parent/'request.json');record=read(folder/'record.json');fresh=read(folder/'fresh.json');binding=read(folder/'binding.json');rid=folder.parent.name
 if str(uuid.UUID(rid))!=rid:raise ValueError('RUN_FOLDER_UUID')
 validate_member(envelope,record,fresh,binding,rid,kind)
 for phase in ('construct','fresh','bind'):
  s=read(folder/(phase+'_supervision.json'));receipt=read(folder/(phase+'_worker_receipt.json'))
  if not clean(s):raise ValueError('UNCLEAN_CURRENT_PHASE:'+phase)
  if receipt.get('run_id')!=rid or receipt.get('kind')!=kind or receipt.get('phase')!=phase or receipt.get('source_guard_before_after')is not True or receipt.get('record_digest')!=digest(record):raise ValueError('CURRENT_PHASE_RECEIPT:'+phase)
  if phase!='construct'and receipt.get('fresh_digest')!=digest(fresh):raise ValueError('PHASE_FRESH_BINDING')
 identity=read(folder/'review_identity.json')
 if identity!={'run_id':rid,'kind':kind,'review_id':binding['review_id'],'record_digest':digest(record),'fresh_digest':digest(fresh)}:raise ValueError('REVIEW_IDENTITY_RECEIPT')
 raw=fresh['raw_report']
 if require_physical_pass and(raw['status']!='PASS_CONCEPT_SCOPED_REVIEW'or raw['errors']or raw['pending']):raise ValueError('CURRENT_PHYSICAL_NOT_PASS')
 return {'record':record,'fresh':fresh,'binding':binding,'request':envelope}

def partial(state,run_id):return {'state':state,'transport_run_id':run_id,'test_only':False,'experimental':True,'requested_count':2,'tested_branch_count':0,'request_fulfilled':False,'accepted':False,'delivery_allowed':False,'qualified_selected_set':False,'semantic_state':'UNKNOWN_CURRENT_DEPENDENCIES','repair_attempted':False,'daylight_ventilation_scope':'EXCLUDED_FROM_MVP_NOT_EVALUATED'}
