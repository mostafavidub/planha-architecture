"""One real browser submission; always drain owner before server shutdown."""
import json,sys,time,subprocess,urllib.request,traceback,hashlib,socket,errno,psutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from guard390 import guard
P=Path(sys.argv[1]);expected=sys.argv[2];HERE=Path(__file__).resolve().parent;guard(expected)
server=subprocess.Popen([sys.executable,'-B',str(HERE/'server390.py'),str(P),expected]);start=time.monotonic();url=None;error=None;posts=[]
def api(path,data=None):
 req=urllib.request.Request(url+path,data=data,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=5)as r:return json.load(r)
try:
 while not(P/'server_address.json').exists():
  if server.poll()is not None or time.monotonic()-start>20:raise ValueError('SERVER_NOT_READY')
  time.sleep(.1)
 address=json.loads((P/'server_address.json').read_text());url=address['url']
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  try:
   page=browser.new_page(viewport={'width':1200,'height':1000})
   def request(req):
    if req.method=='POST'and req.url==url+'/api/runs':posts.append({'url':req.url,'method':req.method,'body':req.post_data})
   page.on('request',request);page.goto(url,wait_until='networkidle')
   for k,v in {'W':'۲۶','L':'۲۸','n':'۲','requested_count':'۲'}.items():page.locator('input[name="'+k+'"]').fill(v)
   page.screenshot(path=str(P/'before_form.png'),full_page=True);page.locator('#submit').click()
   page.wait_for_function('window.finalResult !== undefined',timeout=600000)
   result=page.evaluate('window.finalResult');(P/'browser_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));page.screenshot(path=str(P/'terminal.png'),full_page=True)
   if len(posts)!=1:raise ValueError('EXACTLY_ONE_BROWSER_POST_REQUIRED')
   if json.loads(posts[0]['body'])!={'W':'۲۶','L':'۲۸','n':'۲','requested_count':'۲'}:raise ValueError('RAW_PERSIAN_REQUEST_CHANGED')
   if result.get('test_only')is not False or result.get('experimental')is not True or result.get('accepted')is not False or result.get('semantic_state')not in('UNKNOWN_CURRENT_DEPENDENCIES','PASS_SCOPED_CURRENT_SET'):raise ValueError('PARTIAL_EXPERIMENTAL_SCOPE')
   if result.get('request_fulfilled')is not result.get('qualified_selected_set'):raise ValueError('FULFILLMENT_QUALIFICATION_BINDING')
   if result.get('transport_run_id')!=page.evaluate('window.transportRunId'):raise ValueError('BROWSER_TRANSPORT_RUN_BINDING')
   binding=result.get('binding',{})
   if binding.get('run_id')!=result['transport_run_id']or binding.get('transport_body_sha256')!=hashlib.sha256(posts[0]['body'].encode()).hexdigest():raise ValueError('BROWSER_BODY_RESULT_BINDING')
   from contract390 import validate_member_folder
   runfolder=P/'runs'/result['transport_run_id'];audits={}
   for kind in ('balanced','joint'):
    audits[kind]=validate_member_folder(runfolder/kind,expected,require_physical_pass=False)['binding']
    member=next(m for m in result['members']if m['kind']==kind)
    if member['binding']!=audits[kind]:raise ValueError('BROWSER_MEMBER_BINDING_CHANGED:'+kind)
   (P/'browser_binding_audit.json').write_text(json.dumps({'verified':True,'members':audits,'post_count':len(posts)},indent=2))
  finally:browser.close()
except BaseException as e:
 error=type(e).__name__+':'+str(e);(P/'browser_error.txt').write_text(traceback.format_exc())
finally:
 (P/'browser_posts.json').write_text(json.dumps(posts,ensure_ascii=False,indent=2))
 # No terminate()/kill() on the server. Its owner must finish supervised work.
 if url:
  drain=[]
  while True:
   try:
    state=api('/health');drain.append({'seconds':time.monotonic()-start,**state})
    if not state['active']and not state['unsafe_cleanup']:
     shutdown=api('/shutdown',b'{}');(P/'shutdown_response.json').write_text(json.dumps(shutdown));break
   except Exception as e:drain.append({'seconds':time.monotonic()-start,'error':str(e)})
   if time.monotonic()-start>640:
    (P/'drain_unresolved.json').write_text(json.dumps(drain,indent=2));raise RuntimeError('OWNER_DRAIN_UNRESOLVED_OUTER_CONTAINMENT_REQUIRED')
   time.sleep(.25)
  (P/'drain_evidence.json').write_text(json.dumps(drain,indent=2))
  server.wait(timeout=10)
  (P/'server_reaped.json').write_text(json.dumps({'returncode':server.returncode,'safe_shutdown_requested':True}))
  try:
   connection=socket.create_connection(('127.0.0.1',int(url.rsplit(':',1)[1])),timeout=2);connection.close();raise ValueError('LISTENER_STILL_OPEN')
  except OSError as e:
   if e.errno!=errno.ECONNREFUSED:raise
   (P/'listener_closed.json').write_text(json.dumps({'verified':True,'errno':e.errno,'url':url}))
  alive=False
  try:alive=abs(psutil.Process(address['pid']).create_time()-address['create_time'])<.01
  except psutil.NoSuchProcess:pass
  (P/'server_identity_audit.json').write_text(json.dumps({'pid':address['pid'],'create_time':address['create_time'],'original_process_gone':not alive}))
  if alive:raise ValueError('SERVER_IDENTITY_STILL_ALIVE')
 guard(expected)
if error:raise RuntimeError(error)
