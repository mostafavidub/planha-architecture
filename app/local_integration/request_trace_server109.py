"""Separate loopback study endpoint; original public runtime is unchanged."""
import json,threading
from http.server import ThreadingHTTPServer
from public_wln_server import Handler as BaseHandler
from public_wln_contract import parse_public,verify_public
from dimension_contract import InputError,MAX_BODY
from request_trace109 import run,preflight,AUTH
LOCK=threading.Lock()
def projection(r):
 # r is an explicit safe result schema, not a model/report dump.
 if 'preflight'in r:
  return {'schema':'REQUEST_TRACE_HTTP109_V1','status':r['state'],'state':r['state'],'attempt_count':0,'trace':[],'plan_payload':None,'download_available':False,**{k:False for k in AUTH}}
 return {'schema':'REQUEST_TRACE_HTTP109_V1','status':'BLOCKED','study_result':r,'plan_payload':None,'download_available':False,**{k:False for k in AUTH}}
class Handler(BaseHandler):
 def do_GET(self):
  if not self.host_ok():self.reply(403,{'code':'LOOPBACK_HOST_REQUIRED'});return
  if self.path=='/health':self.reply(200,{'schema':'REQUEST_TRACE_HEALTH109_V1','mode':'SEPARATE18x22_STUDY','public_fields':['W','L','n'],**{k:False for k in AUTH}});return
  self.reply(404,{'code':'NOT_FOUND_NO_PRODUCT_UI'})
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
  except InputError as ex:self.reply(ex.status,{'schema':'PUBLIC_WLN_INPUT_ERROR_V1','code':ex.code,'field':ex.field,**{k:False for k in AUTH}});return
  if not pf['execution_ready']:
   self.reply(409,projection(run(body)));return
  if not LOCK.acquire(blocking=False):self.reply(409,{'code':'STUDY_BUSY_NO_QUEUE','retry_automatic':False,**{k:False for k in AUTH}});return
  try:self.reply(200,projection(run(body)))
  except Exception as ex:self.reply(500,{'code':'STUDY_FAILED_CLOSED','error_type':type(ex).__name__,'plan_count_available':0,**{k:False for k in AUTH}})
  finally:LOCK.release()
def server(port=0):return ThreadingHTTPServer(('127.0.0.1',port),Handler)
