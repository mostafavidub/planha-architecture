"""Private P06 experiment: one clock, two explicit programmes, no public wiring."""
import argparse, copy, hashlib, inspect, json, math, os, re, signal, stat, subprocess, sys, time, uuid
from pathlib import Path

SELF=Path(__file__).resolve()
ROOT=SELF.parents[1];LOCAL=ROOT/'app/local_integration'
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(LOCAL),str(ENGINE),str(ROOT/'frontend')]
BODY=b'{"W":"18","L":"20","n":2}'
CASE={'W':'18','L':'20','n':2,'requested_count':1}
P2='PROGRAM_2BED_V1';P1='PROGRAM_1BED_V1'
SECONDS=300;SOLVER=30;START_MARGIN=5
PHASE_CEILING={P2:180,P1:240}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
DENIED={**{k:False for k in AUTH},'production_supported':False,'quality_winner':False,'global_infeasibility_proven':False}
NAMES=(P2,P1)
CAP=32*1024*1024
def need(ok,code):
 if not ok:raise ValueError(code)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def digest(v):return sha(enc(v))
def hexn(v,n):return type(v)is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',v) is not None
def auth(v):return type(v)is dict and all(v.get(k)is False for k in AUTH)
def finite(x):return type(x) in (int,float) and math.isfinite(x)
def unique(rows):
 d={}
 for k,v in rows:
  need(k not in d,'P06_DUPLICATE_KEY');d[k]=v
 return d
def nonfinite(_):raise ValueError('P06_NONFINITE_JSON')
def strict_num(s):
 n=float(s);need(finite(n),'P06_NONFINITE_JSON');return n
def decode(b):return json.loads(b,object_pairs_hook=unique,parse_float=strict_num,parse_constant=nonfinite)
def safe_root(p):
 return p.is_absolute() and p.resolve()==p and p.is_dir() and p.stat().st_uid==os.getuid() and not p.stat().st_mode&0o077
def read(path):
 with os.fdopen(os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK),'rb')as f:
  st=os.fstat(f.fileno())
  need(stat.S_ISREG(st.st_mode) and st.st_uid==os.getuid() and not st.st_mode&0o077 and st.st_size<=CAP,'P06_PRIVATE_REGULAR_FILE')
  b=f.read(CAP+1);need(len(b)==st.st_size,'P06_FILE_SIZE');return b
