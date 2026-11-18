"""Exact partial390 state-transition replay against actual HTML; never generation."""
from __future__ import annotations
import copy, hashlib, json, socket, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
HTML399=ROOT/'reconstruction357/staging399_e1_5_member_identity/index.html'
HTML400=Path(__file__).resolve().parent/'index.html'
RESULT_PATH=ROOT/'review390_actual_v1/runs/c72145e6-a608-4122-ad15-29ee430ce4bf/result.json'
REAL=json.loads(RESULT_PATH.read_text());RID=REAL['transport_run_id'];OUT=Path(sys.argv[1])
sys.path.insert(0,str(Path(__file__).resolve().parent))
from contract390 import partial

RUNNING=partial('RUNNING',RID)
FAILURE={**partial('UNKNOWN',RID),'semantic_state':'UNKNOWN_OWNER_FAILURE','reason':'SyntheticOwnerFailure:controlled replay'}

def terminal(kind):
 value=copy.deepcopy(REAL)
 if kind=='compatible':pass
 elif kind=='member_wrong_run':value['members'][0]['binding']['run_id']='11111111-1111-4111-8111-111111111111'
 elif kind=='model_digest_mismatch':value['members'][0]['model']['_synthetic_tamper']=True
 elif kind=='outer_wrong_run':value['transport_run_id']='22222222-2222-4222-8222-222222222222'
 elif kind=='request_body_mismatch':
  value['binding']['transport_body_sha256']='0'*64
  for member in value['members']:member['binding']['transport_body_sha256']='0'*64
 else:raise ValueError(kind)
 return value

class Local:
 def __init__(self,html,sequence,post_delay=0,invalid=False):
  self.html=html.read_bytes();self.sequence=sequence;self.post_delay=post_delay;self.invalid=invalid;self.posts=[];self.gets=0;self.post_seen=threading.Event();outer=self
  class Handler(BaseHTTPRequestHandler):
   def log_message(self,*_):pass
   def sendv(self,code,value,kind='application/json'):
    data=value if isinstance(value,bytes)else json.dumps(value,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
   def do_GET(self):
    if self.path=='/':return self.sendv(200,outer.html,'text/html; charset=utf-8')
    if self.path=='/api/runs/'+RID:
     value=outer.sequence[min(outer.gets,len(outer.sequence)-1)];outer.gets+=1;return self.sendv(200,value)
    return self.sendv(404,{})
   def do_POST(self):
    raw=self.rfile.read(int(self.headers.get('Content-Length','0'))).decode();outer.posts.append(raw);outer.post_seen.set();time.sleep(outer.post_delay)
    if outer.invalid:return self.sendv(422,{'state':'INPUT_INVALID','reason':'UNSUPPORTED_EXACT_FIXED_DIMENSION:W','generation_started':False})
    return self.sendv(202,{'transport_run_id':RID,'status_url':'/api/runs/'+RID,'synthetic_replay':True})
  self.http=ThreadingHTTPServer(('127.0.0.1',0),Handler);self.thread=threading.Thread(target=self.http.serve_forever);self.thread.start();self.url=f'http://127.0.0.1:{self.http.server_port}'
 def close(self):
  port=self.http.server_port;self.http.shutdown();self.http.server_close();self.thread.join();probe=socket.socket();probe.settimeout(1);code=probe.connect_ex(('127.0.0.1',port));probe.close();return {'port':port,'thread_alive':self.thread.is_alive(),'listener_connect_ex_after':code}

def state(page):
 return page.evaluate("""() => ({models:document.querySelector('#models').children.length,summary:document.querySelector('#summary').textContent,values:Object.fromEntries(new FormData(document.querySelector('#form'))),finalState:window.finalResult?.state||null,finalReason:window.finalResult?.reason||null,displayBinding:window.displayBinding||null,partialResultBinding:window.partialResultBinding||null,staleResult:window.staleResult||null,ledger:window.requestLedger||null})""")

def run(playwright,name,html,sequence,action=None,post_delay=0,invalid=False):
 local=Local(html,sequence,post_delay,invalid);browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);row={'name':name,'source_html':str(html.relative_to(ROOT)),'exact_partial_from_contract390':True,'synthetic_replay':True}
 try:
  page=browser.new_page();page.goto(local.url+'/',wait_until='domcontentloaded')
  if action=='prior_invalid':
   page.evaluate("members=>{render(members);window.displayBinding={synthetic_prior:true}}",REAL['members']);row['prior_models']=page.locator('#models').locator(':scope > *').count();page.locator('input[name="W"]').fill('۲۵');row['after_edit']=state(page)
  page.locator('#submit').click();assert local.post_seen.wait(2)
  if action=='edit_before_accept':page.locator('input[name="W"]').fill('۲۵')
  if action=='edit_after_running':
   page.wait_for_function("window.requestLedger && window.requestLedger.some(e=>e.type==='POLL_RESPONSE'&&e.schema_kind==='progress')");page.locator('input[name="L"]').fill('۲۷')
  if invalid:page.wait_for_function("window.finalResult && window.finalResult.state==='INPUT_INVALID'",timeout=5000)
  else:page.wait_for_function("window.finalResult !== null || window.staleResult !== undefined",timeout=8000)
  row.update(state=state(page),posts=list(local.posts),get_count=local.gets)
 finally:
  browser.close();row['cleanup']=local.close()
 return row

