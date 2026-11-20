"""Operator-only, private one-shot archive evaluation on loopback. No generator."""
import argparse, hashlib, inspect, io, json, math, os, re, stat, sys, threading, time, traceback, zipfile
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SELF=Path(__file__).resolve()
ROOT=SELF.parents[1]
LOCAL=ROOT/'app/local_integration'
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(LOCAL),str(ENGINE),str(ROOT/'frontend')]
from http_withholding_x04 import Boundary
from public_input_errors403 import parse_public_errors,response as input_error_response
from current_entry_boundary_x03 import public_request,check_model_domain
from dimension_contract import InputError,MAX_BODY
from same_version_front_rear_contract import digest,ENGINE_REVISION

RAW={'W':'20','L':'25','n':2,'requested_count':1}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
ZERO={**{k:False for k in AUTH},'generation_started':False,'actual_live_attempts':0,'plan_count_available':0,'download_available':False}
CAP=32*1024*1024
ROUTE='/api/public/plan'
CASE_SCOPE=['20','25',2]
ARCHIVE_MEMBER='frame125-two-nonsquare.json'

def need(v,c):
 if not v:raise ValueError(c)
def sha(v):return hashlib.sha256(v).hexdigest()
def hash_token(v):return type(v)is str and re.fullmatch('[0-9a-f]{64}',v) is not None
def unique(rows):
 out={}
 for k,v in rows:
  need(k not in out,'ARCHIVE_DUPLICATE_KEY');out[k]=v
 return out
def float_num(s):
 v=float(s);need(math.isfinite(v),'ARCHIVE_NONFINITE');return v
def bad_number(_):raise ValueError('ARCHIVE_NONFINITE')
def decode(b):
 return json.loads(b,object_pairs_hook=unique,parse_float=float_num,parse_constant=bad_number)
def canonical(v):
 return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()

def checked_path(path):
 p=Path(path)
 need(p.is_absolute() and p.resolve()==p,'PRIVATE_PATH_REQUIRED')
 return p

def private_read(path):
 p=checked_path(path)
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK),'rb')as f:
  st=os.fstat(f.fileno())
  need(stat.S_ISREG(st.st_mode) and not st.st_mode&0o077 and st.st_uid==os.getuid() and st.st_size<=CAP,'PRIVATE_FILE_REQUIRED')
  b=f.read(CAP+1);need(len(b)==st.st_size,'PRIVATE_FILE_SIZE')
 return b

def private_directory(path):
 p=checked_path(path)
 p.mkdir(mode=0o700,exist_ok=False)
 need(p.resolve()==p and p.stat().st_mode&0o077==0 and p.stat().st_uid==os.getuid(),'PRIVATE_DIRECTORY_REQUIRED')
 return p

def write(path,name,value):
 b=value if type(value)is bytes else canonical(value)+b'\n'
 dst=path/name;part=path/(name+'.part')
 with os.fdopen(os.open(part,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600),'wb')as f:
  f.write(b);f.flush();os.fsync(f.fileno())
 os.link(part,dst);part.unlink()
 need(private_read(dst)==b,'PRIVATE_OUTPUT_READBACK')
 return sha(b)

def exact_request(body):
 envelope=parse_public_errors(body)
 second,raw=public_request(body)
 need(digest(envelope)==digest(second),'REQUEST_PARSE_CONFLICT')
 return digest(raw)==digest(RAW)

def archive_row(blob,pin,modelpin):
 need(hash_token(pin) and hash_token(modelpin) and sha(blob)==pin,'ARCHIVE_PIN')
 with zipfile.ZipFile(io.BytesIO(blob))as z:
  need(z.namelist()==[ARCHIVE_MEMBER] and z.getinfo(ARCHIVE_MEMBER).file_size<=CAP and z.testzip()is None,'ARCHIVE_INVENTORY')
  doc=decode(z.read(ARCHIVE_MEMBER))
 need(doc['engine_revision']==ENGINE_REVISION,'ARCHIVE_ENGINE')
 found=[r for r in doc['cases'] if digest(r.get('raw'))==digest(RAW)]
 need(len(found)==1,'ARCHIVE_EXACT_CASE')
 r=found[0];p=r['packet'];ctx=r['context'];t=ctx['construction_trace'];m=p['world_model']
 need(p['family']==t['family']=='LEFT_RIGHT' and p['admission_claim'] is False,'ARCHIVE_FAMILY')
 need(digest([r['raw'],r['proposal'],p,ctx])==r['input_bundle_digest']==r['input_bundle_digest_after'],'ARCHIVE_BUNDLE')
 need(digest(m)==modelpin==r['world_model_digest']==t['model_hash'] and digest(p['core'])==t['core_hash'] and digest(p['local_model'])==t['local_model_hash'],'ARCHIVE_MODEL')
 need(m['inputs']==ctx['inputs']==CASE_SCOPE and p['core']['solver_inputs']==['25','20',2] and r['source_binding']['scoped_verified'] is True,'ARCHIVE_FRAME')
 need(digest(t['raw'])==digest(RAW) and digest(t['proposals'])==digest({'A':r['proposal'],'B':r['proposal']}),'ARCHIVE_PROPOSALS')
 need(t['source_revision']==ENGINE_REVISION and r['replay']['verified'] is True,'ARCHIVE_REPLAY')
 need({'replay','historical_report','current_report','source_binding'}<=set(r['completed_report_digests']),'ARCHIVE_REPORT_SET')
 for k,v in r['completed_report_digests'].items():need(digest(r[k])==v,'ARCHIVE_ORIGINAL_REPORT')
 return r

