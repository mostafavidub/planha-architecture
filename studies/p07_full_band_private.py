"""Private archival wrapper for the unchanged historical FULL_BAND child. No default wiring."""
import argparse, hashlib, inspect, json, math, os, re, signal, stat, subprocess, sys, time, types, uuid
from pathlib import Path

SELF=Path(__file__).resolve()
ROOT=SELF.parents[1]
LOCAL=ROOT/'app/local_integration'
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
GUARD=ROOT/'app/reconstruction357/staging400_e1_5_schema_states/guard400.py'
sys.path[:0]=[str(ENGINE),str(LOCAL),str(GUARD.parent),str(ROOT/'frontend')]
STOCK=LOCAL/'core_choice_pair_study.py'
STOCK_BLOB='4ed751238583d63ec2d9bb570bccbb9b0802cd3c'
CHOICE='FRONT_REAR_FULL_BAND114'
RAW={'W':'18','L':'20','n':2,'requested_count':1}
SECONDS=240
SOLVER=30
DENIED={k:False for k in ('accepted','qualified','display_allowed','delivery_allowed','production_supported','core_quality_winner')}
REPORTS={'independent_replay','original_replay','physical','core_partition','core_concept','opening_hosts','core_assessment','actual_detached_negatives'}
WATCH=('producer','milp','highs')
CAP=32*1024*1024
CONTEXT_FILES=('constructor127.py','assemble114.py','contract114.py','frame_contract125.py','common_core125.py','world_transform125.py')

def need(x,c):
 if not x:raise ValueError(c)
def encode(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(x):return sha(encode(x))
def ishex(x,n):return type(x)is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',x) is not None
def finite(x):return type(x) in (int,float) and math.isfinite(x)
def unique(pairs):
 d={}
 for k,v in pairs:
  need(k not in d,'P07_DUPLICATE_JSON')
  d[k]=v
 return d
def no_constant(_):raise ValueError('P07_NONFINITE_JSON')
def floating(s):
 x=float(s);need(finite(x),'P07_NONFINITE_JSON');return x
def decode(b):return json.loads(b,object_pairs_hook=unique,parse_constant=no_constant,parse_float=floating)
def private_dir(p):
 return p.is_absolute() and p.resolve()==p and p.is_dir() and p.stat().st_uid==os.getuid() and stat.S_IMODE(p.stat().st_mode)==0o700
def read(p):
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK),'rb')as f:
  s=os.fstat(f.fileno())
  need(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and not s.st_mode&0o077 and 0<=s.st_size<=CAP,'P07_PRIVATE_FILE')
  b=f.read(CAP+1);need(len(b)==s.st_size,'P07_FILE_READBACK')
 return b
def write(p,v,*,native_order=False):
 b=(json.dumps(v,ensure_ascii=False,sort_keys=False,separators=(',',':'),allow_nan=False).encode() if native_order else encode(v))
 tmp=p.with_name('.'+p.name+'.partial')
 with os.fdopen(os.open(tmp,os.O_WRONLY|os.O_NOFOLLOW|os.O_EXCL|os.O_CREAT,0o600),'wb')as f:
  f.write(b);f.flush();os.fsync(f.fileno())
 os.link(tmp,p,follow_symlinks=False);tmp.unlink()
 need(read(p)==b,'P07_WRITE_READBACK');return sha(b)
def stock():
 import core_choice_pair_study as s
 b=STOCK.read_bytes()
 need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==STOCK_BLOB,'P07_HISTORIC_CHILD_BLOB')
 need(Path(inspect.getsourcefile(s.child)).resolve()==STOCK,'P07_CHILD_ORIGIN')
 return s
