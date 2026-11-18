"""One real browser submission; always drain owner before server shutdown."""
import json,sys,time,subprocess,urllib.request,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
from guard375 import guard
P=Path(sys.argv[1]);expected=sys.argv[2];HERE=Path(__file__).resolve().parent;guard(expected)
server=subprocess.Popen([sys.executable,'-B',str(HERE/'server375.py'),str(P),expected]);start=time.monotonic();url=None;error=None;posts=[]
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
   page.wait_for_function('window.finalResult !== undefined',timeout=300000)
   result=page.evaluate('window.finalResult');(P/'browser_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));page.screenshot(path=str(P/'terminal.png'),full_page=True)
   if len(posts)!=1:raise ValueError('EXACTLY_ONE_BROWSER_POST_REQUIRED')
   if json.loads(posts[0]['body'])!={'W':'۲۶','L':'۲۸','n':'۲','requested_count':'۲'}:raise ValueError('RAW_PERSIAN_REQUEST_CHANGED')
   if not result.get('test_only')or result.get('request_fulfilled')is not False or result.get('accepted')is not False:raise ValueError('PARTIAL_TEST_SCOPE')
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
   if time.monotonic()-start>340:
    (P/'drain_unresolved.json').write_text(json.dumps(drain,indent=2));raise RuntimeError('OWNER_DRAIN_UNRESOLVED_OUTER_CONTAINMENT_REQUIRED')
   time.sleep(.25)
  (P/'drain_evidence.json').write_text(json.dumps(drain,indent=2))
  server.wait(timeout=10)
  (P/'server_reaped.json').write_text(json.dumps({'returncode':server.returncode,'safe_shutdown_requested':True}))
 guard(expected)
if error:raise RuntimeError(error)