def audit(fns):
 from engine114 import revision
 from current_entry_boundary_x03 import source_snapshot
 from current_four_decision import REQUIRED_SOURCES
 need(revision()==ENGINE_REVISION,'EVALUATOR_ENGINE_REVISION')
 files={SELF,LOCAL/'http_withholding_x04.py',LOCAL/'public_input_errors403.py',LOCAL/'front_rear_runtime_adapter.py'}
 files|={ROOT/f for ks in REQUIRED_SOURCES.values() for f in ks}
 for f,name in fns:
  p=(ENGINE if name in ('construction_replay127.py','evaluate_pair127.py') else LOCAL)/name
  need(Path(inspect.getsourcefile(f)).resolve()==p,'EVALUATOR_IMPORT_PATH')
  files.add(p)
 need(Path(inspect.getsourcefile(Boundary.execute)).resolve()==LOCAL/'http_withholding_x04.py','BOUNDARY_IMPORT_PATH')
 need(all(p.resolve()==p and p.is_relative_to(ROOT) for p in files),'EVALUATOR_SOURCE_PATH')
 return {'engine':ENGINE_REVISION,'boundary':source_snapshot(),'files':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted(files)}}

def evaluate_archive(body,archive_path,archive_pin,model_pin,output_path):
 from construction_replay127 import verify
 from evaluate_pair127 import evaluate
 import current_four_decision as four
 from current_programme_evaluator import assess as programme
 from source_guest_route_evaluator import assess as guest
 from source_living_evaluator import assess as living
 from source_wall_function_evaluator import assess as wall
 from frame125_two_source_binding import proposal_check
 evaluators=dict(zip(four.SCHEMAS,(programme,guest,living,wall)))
 fns=[(verify,'construction_replay127.py'),(evaluate,'evaluate_pair127.py'),(four.assemble,'current_four_decision.py'),
  (programme,'current_programme_evaluator.py'),(guest,'source_guest_route_evaluator.py'),(living,'source_living_evaluator.py'),(wall,'source_wall_function_evaluator.py')]
 folder=private_directory(output_path)
 files={};timeline=[];stage='INITIAL';anchor=time.monotonic();request_pin=sha(body)
 def keep(n,v):files[n]=write(folder,n,v)
 def mark(name,state):
  timeline.append({'stage':name,'state':state,'elapsed_seconds':time.monotonic()-anchor,'utc':datetime.now(timezone.utc).isoformat()})
  write(folder,'phase-'+str(len(timeline))+'.json',timeline[-1])
 try:
  keep('request.json',body)
  stage='ARCHIVE_SOURCE_BINDING';mark(stage,'STARTED');source=audit(fns)
  blob=private_read(archive_path);r=archive_row(blob,archive_pin,model_pin)
  # Keep ZIP-native object insertion order in this live bundle. Do not
  # deserialize our canonical private snapshots back into assessor input.
  p=r['packet'];ctx=r['context'];m=p['world_model'];t=ctx['construction_trace']
  check_model_domain(m)
  for u in ('A','B'):proposal_check(t['proposals'][u],p['core'])
  original=digest(r);keep('archived-row.json',r);keep('source-before.json',source);mark(stage,'RETURNED')
  stage='ORIGINAL_REPLAY';mark(stage,'STARTED')
  replay=verify(m,ctx);keep('replay.json',replay)
  need(replay['verified'] is True and replay['model_hash']==model_pin and digest(replay)==digest(r['replay']),'ARCHIVE_REPLAY_READBACK')
  mark(stage,'RETURNED')
  stage='WHOLE_ORIGINAL_PHYSICAL';mark(stage,'STARTED')
  ph=evaluate(p,ctx);keep('physical.json',ph)
  need(ph['model_hash']==model_pin and ph['accepted'] is False and ph['release'] is False and digest(ph['multiproposal_provenance127'])==digest(replay),'ARCHIVE_PHYSICAL_BINDING')
  mark(stage,'RETURNED')
  reports={'replay':replay,'physical':ph,'original_archived_physical':r['historical_report'],'original_archived_replay':r['replay']}
  bundle={'schema':'P19_ARCHIVED_LR_PRIVATE_EVALUATION_INPUT_V1','packet':p,'context':ctx,'model_digest':model_pin,'engine_revision':ENGINE_REVISION,
   'reports':reports,'report_digests':{k:digest(v)for k,v in reports.items()},**{k:False for k in AUTH}}
  bpin=digest(bundle);keep('bound-input.json',bundle)
  results={}
  for criterion,fn in evaluators.items():
   stage=criterion;mark(stage,'STARTED');current=fn(bundle);keep(criterion+'.json',current)
   need(current['model_digest']==model_pin and digest(bundle)==bpin and digest(r)==original,'ARCHIVE_ASSESSMENT_BINDING')
   results[criterion]=current;mark(stage,'RETURNED')
  stage='DECISION_AND_READBACK';mark(stage,'STARTED')
  decision=four.assemble(bundle,results,{k:digest(v)for k,v in results.items()});keep('decision.json',decision)
  need(decision['integrity_verified'] is True and decision['model_digest']==model_pin and all(decision[k]is False for k in AUTH),'ARCHIVE_DECISION_BINDING')
  need(digest(bundle)==bpin and digest(r)==original and audit(fns)==source and private_read(archive_path)==blob,'ARCHIVE_FINAL_SOURCE_OR_INPUT_DRIFT')
  need(all(sha(private_read(folder/n))==v for n,v in files.items()),'ARCHIVE_FINAL_FILES')
  mark(stage,'RETURNED')
  # One actual archive re-evaluation receipt; this is not a live generation attempt.
  receipt={'schema':'P19_ARCHIVED_LR_PRIVATE_REPORT_BINDING_V1','request_digest':request_pin,'archive_byte_sha256':archive_pin,
   'case':CASE_SCOPE,'family':'LEFT_RIGHT','archive_model_digest':model_pin,'binding_verified':True,
   'files_sha256':dict(files),'source_digest':digest(source),'decision_digest':digest(decision),'decision_state':decision['decision']['state'],
   'selected_report_states':{k:v['state']for k,v in results.items()},'physical_status':ph['status'],
   'structurally_matches_historical_physical':digest(ph)==digest(r['historical_report']),
   'timeline':timeline,**ZERO}
  receipt_bytes=write(folder,'receipt.json',receipt)
  return {'source_integrity_verified':True,'attempts':[{'receipt_verified':True}],
   'receipt_sha256':receipt_bytes,'archived_model_reused':True,'physical_status':ph['status'],
   'decision':{'state':decision['decision']['state'],'blockers':decision['decision']['blockers']}}
 except Exception:
  write(folder,'failure.json',{'stage':stage,'request_digest':request_pin,'private_traceback':traceback.format_exc(),'files_sha256':files,'timeline':timeline,**ZERO})
  raise