def source():
 import engine114,guard400,search114,constructor127,assemble114,construction_replay127,evaluate_pair127,core_wall_audit118,contract114
 import program_profile_registry
 from same_version_front_rear_contract import ENGINE_REVISION,FREEZE
 s=stock()
 mods=((search114,('propose',)),(contract114,('full_band_core_first','core_first')),
  (constructor127,('context',)),(assemble114,('assemble',)),(construction_replay127,('verify',)),
  (evaluate_pair127,('evaluate',)),(core_wall_audit118,('core_concept','opening_hosts')),
  (engine114,('revision',)),(guard400,('guard',)),(program_profile_registry,('lookup',)),
  (s,('core_predicates','actual_candidate_negatives','selected_core')))
 expect={s:STOCK,guard400:GUARD,program_profile_registry:LOCAL/'program_profile_registry.py'}
 paths={SELF,STOCK,ENGINE/'entry117.py',ENGINE/'checker114.py',ENGINE/'private_binding121.py',*(ENGINE/n for n in CONTEXT_FILES),
  LOCAL/'front_rear_runtime_adapter.py',LOCAL/'same_version_front_rear_contract.py',LOCAL/'one_bed_pair_source_study.py'}
 for mod,names in mods:
  p=expect.get(mod,ENGINE/(mod.__name__+'.py'));paths.add(p)
  for n in names:need(Path(inspect.getsourcefile(getattr(mod,n))).resolve()==p,'P07_ACTUAL_IMPORT_SOURCE')
 need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991,'P07_ENGINE_GUARD')
 return {'engine_revision':ENGINE_REVISION,'stock_git_blob':STOCK_BLOB,'files':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted(paths)}}
def inputs():
 from program_profile_registry import lookup
 s=stock();p=lookup('PROGRAM_2BED_V1');s.bind_profile(p)
 c,_=s.selected_core(RAW,CHOICE);base,_=s.selected_core(RAW,'FRONT_REAR_COMPACT118')
 need(digest(c)!=digest(base),'P07_DIFFERENT_CORE_REQUIRED')
 return {'raw_digest':digest(RAW),'profile_digest':digest(p),'core_digest':digest(c),'different_compact_core_digest':digest(base)}
def cfg_valid(v):
 need(type(v)is dict and set(v)=={'schema','nonce','choice','start','deadline','source','inputs'}
  and v['schema']=='P07_PRIVATE_LAUNCH_V1' and ishex(v['nonce'],32) and v['choice']==CHOICE
  and finite(v['start']) and finite(v['deadline']) and v['deadline']-v['start']==SECONDS,'P07_LAUNCH_IDENTITY')
def retained_packet(l,cfg):
 # Copy out by serialization immediately at the sha-pinned stock child's own
 # INDEPENDENT_REPLAY pre-report checkpoint. Do not mutate any child object.
 keys=('raw','profile','core','proposals','packet','ctx','receipt','snap','tr')
 need(all(k in l for k in keys),'P07_ARCHIVED_PACKET_MISSING')
 need(l['out'].get('stage')=='INDEPENDENT_REPLAY','P07_CAPTURE_STAGE')
 v={k:l[k]for k in keys}
 return {'schema':'P07_EARLY_STOCK_CHECKPOINT_V1','choice':CHOICE,'nonce':cfg['nonce'],'source_digest':digest(cfg['source']),**v}
