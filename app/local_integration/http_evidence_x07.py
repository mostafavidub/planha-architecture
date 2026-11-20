"""Same-request full-file decision consistency. Not producer authenticity or admission.
Consumes existing scheduler files read-only inside the X04 worker/deadline.
"""
import stop_observation_p01 as stop
import copy,hashlib,inspect,json,math,re,os,stat
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EVIDENCE_ROOT=ROOT/'live-program-evidence'
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
COMPLETE='LIVE_ORIGINAL_CHAIN_AND_CURRENT_DECISION_COMPLETED_NOT_QUALIFIED'
PINS={
 'live_program_scheduler.py':'104a8f84baac13501223013d1f370c14aba214aa',
 'parametric_pair_p04.py':'7fefe7778ec6195850e7da4cce8357c90c7dcf6e',
 'precision_boundary208.py':'e1ece20ad40d7d17e268fc9e1c2fe701ca383548',
 'source_fit_profile207.py':'8454b4a0a1e99cc49055fd6a7f375f048d9520f0',
 'current_four_decision.py':'55e503d1459fb8005607997f3e09df983bc6d041',
 'front_rear_runtime_adapter.py':'92ce916b71bb05f0087e2527a51dd8de4d40a676',
 'same_version_front_rear_contract.py':'0c182a3e26ba48ef6a42df2bf40c2a2ab67c055c',
 'current_entry_boundary_x03.py':'8383c54d4f6bfd3d94580ede2ab20276b917f414',
 'public_wln_contract.py':'80fd2b2710342735dc35e484c9b0da790995d830',
 'dimension_contract.py':'058502cd97b5131908b82fdbdba34c62d3376ea3',
 'program_profile_registry.py':'af549f86f39e2e57554cd48e0ffdea54d5444262'}
def need(ok,code):
 if not ok:raise ValueError(code)
def strict(value,depth=0):
 need(depth<=96,'X07_JSON_DEPTH')
 t=type(value)
 need(t in (dict,list,str,int,float,bool,type(None)),'X07_JSON_TYPE')
 if t is dict:
  need(all(type(k)is str for k in value),'X07_JSON_KEY')
  for v in value.values():strict(v,depth+1)
 elif t is list:
  for v in value:strict(v,depth+1)
 elif t is float:need(math.isfinite(value),'X07_NONFINITE')
def digest(value):
 strict(value)
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def decode(data):
 def unique(rows):
  out={}
  for k,v in rows:need(k not in out,'X07_DUPLICATE_KEY');out[k]=v
  return out
 def bad(v):raise ValueError('X07_NONFINITE')
 value=json.loads(data,object_pairs_hook=unique,parse_constant=bad);strict(value);return value
def guard():
 import live_program_scheduler as live,current_four_decision as decision
 import front_rear_runtime_adapter as runtime,same_version_front_rear_contract as contract
 import current_entry_boundary_x03 as boundary,parametric_pair_p04 as parametric
 snap={}
 for name,pin in PINS.items():
  p=ROOT/'app/local_integration'/name;data=p.read_bytes()
  need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==pin,'X07_SOURCE_PIN')
  snap[name]=hashlib.sha256(data).hexdigest()
 for mod,fn,name in [(live,live.bind_completed,'live_program_scheduler.py'),(live,live.preflight,'live_program_scheduler.py'),
  (decision,decision.assemble,'current_four_decision.py'),(runtime,decision.transport,'front_rear_runtime_adapter.py'),
  (contract,decision.digest,'same_version_front_rear_contract.py'),(boundary,boundary.check_model_domain,'current_entry_boundary_x03.py'),
  (parametric,parametric.prepare,'parametric_pair_p04.py'),(parametric,parametric.run,'parametric_pair_p04.py'),
  (parametric,parametric.guard,'parametric_pair_p04.py'),(parametric,parametric.verify_completed,'parametric_pair_p04.py'),
  (parametric,parametric.bath_alignment,'parametric_pair_p04.py'),(parametric,parametric.observe_bath_alignment,'parametric_pair_p04.py'),
  (stop,stop.source_snapshot,'stop_observation_p01.py'),(stop,stop.snapshot,'stop_observation_p01.py'),(stop,stop.observe,'stop_observation_p01.py')]:
  expected=(ROOT/'app/local_integration'/name).resolve()
  need(Path(mod.__file__).resolve()==expected and Path(inspect.getsourcefile(fn)).resolve()==expected,'X07_IMPORT_PATH')
 selfpath=ROOT/'app/local_integration/http_evidence_x07.py'
 need(Path(__file__).resolve()==selfpath.resolve(),'X07_SELF_PATH')
 snap['self']=hashlib.sha256(selfpath.read_bytes()).hexdigest()
 snap['boundary']=boundary.source_snapshot()
 snap['parametric']=parametric.guard()
 snap['stop_observation']=stop.source_snapshot()
 return snap