def project(v):
 need(v.get('archived_model_reused')is True and hash_token(v.get('receipt_sha256')),'ARCHIVE_PROJECT_RECEIPT')
 return {'status':'ARCHIVED_MODEL_EVALUATION_COMPLETED','archived_model_reused':True,'archived_evaluation_started':True,
  'archive_report_receipt_sha256':v['receipt_sha256'],'decision':v['decision'],'physical_status':v['physical_status'],**ZERO}

def safe_response(status,obj):
 lifecycle=obj.get('http_lifecycle',{}) if status==200 else obj
 base={'schema':'P19_PRIVATE_ARCHIVE_HTTP_V1','family':'LEFT_RIGHT','scope':'OPERATOR_ONLY_ARCHIVED_MODEL_STUDY','case':CASE_SCOPE,**ZERO}
 if status==200 and obj.get('archived_model_reused')is True:
  return {**base,'status':obj['status'],'archive_report_receipt_sha256':obj['archive_report_receipt_sha256'],
   'archived_evaluation_started':True,'archived_model_reused':True,'physical_status':obj['physical_status'],
   'decision':obj['decision'],'outer_observation':{'state':lifecycle.get('response_state'),'receipt_verified':False,'evidence_usable':False}}
 if status==200:status_code='ARCHIVE_RECEIPT_UNAVAILABLE'
 else:status_code=obj.get('code','ARCHIVE_FAILED_CLOSED')
 return {**base,'status':status_code,'archived_evaluation_started':lifecycle.get('generation_started')is True,'archived_model_reused':False}

