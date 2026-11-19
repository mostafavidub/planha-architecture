"""Navigation QA: real Chromium/HTTP and controlled nongeometry subprocess.
No solver, model, runtime receipt, cancel, recovery or pixel-quality claim.
"""
import hashlib,json,subprocess,sys,threading,time,platform,importlib.metadata
from pathlib import Path
from unittest.mock import patch
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import public_wln_server as m
PATHS=[ROOT/'app/local_integration'/n for n in ('public_wln_server.py','public_wln.html','public_wln.js','public_input_errors403.py','public_wln_contract.py','live_program_scheduler.py')]
def pins():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PATHS}
def until(predicate):
 end=time.monotonic()+10
 while not predicate():
  if time.monotonic()>=end:raise AssertionError('CONTROLLED_WAIT_EXPIRED')
  time.sleep(.01)
def main():
 before=pins();rows=[]
 with sync_playwright() as p:
  browser=p.chromium.launch();browser_version=browser.version
  try:
   for width,height in [(390,844),(768,1024),(1280,900)]:
    for mode in ('reload','back_forward_then_reload'):
     entered=threading.Event();release=threading.Event();finished=threading.Event()
     calls=[];processes=[];errors=[]
     def worker(body):
      calls.append(body)
      child=subprocess.Popen([sys.executable,'-c','import sys; sys.stdin.readline()'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
      processes.append(child);entered.set()
      try:
       if not release.wait(60):raise AssertionError('CONTROLLED_RELEASE_MISSING')
       child.communicate('finish\n',timeout=5)
       assert child.returncode==0
       return {'preflight':{'input_valid':True},'state':'CONTROLLED_COMPLETED','attempts':[{'state':'CONTROLLED_NOT_GEOMETRY'}],
        'fresh_model_executed':False,'source_integrity_verified':True,'current_decision':{'state':'BLOCKED','blockers':['CONTROLLED_NOT_GEOMETRY']}}
      finally:
       if child.poll() is None:child.kill();child.wait()
       finished.set()
     server=m.server();server.handle_error=lambda *args:errors.append('HANDLER_EXCEPTION')
     thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
     page=browser.new_page(viewport={'width':width,'height':height})
     page.set_default_timeout(5000);page.set_default_navigation_timeout(10000)
     page.add_init_script("window.__pageshowPersisted=null;addEventListener('pageshow',e=>window.__pageshowPersisted=e.persisted)")
     posts=[];page.on('request',lambda r:posts.append(r.post_data) if r.method=='POST' else None)
     url='http://127.0.0.1:'+str(server.server_address[1])
     try:
      with patch.object(m,'run_live',side_effect=worker):
       page.goto(url);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
       page.locator('#submit').click();until(entered.is_set)
       expect(page.locator('#submit')).to_be_disabled()
       page.evaluate("document.querySelector('#plan-form').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))")
       page.wait_for_timeout(100);assert len(posts)==1 and len(calls)==1 and m.LOCK.locked()
       history=[]
       if mode=='back_forward_then_reload':
        page.goto(url+'/health')
        for navigate in (page.go_back,page.go_forward,page.go_back):
         navigate();assert len(posts)==1 and len(calls)==1 and m.LOCK.locked()
         history.append(page.evaluate("({url:location.pathname,persisted:window.__pageshowPersisted,type:performance.getEntriesByType('navigation')[0]?.type||null,state:document.querySelector('#result')?.dataset.state||null})"))
        assert page.locator('svg,canvas,img,a[download]').count()==0
        assert 'بررسی اجرا شد' not in page.locator('#result').inner_text()
       page.reload()
       expect(page.locator('#result')).to_contain_text('هنوز بررسی انجام نشده')
       assert len(posts)==1 and len(calls)==1 and m.LOCK.locked()
       page.locator('#submit').click()
       expect(page.locator('#result')).to_contain_text('در صف قرار نگرفت')
       assert len(posts)==2 and len(calls)==1
       text=page.locator('#result').inner_text()
       release.set();until(finished.is_set);until(lambda:not m.LOCK.locked())
       page.wait_for_timeout(200)
       assert page.locator('#result').inner_text()==text
       assert len(posts)==2 and len(calls)==1 and all(x.poll()==0 for x in processes)
       with page.expect_response(lambda r:r.url.endswith('/api/public/plan')) as response:
        page.locator('#submit').click()
       assert response.value.status==200 and response.value.json()['decision']['state']=='NO_VERIFIED_DECISION'
       expect(page.locator('#result')).to_have_attribute('data-state','blocked')
       until(lambda:not m.LOCK.locked())
       assert len(posts)==3 and len(calls)==2 and len(processes)==2
       assert all(x.poll()==0 for x in processes) and errors==[]
       assert page.locator('svg,canvas,img,a[download]').count()==0
       assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
       rows.append({'viewport':[width,height],'navigation':mode,'intermediate_history_observations':history,'post_count':len(posts),'worker_count':len(calls),
        'no_automatic_resubmit':True,'late_result_not_rendered_in_new_document':True,'lock_released_after_worker':True,
        'explicit_second_request_completed':True,'all_processes_waited':True,'handler_exception_count':len(errors)})
     finally:
      release.set();page.close();server.shutdown();server.server_close();thread.join(timeout=5)
      for child in processes:
       if child.poll() is None:child.kill();child.wait()
     assert not m.LOCK.locked()
  finally:browser.close()
 assert pins()==before
 print(json.dumps({'schema':'PUBLIC_NAVIGATION310_CONTROLLED_V1','rows':rows,'source_hashes':before,
  'actual_http_browser':True,'chromium_version':browser_version,'playwright_version':importlib.metadata.version('playwright'),'python_version':platform.python_version(),'os_release':platform.freedesktop_os_release(),'worker':'CONTROLLED_SUBPROCESS_NOT_GEOMETRY','solver_count':0,
  'production_geometry':False,'cancel_verified':False,'persistence_recovery_verified':False,
  'screenshots_created':False,'pixel_review':'NOT_VERIFIED','artifact_upload':False,
  'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False},sort_keys=True))
if __name__=='__main__':main()
