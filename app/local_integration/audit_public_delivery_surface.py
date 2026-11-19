"""Task5.4 negative current public delivery surface; qualified display/DXF is blocked."""
import hashlib,json,pathlib,sys,threading,urllib.request,urllib.error
from html.parser import HTMLParser
from public_wln_server import server,public_summary
from live_program_scheduler import bind_completed
from run_wln_http_matrix import one,source_compatible
from same_version_front_rear_contract import digest
ROOT=pathlib.Path(__file__).resolve().parents[2]
OLD_UI_BLOB_PINS={"public_wln.html":"74523800b75b4642cd33e01f4ce56ee7dcb3f17f","public_wln.js":"babc068abc3f3be571cc09b4db37351f4462c039","public_wln_server.py":"e92c711e37ef2fec46bf03e76cd1f4b59f61c5be"}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
class Surface(HTMLParser):
 def __init__(self):super().__init__();self.inputs=[];self.render=[];self.download=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input':self.inputs.append(a)
  if tag in ('svg','canvas','img'):self.render.append(tag)
  if 'download' in a:self.download.append(a)
def main(root):
 browser=one(root,'browser-receipt.json');runtime=one(root,'runtime-bundle.json');request=one(root,'request.json')
 child=one(root,'child-complete.json');scheduler=one(root,'scheduler.json');decision=one(root,'decision.json')
 bind_completed(child,request,runtime,decision)
 assert digest(browser['actual_response'])==digest(public_summary(scheduler))
 compatibility=source_compatible(runtime,scheduler)
 for name,h in OLD_UI_BLOB_PINS.items():
  b=(ROOT/'app/local_integration'/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==h
 response=browser['actual_response']
 assert response['decision']['state']=='BLOCKED' and all(response[k] is False for k in AUTH)
 assert response['plan_count_available']==0 and response['plan_payload'] is None and response['download_available'] is False
 assert browser['plan_rendered'] is False and browser['download_available'] is False and browser['public_deployed'] is False
 pins={p:hashlib.sha256((ROOT/'app/local_integration'/p).read_bytes()).hexdigest() for p in ('public_wln_server.py','public_wln.html','public_wln.js','audit_public_delivery_surface.py')}
 process_attempts=[]
 def audit(event,args):
  if event=='subprocess.Popen':process_attempts.append(event);raise RuntimeError('NEGATIVE_DELIVERY_TEST_FORBIDS_NEW_GENERATION_PROCESS')
 sys.addaudithook(audit)
 s=server(0);t=threading.Thread(target=s.serve_forever,daemon=True);t.start();url='http://127.0.0.1:'+str(s.server_address[1])
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}));tests=[]
 try:
  with opener.open(url+'/',timeout=5) as r:html=r.read().decode();assert r.status==200
  parsed=Surface();parsed.feed(html)
  assert [a['name'] for a in parsed.inputs]==['W','L','n'] and not any(a.get('type')=='hidden' for a in parsed.inputs)
  assert parsed.render==[] and parsed.download==[]
  for flag in AUTH:
   body=json.dumps({'W':'18','L':'20','n':2,flag:True}).encode()
   req=urllib.request.Request(url+'/api/public/plan',data=body,headers={'Content-Type':'application/json'},method='POST')
   try:opener.open(req,timeout=5);raise AssertionError('Forged authority request accepted')
   except urllib.error.HTTPError as ex:
    data=json.loads(ex.read());assert ex.code==422 and data['code']=='UNEXPECTED_PUBLIC_FIELD' and data['field']==flag
    assert all(data[k] is False for k in AUTH)
    tests.append({'flag':flag,'actual_http_status':ex.code,'response':data})
 finally:s.shutdown();s.server_close();t.join(timeout=5)
 assert not t.is_alive() and process_attempts==[]
 assert source_compatible(runtime,scheduler)==compatibility
 assert pins=={p:hashlib.sha256((ROOT/'app/local_integration'/p).read_bytes()).hexdigest() for p in pins}
 out={'schema':'TASK5_4_PUBLIC_DELIVERY_NEGATIVE_EVIDENCE_V1','state':'NEGATIVE_NO_DELIVERY_VERIFIED_POSITIVE_DISPLAY_DXF_BLOCKED',
  'actual_http_forged_authority_tests':tests,'actual_current_get_form':{'inputs':['W','L','n'],'renderer_elements':parsed.render,'download_elements':parsed.download},
  'reused_actual_browser_evidence':{'run':44462498782,'artifact':14500313851,'sha256':'fcbfe269bf8189882145b85570625c7f3f40491cc1296d19ecf53c357fbcb02b','receipt_digest':digest(browser),'plan_rendered':False,'download_available':False,'scope':'Existing actual DOM/browser test, not a new browser journey'},
  'positive_test':{'state':'BLOCKED','reasons':['No qualified model in inspected current runtime/history evidence','No active plan rendering or DXF export route implemented in this public_wln_server study surface'],'synthetic_positive_used':False,'dxf_exporter_test_executed':False},
  'old_browser_tested_commit':'d2b063dcce0f5071ea359f4b402850df8e8ef6ca','current_ui_matches_old_tested_commit_blob_pins':OLD_UI_BLOB_PINS,'source_snapshot':pins,'source_compatibility':compatibility,'fresh_geometry_executed':False,'new_solver_calls':0,'new_browser_journey':False,'subprocess_attempts':process_attempts,
  'scope':'Real negative HTTP and current static HTML plus separately reused real browser evidence. Not a successful DXF exporter test and not a statement about unrelated historical/diagnostic exporters.',
  **{k:False for k in AUTH}}
 pathlib.Path('public-delivery-negative.json').write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2));print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main(pathlib.Path(sys.argv[1]))