with sync_playwright() as p:
 cases={
  '399_running_regression':run(p,'399_running_regression',HTML399,[RUNNING,terminal('compatible')]),
  '400_running_terminal':run(p,'400_running_terminal',HTML400,[RUNNING,terminal('compatible')]),
  '400_running_failure_partial':run(p,'400_running_failure_partial',HTML400,[RUNNING,FAILURE]),
  '400_wrong_run_progress':run(p,'400_wrong_run_progress',HTML400,[{**RUNNING,'transport_run_id':'22222222-2222-4222-8222-222222222222'}]),
  '400_member_wrong_run':run(p,'400_member_wrong_run',HTML400,[terminal('member_wrong_run')]),
  '400_model_digest_mismatch':run(p,'400_model_digest_mismatch',HTML400,[terminal('model_digest_mismatch')]),
  '400_outer_wrong_run':run(p,'400_outer_wrong_run',HTML400,[terminal('outer_wrong_run')]),
  '400_request_body_mismatch':run(p,'400_request_body_mismatch',HTML400,[terminal('request_body_mismatch')]),
  '400_stale_before_accept':run(p,'400_stale_before_accept',HTML400,[RUNNING,terminal('compatible')],'edit_before_accept',.35),
  '400_stale_after_running':run(p,'400_stale_after_running',HTML400,[RUNNING,terminal('compatible')],'edit_after_running'),
  '400_prior_model_invalid':run(p,'400_prior_model_invalid',HTML400,[],'prior_invalid',invalid=True),
 }

assert cases['399_running_regression']['state']['finalState']=='IDENTITY_MISMATCH' and cases['399_running_regression']['state']['finalReason']=='OUTER_BINDING_RUN_MISMATCH'
ok=cases['400_running_terminal']['state'];assert ok['finalState']==REAL['state'] and ok['models']==2 and ok['displayBinding']['transport_run_id']==RID and cases['400_running_terminal']['get_count']>=2
fail=cases['400_running_failure_partial']['state'];assert fail['finalState']=='UNKNOWN' and fail['models']==0 and fail['displayBinding'] is None and fail['partialResultBinding']['no_model'] is True
wrong=cases['400_wrong_run_progress']['state'];assert wrong['finalState']=='IDENTITY_MISMATCH' and wrong['finalReason']=='POLL_RUN_ID_MISMATCH' and wrong['models']==0
for name,reason in [('400_member_wrong_run','MEMBER_RUN_OR_KIND_MISMATCH'),('400_model_digest_mismatch','MEMBER_MODEL_DIGEST_MISMATCH'),('400_outer_wrong_run','POLL_RUN_ID_MISMATCH'),('400_request_body_mismatch','OUTER_REQUEST_BODY_MISMATCH')]:
 s=cases[name]['state'];assert s['finalState']=='IDENTITY_MISMATCH' and s['finalReason']==reason and s['models']==0
for name in ('400_stale_before_accept','400_stale_after_running'):
 s=cases[name]['state'];assert s['models']==0 and s['displayBinding'] is None and s['staleResult']['transport_run_id']==RID and any(e['type']=='TERMINAL_SUPPRESSED_STALE' for e in s['ledger'])
invalid=cases['400_prior_model_invalid'];assert invalid['prior_models']==2 and invalid['after_edit']['models']==0 and invalid['state']['models']==0 and invalid['state']['finalState']=='INPUT_INVALID'
for c in cases.values():assert len(c['posts'])==1 and not c['cleanup']['thread_alive'] and c['cleanup']['listener_connect_ex_after']==111
OUT.joinpath('SCHEMA_STATE_BROWSER_RESULT.json').write_text(json.dumps({'schema':'E1_5_SCHEMA_STATE400_BROWSER_V1','verified':True,'real_result_sha256':hashlib.sha256(RESULT_PATH.read_bytes()).hexdigest(),'partial_running':RUNNING,'partial_failure':FAILURE,'real_generation':False,'cases':cases},ensure_ascii=False,indent=2)+'\n')