def bind_packet(v,cfg):
 s=stock()
 need(type(v)is dict and set(v)=={'schema','choice','nonce','source_digest','raw','profile','core','proposals','packet','ctx','receipt','snap','tr'}
  and v['schema']=='P07_EARLY_STOCK_CHECKPOINT_V1' and v['choice']==CHOICE and v['nonce']==cfg['nonce']
  and v['source_digest']==digest(cfg['source']),'P07_CAPTURE_IDENTITY')
 a=cfg['inputs']
 need(digest(v['raw'])==digest(RAW)==a['raw_digest'] and digest(v['profile'])==a['profile_digest']
  and digest(v['core'])==a['core_digest'] and a['core_digest']!=a['different_compact_core_digest'],'P07_INPUT_CORE_PROFILE')
 p=v['packet'];ctx=v['ctx'];t=ctx['construction_trace'];m=p['world_model'];mh=digest(m);props=v['proposals']
 need(p['family']==t['family']=='FRONT_REAR' and t['schema']=='CONSTRUCTION_TRACE127_PAIR_V1'
  and p['admission_claim'] is False and digest(p['core'])==t['core_hash']==a['core_digest']
  and digest(t['raw'])==a['raw_digest'] and digest(p['local_model'])==t['local_model_hash']==t['model_hash']==mh
  and t['source_revision']==cfg['source']['engine_revision'],'P07_PACKET_TRACE')
 need(set(props)=={'A','B'} and digest(props)==digest(t['proposals']) and
  {k:digest(q)for k,q in props.items()}==p['unit_proposal_hashes']==t['unit_proposal_hashes']
  and all(type(q['bedrooms'])is int and q['bedrooms']==2 and q['sleep_roles']==['double','twin'] and q['status']=='PROPOSAL_ONLY'
    and type(q['variant'])is int and q['variant']==0 for q in props.values()),'P07_PROPOSAL_BINDING')
 need(type(v['tr'])is dict and type(v['tr'].get('coordinate_conversions'))is list and
  v['tr']['before_digest']==v['tr']['after_digest']==digest(props['A'])==digest(props['B']),'P07_PROPOSAL_TRANSPORT')
 s.bind_program(m,v['profile'])
 need(digest(m['inputs'])==digest(['18','20',2]) and digest(ctx['inputs'])==digest(m['inputs']),'P07_MODEL_INPUT')
 expected={k:cfg['source']['files'][str((ENGINE/k).relative_to(ROOT))] for k in CONTEXT_FILES}
 need(ctx['operation']=='generate_from_dimensions' and ctx['baseline_model_hash'] is None and ctx['existing_plan_id'] is None
  and digest(ctx['source_files'])==digest(expected),'P07_CONSTRUCTOR_CONTEXT_SOURCE')
 need(digest({k:cfg['source']['files'][k]for k in v['snap']})==digest(v['snap']) and
  {'app/local_integration/core_choice_pair_study.py','app/local_integration/program_profile_registry.py',
   str((ENGINE/'assemble114.py').relative_to(ROOT)),str((ENGINE/'contract114.py').relative_to(ROOT))}<=set(v['snap']),'P07_SNAPSHOT_CLOSURE')
 s.bind_receipt(v['receipt'],v['raw'],CHOICE,v['profile'],v['core'],props,m,v['snap'],cfg['nonce'])
 return mh
def capture_parent(f,child_code,retain_code):
 caller=f.f_back
 if caller.f_code is child_code:return caller
 if caller.f_code is retain_code and caller.f_back.f_code is child_code:return None
 raise ValueError('P07_CAPTURE_PARENT')