def server(run, port=0):
 need(type(port)is int and 0<=port<=65535,'LOOPBACK_PORT')
 boundary=Boundary();worker_lock=threading.Lock();used=False
 class Handler(BaseHTTPRequestHandler):
  protocol_version='HTTP/1.0'
  def setup(self):super().setup();self.connection.settimeout(3)
  def log_message(self,*args):pass
  def respond(self,status,value):
   b=canonical(value);self.send_response(status);self.send_header('Content-Type','application/json')
   self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store')
   self.send_header('X-Content-Type-Options','nosniff');self.end_headers()
   try:self.wfile.write(b)
   except (BrokenPipeError,ConnectionResetError):pass
  def deny(self,status,code):self.respond(status,safe_response(status,{'code':code}))
  def do_POST(self):
   nonlocal used
   siteport=self.server.server_port
   allowed=('127.0.0.1:'+str(siteport),'localhost:'+str(siteport))
   if self.headers.get('Host') not in allowed:return self.deny(403,'LOOPBACK_HOST_REQUIRED')
   if self.path!=ROUTE:return self.deny(404,'NOT_FOUND')
   if self.headers.get('Origin') not in (None,*('http://'+host for host in allowed)):return self.deny(403,'SAME_ORIGIN_REQUIRED')
   lengths=self.headers.get_all('Content-Length',[])
   if self.headers.get('Transfer-Encoding')is not None or len(lengths)!=1 or not lengths[0].isascii()or not lengths[0].isdigit():return self.deny(422,'BODY_LENGTH_REQUIRED')
   if len(lengths[0])>8 or int(lengths[0])>MAX_BODY:return self.deny(409,'UNSUPPORTED_BODY_LIMIT')
   if self.headers.get_content_type()!='application/json':return self.deny(415,'JSON_CONTENT_TYPE_REQUIRED')
   try:body=self.rfile.read(int(lengths[0]))
   except TimeoutError:return self.deny(408,'BODY_READ_TIMEOUT')
   if len(body)!=int(lengths[0]):return self.deny(422,'BODY_INCOMPLETE')
   accepted=time.monotonic()
   try:ready=exact_request(body)
   except InputError as ex:return self.respond(ex.status,{**safe_response(ex.status,{'code':ex.code}),'input_error':input_error_response(ex)})
   except Exception:return self.deny(500,'ARCHIVE_INPUT_FAILED_CLOSED')
   if not ready:return self.deny(409,'UNSUPPORTED_ARCHIVED_CASE')
   if not worker_lock.acquire(blocking=False):return self.deny(409,'ARCHIVE_WORKER_BUSY')
   if used:
    worker_lock.release();return self.deny(409,'ARCHIVE_ONE_SHOT_ALREADY_USED')
   used=True
   status,result=boundary.execute(body,accepted_at=accepted,lock=worker_lock,run=run,project=project)
   safe=safe_response(status,result)
   if status==200 and safe['status']=='ARCHIVE_RECEIPT_UNAVAILABLE':status=500
   return self.respond(status,safe)
 s=ThreadingHTTPServer(('127.0.0.1',port),Handler)
 s.private_boundary=boundary;s.private_worker_lock=worker_lock
 return s

def main():
 ap=argparse.ArgumentParser(description='Private one-shot archived LR loopback evaluation. No solver.')
 ap.add_argument('--archive',required=True,type=Path);ap.add_argument('--archive-sha256',required=True)
 ap.add_argument('--model-sha256',required=True);ap.add_argument('--output',required=True,type=Path)
 a=ap.parse_args()
 apath=checked_path(a.archive);out=checked_path(a.output)
 need(hash_token(a.archive_sha256) and hash_token(a.model_sha256) and not out.exists(),'OPERATOR_PRIVATE_CONFIGURATION')
 s=server(lambda body:evaluate_archive(body,apath,a.archive_sha256,a.model_sha256,out))
 print(json.dumps({'port':s.server_port,'scope':'OPERATOR_ONLY_ARCHIVED_MODEL_STUDY'}),flush=True)
 try:s.serve_forever()
 finally:s.server_close()
if __name__=='__main__':main()
