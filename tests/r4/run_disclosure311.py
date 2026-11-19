"""Study disclosure only; intercepted counters are not runtime lifecycle evidence."""
import copy,hashlib,json,sys,threading
from pathlib import Path
from unittest.mock import patch
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'app/local_integration'))
import public_wln_server as m
def handler(payload):
 return lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(payload))
def main():
 paths=[ROOT/'app/local_integration'/n for n in ('public_wln.html','public_wln.js','public_wln_server.py')]
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 server=m.server();thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 rows=[]
 try:
  with patch.object(m,'run_live',side_effect=AssertionError('NO_GENERATION')) as dispatch:
   with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844})
    page.goto('http://127.0.0.1:'+str(server.server_address[1]))
    disclosure=page.locator('#stage-disclosure')
    for text in ('مفهومی','تأیید قانونی','پله و آسانسور','تا ۶','جایگزینی اصلاحی','NOT_REPORTED'):
     expect(disclosure).to_contain_text(text)
    assert page.locator('#stage-counts').inner_text().count('NOT_REPORTED')==8
    fixtures=[('zero',0,False),('duplicate',2,True),('repair_replacement',2,True),('partial',1,False),('invalid_bool',True,True)]
    for name,attempts,fresh in fixtures:
     data={'schema':'PUBLIC_WLN_STUDY_SUMMARY_V1','status':'BLOCKED','actual_live_attempts':attempts,
      'fresh_model_executed':fresh,'plan_count_available':0,'plan_payload':None,'download_available':False,
      'source_integrity_verified':True,'decision':{'state':'BLOCKED'},
      **{k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')},
      'candidate_count':6,'constructed_count':6,'qualified_count':6,'downloaded_count':6}
     page.route('**/api/public/plan',handler(data))
     page.locator('#submit').click();expect(page.locator('#result')).to_have_attribute('data-state','blocked')
     counts=page.locator('#stage-counts').inner_text()
     assert counts.count('NOT_REPORTED')==(7 if type(attempts) is bool else 6)
     assert 'پلان قابل ارائه در این پاسخ: 0' in counts
     assert all(label+': NOT_REPORTED' in counts for label in ('نامزد','ساخته‌شده','بررسی‌شده','واجد شرایط','نمایش‌داده‌شده','دانلودشده'))
     assert 'تلاش‌های گزارش‌شده در این پاسخ: '+('NOT_REPORTED' if type(attempts)is bool else str(attempts)) in counts
     assert page.locator('svg,canvas,img,a[download]').count()==0
     rows.append({'fixture':name,'stage_counters':'NOT_REPORTED','scope':'SYNTHETIC_UI_TRANSPORT_ONLY'})
     page.unroute('**/api/public/plan')
    page.locator('#W').fill('25.001');page.locator('#submit').click()
    expect(page.locator('#result')).to_have_attribute('data-state','error')
    assert page.locator('#stage-counts').inner_text().count('NOT_REPORTED')==8
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    dispatch.assert_not_called();browser.close()
  assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}==before
  print(json.dumps({'schema':'DISCLOSURE311_UI_ONLY_V1','fixtures':rows,'real_http_invalid':1,'source_hashes':before,
   'solver_count':0,'lifecycle_count_binding':False,'pixel_review':'NOT_VERIFIED','artifact_upload':False,
   'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False},sort_keys=True))
 finally:server.shutdown();server.server_close();thread.join()
if __name__=='__main__':main()