def worker(output):
 import search114
 import scipy.optimize._milp as sm
 import scipy.optimize as opt
 cfg_bytes=read(output/'launch.json');cfg=decode(cfg_bytes);cfg_valid(cfg)
 need(private_dir(output) and source()==cfg['source'] and inputs()==cfg['inputs'] and cfg['start']<=time.monotonic()<cfg['deadline'],'P07_WORKER_INPUT')
 s=stock()
 locals_code={k:[x for x in s.child.__code__.co_consts if isinstance(x,types.CodeType) and x.co_name==k] for k in ('save','retain')}
 need(all(len(x)==1 for x in locals_code.values()),'P07_STOCK_CAPTURE_CODE')
 save=locals_code['save'][0];retain=locals_code['retain'][0]
 watch={search114.propose.__code__:'producer',sm.milp.__code__:'milp',sm._highs_wrapper.__code__:'highs'}
 need(search114.milp.__code__ is opt.milp.__code__ is sm.milp.__code__,'P07_MILP_ALIAS')
 proof={'schema':'P07_WORKER_OBSERVATION_V1','nonce':cfg['nonce'],'choice':CHOICE,'config_sha256':sha(cfg_bytes),
        'starts':dict.fromkeys(WATCH,0),'returns':dict.fromkeys(WATCH,0),'faults':[]}
 def monitor(code,_):
  f=sys._getframe(1)
  try:
   need(time.monotonic()<cfg['deadline'],'P07_WORKER_CUTOFF')
   if code is save:
    parent=capture_parent(f,s.child.__code__,retain)
    if parent is None:return # Only inner stock save of its original reports; not a capture hook.
    l=parent.f_locals
    if l['out'].get('stage')=='INDEPENDENT_REPLAY' and 'capture_sha256' not in proof:
     v=retained_packet(l,cfg)
     proof['capture_sha256']=write(output/'packet-checkpoint.json',v,native_order=True)
     bind_packet(v,cfg)
    if l['out'].get('state')=='NO_PROPOSAL_NO_INFEASIBILITY_CLAIM' and 'proposal_only_sha256' not in proof:
     proof['proposal_only_sha256']=write(output/'no-witness-proposal.json',l['p'])
    return
   k=watch[code];a=f.f_locals
   need(not proof['starts'][k],'P07_DUPLICATE_OPTIMIZER_OR_PROPOSER')
   if k=='producer':
    need(f.f_back.f_code is s.child.__code__ and a['bedrooms']==2 and a['variant']==0 and
     a['sleep_roles']==['double','twin'] and a['time_limit']==SOLVER and a['topology']=='SIDE_ROOTED_SERVICES' and
     a['fixed_witness'] is None and a['diagnostic_capture'] is None and a['ordered_macro'] is False and
     digest(a['core'])==cfg['inputs']['core_digest'],'P07_PRODUCER_CALL')
   elif k=='milp':
    need(f.f_back.f_code is search114.propose.__code__ and a['options']['time_limit']==SOLVER
      and cfg['deadline']-time.monotonic()>=SOLVER,'P07_SOLVER_CALL_OR_RESIDUAL')
   else:need(f.f_back.f_code is sm.milp.__code__,'P07_HIGHS_CALL')
   write(output/(k+'-started.json'),{'kind':k,'clock':time.monotonic(),'nonce':cfg['nonce']})
   proof['starts'][k]+=1
  except Exception as ex:
   proof['faults'].append(type(ex).__name__);raise
 def returned(code,_,v):
  k=watch[code];proof['returns'][k]+=1
  if k=='milp':proof.update(solver_status=int(v.status),incumbent=v.x is not None)
 m=sys.monitoring;e=m.events;t=4
 m.use_tool_id(t,'p07-single-historical-branch')
 m.register_callback(t,e.PY_START,monitor);m.register_callback(t,e.PY_RETURN,returned)
 m.set_local_events(t,save,e.PY_START)
 for code in watch:m.set_local_events(t,code,e.PY_START|e.PY_RETURN)
 try:s.child(output/'stock',CHOICE,cfg['nonce'])
 finally:
  for code in (*watch,save):m.set_local_events(t,code,0)
  m.free_tool_id(t)
  proof['source_unchanged']=source()==cfg['source']
  proof['observed_worker_end']=time.monotonic()
  write(output/'worker-proof.json',proof)

def bind_original_reports(rep,ph,mh,trace,summary,revision):
 need(type(rep.get('verified'))is bool and rep['verified'] is summary['legacy_replay_verified'] and rep['accepted'] is False and
  rep['model_hash']==mh and rep['trace_hash']==digest(trace) and rep['source_revision']==revision and
  type(rep['errors'])is list and type(rep['pending'])is list and
  digest(rep)==digest(ph['multiproposal_provenance127']) and ph['model_hash']==mh and
  ph['status']==summary['physical_status'] and type(ph['errors'])is list and type(ph['pending'])is list,'P07_DISTINCT_ORIGINAL_REPORTS')

