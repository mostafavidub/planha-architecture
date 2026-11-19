"""Loopback-only three-field public-contract study UI. Not published production."""
import argparse,json,threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from public_wln_contract import verify_public
from public_input_errors403 import parse_public_errors as parse_public, response as input_error_response
from dimension_contract import InputError,MAX_BODY
from automatic_program_search import run_live
from live_program_scheduler import preflight
LOCK=threading.Lock()
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def public_summary(result):
 # Never expose world model, routes, SVG, artifacts or internal local file paths.
 pf=result['preflight'];rows=result.get('attempts',[])
 decision=result.get('current_decision')
 return {'schema':'PUBLIC_WLN_STUDY_SUMMARY_V1','mode':'LOCAL_SCOPED_STUDY_NOT_PRODUCT',
  'status':result['state'],'input_valid':pf['input_valid'],'case_scope':'18x20/n2 only; other valid cases currently unsupported',
  'programme_source':'Automatic approved registry programme2 for the selected study case; not quality-optimal selection',
  'actual_live_attempts':len(rows),'fresh_model_executed':result.get('fresh_model_executed',False),
  'source_integrity_verified':result.get('source_integrity_verified',False),
  'attempt_states':[r['state'] for r in rows],
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
  try:
   envelope=parse_public(body);verify_public(body,envelope);pf=preflight(body)
  except InputError as ex:self.reply(ex.status,input_error_response(ex));return
  except Exception:self.reply(500,{'code':'INPUT_VALIDATION_FAILED_CLOSED','generation_started':False,**{k:False for k in AUTH}});return
  if not pf['execution_ready']:
   self.reply(409,public_summary({'preflight':pf,'state':pf['state']}));return
  if not LOCK.acquire(blocking=False):self.reply(409,{'code':'STUDY_BUSY_NO_QUEUE','retry_automatic':False,**{k:False for k in AUTH}});return
  try:self.reply(200,public_summary(run_live(body)))
  except Exception as ex:self.reply(500,{'code':'STUDY_FAILED_CLOSED','error_type':type(ex).__name__,'plan_count_available':0,**{k:False for k in AUTH}})
  finally:LOCK.release()
def server(port=0):return ThreadingHTTPServer(('127.0.0.1',port),Handler)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=0);args=p.parse_args();s=server(args.port)
 print('http://127.0.0.1:'+str(s.server_address[1]),flush=True)
 try:s.serve_forever()
 finally:s.server_close()