def write(path,value):
 b=enc(value);part=path.with_name('.'+path.name+'.partial')
 fd=os.open(part,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 os.link(part,path,follow_symlinks=False);part.unlink()
 need(read(path)==b,'P06_FILE_READBACK');return sha(b)

class Budget:
 def __init__(self,clock=None,start=None):
  self.clock=time.monotonic if clock is None else clock
  self.start=self.clock()if start is None else start;need(finite(self.start),'P06_CLOCK')
  self.last=self.start;self.deadline=self.start+SECONDS;self.used=0
 def now(self):
  v=self.clock();need(finite(v) and v>=self.last,'P06_CLOCK')
  self.last=v;return v
 def remaining(self):return self.deadline-self.now()
 def lease(self,programme):
  need(self.used<2 and NAMES[self.used]==programme,'P06_PROGRAMME_ORDER')
  start=self.now();need(self.deadline-start>=SOLVER+START_MARGIN,'P06_INSUFFICIENT_SHARED_REMAINING')
  self.used+=1
  return {'ordinal':self.used,'started':start,'common_deadline':self.deadline,
   'child_deadline':min(self.deadline,start+PHASE_CEILING[programme])}
 def ledger(self,account,at):
  return {'account_id':account,'limit_attempts':2,'used_attempts':self.used,'limit_seconds':SECONDS,'used_seconds':at-self.start}

def source_state():
 import live_program_scheduler as live,one_bed_pair_p14 as p14,front_rear_runtime_adapter as fr,program_search_order as policy
 import current_four_decision as four,search114,constructor127
 from producer_provenance import snapshot
 from engine114 import revision
 from same_version_front_rear_contract import ENGINE_REVISION
 fns=[(live.child,LOCAL/'live_program_scheduler.py'),(live.bind_completed,LOCAL/'live_program_scheduler.py'),
 (p14.run,LOCAL/'one_bed_pair_p14.py'),(p14.binding,LOCAL/'one_bed_pair_p14.py'),(p14.decision,LOCAL/'one_bed_pair_p14.py'),
 (policy.lower_program_transition,LOCAL/'program_search_order.py'),(four.assemble,LOCAL/'current_four_decision.py'),
 (fr.run,LOCAL/'front_rear_runtime_adapter.py'),(search114.propose,ENGINE/'search114.py'),(constructor127.frame,ENGINE/'constructor127.py')]
 need(revision()==ENGINE_REVISION and all(Path(inspect.getsourcefile(f)).resolve()==p for f,p in fns),'P06_SOURCE_OR_IMPORT')
 files={str(p.relative_to(ROOT))for _,p in fns}|set(p14.PATHS)|{str(SELF.relative_to(ROOT)),'app/local_integration/programme_prefilter_p05.py'}
 return {'engine_revision':ENGINE_REVISION,'files':snapshot(ROOT,sorted(files))}

def prepare(body):
 import live_program_scheduler as live,one_bed_pair_p14 as p14
 from constructor127 import frame
 from program_profile_registry import lookup
 from programme_prefilter_p05 import inspect_request
 need(type(body)is bytes and body==BODY,'P06_EXACT_SAME_REQUEST')
 p2=live.preflight(body);p1=p14.prepare(body);b=p2['binding']
 need(p2['execution_ready'] is True and digest(b['raw'])==digest(p1['raw'])==digest(CASE),'P06_BOTH_RAW')
 need(b['schema']=='FRONT_REAR_TWO_REQUEST_BINDING_V1' and p1['schema']=='P14_EXPLICIT_PRIVATE_STUDY_REQUEST_V1'
   and p1['family']=='FRONT_REAR' and type(p1['variant'])is int and p1['variant']==0,'P06_RUNTIME_VERSION_FAMILY')
 programmes={k:digest(lookup(k))for k in NAMES}
 need(b['program_registry_digest']==programmes[P2] and p1['programme_digest']==programmes[P1] and programmes[P1]!=programmes[P2],'P06_TWO_PROGRAMMES')
 core,_=frame(copy.deepcopy(CASE),'FRONT_REAR')
 return {'body_hex':body.hex(),'request_sha256':sha(body),'canonical_raw_digest':digest(CASE),'family':'FRONT_REAR','core_digest':digest(core),
   'programme_digests':programmes,'p2_preflight_digest':digest(p2),'p2_binding_digest':digest(b),'p1_request_digest':digest(p1),
   'p05_advisory':{k:inspect_request(body,k) for k in NAMES}}

def task_config(account,programme,lease,request,source):
 return {'schema':'P06_EXACT_WORKER_CONFIGURATION_V1','account_id':account,'programme':programme,'ordinal':lease['ordinal'],
  'started':lease['started'],'common_deadline':lease['common_deadline'],'child_deadline':lease['child_deadline'],
  'body_hex':request['body_hex'],'core_digest':request['core_digest'],'request_sha256':request['request_sha256'],
  'programme_digest':request['programme_digests'][programme],'source_digest':digest(source)}
def config_shape(v):
 need(type(v)is dict and set(v)=={'schema','account_id','programme','ordinal','started','common_deadline','child_deadline','body_hex','core_digest','request_sha256','programme_digest','source_digest'}
   and v['schema']=='P06_EXACT_WORKER_CONFIGURATION_V1' and hexn(v['account_id'],32) and type(v['programme'])is str and v['programme']in NAMES
   and type(v['ordinal'])is int and v['ordinal']==NAMES.index(v['programme'])+1 and v['body_hex']==BODY.hex() and v['request_sha256']==sha(BODY)
   and all(hexn(v[k],64)for k in ('core_digest','programme_digest','source_digest')),'P06_CONFIG_IDENTITY')
 need(all(finite(v[k])for k in ('started','common_deadline','child_deadline')) and
   SOLVER<=v['child_deadline']-v['started']<=PHASE_CEILING[v['programme']] and v['child_deadline']<=v['common_deadline']
   and v['common_deadline']-v['started']<=SECONDS,'P06_CONFIG_CLOCKS')

def worker(folder):
 import scipy.optimize._milp as sm,scipy.optimize as opt
 import search114,live_program_scheduler as live,one_bed_pair_p14 as p14
 from program_profile_registry import lookup
 from constructor127 import frame
 import importlib
 folder=Path(folder);need(safe_root(folder),'P06_WORKER_DIRECTORY')
 raw=read(folder/'config.json');v=decode(raw);config_shape(v)
 p=v['programme'];src=source_state()
 core,_=frame(copy.deepcopy(CASE),'FRONT_REAR')
 need(digest(core)==v['core_digest'] and digest(src)==v['source_digest'] and digest(lookup(p))==v['programme_digest'],'P06_WORKER_SOURCE_PROGRAMME')
 proof={'schema':'P06_WORKER_COMPLETION_V1','config_sha256':sha(raw),'programme':p,'account_id':v['account_id'],
        'starts':{'producer':0,'milp':0,'highs':0},'returns':{'producer':0,'milp':0,'highs':0},'guards':[]}
 watched={search114.propose.__code__:'producer',sm.milp.__code__:'milp',sm._highs_wrapper.__code__:'highs'}
 need(opt.milp.__code__ is sm.milp.__code__ and search114.milp.__code__ is sm.milp.__code__,'P06_SOLVER_ALIAS')
 sys.path[:0]=[str(LOCAL/'candidate'),str(LOCAL/'candidate/bundle25')]
 forbidden=set()
 for name in ('search_split135','search_split_side135','source_fit_candidate207','coarse_bundle25_candidate','coarse_kitchen305_candidate',
  'four_seat_group_candidate','cause_directed_candidate108','cause_parent_witness108','compound_panel_candidate108','parametric_repair',
  'coarse_access_master132','coarse_branch146','coarse_branch_rooted149','coarse_l3_master131','coarse_master128','coarse_master129',
  'coarse_mixed_master132','coarse_sidecar_circulation144','coarse_sidecar_compact142','coarse_sidecar_group138','coarse_sidecar_master136',
  'coarse_sidecar_rooted139','coarse_sidecar_seating136','coarse_stagger_master132','coarse_t_connected134','coarse_t_master133',
  'coarse_t_master134','shared_producer137'):
  fn=importlib.import_module(name).propose
  path=Path(inspect.getsourcefile(fn)).resolve()
  need(path.is_relative_to(ROOT) and path.stem==name,'P06_FORBIDDEN_PRODUCER_ORIGIN')
  forbidden.add(fn.__code__)
 def guard_sentinel():raise AssertionError('P06_PREBODY_CONTROL_MISSED')
 forbidden.add(guard_sentinel.__code__)
 expected_source=LOCAL/('front_rear_runtime_adapter.py'if p==P2 else'one_bed_pair_p14.py')
 def guard(code,_):
  try:
   need(code not in forbidden,'P06_ALTERNATIVE_PRODUCER')
   k=watched[code];f=sys._getframe(1);a=f.f_locals
   need(proof['starts'][k]==0,'P06_DUPLICATE_SOLVE')
   if k=='producer':
    n=2 if p==P2 else 1
    need(Path(f.f_back.f_code.co_filename).resolve()==expected_source and type(a['bedrooms'])is int and a['bedrooms']==n and a['sleep_roles']==(['double','twin']if n==2 else['double'])
     and a['variant']==0 and a['time_limit']==SOLVER and a['fixed_witness']is None and a['diagnostic_capture']is None and a['ordered_macro']is False
     and a['topology']=='SIDE_ROOTED_SERVICES' and digest(a['core'])==v['core_digest'],'P06_PRODUCER_SCOPE')
   if k=='milp':
    need(f.f_back.f_code is search114.propose.__code__ and a['options']['time_limit']==SOLVER,'P06_SOLVER_SCOPE')
    need(v['child_deadline']-time.monotonic()>=SOLVER,'P06_REMAINING_BEFORE_MILP')
   if k=='highs':need(f.f_back.f_code is sm.milp.__code__,'P06_HIGHS_SCOPE')
   proof['starts'][k]+=1
   write(folder/(k+'-started.json'),{'code':k,'clock':time.monotonic(),'config_sha256':sha(raw)})
  except ValueError as ex:proof['guards'].append(str(ex));raise
 def returned(code,_,ob):
  k=watched[code];proof['returns'][k]+=1
  if k=='milp':proof['solver_status']=int(ob.status);proof['incumbent']=ob.x is not None
 m=sys.monitoring;ev=m.events;tool=4
 m.use_tool_id(tool,'p06-bounded-one-call')
 m.register_callback(tool,ev.PY_START,guard);m.register_callback(tool,ev.PY_RETURN,returned)
 for code in watched:m.set_local_events(tool,code,ev.PY_START|ev.PY_RETURN)
 for code in forbidden:m.set_local_events(tool,code,ev.PY_START)
 try:
  try:guard_sentinel()
  except ValueError as ex:need(str(ex)=='P06_ALTERNATIVE_PRODUCER' and proof['guards']==['P06_ALTERNATIVE_PRODUCER'],'P06_GUARD_CONTROL')
  else:raise ValueError('P06_GUARD_CONTROL_MISSING')
  proof['guards'].clear();proof['synthetic_prebody_guard_verified']=True
  need(time.monotonic()<v['child_deadline'],'P06_EXPIRED_WORKER')
  if p==P2:live.child(folder/'runner')
  else:
   need(p14.SOLVER_SECONDS==SOLVER,'P06_P14_LIMIT')
   # Use the unmodified P14 private function and atomic receipt writer.
   data=folder/'runner';data.mkdir(mode=0o700,exist_ok=False)
   summary=p14.run(BODY,data);p14.retain_private(data,'summary.json',summary)
 finally:
  for code in set(watched)|forbidden:m.set_local_events(tool,code,0)
  m.free_tool_id(tool)
  proof['source_still_matches']=source_state()==src;proof['finished_clock']=time.monotonic()
  write(folder/'worker-proof.json',proof)

def observed_files(folder):
 root=folder/'runner'
 if not root.exists():return {}
 need(safe_root(root),'P06_RUNNER_PATH')
 files={}
 for p in sorted(root.iterdir()):
  need(p.is_file() and not p.is_symlink(),'P06_WORKER_FILE_SHAPE')
  files[p.name]={'sha256':sha(read(p))}
 return files

def run_child(folder,limit):
 # Timer is never restarted after timeout, failure or process interruption.
 delay=limit-time.monotonic();need(delay>0,'P06_CHILD_CUTOFF_BEFORE_SPAWN')
 with (folder/'stdout.log').open('xb')as out,(folder/'stderr.log').open('xb')as err:
  proc=None;timeout=False;killed=False
  signals={signal.SIGALRM,signal.SIGTERM,signal.SIGINT}
  oldmask=signal.pthread_sigmask(signal.SIG_BLOCK,signals)
  try:
   try:
    proc=subprocess.Popen([sys.executable,'-B',str(SELF),'--worker',str(folder)],cwd=ROOT,stdout=out,stderr=err,start_new_session=True)
   finally:signal.pthread_sigmask(signal.SIG_SETMASK,oldmask)
   try:proc.wait(timeout=max(0,limit-time.monotonic()))
   except subprocess.TimeoutExpired:timeout=True
  finally:
   if proc is not None and proc.poll()is None:
    try:os.killpg(proc.pid,signal.SIGKILL);killed=True
    except ProcessLookupError:pass
    proc.wait()
  return {'returncode':proc.returncode,'timed_out':timeout,'kill_sent':killed,'wait_completed':proc.poll() is not None,'observed_terminal_clock':time.monotonic()}

def worker_proof(folder,cfg,proc):
 raw=read(folder/'config.json');v=decode(raw);config_shape(v)
 need(digest(v)==digest(cfg),'P06_CONFIG_READBACK')
 need(type(proc)is dict and proc.get('wait_completed')is True and proc.get('timed_out')is False
  and type(proc.get('returncode'))is int and proc['returncode']==0 and finite(proc.get('observed_terminal_clock'))
  and v['started']<=proc['observed_terminal_clock']<=v['child_deadline'],'P06_PROCESS_TERMINAL')
 p=decode(read(folder/'worker-proof.json'))
 need(type(p)is dict and p.get('schema')=='P06_WORKER_COMPLETION_V1' and p.get('config_sha256')==sha(raw)
  and p.get('programme')==v['programme'] and p.get('account_id')==v['account_id'],'P06_WORKER_PROOF_IDENTITY')
 need(p.get('source_still_matches') is True and p.get('synthetic_prebody_guard_verified') is True and p.get('guards')==[] and finite(p.get('finished_clock'))
  and v['started']<=p['finished_clock']<=proc['observed_terminal_clock']<=v['child_deadline'],'P06_WORKER_PROOF_SOURCE_TIME')
 for h in ('starts','returns'):
  s=p.get(h)
  need(type(s)is dict and set(s)=={'producer','milp','highs'} and
   all(type(s[k])is int and s[k] in (0,1)for k in s) and s['producer']==1 and s['milp']==s['highs'],'P06_WORKER_PROOF_COUNTS')
 need(p['starts']==p['returns'],'P06_WORKER_WITH_UNRETURNED_CALL')
 if p['starts']['milp']:
  need(type(p.get('solver_status'))is int and type(p.get('incumbent'))is bool,'P06_SOLVER_TELEMETRY')
 return p

def proposal_evidence(prop,proof):
 from front_rear_runtime_adapter import proposal_disposition
 state=proposal_disposition(prop)
 count=proof['starts']['milp']
 if not count:
  need(state=='NO_PROPOSAL_IN_THIS_PROGRAM' and prop.get('reason')=='ROOM_OR_CORE_BOUND_CONFLICT'
       and 'solver_status' not in prop,'P06_PRE_SOLVER_DISPOSITION')
  return 'BOUND_CONFLICT_NO_SOLVER'
 status=prop.get('solver_status');incumbent=proof.get('incumbent')
 need(type(status)is int and status==proof.get('solver_status') and type(incumbent)is bool and prop.get('budget_seconds')==SOLVER,'P06_SOLVER_READBACK')
 if state=='PROPOSAL_ONLY':
  need(status in (0,1) and incumbent is True,'P06_STATUS_INCUMBENT_CONFLICT')
  return 'WITNESS'
 if state=='ROUNDED_PROPOSAL_REJECTED':
  need(status in (0,1) and incumbent is True,'P06_STATUS_INCUMBENT_CONFLICT')
  return 'ROUNDED_REJECTED'
 if state=='SEARCH_TIMEOUT_NO_WITNESS':
  need(status==1 and incumbent is False,'P06_STATUS_INCUMBENT_CONFLICT')
  return 'SOLVER_TIMEOUT'
 need(state=='NO_PROPOSAL_IN_THIS_TOPOLOGY' and status in (2,3,4) and incumbent is False,'P06_STATUS_INCUMBENT_CONFLICT')
 return 'BOUNDED_NO_WITNESS'if status==2 else'SOLVER_FAULT'

def bound_model(bundle,request,programme):
 rt=bundle;packet=rt['packet'];context=rt['context'];t=context['construction_trace'];m=packet['world_model'];mh=rt['model_digest']
 need(auth(rt) and packet['family']=='FRONT_REAR' and packet['admission_claim']is False and
  t['schema']=='CONSTRUCTION_TRACE127_PAIR_V1' and t['family']=='FRONT_REAR' and digest(t['raw'])==request['canonical_raw_digest'] and digest(packet['core'])==request['core_digest']==t['core_hash'],'P06_MODEL_FRAME_CORE')
 need(hexn(mh,64) and digest(m)==digest(packet['local_model'])==mh==t['model_hash']==t['local_model_hash'] and digest(m['inputs'])==digest(context['inputs'])==digest(['18','20',2]),'P06_MODEL_IDENTITY')
 n=2 if programme==P2 else 1;roles=['double','twin']if n==2 else['double']
 need(type(m['program']['units'])is int and m['program']['units']==2 and type(m['program']['bedrooms_per_unit'])is int
  and m['program']['bedrooms_per_unit']==n and m['program']['sleep_roles']==roles and [u['id']for u in m['units']]==['A','B']
  and type(m['program']['design_occupants_per_unit'])is int and m['program']['design_occupants_per_unit']==2*n
  and digest(m['profile'])==digest({'body_m':'.7'})
  and all(type(u['public_program']['capacity']['residents'])is int and u['public_program']['capacity']['residents']==2*n
    and [k for k in sorted(u['rooms'])if k.startswith('bed')]==['bed'+str(i+1) for i in range(n)] for u in m['units']),'P06_MODEL_PROGRAMME')
 need(set(t['proposals'])=={'A','B'} and all(type(z['bedrooms'])is int and z['bedrooms']==n and z['sleep_roles']==roles and
  z['status']=='PROPOSAL_ONLY' for z in t['proposals'].values()),'P06_PROPOSAL_PROGRAMME')
 return mh

def bind_p2(folder,cfg,request,source,initial_request,proof):
 import live_program_scheduler as live,front_rear_runtime_adapter as fr,current_four_decision as four
 from producer_provenance import require_unchanged
 get=lambda n:decode(read(folder/'runner'/n))
 rr=get('request.json');rt=get('runtime-bundle.json');child=get('child-complete.json')
 need(digest(rr)==digest(initial_request) and rr['nonce']==sha((cfg['account_id']+':P2').encode())[:32]
  and rr['body_hex']==request['body_hex'] and rr['preflight_digest']==request['p2_preflight_digest'],'P06_P2_WORKER_REQUEST')
 need(auth(rt) and rt['engine_revision']==source['engine_revision'] and rt['object_integrity_verified']is True and rt.get('completed')is True
  and not rt['errors'] and rt.get('report_mutations')==[] and rt.get('object_mutations')==[] and rt['object_digests']['core']==request['core_digest']
  and rt['binding']['program_registry_digest']==cfg['programme_digest'] and digest(rt['binding'])==request['p2_binding_digest'],'P06_P2_RUNTIME')
 need(set(rt['reports'])==set(rt['report_digests']) and digest(rt['reports']['source_audit'])==digest(fr.source_audit()),'P06_P2_ORIGINAL_SOURCE_AUDIT')
 require_unchanged(ROOT,rt['source_snapshot']);fr.verify_reports(rt['reports'],rt['report_digests'])
 prop=rt['proposal'];need(type(prop['bedrooms'])is int and prop['bedrooms']==2 and prop.get('sleep_roles')==['double','twin']
  and prop.get('variant')==0,'P06_P2_PROPOSAL_SCOPE')
 observed=proposal_evidence(prop,proof)
 if child['state']=='ORIGINAL_RUNTIME_INCOMPLETE_NO_FOUR_REPORT_DECISION':
  need(live.bind_completed(child,rr,rt,None) is True and rt['status']=='NO_PROPOSAL_IN_BOUNDED_ATTEMPT' and
   rt.get('model_binding_verified')is False and child['model_digest']is None and child.get('assessments')=={},'P06_P2_NO_WITNESS_BINDING')
  need(observed!='WITNESS','P06_P2_PROPOSAL_DISPOSITION')
  if observed in ('SOLVER_TIMEOUT','SOLVER_FAULT'):
   return {'result':'VERIFIED_SOLVER_TIMEOUT_NO_WITNESS'if observed=='SOLVER_TIMEOUT'else'VERIFIED_SOLVER_FAULT_NO_LOWER_EXPLORATION',
    'proposal_evidence':observed,'p1_eligible':False,'model_digest':None}
  return {'result':'VERIFIED_NO_WITNESS_IN_BOUNDED_ATTEMPT','proposal_evidence':observed,'p1_eligible':True,'model_digest':None}
 dec=get('decision.json');reports={k:get(k+'.json')for k in four.SCHEMAS}
 need(observed=='WITNESS','P06_P2_VERIFIED_INCUMBENT')
 need(live.bind_completed(child,rr,rt,dec)is True and digest(child['assessments'])==digest(reports),'P06_P2_FULL_REPORTS')
 mh=bound_model(rt,request,P2)
 need(child.get('schema')=='LIVE_SCHEDULER_CHILD_V1','P06_P2_CHILD_SCHEMA')
 need(fr.packet_binding(rt['packet'],rt['context'],CASE,prop)==mh,'P06_P2_PROPOSAL_TO_PACKET')
 reb=four.assemble(rt,reports,{k:digest(v)for k,v in reports.items()})
 need(digest(reb)==digest(dec) and dec['integrity_verified']is True and dec['model_digest']==mh and auth(dec['decision']),'P06_P2_DECISION_REDERIVATION')
 states={k:v['state']for k,v in reports.items()}
 block=dec['decision']['state']=='BLOCKED'
 errors='EVALUATOR_ERROR'in dec['decision']['blockers'] or any(v.get('integrity_verified')is not True for v in reports.values())
 return {'result':'VERIFIED_WITH_WITNESS_EVALUATOR_FAULT'if errors else 'VERIFIED_WITH_WITNESS_NOT_QUALIFIED'if block else 'VERIFIED_WITH_WITNESS_NO_LOWER_EXPLORATION',
  'p1_eligible':block and not errors,'model_digest':mh,'states':states,'decision_digest':digest(dec),'decision_state':dec['decision']['state']}

def stock_index(root,index,expected):
 files=index.get('files')
 need(auth(index) and type(files)is dict and set(files)==set(expected),'P06_P1_EXACT_STOCK_FILE_SET')
 for name,claim in files.items():
  need(type(name)is str and Path(name).name==name and type(claim)is dict and set(claim)=={'bytes','sha256'}
   and type(claim['bytes'])is int and claim['bytes']>=0 and hexn(claim['sha256'],64),'P06_P1_INDEX_FILE_SHAPE')
  b=read(root/name);need(len(b)==claim['bytes'] and sha(b)==claim['sha256'],'P06_P1_STOCK_INDEX')

def bind_p1(folder,cfg,request,proof):
 import one_bed_pair_p14 as p14,current_four_decision as four
 from front_rear_runtime_adapter import source_audit
 from producer_provenance import require_unchanged
 root=folder/'runner';get=lambda n:decode(read(root/n))
 index=get('evidence-index.json');request_saved=get('request.json');s=get('summary.json')
 need(auth(s) and request_saved['request_body_hex']==request['body_hex'] and
  digest(request_saved['request'])==request['p1_request_digest'] and request_saved['request']['programme_digest']==cfg['programme_digest'],'P06_P1_WORKER_REQUEST')
 need(digest(index['engine'])==digest(source_audit()) and set(index['local_source'])==p14.PATHS,'P06_P1_STOCK_SOURCE')
 require_unchanged(ROOT,index['local_source'])
 if s['state']=='NO_WITNESS_WITHIN_SINGLE_ATTEMPT':
  stock_index(root,index,{'request.json','attempt-open.json','proposal-observed.json'})
  v=get('proposal-observed.json')
  observed=proposal_evidence(v,proof)
  need(type(s['exact_attempts'])is int and s['exact_attempts']==1 and s['proposal_disposition']==v['status'] and observed!='WITNESS','P06_P1_NO_WITNESS')
  label={'SOLVER_TIMEOUT':'VERIFIED_P1_SOLVER_TIMEOUT_NO_WITNESS','SOLVER_FAULT':'VERIFIED_P1_SOLVER_FAULT_NO_ADMISSION'}.get(observed,'VERIFIED_P1_NO_WITNESS_IN_BOUNDED_ATTEMPT')
  return {'result':label,'proposal_evidence':observed,'model_digest':None,'p1_eligible':False}
 need(s['state'] in ('ONE_BEDROOM_PAIR_SOURCE_STUDY_NOT_QUALIFIED','FOUR_ASSESSMENTS_WITH_EVALUATOR_ERRORS_NOT_QUALIFIED')
      and proof['starts']['milp']==1 and proof.get('incumbent')is True,'P06_P1_TERMINAL')
 stock_index(root,index,{'request.json','attempt-open.json','proposal.json','proposal-transport.json','packet.json','context.json',
    'replay-original.json','physical-original.json','runtime-bundle.json','decision.json',*(k+'.json' for k in four.SCHEMAS)})
 rt=get('runtime-bundle.json');dec=get('decision.json');rs={k:get(k+'.json')for k in four.SCHEMAS}
 need(auth(rt) and digest(rt['request'])==request['p1_request_digest'] and rt['request']['programme_digest']==cfg['programme_digest']
  and rt['request_body_hex']==request['body_hex'],'P06_P1_RUNTIME')
 need(all(digest(rt[k])==digest(get(k+'.json'))for k in ('packet','proposal','context')) and
  digest(rt['reports']['physical'])==digest(get('physical-original.json')) and digest(rt['reports']['replay'])==digest(get('replay-original.json'))
  and digest(rt['source_snapshot'])==digest(index['local_source']),'P06_P1_ORIGINAL_REPORTS')
 need(proposal_evidence(rt['proposal'],proof)=='WITNESS','P06_P1_VERIFIED_INCUMBENT')
 mh=bound_model(rt,request,P1);p14.binding(rt)
 reb=p14.decision(rt,rs,{k:digest(v)for k,v in rs.items()})
 need(digest(reb)==digest(dec) and dec['integrity_verified'] is True and mh==s['model_digest']==dec['model_digest'] and
   digest(s['decision'])==digest(dec['decision']) and auth(dec['decision']),'P06_P1_DECISION_REDERIVATION')
 errored='EVALUATOR_ERROR'in dec['decision']['blockers'] or any(v.get('integrity_verified')is not True for v in rs.values())
 return {'result':'VERIFIED_P1_WITH_WITNESS_EVALUATOR_FAULT'if errored else'VERIFIED_P1_WITH_WITNESS_NOT_QUALIFIED','p1_eligible':False,'model_digest':mh,
    'states':{k:v['state']for k,v in rs.items()},'decision_digest':digest(dec),'decision_state':dec['decision']['state']}

def stage_records(account,verdict):
 from program_search_order import stage_record
 return [stage_record('CORE','NOT_ENUMERATED','Fixed registered FRONT_REAR core used; no core alternative attempted.'),
  stage_record('SPLIT','NOT_ENUMERATED','Fixed registered split used; no alternate split attempted.'),
  stage_record('PLACEMENT','ATTEMPTED_WITH_WITNESS' if verdict['model_digest'] else 'TIMED_OUT' if verdict['result']=='VERIFIED_SOLVER_TIMEOUT_NO_WITNESS' else 'ATTEMPTED_NO_WITNESS',
    'One bounded registered P2 placement; disposition is not infeasibility or qualification.',[account+':P2:1']),
  stage_record('OPTIONAL_NONBED_MERGE','NOT_IMPLEMENTED','No bounded non-bedroom merge adapter in this experiment.')]

def transition_gate(budget,account,verdict):
 from program_search_order import lower_program_transition
 now=budget.now()
 need(budget.used==1 and now<budget.deadline,'P06_BEFORE_TRANSITION_CUTOFF')
 disposition=stage_records(account,verdict)
 marks=lower_program_transition(P2,P1,disposition,unit_count=2,budget_ledger=budget.ledger(account,now))
 # The prior policy is recorded intact; it does not authorize a worker.
 allowed=verdict.get('p1_eligible') is True and verdict['result'] in (
  'VERIFIED_NO_WITNESS_IN_BOUNDED_ATTEMPT','VERIFIED_WITH_WITNESS_NOT_QUALIFIED') and budget.deadline-now>=SOLVER+START_MARGIN
 return {'verified_p2_result':verdict['result'],'study_p1_allowed':allowed,'observed_at':now,'policy_record':marks,
    'bounded_comparison_only':True,'not_automatic_downgrade':True,'ap07_exhaustive_not_claimed':True,**DENIED}

def execute(root,budget):
 import live_program_scheduler as live
 need(safe_root(root),'P06_PRIVATE_ROOT')
 need(budget.remaining()>0,'P06_EXPIRED_SETUP')
 account=uuid.uuid4().hex
 src=source_state();request=prepare(BODY)
 initial_body_sha=request['request_sha256'];pin=digest([request,src])
 write(root/'origin.json',{'schema':'P06_EXPERIMENT_ORIGIN_V1','account_id':account,
      'start_clock':budget.start,'common_deadline':budget.deadline,'source':src,'request':request,**DENIED})
 result={'schema':'P06_SHARED_BUDGET_COMPARISON_V1','account_id':account,'request_sha256':initial_body_sha,
  'core_digest':request['core_digest'],'programme_digests':request['programme_digests'],'attempts':[],'state':'NOT_STARTED',
  'authorization_scope':'Independent private experiment; same n/fixed core, no public dispatch, generation admission, prior-policy promotion or quality ranking.',**DENIED}
 for p in NAMES:
  if p==P1 and not result.get('transition',{}).get('study_p1_allowed'):break
  row={'programme':p,'attempted':False,'verified':False,'state':'NOT_LAUNCHED'}
  result['attempts'].append(row)
  try:
   cfg=task_config(account,p,budget.lease(p),request,src);config_shape(cfg)
   d=root/('p2'if p==P2 else'p1');d.mkdir(mode=0o700)
   write(d/'config.json',cfg)
   rr=None
   if p==P2:
    f=d/'runner';f.mkdir(mode=0o700);rr={'schema':'LIVE_PROGRAM_ATTEMPT_V1','nonce':sha((account+':P2').encode())[:32],
        'body_hex':request['body_hex'],'preflight_digest':request['p2_preflight_digest'],'budget':live.budgets()}
    write(f/'request.json',rr)
   row['attempted']=True;row['config_sha256']=sha(read(d/'config.json'))
   proc=run_child(d,cfg['child_deadline']);row['process']=proc
   files=observed_files(d);row['observed_files']=files
   proof=worker_proof(d,cfg,proc)
   need(budget.remaining()>0,'P06_BEFORE_READBACK_CUTOFF')
   v=bind_p2(d,cfg,request,src,rr,proof) if p==P2 else bind_p1(d,cfg,request,proof)
   need(observed_files(d)==files and source_state()==src and digest([request,src])==pin,'P06_POST_READBACK_INTEGRITY')
   need(budget.remaining()>0,'P06_READBACK_AFTER_SHARED_CUTOFF')
   row.update(state=v['result'],verified=True,solver_starts=proof['starts']['milp'],receipt=v)
   if p==P2:
    result['transition']=transition_gate(budget,account,v)
    write(root/'p2-finished-transition.json',result['transition'])
   result['state']=('TWO_TERMINALS_RETAINED_P1_FAILURE'if v['result'] in ('VERIFIED_P1_WITH_WITNESS_EVALUATOR_FAULT','VERIFIED_P1_SOLVER_FAULT_NO_ADMISSION')else'TWO_PROGRAMME_TERMINALS_VERIFIED_NO_ADMISSION')if p==P1 else'P2_VERIFIED_LOWER_NOT_YET_EXECUTED'
  except Exception as ex:
   row.update(verified=False,state='P06_ATTEMPT_STOPPED_FAIL_CLOSED',error_type=type(ex).__name__,error_code=str(ex))
   result['state']='SCOPED_PARTIAL_OR_FAILED_CLOSED'
   # Never retain authorization to launch a lower programme after error.
   if p==P2 and 'transition'in result:result['transition']['study_p1_allowed']=False
   break
 if len(result['attempts'])==1:
  result['attempts'].append({'programme':P1,'attempted':False,'verified':False,'state':'NOT_LAUNCHED'})
 now=budget.now();result['budget']=budget.ledger(account,now);result['common_deadline']=budget.deadline
 if now>=budget.deadline:
  result['state']='SHARED_DEADLINE_EXPIRED_RECEIPTS_FORENSIC_ONLY'
  for r in result['attempts']:r['verified_before_shared_cutoff']=r['verified'];r['verified']=False
  if 'transition'in result:result['transition']['study_p1_allowed']=False
 out=root/'summary.json'
 write(out,result)
 if budget.now()>=budget.deadline and result['state']!='SHARED_DEADLINE_EXPIRED_RECEIPTS_FORENSIC_ONLY':
  os.rename(out,root/'late-summary-unverified.json')
  return {'state':'SHARED_DEADLINE_EXPIRED_RECEIPTS_FORENSIC_ONLY',**DENIED}
 return result

class SharedCutoff(BaseException):pass

def main():
 entry=time.monotonic()
 ap=argparse.ArgumentParser(description='Private two-programme study. No public dispatch.')
 g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--private-output',type=Path);g.add_argument('--worker',type=Path)
 a=ap.parse_args();os.umask(0o077)
 if a.worker is not None:worker(a.worker);return
 budget=Budget(start=entry)
 p=a.private_output
 need(p.is_absolute() and safe_root(p.parent) and p.resolve()==p,'P06_PRIVATE_PARENT')
 p.mkdir(mode=0o700,exist_ok=False)
 def interrupt(_sig,_frame):raise KeyboardInterrupt('P06_EXTERNAL_STOP')
 signal.signal(signal.SIGTERM,interrupt)
 def cutoff(_sig,_frame):raise SharedCutoff('P06_ABSOLUTE_DEADLINE')
 signal.signal(signal.SIGALRM,cutoff)
 signal.setitimer(signal.ITIMER_REAL,max(.000001,budget.remaining()))
 try:out=execute(p,budget)
 except SharedCutoff:
  # Only a forensic terminal is written after cutoff; no authorization marker.
  summary=p/'summary.json'
  if summary.exists():os.replace(summary,p/'late-summary-unverified.json')
  out={'state':'SHARED_DEADLINE_EXPIRED_RECEIPTS_FORENSIC_ONLY',**DENIED}
  write(p/'deadline-expired.json',out)
 finally:signal.setitimer(signal.ITIMER_REAL,0)
 print(json.dumps({'schema':'P06_SAFE_CLI_RESULT_V1','state':out['state'],**DENIED},sort_keys=True))
if __name__=='__main__':main()