def archive_report(output,cfg,wait):
 cfg_valid(cfg)
 need(type(wait)is dict and wait['exit']==0 and wait['timeout'] is False and wait['reaped'] is True and
  cfg['start']<=wait['observed_terminal']<cfg['deadline'],'P07_PROCESS_NOT_COMPLETED')
 p=decode(read(output/'worker-proof.json'))
 need(p['schema']=='P07_WORKER_OBSERVATION_V1' and p['choice']==CHOICE and p['nonce']==cfg['nonce']
  and p['config_sha256']==sha(read(output/'launch.json')) and p['source_unchanged'] is True and p['faults']==[]
  and cfg['start']<=p['observed_worker_end']<=wait['observed_terminal']
  and set(p['starts'])==set(p['returns'])==set(WATCH) and digest(p['starts'])==digest(p['returns'])
  and all(type(x)is int and x in (0,1)for x in p['starts'].values()) and p['starts']['producer']==1
  and p['starts']['milp']==p['starts']['highs'],'P07_WORKER_PROOF')
 for k,n in p['starts'].items():
  f=output/(k+'-started.json')
  if n:
   v=decode(read(f));need(v['kind']==k and v['nonce']==cfg['nonce'] and cfg['start']<=v['clock']<=p['observed_worker_end'],'P07_START_RECORD')
  else:need(not f.exists(),'P07_UNEXPECTED_START_RECORD')
 s_path=output/'stock/summary.json';r_path=output/'stock/reports.json'
 s_b,r_b=read(s_path),read(r_path);s,r=decode(s_b),decode(r_b)
 need(s['run_nonce']==cfg['nonce'] and s['choice']==CHOICE and s['schema']=='CORE_CHOICE_STUDY_V1'
  and s['completed']is True and s['integrity_verified']is True and
  all(s[k] is False for k in ('accepted','qualified','display_allowed','delivery_allowed')),'P07_STOCK_SUMMARY')
 need(all(s[k]==cfg['inputs'][k]for k in ('raw_digest','profile_digest','core_digest')),'P07_STOCK_INPUTS')
 need(set(r)==set(s['report_digests']) and all(digest(v)==s['report_digests'][k] for k,v in r.items()),'P07_ORIGINAL_REPORT_DIGESTS')
 result={'schema':'P07_PRIVATE_FULL_BAND_TERMINAL_V1','choice':CHOICE,'nonce':cfg['nonce'],'wait':wait,
  'state':'VERIFIED_NONADMISSION','scope':'PRIVATE_ONE_CHOICE_CONCEPT_STUDY_ONLY',
  'stock_summary_sha256':sha(s_b),'stock_originals_sha256':sha(r_b),'worker':p,**DENIED}
 if s['state']=='NO_PROPOSAL_NO_INFEASIBILITY_CLAIM':
  b=read(output/'no-witness-proposal.json');q=decode(b)
  from front_rear_runtime_adapter import proposal_disposition
  state=proposal_disposition(q)
  need(not r and not (output/'packet-checkpoint.json').exists() and sha(b)==p['proposal_only_sha256']
   and state==s['producer_status'] and state!='PROPOSAL_ONLY','P07_NO_WITNESS_PROOF')
  if not p['starts']['milp']:
   need(state=='NO_PROPOSAL_IN_THIS_PROGRAM' and q.get('reason')=='ROOM_OR_CORE_BOUND_CONFLICT','P07_PRE_SOLVER_STOP')
  else:
   j=p['solver_status'];i=p['incumbent']
   need(type(j)is int and j==q.get('solver_status') and type(i)is bool and q.get('budget_seconds')==SOLVER and
    ((state=='SEARCH_TIMEOUT_NO_WITNESS' and j==1 and i is False) or
     (state=='NO_PROPOSAL_IN_THIS_TOPOLOGY' and j in (2,3,4) and i is False) or
     (state=='ROUNDED_PROPOSAL_REJECTED' and j in (0,1) and i is True)),'P07_NO_WITNESS_TELEMETRY')
  label=('VERIFIED_SOLVER_FAULT_NO_INFEASIBILITY_CLAIM' if p.get('solver_status') in (3,4) else
         'VERIFIED_SOLVER_TIMEOUT_NO_WITNESS' if state=='SEARCH_TIMEOUT_NO_WITNESS' else
         'VERIFIED_BOUNDED_NO_WITNESS_NO_INFEASIBILITY_CLAIM')
  result.update(state=label,producer_status=state)
 else:
  need(s['state']=='FULL_REPORTS_RETAINED_NOT_QUALIFIED' and s['producer_status']=='PROPOSAL_ONLY'
   and p['starts']['milp']==1 and type(p.get('solver_status'))is int and p['solver_status'] in (0,1) and p['incumbent']is True
   and set(r)==REPORTS,'P07_COMPLETE_ORIGINAL_REPORT_SET')
  b=read(output/'packet-checkpoint.json');v=decode(b)
  need(sha(b)==p['capture_sha256'],'P07_CAPTURE_READBACK')
  mh=bind_packet(v,cfg);c=v['packet'];m=c['world_model'];a=r['independent_replay']
  need(s['model_digest']==mh==r['physical']['model_hash']==a['model_hash'] and a['authority']is False and
   a['verified']is True and a['receipt_digest']==s['receipt_digest']==digest(v['receipt'])
   and s['independent_origin_verified']is True and s['source_digest']==digest(v['snap']),'P07_REASSEMBLY_REPORT_BINDING')
  rep=r['original_replay'];ph=r['physical']
  bind_original_reports(rep,ph,mh,v['ctx']['construction_trace'],s,cfg['source']['engine_revision'])
  f=stock();expected={'core_partition','core_concept','opening_hosts'}
  direct={k:r[k]for k in expected};recomputed=f.core_predicates(m,v['core'])
  # Stock report ordering is preserved; a mismatch is not normalized.
  need(digest(direct)==digest(recomputed),'P07_DIRECT_GEOMETRY_READBACK')
  verified=f.predicates_verified(direct);ca=r['core_assessment'];neg=r['actual_detached_negatives']
  need(type(verified)is bool and ca['core_scoped_verified'] is s['core_scoped_verified'] is verified and
   ca['model_hash']==mh and ca['core_hash']==cfg['inputs']['core_digest'] and
   ca['origin_receipt_hash']==a['receipt_digest'] and digest(ca['predicates'])==digest(direct),'P07_GEOMETRY_RECEIPT')
  need(neg['model_hash']==mh and neg['original_unchanged'] is True and neg['all_expected_rejected']is True and
   {x['mutation']for x in neg['rows']}=={'MISSING_LIFT','DUPLICATE_STAIR','ENTRY_FROM_STAIR','OWNERSHIP_OVERLAP','COMMON_ROUTE_THROUGH_OTHER_CORE','EMPTY_COMMON_ROUTE'}
   and len(neg['rows'])==6 and all(x['binding_rejected'] is True and x['direct_geometry_rejected'] is True for x in neg['rows']),'P07_NEGATIVE_RECEIPT')
  result.update(state='VERIFIED_ARCHIVED_WITNESS_NO_ADMISSION',packet_checkpoint_sha256=sha(b),model_digest=mh,core_predicates_verified=verified,
   legacy_replay_verified=rep['verified'],physical_status=ph['status'],physical_errors=len(ph['errors']),physical_pending=len(ph['pending']),
   current_four='NOT_EVALUATED_CORE_CHOICE_ADAPTER_MISSING')
 need(read(s_path)==s_b and read(r_path)==r_b and (not result.get('packet_checkpoint_sha256') or
  sha(read(output/'packet-checkpoint.json'))==result['packet_checkpoint_sha256']) and source()==cfg['source'] and time.monotonic()<cfg['deadline'],'P07_END_INTEGRITY_OR_DEADLINE')
 return result

