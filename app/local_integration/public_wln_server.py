"""Loopback-only three-field public-contract study UI. Not published production."""
import argparse,json,threading,time,hashlib
import stop_observation_p01 as stop
import programme_prefilter_p05 as capacity
from http_withholding_x04 import Boundary
from public_program_dispatch_p17 import run_bound
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from public_wln_contract import verify_public
from public_input_errors403 import parse_public_errors as parse_public, response as input_error_response
from dimension_contract import InputError,MAX_BODY
from automatic_program_search import run_live
from public_program_dispatch_p17 import preflight
LOCK=threading.Lock()
HTTP_BOUNDARY=Boundary()
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def public_summary(result,body=None):
 # Never expose world model, routes, SVG, artifacts or internal local file paths.
 pf=result['preflight'];rows=result.get('attempts',[])
 decision=result.get('current_decision')
 return {'schema':'PUBLIC_WLN_STUDY_SUMMARY_V1','mode':'LOCAL_SCOPED_STUDY_NOT_PRODUCT',
  'stop_record':stop.safe(result.get('stop_record'),hashlib.sha256(body).hexdigest())if type(body)is bytes else None,
  'status':result['state'],'input_valid':pf['input_valid'],'case_scope':pf.get('case_scope','FRONT_REAR/P2 study: 18x20, 18.1x22.2, 25x25 (n2); 18x20 only (n1)'),
  'programme_source':'Automatic approved registry programme2 for the selected study case; not quality-optimal selection',
  'actual_live_attempts':len(rows),'fresh_model_executed':result.get('fresh_model_executed',False),
  'source_integrity_verified':result.get('source_integrity_verified',False),
  'attempt_states':[r['state'] for r in rows],
  'single_unit_evidence':rows if result.get('schema')=='SINGLE_HTTP_RESULT_P17_V1' else None,
  'full_evidence_binding':result.get('http_full_evidence',{'state':'NOT_EVALUATED','binding_verified':False}),
  'decision':decision if decision is not None else {'state':'NO_VERIFIED_DECISION','blockers':['NO_VERIFIED_COMPLETE_EVIDENCE']},
  'remaining':['Variable-dimension automatic programme search incomplete','One-bedroom adapter not ready','Current functional quality/profile checks unresolved'],
  'plan_count_available':0,'plan_payload':None,'download_available':False,
  **{k:False for k in AUTH}}
class Handler(BaseHTTPRequestHandler):
 protocol_version='HTTP/1.0'
 def setup(self):
  super().setup();self.connection.settimeout(3)
 def log_message(self,*args):pass
 def host_ok(self):
  port=self.server.server_address[1]
  return self.headers.get('Host') in ('127.0.0.1:'+str(port),'localhost:'+str(port))
 def reply(self,status,value):
  data=json.dumps(value,ensure_ascii=False,allow_nan=False).encode()
  self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers()
  try:self.wfile.write(data)
  except (BrokenPipeError,ConnectionResetError):pass
 def do_GET(self):
  if not self.host_ok():self.reply(403,{'code':'LOOPBACK_HOST_REQUIRED'});return
  assets={'/':('public_wln.html','text/html; charset=utf-8'),'/public_wln.js':('public_wln.js','text/javascript; charset=utf-8')}
  if self.path=='/health':self.reply(200,{'mode':'LOCAL_SCOPED_STUDY_NOT_PRODUCT','public_fields':['W','L','n'],**{k:False for k in AUTH}});return
  if self.path not in assets:self.reply(404,{'code':'NOT_FOUND'});return
  name,kind=assets[self.path];data=Path(__file__).with_name(name).read_bytes()
  self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
  self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
  self.end_headers();self.wfile.write(data)
 def do_POST(self):
  if not self.host_ok():self.reply(403,{'code':'LOOPBACK_HOST_REQUIRED'});return
  if self.path!='/api/public/plan':self.reply(404,{'code':'NOT_FOUND'});return
  origin=self.headers.get('Origin');allowed={'http://127.0.0.1:'+str(self.server.server_address[1]),'http://localhost:'+str(self.server.server_address[1])}
  if origin is not None and origin not in allowed:self.reply(403,{'code':'SAME_ORIGIN_REQUIRED'});return
  lengths=self.headers.get_all('Content-Length',[])
  if self.headers.get('Transfer-Encoding') is not None or len(lengths)!=1 or not lengths[0].isascii() or not lengths[0].isdigit():self.reply(422,{'code':'BODY_LENGTH_REQUIRED'});return
  if self.headers.get_content_type()!='application/json':self.reply(415,{'code':'JSON_CONTENT_TYPE_REQUIRED'});return
  if len(lengths[0])>8 or int(lengths[0])>MAX_BODY:self.reply(409,{'code':'UNSUPPORTED_BODY_LIMIT'});return
  try:body=self.rfile.read(int(lengths[0]))
  except TimeoutError:self.reply(408,{'code':'BODY_READ_TIMEOUT'});return
  if len(body)!=int(lengths[0]):self.reply(422,{'code':'BODY_INCOMPLETE'});return
  accepted_at=time.monotonic() # Complete body received; before input preflight/source checks.
  try:
   envelope=parse_public(body);verify_public(body,envelope);pf=preflight(body)
  except InputError as ex:self.reply(ex.status,input_error_response(ex));return
  except Exception:self.reply(500,{'code':'INPUT_VALIDATION_FAILED_CLOSED','generation_started':False,**{k:False for k in AUTH}});return
  observation=None
  observes_capacity=envelope['canonical_request']['unit_count']==2
  def capture():
   nonlocal observation
   if observes_capacity:
    try:observation=capacity.capture_http(body,envelope)
    except Exception:pass # Observation failure is not an execution failure.
  def with_capacity(summary):
   if not observes_capacity:return summary
   try:return capacity.attach_http(summary,body,observation,envelope['canonical_request_digest'])
   except Exception:return summary # Advisory projection cannot replace the existing response.
  def project(result):
   summary=public_summary(result,body)
   # Dispatch already settled. Omit optional measurement when close to X04 cutoff.
   if not observes_capacity or time.monotonic()>=accepted_at+179:return summary
   capture()
   return with_capacity(summary)
  if not pf['execution_ready']:
   capture()
   summary=public_summary({'preflight':pf,'state':pf['state'],'stop_record':stop.unsupported(body)},body)
   self.reply(409,with_capacity(summary));return
  if not LOCK.acquire(blocking=False):self.reply(409,{'code':'STUDY_BUSY_NO_QUEUE','retry_automatic':False,**{k:False for k in AUTH}});return
  status,value=HTTP_BOUNDARY.execute(body,accepted_at=accepted_at,lock=LOCK,run=lambda b:run_bound(b,run_live,deadline=accepted_at+180),project=project)
  self.reply(status,value)
def server(port=0):return ThreadingHTTPServer(('127.0.0.1',port),Handler)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=0);args=p.parse_args();s=server(args.port)
 print('http://127.0.0.1:'+str(s.server_address[1]),flush=True)
 try:s.serve_forever()
 finally:s.server_close()
