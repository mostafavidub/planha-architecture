"""P01 safe stop observations, not raw archive, diagnosis or admission.
Only existing writer files are consumed. Unknown text/code stays a digest/count.
"""
import hashlib,inspect,json,math,os,re,stat
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
FILES=('request.json','summary.json','bundle.json','current.json','decision.json','originals.json','proposal.json','model.json','negatives.json','runtime-bundle.json','child-progress.json','child-complete.json','scheduler.json','CURRENT_PROGRAM_SUITABILITY.json','KITCHEN_GUEST_PATH_SEPARATION.json','CONTINUOUS_USEFUL_LIVING.json','NONFUNCTIONAL_WALL_EXCLUSION.json')
STAGES={'PREFLIGHT','SETUP','PROPOSE','PROPOSAL','FRAME','CONSTRUCT','CONSTRUCTOR','REPLAY','ACCESS','HISTORICAL_PHYSICAL','SINGLE_PHYSICAL','PHYSICAL','FUNCTIONAL','DECISION','FINAL_BIND','FINAL_INTEGRITY','SOURCE_AUDIT','CURRENT','UNKNOWN'}
PRODUCER={'PROPOSAL_ONLY','SEARCH_TIMEOUT_NO_WITNESS','NO_PROPOSAL_IN_THIS_TOPOLOGY','NO_PROPOSAL_IN_THIS_PROGRAM','ROUNDED_PROPOSAL_REJECTED'}
REASONS={'ROOM_OR_CORE_BOUND_CONFLICT','ORDERED_SIX_PERSON_MACRO_NOT_APPLICABLE'}
OUTCOMES={'VALID_UNSUPPORTED','PRE_SOLVER_REJECTED','SOLVER_INFEASIBLE_THIS_MILP','SOLVER_LIMIT_NO_INCUMBENT','SOLVER_LIMIT_WITH_INCUMBENT','PROPOSAL_OBSERVED','ROUNDED_PROPOSAL_REJECTED','NO_PROPOSAL_OBSERVED','ASSEMBLY_ERROR','EXECUTION_ERROR','OUTER_TIMEOUT','COMPLETED_OBSERVED','UNOBSERVED','EVIDENCE_READ_ERROR','WORKER_START_FAILED'}
ERROR_TYPES={'ValueError','KeyError','TypeError','AssertionError','OSError','FileNotFoundError','RecursionError','RuntimeError','JSONDecodeError','UNKNOWN'}
PHYSICAL_CODES=set(["A9_SINGLE_BED_SOURCE_CHANGED","ACTIVITY_ROUTE_INVENTORY","AUDIT_MUTATED_MODEL","BEDROOM_FIXTURE_MEMBERSHIP","BEDROOM_PROGRAM_COUNT","BODY_FIXTURE_COLLISION","BODY_OUTSIDE_OWNERSHIP","BODY_WALL_COLLISION","CATALOG_REFERENCE_SIZE_MISMATCH","COMMON_BODY_FIXTURE_COLLISION","COMMON_BODY_OTHER_CORE","COMMON_BODY_OTHER_UNIT","COMMON_BODY_OUTSIDE_FRAME","COMMON_BODY_PRIVATE_ROOM","COMMON_BODY_WALL_COLLISION","COMMON_ROUTE_INVENTORY","COMMON_ROUTE_NOT_FROM_CORE","COMMON_ROUTE_NOT_TO_REAL_ENTRY_FLOOR","COMMON_ROUTE_UNKNOWN_ENDPOINT","CONCEPT_SCOPE_SOURCE_CHANGED","DECLARED_BEDROOM_PROGRAM_BINDING","DINING_SOURCE_INVENTORY_BINDING","DUPLICATE_MODULE_PLACEMENT","FIXTURE_CATALOG_BINDING","FIXTURE_COLLISION","FIXTURE_INVENTORY","FIXTURE_OUTSIDE_OWNERSHIP","FIXTURE_ROTATION","FIXTURE_WALL_COLLISION","HOST_WALL_UNACCOUNTED_GAP","IMMUTABLE_FIXTURE_SIZE_CHANGED","IMMUTABLE_REFERENCE_FILE_CHANGED","INPUT_PROGRAM_DOMAIN","KITCHEN_ACTUAL_ARCH_CUT","KITCHEN_APRON_ACTUAL_OCCUPIED_COLLISION","KITCHEN_ARCH_TYPE_NOT_SOURCE_PROFILE","KITCHEN_FIXTURE_COLLISION","KITCHEN_FIXTURE_FLOOR_OR_WALL","KITCHEN_FIXTURE_ROTATION","KITCHEN_IMMUTABLE_FIXTURE_SIZE","KITCHEN_MODULE_BODY_COLLISION","KITCHEN_MODULE_FIXTURE_INVENTORY","KITCHEN_MODULE_FIXTURE_SOURCE_BINDING","KITCHEN_MODULE_PRODUCER_SOURCE_CHANGED","KITCHEN_MODULE_ROUTE_INVENTORY","KITCHEN_MODULE_SCHEMA","KITCHEN_MODULE_SCHEMA_OR_GEOMETRY","KITCHEN_OWNERSHIP_ACCOUNTING","KITCHEN_PORT_BINDING","KITCHEN_PORT_BODY_ACTUAL_OCCUPIED_COLLISION","KITCHEN_PORT_ROLE_BINDING","KITCHEN_ROOM_FLOOR_BINDING","KITCHEN_ROUTE_PORT_TARGET_BINDING","MISSING_REQUIRED_ACTIVITY_ROUTES","MODEL_BODY_CONTRACT_BINDING","MODEL_SCHEMA_OR_GEOMETRY_ERROR","MODULE_ACTIVITY_ROUTE_INVENTORY","MODULE_APERTURE_HOST_PARTITION","MODULE_APERTURE_NOT_CUT","MODULE_APRON_NOT_REAL_PUBLIC_FLOOR","MODULE_BODY_OBSTACLE_COLLISION","MODULE_CLOSET_HALF_INVENTORY","MODULE_CLOSET_OPERATION_INVENTORY","MODULE_CONSTRAINT_VERSION","MODULE_DOOR_OPERATION_INVENTORY","MODULE_FIXTURE_CATALOG_BINDING","MODULE_FIXTURE_COLLISION","MODULE_FIXTURE_KIND_BINDING","MODULE_FIXTURE_ORIENTATION","MODULE_FIXTURE_OUTSIDE_OWNER","MODULE_FIXTURE_RIGID_SIZE","MODULE_FIXTURE_WALL_COLLISION","MODULE_ISOMETRY_NOT_ALLOWED","MODULE_KITCHEN_MOTION_PARAMETER_BINDING","MODULE_KITCHEN_OPERATION_INVENTORY","MODULE_OPENING_INVENTORY","MODULE_OPENING_ROLE_HOST_BINDING","MODULE_OPERATION_ROLE_BINDING","MODULE_OPERATION_STATE_INVENTORY","MODULE_OWNERSHIP_OUTSIDE_BOUNDS","MODULE_PLACED_PORT_INVENTORY","MODULE_PLACED_PORT_ROLE_OPENING_BINDING","MODULE_PLACEMENT_CONSTRAINT_BINDING","MODULE_PLACEMENT_PHYSICAL_BINDING","MODULE_PLACEMENT_SCHEMA_OR_GEOMETRY","MODULE_PORT_APERTURE_BINDING","MODULE_PORT_APPROACH_NOT_ADJACENT_TO_APERTURE","MODULE_PORT_APPROACH_NOT_REAL_OWNED_FLOOR","MODULE_PORT_CENTER_NOT_IN_ACTUAL_PORT","MODULE_PORT_ROLE_NOT_CONNECTED","MODULE_PORT_TOO_NARROW","MODULE_PRIVATE_FIXTURE_INVENTORY","MODULE_PRODUCER_SOURCE_CHANGED","MODULE_PROGRAM_BODY_BINDING","MODULE_PUBLIC_TYPE_NOT_ALLOWED","MODULE_REFERENCE_BINDING","MODULE_ROOM_FLOOR_WALL_OVERLAP","MODULE_ROOM_OUTSIDE_OWNERSHIP","MODULE_ROOM_OVERLAP","MODULE_ROUTE_NOT_FROM_PORT","MODULE_ROUTE_OUTSIDE_OWNER","MODULE_ROUTE_TARGET_BINDING","MODULE_SCHEMA","MODULE_SCHEMA_OR_GEOMETRY_ERROR","MODULE_SERVICE_REGION_OWNER_BINDING","MODULE_SOURCE_HASH_MISMATCH","MODULE_TYPED_PUBLIC_ROLE","MODULE_UNACCOUNTED_FLOOR","NO_BODY_CROSSING_AT_ACTUAL_APERTURE","OPENING_NOT_ACTUALLY_CUT","OPENING_OUTSIDE_HOST","OWNERSHIP_OUTSIDE_FRAME","PHYSICAL_REPORT_BINDING_OR_ORIGIN","PLACED_MODULE_ROUTE_FIXTURE_COLLISION","PLACED_MODULE_ROUTE_OUTSIDE_OWNER","PLACED_MODULE_ROUTE_WALL_COLLISION","PLACED_PORT_BODY_NOT_ON_PUBLIC_FLOOR","Q11_IMPACT_MODEL_PROGRAM_BINDING","Q11_REQUIRED_ACTIVITY_REMOVED","Q11_SEPARATE_SIGHT_SCREEN_REMAINS","ROOM_OUTSIDE_OWNERSHIP","ROOM_OVERLAP","ROTATION_SOURCE133_BINDING","ROUTE_TARGET_BINDING","RULE_FAILED","SERVICE_ACTIVITY_ROUTE_INVENTORY","SERVICE_BODY_FIXTURE","SERVICE_BODY_FLOOR_WALL","SERVICE_FIXTURE_CATALOG_BINDING","SERVICE_FIXTURE_COLLISION","SERVICE_FIXTURE_FLOOR_WALL","SERVICE_FIXTURE_INVENTORY","SERVICE_MODULE_SCHEMA","SERVICE_MODULE_SCHEMA_OR_GEOMETRY","SERVICE_PRIVACY_TARGET_OUTSIDE_ACTUAL_FLOOR","SERVICE_PRIVATE_TARGET_VISIBLE","SERVICE_PRODUCER_SOURCE_CHANGED","SERVICE_RIGID_FIXTURE_DIMENSION","SERVICE_ROOM_ACTUAL_FLOOR","SERVICE_ROUTE_ENDPOINT_BINDING","SERVICE_SOURCE_BINDING","SIX_PERSON_PROGRAM_OCCUPANCY_BINDING","SLEEP_ROLE_MODULE_BINDING","SOURCE_MODULE_RECHECK_FAILED","TWIN_BASE_MODULE_SOURCE_CHANGED","TWIN_BED_ACTIVITY_NOT_ACTUAL_ADJACENT_BAND","TWIN_EACH_BED_ACTIVITY_INVENTORY","TWIN_INSTANCE_ID_INVENTORY","TWIN_SLEEP_PROFILE_BINDING","TWIN_SOURCE_CHANGED","UNACCOUNTED_OWNERSHIP_FLOOR","UNEXPECTED_MODULE_FIXTURE","UNIT_COUNT","UNIT_OWNERSHIP_OVERLAP","UNKNOWN_FIXTURE_TYPE","UNSUPPORTED_CONSTRAINT_CONTRACT_VERSION","UNTRUSTED_RECEIPTS_NOT_ACCEPTED","WALL_OUTSIDE_FRAME","WHOLE_MODULE_BEDROOM_INVENTORY","WHOLE_MODULE_PORT_INVENTORY","WHOLE_PRIVACY_BATH_MISSING","WHOLE_PRIVACY_BED_INVENTORY_EMPTY","WINDOW_HEIGHT_OR_FLOOR_PORTAL","WINDOW_HOST_MISSING_OR_OUTSIDE"])
PINS={'search114.py':'65e0f278c9f9ef480388d3ea8056161c0a938a36','checker114.py':'4f25ae5b9444c077159af90e872a84f4fcb25f42','rule_contract118.py':'97bf97b3fe90d14314f0633357e6e66856597f8b'}
def digest(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def sha(value,n=64):return type(value)is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',value)is not None
def source_snapshot():
 out={}
 for name,pin in PINS.items():
  path=ENGINE/name;data=path.read_bytes()
  if path.is_symlink()or hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()!=pin:raise ValueError('P01_SOURCE_PIN')
  out[name]=hashlib.sha256(data).hexdigest()
 physical=ROOT/'app/local_integration/single_physical_p17.py';data=physical.read_bytes()
 if physical.is_symlink()or hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()!='16a16f20af2603ea67a2cb631954342462fe73a0':raise ValueError('P01_PHYSICAL_SOURCE_PIN')
 out['single_physical_p17.py']=hashlib.sha256(data).hexdigest()
 path=ROOT/'app/local_integration/stop_observation_p01.py'
 if Path(__file__).resolve()!=path.resolve()or Path(inspect.getsourcefile(observe)).resolve()!=path.resolve():raise ValueError('P01_IMPORT_PATH')
 out['self']=hashlib.sha256(path.read_bytes()).hexdigest()
 return out
def decode(data):
 def pairs(rows):
  out={}
  for k,v in rows:
   if k in out:raise ValueError('DUPLICATE')
   out[k]=v
  return out
 def bad(value):raise ValueError('NONFINITE')
 value=json.loads(data,object_pairs_hook=pairs,parse_constant=bad);digest(value);return value
def snapshot(folder,names=FILES):
 """All readable bytes hashed BEFORE parsing; per-file errors never stop siblings.
 private_bytes is process-local, not a deliverable or durable archive.
 """
 out={'parsed':{},'files':[],'private_bytes':{}};total=0
 for name in names:
  if name not in FILES:raise ValueError('P01_FILE_NAME')
  item={'file':name,'state':'MISSING','bytes_digest':None,'byte_count':None}
  try:
   if folder.is_symlink():raise OSError('ROOT_SYMLINK')
   path=folder/name
   if not path.exists():out['files'].append(item);continue
   fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
   with os.fdopen(fd,'rb')as stream:
    before=os.fstat(stream.fileno())
    if not stat.S_ISREG(before.st_mode)or before.st_size>32*1024*1024 or total+before.st_size>96*1024*1024:raise OSError('LIMIT')
    data=stream.read(32*1024*1024+1);after=os.fstat(stream.fileno())
   if len(data)>32*1024*1024:raise OSError('LIMIT')
   total+=len(data)
   item.update(bytes_digest=hashlib.sha256(data).hexdigest(),byte_count=len(data),state='BYTES_OBSERVED')
   out['private_bytes'][name]=data
   if (before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns):item['state']='CHANGED_DURING_READ'
   else:
    try:out['parsed'][name]=decode(data);item['state']='PARSED_OBSERVED'
    except (ValueError,TypeError,UnicodeError,RecursionError):item['state']='PARSE_FAILED'
  except OSError:item['state']='READ_FAILED'
  out['files'].append(item)
 return out
def solver_observation(proposal):
 q=proposal if type(proposal)is dict else {}
 status=q.get('status');status=status if type(status)is str and status in PRODUCER else None
 reason=q.get('reason');reason=reason if type(reason)is str and reason in REASONS else 'UNKNOWN_CODE' if reason is not None else None
 code=q.get('solver_status');code=code if type(code)is int and code in range(5) else None
 num=lambda k:q[k]if type(q.get(k))in(int,float)and math.isfinite(q[k])and q[k]>=0 else None
 called=None;incumbent=None;evidence='UNOBSERVED'
 pre_fields_absent=all(k not in q for k in ('solver_status','solver_seconds','budget_seconds'))
 if status=='NO_PROPOSAL_IN_THIS_PROGRAM'and reason=='ROOM_OR_CORE_BOUND_CONFLICT'and pre_fields_absent:called=False;evidence='SOURCE_PRE_SOLVER_RETURN'
 elif status=='NO_PROPOSAL_IN_THIS_TOPOLOGY'and reason=='ORDERED_SIX_PERSON_MACRO_NOT_APPLICABLE'and pre_fields_absent:called=False;evidence='SOURCE_PRE_SOLVER_RETURN'
 elif code is not None and num('solver_seconds')is not None and num('budget_seconds')is not None:
  called=True;evidence='SOURCE_RETURN_OBSERVATION'
  if status in ('PROPOSAL_ONLY','ROUNDED_PROPOSAL_REJECTED'):incumbent=True
  elif status in ('SEARCH_TIMEOUT_NO_WITNESS','NO_PROPOSAL_IN_THIS_TOPOLOGY'):incumbent=False
 return status,reason,{'called':called,'status':code,'seconds':num('solver_seconds'),'budget_seconds':num('budget_seconds'),'incumbent_observed':incumbent,'evidence':evidence}
def physical_observation(report,model_hash,bound):
 r=report if type(report)is dict else {};errors=r.get('errors');pending=r.get('pending')
 codes={}
 if type(errors)is list:
  for error in errors:
   code=error.get('code')if type(error)is dict else error if type(error)is str else None
   code=code if type(code)is str and code in PHYSICAL_CODES else 'UNKNOWN_CODE'
   codes[code]=codes.get(code,0)+1
 mh=r.get('model_hash',r.get('model_digest'))
 match=sha(model_hash)and mh==model_hash
 status=r.get('status');status=status if status in ('FAIL','PASS_CONCEPT_SCOPED_REVIEW','NOT_EVALUATED')else None
 return {'state':'BOUND_REPORT_OBSERVATION'if bound and match else'OBSERVED_UNVERIFIED'if r else'NOT_REPORTED',
  'status':status,'error_count':len(errors)if type(errors)is list else None,'pending_count':len(pending)if type(pending)is list else None,
  'error_codes':[{'code':k,'count':v}for k,v in sorted(codes.items())],
  'report_digest':digest(r)if r else None,'model_digest':mh if sha(mh)else None}
def observe(body,nonce,family,snap,*,timed_out=False,returncode=None,bound=False,source_ok=False,source_digest=None,parent_error=None,parent_stage=None):
 """caller bound means its existing full receipt passed; never inferred here."""
 p=snap['parsed'];summary=p.get('summary.json',{});summary=summary if type(summary)is dict else{}
 runtime=p.get('runtime-bundle.json',{});runtime=runtime if type(runtime)is dict else{}
 proposal=p.get('proposal.json',runtime.get('proposal'));proposal=proposal if type(proposal)is dict else{}
 status,reason,solver=solver_observation(proposal)
 stage=parent_stage if parent_stage in STAGES else summary.get('stage')
 if type(stage)is str and stage.startswith('CURRENT_'):stage='CURRENT'
 if type(stage)is not str or stage not in STAGES:
  errors=runtime.get('errors',[])
  last=errors[-1]if type(errors)is list and errors and type(errors[-1])is dict else{}
  stage=str(last.get('stage','UNKNOWN')).upper()
  if stage=='UNKNOWN'and type(runtime.get('stages'))is list and runtime['stages']:stage=str(runtime['stages'][-1]).upper()
  if stage not in STAGES:stage='UNKNOWN'
 errors=runtime.get('errors',[])
 error=errors[-1]if type(errors)is list and errors and type(errors[-1])is dict else{}
 error_type=type(parent_error).__name__ if parent_error is not None else summary.get('error_type',error.get('type'))
 execution_error=parent_error is not None or returncode not in (None,0)or summary.get('state')=='FAILED_CLOSED'or runtime.get('status')=='RUNTIME_FAILED_CLOSED'
 outcome='UNOBSERVED'
 if status=='PROPOSAL_ONLY':outcome='SOLVER_LIMIT_WITH_INCUMBENT'if solver['status']==1 else'PROPOSAL_OBSERVED'
 elif status=='ROUNDED_PROPOSAL_REJECTED':outcome='ROUNDED_PROPOSAL_REJECTED'
 elif solver['called']is False:outcome='PRE_SOLVER_REJECTED'
 elif solver['incumbent_observed']is False:outcome='SOLVER_INFEASIBLE_THIS_MILP'if solver['status']==2 else'SOLVER_LIMIT_NO_INCUMBENT'if solver['status']==1 else'NO_PROPOSAL_OBSERVED'
 if bound:outcome='COMPLETED_OBSERVED'
 if execution_error:outcome='ASSEMBLY_ERROR'if stage in ('CONSTRUCT','CONSTRUCTOR')else'EXECUTION_ERROR'
 if parent_stage=='SETUP'and parent_error is not None:outcome='WORKER_START_FAILED'
 if any(r['state']in('PARSE_FAILED','CHANGED_DURING_READ','READ_FAILED')for r in snap['files']):outcome='EVIDENCE_READ_ERROR'
 if timed_out:outcome='OUTER_TIMEOUT'
 originals=p.get('originals.json',runtime.get('reports',{}));originals=originals if type(originals)is dict else{}
 model_hash=summary.get('model_digest',runtime.get('model_digest'))
 # Input/body binding is independent of parser or receipt success.
 request=p.get('request.json',{});request=request if type(request)is dict else{}
 request_ok=request.get('body_hex')==body.hex()and request.get('nonce')==nonce and sha(nonce,32)
 out={'schema':'STOP_OBSERVATION_P01_V1','request_digest':hashlib.sha256(body).hexdigest(),'attempt_nonce':nonce if sha(nonce,32)else None,
  'family':family if family in ('SINGLE_FRONT_TOP_CORE_P15_V1','FRONT_REAR')else'UNKNOWN',
  'programme':'PROGRAM_2BED_V1','stage':stage,'outcome':outcome,'producer_status':status,'producer_reason':reason,
  'solver':solver,'physical':physical_observation(originals.get('physical'),model_hash,bound and request_ok and source_ok),
  'execution_error_type':error_type if type(error_type)is str and error_type in ERROR_TYPES else'UNKNOWN'if execution_error else None,
  'error_record_digest':digest({'worker_error_code':summary.get('error_code'),'runtime_error':error,'parent_error_type':type(parent_error).__name__ if parent_error is not None else None})if execution_error else None,
  'files':snap['files'],'source_digest':source_digest if sha(source_digest)else None,'source_unchanged':source_ok is True,
  'binding_verified':bound is True and request_ok and source_ok is True,'constraint_cause':'UNKNOWN',
  'raw_archive_durable':False,**{k:False for k in AUTH}}
 out['record_digest']=digest(out);return out
def unsupported(body):
 out=observe(body,None,'UNKNOWN',{'parsed':{},'files':[]})
 out.update(programme='NOT_SELECTED',stage='PREFLIGHT',outcome='VALID_UNSUPPORTED')
 out.pop('record_digest');out['record_digest']=digest(out);return out
def _safe(value,request_digest):
 """Exact generated shape + finite typed scalars + semantic enum allowlists."""
 if type(value)is not dict:return None
 expected={'schema','request_digest','attempt_nonce','family','programme','stage','outcome','producer_status','producer_reason','solver','physical','execution_error_type','error_record_digest','files','source_digest','source_unchanged','binding_verified','constraint_cause','raw_archive_durable','record_digest',*AUTH}
 if set(value)!=expected or value['schema']!='STOP_OBSERVATION_P01_V1'or value['request_digest']!=request_digest:return None
 if any(value[k]is not False for k in (*AUTH,'raw_archive_durable'))or type(value['source_unchanged'])is not bool or type(value['binding_verified'])is not bool:return None
 if value['stage']not in STAGES or value['outcome']not in OUTCOMES or value['family']not in ('UNKNOWN','SINGLE_FRONT_TOP_CORE_P15_V1','FRONT_REAR')or value['programme']not in ('PROGRAM_2BED_V1','NOT_SELECTED'):return None
 if value['producer_status']not in PRODUCER|{None}or value['producer_reason']not in REASONS|{None,'UNKNOWN_CODE'}or value['constraint_cause']!='UNKNOWN'or value['execution_error_type']not in ERROR_TYPES|{None}:return None
 for k,n in (('attempt_nonce',32),('source_digest',64),('error_record_digest',64)):
  if value[k]is not None and not sha(value[k],n):return None
 sol=value['solver']
 if type(sol)is not dict or set(sol)!= {'called','status','seconds','budget_seconds','incumbent_observed','evidence'}:return None
 if any(sol[k]is not None and type(sol[k])is not bool for k in ('called','incumbent_observed'))or sol['status']is not None and(type(sol['status'])is not int or sol['status']not in range(5)):return None
 if any(sol[k]is not None and(type(sol[k])not in(int,float)or not math.isfinite(sol[k])or sol[k]<0)for k in ('seconds','budget_seconds'))or sol['evidence']not in ('UNOBSERVED','SOURCE_PRE_SOLVER_RETURN','SOURCE_RETURN_OBSERVATION'):return None
 ph=value['physical']
 if type(ph)is not dict or set(ph)!= {'state','status','error_count','pending_count','error_codes','report_digest','model_digest'}:return None
 if ph['state']not in ('BOUND_REPORT_OBSERVATION','OBSERVED_UNVERIFIED','NOT_REPORTED')or ph['status']not in (None,'FAIL','PASS_CONCEPT_SCOPED_REVIEW','NOT_EVALUATED'):return None
 if any(ph[k]is not None and(type(ph[k])is not int or ph[k]<0)for k in ('error_count','pending_count'))or any(ph[k]is not None and not sha(ph[k])for k in ('report_digest','model_digest')):return None
 if type(ph['error_codes'])is not list:return None
 for row in ph['error_codes']:
  if type(row)is not dict or set(row)!={'code','count'}or row['code']not in PHYSICAL_CODES|{'UNKNOWN_CODE'}or type(row['count'])is not int or row['count']<=0:return None
 if ph['error_count']is not None and sum(r['count']for r in ph['error_codes'])!=ph['error_count']:return None
 if len({r['code']for r in ph['error_codes']})!=len(ph['error_codes']):return None
 if type(value['files'])is not list:return None
 if len({r.get('file')for r in value['files']if type(r)is dict})!=len(value['files']):return None
 for row in value['files']:
  if type(row)is not dict or set(row)!={'file','state','bytes_digest','byte_count'}or row['file']not in FILES or row['state']not in ('MISSING','BYTES_OBSERVED','PARSED_OBSERVED','CHANGED_DURING_READ','PARSE_FAILED','READ_FAILED'):return None
  if row['bytes_digest']is not None and not sha(row['bytes_digest'])or row['byte_count']is not None and(type(row['byte_count'])is not int or row['byte_count']<0):return None
 if not sha(value['record_digest'])or digest({k:v for k,v in value.items()if k!='record_digest'})!=value['record_digest']:return None
 return json.loads(json.dumps(value))

def safe(value,request_digest):
 try:return _safe(value,request_digest)
 except (ValueError,TypeError,KeyError,RecursionError,OverflowError):return None
