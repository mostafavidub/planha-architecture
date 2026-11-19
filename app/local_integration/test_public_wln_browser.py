"""GitHub Actions browser test: actual live backend, no mocked generation."""
import json,subprocess,sys,pathlib,time,importlib.metadata
from playwright.sync_api import sync_playwright,expect
ROOT=pathlib.Path(__file__).resolve().parents[2]
def main():
 proc=subprocess.Popen([sys.executable,'-B',str(pathlib.Path(__file__).with_name('public_wln_server.py')),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,cwd=ROOT)
 evidence=ROOT/'public-ui-evidence';evidence.mkdir(exist_ok=False)
 try:
  url=proc.stdout.readline().strip();assert url.startswith('http://127.0.0.1:')
  with sync_playwright() as p:
   browser=p.chromium.launch();page=browser.new_page(viewport={'width':1280,'height':900})
   page.goto(url);assert page.locator('input').count()==3
   assert page.locator('input').evaluate_all('(xs)=>xs.map(x=>x.name)')==['W','L','n']
   assert page.locator('input[type=hidden]').count()==0
   page.screenshot(path=str(evidence/'desktop-empty.png'),full_page=True)
   page.set_viewport_size({'width':390,'height':844})
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   page.screenshot(path=str(evidence/'mobile-empty.png'),full_page=True)
   page.locator('#W').fill('26');page.locator('#submit').click()
   expect(page.locator('#result')).to_have_attribute('data-state','error')
   page.locator('#W').fill('20');page.locator('#submit').click()
   expect(page.locator('#result')).to_contain_text('ورودی معتبر است')
   requests=[]
   def on_request(r):
    if r.url.endswith('/api/public/plan'):requests.append(json.loads(r.post_data))
   page.on('request',on_request)
   page.locator('#W').fill('18')
   started=time.monotonic()
   with page.expect_response(lambda r:r.url.endswith('/api/public/plan'),timeout=240000) as info:
    page.locator('#submit').click()
    assert page.locator('#submit').is_disabled()
    assert page.locator('#W').is_disabled()
   response=info.value;data=response.json()
   expect(page.locator('#result')).to_have_attribute('data-state','blocked')
   assert response.status==200 and data['source_integrity_verified'] is True
   assert data['fresh_model_executed'] is True and data['decision']['state']=='BLOCKED'
   assert len(requests)==1 and set(requests[0])=={'W','L','n'}
   assert all(data[k] is False for k in ('accepted','qualified','display_allowed','delivery_allowed'))
   assert data['plan_count_available']==0 and data['plan_payload'] is None and data['download_available'] is False
   assert page.locator('svg,canvas,img,a[download]').count()==0
   page.screenshot(path=str(evidence/'mobile-blocked-result.png'),full_page=True)
   assert not page.locator('#submit').is_disabled()
   page.route('**/api/public/plan',lambda route:route.fulfill(status=500,content_type='application/json',body='{"code":"STUDY_FAILED_CLOSED"}'))
   page.locator('#submit').click()
   expect(page.locator('#result')).to_contain_text('ممکن است شروع شده باشد')
   page.unroute('**/api/public/plan')
   page.route('**/api/public/plan',lambda route:route.abort())
   page.locator('#submit').click()
   expect(page.locator('#result')).to_have_attribute('data-state','error')
   assert 'تلاش دوباره خودکار' in page.locator('#result').inner_text()
   assert not page.locator('#submit').is_disabled()
   receipt={'schema':'PUBLIC_THREE_FIELD_BROWSER_EVIDENCE_V1','actual_request':requests[0],'actual_response':data,'live_start_through_network_abort_ui_journey_seconds':time.monotonic()-started,'playwright_version':importlib.metadata.version('playwright'),'screenshots_captured_not_human_visual_review':True,
    'viewports':[[1280,900],[390,844]],'horizontal_overflow_mobile':False,'http_invalid_and_unsupported_before_live':True,
    'one_live_request_only':True,'network_abort_after_live_was_intercepted_no_server_execution':True,'synthetic_http500_intercept_preserves_execution_uncertainty':True,
    'diagnostic_api_unchanged':True,'public_deployed':False,'plan_rendered':False,'download_available':False}
   (evidence/'browser-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2));print(json.dumps(receipt,ensure_ascii=False,sort_keys=True))
   browser.close()
 finally:
  proc.terminate()
  try:proc.wait(timeout=10)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
if __name__=='__main__':main()
