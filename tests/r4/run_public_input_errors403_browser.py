"""Real loopback HTTP and browser field-error rendering, no solver or images."""
import sys,pathlib,threading,json,hashlib
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import public_wln_server as P
import request_trace_server109 as T
import request_trace109 as trace
from playwright.sync_api import sync_playwright,expect
FILES=['public_input_errors403.py','public_wln_contract.py','dimension_contract.py','public_wln_server.py','request_trace_server109.py','public_wln.js','public_wln.html','request_trace109.html','request_trace109.js']
def snapshot():return {p:hashlib.sha256((ROOT/'app/local_integration'/p).read_bytes()).hexdigest()for p in FILES}
def main():
 pins=snapshot();rows=[];servers=[]
 with patch.object(P,'run_live',side_effect=AssertionError('NO_SOLVER'))as public_dispatch,patch.object(trace,'make_request',side_effect=AssertionError('NO_SOLVER'))as study_dispatch:
  try:
   for m in (P,T):
    s=m.server(0);t=threading.Thread(target=s.serve_forever,daemon=True);t.start();servers.append((m,s,t))
   with sync_playwright()as pw:
    browser=pw.chromium.launch(headless=True)
    for m,s,t in servers:
     for width,height in [(390,844),(768,1024),(1280,900)]:
      page=browser.new_page(viewport={'width':width,'height':height})
      base='http://127.0.0.1:'+str(s.server_port)
      page.goto(base)
      assert page.locator('form').evaluate('(e)=>e.noValidate') is True
      for vals,want in [(['4.999','25.001','3'],422),(['','',''],422),(['1'*65,'26','3'],409)]:
       for key,value in zip(('W','L','n'),vals):page.locator('#'+key).fill(value)
       with page.expect_response(lambda r:r.url==base+'/api/public/plan'and r.request.method=='POST')as got:
        page.locator('#submit').click()
       response=got.value;data=response.json()
       assert response.status==want and data['schema']=='PUBLIC_WLN_ERROR_SET_V1'
       assert [e['field']for e in data['errors']]==['W','L','n']
       assert response.request.post_data_json==dict(zip(('W','L','n'),vals))
       page.wait_for_function("document.querySelector('#result').dataset.state==='error'||document.querySelector('#result').dataset.state==='invalid'")
       for e in data['errors']:expect(page.locator('#result')).to_contain_text(e['field']+': '+e['code']+' ['+str(e['status'])+']')
       assert page.locator('#submit').is_enabled()
       assert page.locator('svg,canvas,img,[download]').count()==0
       rows.append({'interface':m.__name__,'viewport':[width,height],'status':response.status,'field_error_count':len(data['errors'])})
      # Valid-but-unsupported remains a distinct response, no generation.
      for key,value in zip(('W','L','n'),['5','5','1']):page.locator('#'+key).fill(value)
      with page.expect_response(lambda r:r.url==base+'/api/public/plan'and r.request.method=='POST')as got:page.locator('#submit').click()
      assert got.value.status==409 and got.value.json().get('schema')!='PUBLIC_WLN_ERROR_SET_V1'
      page.wait_for_function("document.querySelector('#submit').disabled===false")
      expect(page.locator('#result')).to_contain_text('ورودی معتبر است')
      rows.append({'interface':m.__name__,'viewport':[width,height],'state':'VALID_UNSUPPORTED'})
      # Synthetic response integrity tests, explicitly not actual HTTP outcomes.
      for badstatus,badprimary in [(200,False),(422,True)]:
       fake={'schema':'PUBLIC_WLN_ERROR_SET_V1','acceptance_contract':'V25_PUBLIC_WLN_CONTRACT_V3',
        'generation_started':False,'primary_status':422,'code':'WRONG'if badprimary else'INVALID_BRIEF','field':'n',
        'errors':[{'code':'INVALID_BRIEF','field':'n','status':422}],**{k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')}}
       page.route('**/api/public/plan',lambda route:route.fulfill(status=badstatus,content_type='application/json',body=json.dumps(fake)))
       page.locator('#submit').click()
       expect(page.locator('#result')).to_contain_text('ممکن است')
       page.wait_for_function("document.querySelector('#submit').disabled===false")
       rows.append({'interface':m.__name__,'viewport':[width,height],'state':'SYNTHETIC_INCONSISTENT_ERROR_RESPONSE_REJECTED'})
       page.unroute('**/api/public/plan')
      page.close()
    version=browser.version;browser.close()
   public_dispatch.assert_not_called();study_dispatch.assert_not_called()
  finally:
   for m,s,t in servers:s.shutdown();s.server_close();t.join(timeout=5);assert not t.is_alive()
 assert snapshot()==pins
 print(json.dumps({'schema':'FIELD_ERROR_BROWSER403_V1','state':'REAL_HTTP_FIELD_ERRORS_AND_UI_VERIFIED',
  'case_count':len(rows),'cases':rows,'browser':version,'source_snapshot':pins,'solver_calls':0,
  'screenshots':False,'pixel_reviewed':False,'accepted':False,'qualified':False,'delivery_allowed':False},sort_keys=True))
if __name__=='__main__':main()
