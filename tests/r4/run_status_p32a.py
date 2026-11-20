"""P32-A synthetic status transport, not geometry/producer authenticity/P25.
Real public parser/preflight/server/X04/projection + Chromium. Only run_bound is
a controlled nongeometry writer. Wire-corruption tests explicitly intercept HTTP.
No private model/report, solver, screenshot upload or positive admission fixture.
"""
import copy,hashlib,json,sys,threading,time,platform
from pathlib import Path
from unittest.mock import patch
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import public_wln_server as m
import http_withholding_x04 as boundary
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
CRITERIA=('CONTINUOUS_USEFUL_LIVING','CURRENT_PROGRAM_SUITABILITY','KITCHEN_GUEST_PATH_SEPARATION','NONFUNCTIONAL_WALL_EXCLUSION')
def h(text):return hashlib.sha256(text.encode()).hexdigest()
def fixture(body,mode,serial):
 """Invented hashes/receipts in a controlled writer, never real evaluation."""
 pf=m.preflight(body);single=json.loads(body)['n']=='1'
 model=h('SYNTHETIC_MODEL_'+str(serial));runtime=h('SYNTHETIC_RUNTIME_'+str(serial))
 states={k:'UNKNOWN' for k in CRITERIA};physical='FAIL'
 blockers=['PHYSICAL_FAIL','CURRENT_UNKNOWN','P25_DELIVERY_NOT_IMPLEMENTED']
 if mode=='quality':
  physical='PASS_CONCEPT_SCOPED_REVIEW';blockers.remove('PHYSICAL_FAIL')
 if mode=='rejected':
  states={k:'PASS' for k in CRITERIA};blockers.remove('CURRENT_UNKNOWN')
 if mode in ('necessary','not_evaluated'):
  physical='PASS_CONCEPT_SCOPED_REVIEW';blockers.remove('PHYSICAL_FAIL');blockers.remove('CURRENT_UNKNOWN')
  states={k:('FAIL' if mode=='necessary' else 'NOT_EVALUATED') for k in CRITERIA}
  blockers.append('CURRENT_NECESSARY_FAIL' if mode=='necessary' else 'CURRENT_NOT_EVALUATED')
 if mode=='evaluator':blockers.append('EVALUATOR_ERROR')
 row={'state':'FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED','receipt_verified':True,
  'nonce':h('SYNTHETIC_NONCE_'+str(serial))[:32],'model_digest':model,'observed_model_digest':model,
  'runtime_digest':runtime,'timed_out':False,'wait_completed':True,'returncode':0,
  'physical_status':physical,'physical_errors':1 if physical=='FAIL' else 0,'physical_pending':0,
  'current_states':states,'observed_file_hashes':{'model':model,'summary':runtime,'decision':h('SYNTHETIC_DECISION')}}
 binding={'schema':'SINGLE_READBACK_P17_V1','binding_verified':True,'raw_archive_durable':False}
 if not single:
  binding={'schema':'HTTP_FULL_EVIDENCE_X07_V1','state':'SAME_REQUEST_FULL_REPORT_CONSISTENCY_VERIFIED_SCOPED',
   'request_digest':hashlib.sha256(body).hexdigest(),'binding_verified':True,'file_count':9,
   **{k:h('SYNTHETIC_'+k+str(serial)) for k in ('nonce_digest','model_digest','decision_digest','source_digest','file_hashes_digest')}}
 if mode=='receipt_false':row['receipt_verified']=False
 if mode=='binding_false':binding['binding_verified']=False
 out={'schema':'SINGLE_HTTP_RESULT_P17_V1' if single else 'CONTROLLED_PAIR_RESULT',
  'preflight':pf,'state':'BLOCKED','attempts':[row],'fresh_model_executed':True,
  'source_integrity_verified':mode!='source_false','http_full_evidence':binding,
  'current_decision':{'state':'BLOCKED','blockers':blockers,**{k:False for k in AUTH}}}
 return out
def until(fn):
 end=time.monotonic()+8
 while not fn():
  if time.monotonic()>end:raise AssertionError('CONTROLLED_WAIT')
  time.sleep(.01)