def existing_nonces():
 need(not EVIDENCE_ROOT.is_symlink(),'X07_ROOT_SYMLINK')
 need(EVIDENCE_ROOT.resolve()==(ROOT/'live-program-evidence').resolve(),'X07_ROOT_CONTAINMENT')
 return {p.name for p in EVIDENCE_ROOT.iterdir()} if EVIDENCE_ROOT.exists() else set()
class EvidenceFailure(ValueError):
 def __init__(self,observed,code):
  super().__init__('HTTP_FULL_EVIDENCE_FAILED_CLOSED')
  self.private_evidence=observed;self.reason_code=code
def read_file(path):
 # No symlink following at the file boundary; directory identity is checked too.
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:
  st=os.fstat(f.fileno());need(stat.S_ISREG(st.st_mode) and st.st_size<=32*1024*1024,'X07_FILE_LIMIT')
  data=f.read(32*1024*1024+1);need(len(data)<=32*1024*1024,'X07_FILE_LIMIT')
  return data,(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)
def consume(body,raw,before_nonces,source_before):
 import live_program_scheduler as live,current_four_decision as dec
 observed={'file_bytes':{},'file_hashes':{},'parsed':{},'verified':False}
 try:
  need(guard()==source_before,'X07_SOURCE_CHANGED')
  rawpin=digest(raw);need(type(body)is bytes,'X07_BODY_BYTES')
  need(raw.get('schema')=='AUTOMATIC_PROGRAM_LIVE_SINGLE_CASE_V1' and raw.get('state')=='LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED','X07_SCHEDULER_SCHEMA_STATE')
  need(raw.get('source_integrity_verified')is True and all(raw.get(k)is False for k in AUTH),'X07_RAW_AUTHORITY_SOURCE')
  rows=raw['attempts'];need(type(rows)is list and len(rows)==1,'X07_ONE_ATTEMPT')
  row=rows[0];nonce=row.get('nonce')
  need(type(nonce)is str and re.fullmatch('[0-9a-f]{32}',nonce) is not None,'X07_NONCE_FORMAT')
  need(nonce not in before_nonces,'X07_REUSED_EVIDENCE_DIRECTORY')
  need(row.get('receipt_verified')is True and row.get('state')==COMPLETE,'X07_COMPLETE_RECEIPT_REQUIRED')
  need(raw.get('evidence_directory')=='live-program-evidence/'+nonce,'X07_DIRECTORY_BINDING')
  need(not EVIDENCE_ROOT.is_symlink(),'X07_ROOT_SYMLINK')
  folder=EVIDENCE_ROOT/nonce
  need(folder.is_dir() and not folder.is_symlink() and folder.resolve().parent==EVIDENCE_ROOT.resolve(),'X07_DIRECTORY_CONTAINMENT')
  dir_identity=(folder.stat().st_dev,folder.stat().st_ino)
  names=['request.json','runtime-bundle.json','child-complete.json','decision.json','scheduler.json']+[k+'.json' for k in dec.SCHEMAS]
  identities={};total=0
  for name in names:
   data,identity=read_file(folder/name);total+=len(data);need(total<=96*1024*1024,'X07_TOTAL_BYTES_LIMIT')
   observed['file_bytes'][name]=data;observed['file_hashes'][name]=hashlib.sha256(data).hexdigest();identities[name]=identity
  parse_errors=[]
  for name,data in observed['file_bytes'].items():
   try:observed['parsed'][name]=decode(data)
   except (ValueError,TypeError,UnicodeError,RecursionError):parse_errors.append(name)
  need(not parse_errors,'X07_FILE_PARSE')
  p=observed['parsed'];request=p['request.json'];bundle=p['runtime-bundle.json'];child=p['child-complete.json'];decision=p['decision.json']
  need(digest(p['scheduler.json'])==rawpin,'X07_RETURNED_SCHEDULER_MISMATCH')
  need(request.get('schema')=='LIVE_PROGRAM_ATTEMPT_V1' and request.get('nonce')==nonce and request.get('body_hex')==body.hex(),'X07_REQUEST_BINDING')
  pf=live.preflight(body)
  need(digest(raw['preflight'])==digest(pf) and request['preflight_digest']==digest(pf),'X07_PREFLIGHT_BINDING')
  need(digest(request['budget'])==digest(raw['budget']) and digest(live.budgets(request['budget']))==digest(request['budget']),'X07_BUDGET_BINDING')
  live.bind_completed(child,request,bundle,decision)
  need(child.get('schema')=='LIVE_SCHEDULER_CHILD_V1' and child['state']==COMPLETE and child['nonce']==nonce,'X07_CHILD_COMPLETE')
  expected_fresh=row['receipt_verified'] is True and bundle.get('construction_returned') is True and bundle.get('model_binding_verified') is True
  need(raw.get('fresh_model_executed') is expected_fresh,'X07_CONSTRUCTION_SUMMARY')
  for key in ('model_digest','runtime_digest','decision_digest'):
   need(type(row.get(key))is str and row[key]==child[key],'X07_ATTEMPT_BINDING')
  need(row.get('budget_account_id')==nonce and row.get('attempt_id')=='PROGRAM_2BED_V1:'+nonce,'X07_ACCOUNT_BINDING')
  reports={k:p[k+'.json'] for k in dec.SCHEMAS}
  need(digest(child['assessments'])==digest(reports),'X07_CHILD_ASSESSMENTS')
  before=digest([bundle,reports,decision,child,request])
  rebuilt=dec.assemble(bundle,reports,{k:digest(v) for k,v in reports.items()})
  observed['rebuilt_decision']=copy.deepcopy(rebuilt)
  need(digest(rebuilt)==digest(decision),'X07_DECISION_REDERIVATION')
  need(digest(raw.get('current_decision'))==digest(rebuilt['decision']),'X07_SUMMARY_DECISION')
  need(digest([bundle,reports,decision,child,request])==before and digest(raw)==rawpin,'X07_INPUT_MUTATION')
  need(guard()==source_before,'X07_SOURCE_CHANGED')
  need(not EVIDENCE_ROOT.is_symlink() and not folder.is_symlink() and (folder.stat().st_dev,folder.stat().st_ino)==dir_identity,'X07_DIRECTORY_CHANGED')
  for name in names:
   data,identity=read_file(folder/name)
   need(identity==identities[name] and data==observed['file_bytes'][name],'X07_FILES_CHANGED')
  return {'schema':'HTTP_FULL_EVIDENCE_X07_V1','state':'SAME_REQUEST_FULL_REPORT_CONSISTENCY_VERIFIED_SCOPED',
   'request_digest':hashlib.sha256(body).hexdigest(),'nonce_digest':digest(nonce),'model_digest':child['model_digest'],
   'decision_digest':digest(decision),'source_digest':digest(source_before),'file_count':len(names),'file_hashes_digest':digest(observed['file_hashes']),
   'binding_verified':True,'producer_authenticity_verified':False,'engine_replay_executed':False,
   'durable_archive_verified':False,'all_PRD_requirements_verified':False,**{k:False for k in AUTH}}
 except (ValueError,KeyError,TypeError,OSError,UnicodeError,RecursionError) as ex:
  code=str(ex) if type(ex)is ValueError and re.fullmatch('X07_[A-Z_]+',str(ex)) else 'X07_EVIDENCE_ERROR'
  raise EvidenceFailure(observed,code) from None