class Cutoff(BaseException):pass
def run(root,start):
 cfg={'schema':'P07_PRIVATE_LAUNCH_V1','nonce':uuid.uuid4().hex,'choice':CHOICE,'start':start,'deadline':start+SECONDS,'source':source(),'inputs':inputs()}
 cfg_valid(cfg);need(time.monotonic()+SOLVER<cfg['deadline'],'P07_NO_TIME_BEFORE_SPAWN')
 write(root/'launch.json',cfg)
 child=None
 timed=False
 with (root/'worker.stdout').open('xb')as log,(root/'worker.stderr').open('xb')as err:
  old=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM,signal.SIGTERM,signal.SIGINT})
  try:
   try:child=subprocess.Popen([sys.executable,'-B',str(SELF),'--worker',str(root)],cwd=ROOT,start_new_session=True,stdout=log,stderr=err)
   finally:signal.pthread_sigmask(signal.SIG_SETMASK,old)
   try:child.wait(timeout=max(0,cfg['deadline']-time.monotonic()))
   except subprocess.TimeoutExpired:timed=True
  finally:
   if child is not None and child.poll() is None:
    try:os.killpg(child.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    child.wait()
 wait={'exit':child.returncode,'timeout':timed,'reaped':child.poll() is not None,'observed_terminal':time.monotonic()}
 write(root/'process-observation.json',wait)
 return archive_report(root,cfg,wait)

def final_result(root,deadline,fn):
 def expire(_sig,_frame):raise Cutoff()
 def external_stop(_sig,_frame):raise KeyboardInterrupt()
 signal.signal(signal.SIGALRM,expire);signal.signal(signal.SIGTERM,external_stop)
 signal.setitimer(signal.ITIMER_REAL,max(.000001,deadline-time.monotonic()))
 try:
  try:
   v=fn()
   need(time.monotonic()<deadline,'P07_RESULT_DEADLINE')
   write(root/'receipt.json',v)
   if time.monotonic()>=deadline:raise Cutoff()
  except ValueError as e:
   v={'state':'FAILED_CLOSED','error_code':str(e) if re.fullmatch('P07_[A-Z0-9_]+',str(e)) else 'UNCLASSIFIED_VALIDATION_ERROR',**DENIED}
  except Exception as e:v={'state':'FAILED_CLOSED','error_type':type(e).__name__,**DENIED}
 except Cutoff:v={'state':'DEADLINE_EXPIRED_PRIVATE_PARTIAL_ONLY',**DENIED}
 except KeyboardInterrupt:v={'state':'INTERRUPTED_PRIVATE_PARTIAL_ONLY',**DENIED}
 finally:signal.setitimer(signal.ITIMER_REAL,0)
 if v['state'] in ('FAILED_CLOSED','DEADLINE_EXPIRED_PRIVATE_PARTIAL_ONLY','INTERRUPTED_PRIVATE_PARTIAL_ONLY'):
  a=root/'receipt.json'
  if a.exists():os.replace(a,root/'forensic-late-receipt.json')
  write(root/'terminal-unverified.json',v)
 return v
def main():
 start=time.monotonic()
 pa=argparse.ArgumentParser(description=__doc__)
 g=pa.add_mutually_exclusive_group(required=True);g.add_argument('--private-output',type=Path);g.add_argument('--worker',type=Path)
 a=pa.parse_args();os.umask(0o077)
 if a.worker is not None:
  worker(a.worker);return
 p=a.private_output;need(private_dir(p.parent) and p.resolve()==p,'P07_PRIVATE_PARENT')
 p.mkdir(mode=0o700,exist_ok=False)
 v=final_result(p,start+SECONDS,lambda:run(p,start))
 print(json.dumps({'state':v['state'],**DENIED},sort_keys=True))
if __name__=='__main__':main()