def main():
 paths=[ROOT/'app/local_integration'/n for n in ('public_wln.js','public_wln.html','public_wln_server.py','public_program_dispatch_p17.py','http_withholding_x04.py','http_evidence_x07.py','single_runtime_p17.py')]
 pins={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 rows=[];calls=[];mode={'value':'mixed'};entered=threading.Event();release=threading.Event()
 def controlled(body,runtime,*,deadline):
  calls.append({'n':json.loads(body)['n'],'mode':mode['value']});which=mode['value']
  if which in ('hold','timeout'):
   entered.set()
   if not release.wait(8):raise AssertionError('TEST_RELEASE')
  if which=='exception':raise ValueError('SYNTHETIC_EVALUATION_ERROR')
  return fixture(body,'mixed' if which in ('hold','timeout') else which,len(calls))
 server=m.server();errors=[];server.handle_error=lambda *args:errors.append('HANDLER_ERROR')
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 url='http://127.0.0.1:'+str(server.server_port)
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch();version=browser.version
   try:
    # Browser driver starts before the global subprocess sentinel.
    with patch.object(m,'run_bound',side_effect=controlled),patch('subprocess.Popen',side_effect=AssertionError('NO_PROCESS_OR_SOLVER')) as spawn:
     for width,height in ((390,844),(1280,900)):
      page=browser.new_page(viewport={'width':width,'height':height})
      page.set_default_timeout(8000);page.goto(url)
      def submit(n='1',w='18'):
       page.locator('#W').fill(w);page.locator('#L').fill('20');page.locator('#n').fill(n)
       page.locator('#submit').click()
      def state(kind):
       expect(page.locator('#result')).to_have_attribute('data-status-kind',kind)
       expect(page.locator('#submit')).to_be_enabled()
       assert page.locator('svg,canvas,img,a[download]').count()==0
       assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
       assert all(x+': NOT_REPORTED' in page.locator('#stage-counts').inner_text() for x in ('نامزد','ساخته‌شده','بررسی‌شده','واجد شرایط','نمایش‌داده‌شده','دانلودشده'))
      for name,n,expected in [('mixed','1','physical_rejected_quality_unknown'),('quality','1','quality_unknown'),
       ('rejected','1','physical_rejected'),('evaluator','1','evaluation_error'),('quality','2','quality_unknown'),
       ('receipt_false','1','observed_unverified'),('binding_false','1','observed_unverified'),
       ('source_false','1','server_error'),('exception','1','server_error'),
       ('necessary','1','current_rejected'),('not_evaluated','1','not_evaluated')]:
       mode['value']=name
       with page.expect_response('**/api/public/plan') as response:submit(n)
       state(expected);data=response.value.json()
       if name in ('mixed','evaluator'):
        expect(page.locator('#result')).to_contain_text('بررسی فیزیکی این مدل رد شده')
        expect(page.locator('#result')).to_contain_text('معیارهای کیفیت هنوز نامشخص')
       if name=='evaluator':expect(page.locator('#result')).to_contain_text('ارزیابی با خطا')
       if name in ('mixed','quality','rejected','evaluator'):
        assert data['http_lifecycle']['receipt_verified'] is False and data['http_lifecycle']['evidence_usable'] is False
        assert data['full_evidence_binding']['binding_verified'] is True
        expect(page.locator('#result')).to_contain_text('تأیید مستقل چرخه')
       rows.append({'viewport':width,'case':name,'n':n,'kind':expected,'http':response.value.status,'scope':'REAL_HTTP_CONTROLLED_WRITER'})
       until(lambda:not m.LOCK.locked())
      before=len(calls);submit(w='4.999');state('invalid_input');submit(w='17');state('unsupported_case');assert len(calls)==before
      rows.extend([{'viewport':width,'case':x,'scope':'REAL_PARSER_NO_DISPATCH'} for x in ('invalid','unsupported')])
      page.route('**/api/public/plan',lambda route:route.continue_(post_data='{"W":18.1,"L":"20","n":"1"}'))
      submit();state('unsupported_wire');page.unroute('**/api/public/plan');assert len(calls)==before
      rows.append({'viewport':width,'case':'numeric_wire','scope':'REAL_PARSER_CHANGED_TRANSPORT_NO_DISPATCH'})
      # Invalid response variants are intercepted, never represented as actual evidence.
      wire=json.dumps({'W':'18','L':'20','n':'1'},separators=(',',':')).encode()
      raw=fixture(wire,'mixed',10000+width);base=m.public_summary(raw)
      base['http_lifecycle']={'schema':'HTTP_WITHHOLDING_X04_V1','response_state':'ON_TIME_OBSERVED',
       'request_id':h('WIRE_'+str(width))[:32],'request_digest':hashlib.sha256(wire).hexdigest(),
       'summary_digest':h('SYNTHETIC_SUMMARY'),'receipt_verified':False,'evidence_usable':False}
      changes={
       'request_mismatch':lambda d:d['http_lifecycle'].update(request_digest=h('OTHER_REQUEST')),
       'model_mismatch':lambda d:d['single_unit_evidence'][0].update(model_digest=h('OTHER_MODEL')),
       'nonce_malformed':lambda d:d['single_unit_evidence'][0].update(nonce='INVALID'),
       'receipt_missing':lambda d:d['single_unit_evidence'][0].pop('receipt_verified'),
       'forged_authority':lambda d:d.update(delivery_allowed=True),
       'source_false_wire':lambda d:d.update(source_integrity_verified=False),
       'decision_contradiction':lambda d:d['decision'].update(blockers=['CURRENT_UNKNOWN']),
       'count_bool':lambda d:d['single_unit_evidence'][0].update(physical_errors=True),
       'current_contradiction':lambda d:d['single_unit_evidence'][0]['current_states'].update(CURRENT_PROGRAM_SUITABILITY='FAIL'),
       'http_mismatch':lambda d:None}
      for name,change in changes.items():
       data=copy.deepcopy(base);change(data);status=500 if name=='http_mismatch' else 200
       # Closure factory avoids Playwright injecting Request into payload defaults.
       def handler(payload,code):
        return lambda route:route.fulfill(status=code,content_type='application/json',body=json.dumps(payload))
       page.route('**/api/public/plan',handler(data,status));submit()
       state('outcome_unknown' if name=='forged_authority' else 'observed_unverified')
       page.unroute('**/api/public/plan')
       rows.append({'viewport':width,'case':name,'scope':'INTERCEPTED_SYNTHETIC_NEGATIVE'})
      # Coherent replay of a response already displayed is rejected locally.
      handler_replay=lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(base))
      page.route('**/api/public/plan',handler_replay);submit();state('physical_rejected_quality_unknown')
      submit();state('observed_unverified');page.unroute('**/api/public/plan')
      rows.append({'viewport':width,'case':'replayed_response','scope':'INTERCEPTED_SYNTHETIC_NEGATIVE'})
      page.route('**/api/public/plan',lambda route:route.abort());submit();state('outcome_unknown');page.unroute('**/api/public/plan')
      rows.append({'viewport':width,'case':'network','scope':'BROWSER_NETWORK_ABORT'})
      # Real HTTP busy and stale local-document generation, no BFCache claim.
      mode['value']='hold';entered.clear();release.clear();before=len(calls);submit()
      until(entered.is_set);expect(page.locator('#result')).to_have_attribute('data-status-kind','running')
      page.evaluate("document.querySelector('#plan-form').dispatchEvent(new Event('submit',{cancelable:true}))")
      assert len(calls)==before+1
      other=browser.new_page();other.goto(url);other.locator('#submit').click()
      expect(other.locator('#result')).to_have_attribute('data-status-kind','busy');other.close()
      page.evaluate("dispatchEvent(new PageTransitionEvent('pagehide'));dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))")
      state('outcome_unknown');submit(w='17');state('unsupported_case')
      with page.expect_response('**/api/public/plan'):release.set()
      until(lambda:not m.LOCK.locked());page.wait_for_timeout(100);state('unsupported_case')
      rows.append({'viewport':width,'case':'stale_local_generation_and_busy','scope':'REAL_HTTP_SYNTHETIC_PAGE_EVENTS'})
      mode['value']='timeout';entered.clear();release.clear()
      with patch.object(boundary,'LIMIT_SECONDS',.15):
       try:submit();state('timeout');assert m.LOCK.locked()
       finally:release.set()
       until(lambda:not m.LOCK.locked())
      rows.append({'viewport':width,'case':'timeout','scope':'REAL_X04_CONTROLLED_TIME_ONLY'})
      page.close()
     spawn.assert_not_called()
   finally:release.set();browser.close()
  assert errors==[] and not m.LOCK.locked()
  assert pins=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
  print(json.dumps({'schema':'P32A_STATUS_CONTROLLED_V1','rows':rows,'source_hashes':pins,
   'chromium_version':version,'python':platform.python_version(),'actual_http':True,'solver_count':0,
   'controlled_writer_calls':len(calls),'private_payload':False,'artifact_upload':False,
   'pixel_review':'NOT_VERIFIED','screenshots_created':False,'preview_tested':False,
   'P25_positive_admission':'NOT_IMPLEMENTED','raw_receipt_authenticity':False,**{k:False for k in AUTH}},sort_keys=True))
 finally:
  release.set();server.shutdown();server.server_close();thread.join(timeout=5)
if __name__=='__main__':main()