def run_bound(body,run):
 sources=guard();before=existing_nonces()
 raw={};row={};nonce=None;parent_stage='RUN_RUNTIME'
 retained={'parsed':{},'files':[],'private_bytes':{}}
 def observation(bound=False,error=None):
  return stop.observe(body,nonce,'FRONT_REAR',retained,timed_out=row.get('timed_out')is True,
   returncode=row.get('returncode'),bound=bound,source_ok=raw.get('source_integrity_verified')is True and guard()==sources,
   source_digest=stop.digest(sources),parent_error=error,parent_stage=parent_stage if error is not None else None)
 try:
  returned=run(body)
  need(type(returned)is dict,'X07_RETURN_OBJECT')
  raw=returned;pin=digest(raw);rows=raw.get('attempts')
  row=rows[0]if type(rows)is list and len(rows)==1 and type(rows[0])is dict else{}
  nonce=row.get('nonce');parent_stage='FILE_SNAPSHOT'
  # Fixed root + new nonce, never an HTTP-supplied path. No guessing after run failure.
  if stop.sha(nonce,32)and nonce not in before and raw.get('evidence_directory')=='live-program-evidence/'+nonce:
   folder=EVIDENCE_ROOT/nonce
   need(not EVIDENCE_ROOT.is_symlink()and not folder.is_symlink()and folder.resolve().parent==EVIDENCE_ROOT.resolve(),'X07_DIRECTORY_CONTAINMENT')
   retained=stop.snapshot(folder)
  complete=row.get('state')==COMPLETE and row.get('receipt_verified')is True
  parent_stage='FULL_READBACK'
  if complete and raw.get('source_integrity_verified')is True:
   evidence=consume(body,raw,before,sources)
   initial={r['file']:r['bytes_digest']for r in retained['files']if r['state']=='PARSED_OBSERVED'}
   expected=['request.json','runtime-bundle.json','child-complete.json','decision.json','scheduler.json']+[k+'.json'for k in __import__('current_four_decision').SCHEMAS]
   need(len(expected)==evidence['file_count']and digest({k:initial[k]for k in expected})==evidence['file_hashes_digest'],'X07_DIAGNOSTIC_SNAPSHOT_CHANGED')
  else:
   evidence={'schema':'HTTP_FULL_EVIDENCE_X07_V1','state':'NOT_EVALUATED_NO_COMPLETE_SOURCE_VERIFIED_RECEIPT',
    'binding_verified':False,'producer_authenticity_verified':False,**{k:False for k in AUTH}}
  parent_stage='FINAL_SOURCE'
  need(digest(raw)==pin and guard()==sources,'X07_RETURN_SOURCE_CHANGED')
  record=observation(evidence['binding_verified'])
 except Exception as ex:
  try:record=observation(error=ex)
  except Exception:record=stop.observe(body,nonce,'FRONT_REAR',retained,parent_error=ex,parent_stage=parent_stage)
  failure=ex if isinstance(ex,EvidenceFailure)else EvidenceFailure(retained,'X07_EVIDENCE_ERROR')
  failure.http_diagnostic={'schema':'P01_PRIVATE_DIAGNOSTIC_V1','request_digest':hashlib.sha256(body).hexdigest(),'stop_record':record}
  failure.stop_private_snapshot=retained
  raise failure from None
 out=copy.deepcopy(raw);out['http_full_evidence']=evidence;out['stop_record']=record
 out['http_diagnostic']={'schema':'P01_PRIVATE_DIAGNOSTIC_V1','request_digest':hashlib.sha256(body).hexdigest(),'stop_record':record}
 if not evidence['binding_verified']:out['current_decision']={'state':'NO_VERIFIED_DECISION','blockers':['NO_COMPLETE_FULL_EVIDENCE']}
 return out
