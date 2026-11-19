"""Real browser HTTP negatives; intercepted positive renderer fixture is not generation."""
import copy,hashlib,importlib.metadata,json,sys,threading
from pathlib import Path
from unittest.mock import patch
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
import request_trace_server109 as servermod
import request_trace109 as contract
paths=[ROOT/'app/local_integration'/n for n in ('request_trace109.html','request_trace109.js','request_trace_server109.py')]
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
before=hashes();s=servermod.server();thread=threading.Thread(target=s.serve_forever,daemon=True);thread.start()
counts={'actual_invalid':0,'actual_unsupported':0,'synthetic_blocked':0,'synthetic_busy':0,'synthetic_500':0,'synthetic_abort':0,'synthetic_forged_authority':0,'synthetic_duplicate_submit_suppressed':0}
try:
 with patch.object(contract,'make_request',side_effect=AssertionError('NO_LIVE_RUNTIME_ALLOWED'))as reserve:
  with sync_playwright()as p:
   browser=p.chromium.launch();chromium_version=browser.version;page=browser.new_page(viewport={'width':390,'height':844})
   url='http://127.0.0.1:'+str(s.server_address[1]);page.goto(url)
   assert page.locator('input').count()==3 and page.locator('input').evaluate_all('(xs)=>xs.map(x=>x.name)')==['W','L','n']
   assert page.locator('input[type=hidden],svg,canvas,img,a[download]').count()==0
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   calls=[]
   page.on('request',lambda r:calls.append(json.loads(r.post_data))if r.url.endswith('/api/public/plan')else None)
   page.locator('#W').fill('25.001');page.locator('#submit').click();expect(page.locator('#result')).to_have_attribute('data-state','invalid');counts['actual_invalid']+=1
   page.locator('#W').fill('18');page.locator('#L').fill('20');page.locator('#submit').click();expect(page.locator('#result')).to_have_attribute('data-state','unsupported');counts['actual_unsupported']+=1
   assert all(set(x)=={'W','L','n'}for x in calls)and len(calls)==2
   reserve.assert_not_called()
   fixture={'schema':'REQUEST_TRACE_HTTP109_V1','status':'BLOCKED','plan_payload':None,'download_available':False,
    **{k:False for k in contract.AUTH},'study_result':{'state':'BLOCKED_NO_SUPPORTED_CAUSE','receipt_verified':True,'source_integrity_verified':True,'evidence_usable':True,**{k:False for k in contract.AUTH}}}
   def intercept(status,body):
    page.unroute('**/api/public/plan');page.route('**/api/public/plan',lambda route:route.fulfill(status=status,content_type='application/json',body=json.dumps(body)))
   intercept(200,fixture);page.locator('#submit').click();expect(page.locator('#result')).to_have_attribute('data-state','blocked');counts['synthetic_blocked']+=1
   page.unroute('**/api/public/plan');held=[];page.route('**/api/public/plan',lambda route:held.append(route))
   before_calls=len(calls);page.locator('#submit').click();expect(page.locator('#submit')).to_be_disabled()
   page.evaluate("document.querySelector('#request').dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))")
   assert len(calls)==before_calls+1 and len(held)==1
   held[0].fulfill(status=200,content_type='application/json',body=json.dumps(fixture));expect(page.locator('#result')).to_have_attribute('data-state','blocked')
   counts['synthetic_duplicate_submit_suppressed']+=1
   intercept(409,{'code':'STUDY_BUSY_NO_QUEUE'});page.locator('#submit').click();expect(page.locator('#result')).to_contain_text('در صف قرار نگرفت');counts['synthetic_busy']+=1
   intercept(500,{'code':'STUDY_FAILED_CLOSED'});page.locator('#submit').click();expect(page.locator('#result')).to_have_attribute('data-state','error');expect(page.locator('#result')).to_contain_text('ممکن است شروع شده باشد');counts['synthetic_500']+=1
   bad=copy.deepcopy(fixture);bad['qualified']=True;intercept(200,bad);page.locator('#submit').click();expect(page.locator('#result')).to_have_attribute('data-state','error');counts['synthetic_forged_authority']+=1
   page.unroute('**/api/public/plan');page.route('**/api/public/plan',lambda route:route.abort());page.locator('#submit').click();expect(page.locator('#result')).to_contain_text('تلاش دوباره خودکار');counts['synthetic_abort']+=1
   expected=len(calls);page.wait_for_timeout(400);assert len(calls)==expected
   assert page.locator('svg,canvas,img,a[download]').count()==0 and not page.locator('#submit').is_disabled()
   page.set_viewport_size({'width':1280,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   reserve.assert_not_called();browser.close()
 assert hashes()==before
 print(json.dumps({'schema':'REQUEST_TRACE_UI109_TEST_V1','counts':counts,'source_hashes':before,'real_browser':True,'playwright_version':importlib.metadata.version('playwright'),'chromium_version':chromium_version,'viewports':[[390,844],[1280,900]],'fresh_solver_attempts':0,'actual_positive_browser_parent':False,'synthetic_positive_scope':'UI_RENDERING_ONLY','screenshots_created':False,'visual_pixel_review':False,'authorities':False,'artifact_upload':False},sort_keys=True))
finally:s.shutdown();s.server_close();thread.join()
