"""Private P28 child-only study; original parent and reference matrix are external pinned evidence."""
import argparse, copy, hashlib, inspect, io, json, math, os, re, signal, stat, subprocess, sys, time, zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
SELF=Path(__file__).resolve()
LOCAL=BASE/'app/local_integration'
ENGINE=BASE/'app/reconstruction357/planha_general150_runtime_work'
GUARD=BASE/'app/reconstruction357/staging400_e1_5_schema_states'
sys.path[:0]=[str(LOCAL),str(ENGINE),str(GUARD),str(BASE/'studies'),str(BASE/'studies/r4'),str(BASE/'frontend')]
RAW={'W':'18','L':'20','n':2,'requested_count':1}
BODY=b'{"W":"18","L":"20","n":2}'
CAUSE='PLANNED_ENTRY_PANEL_AND_KITCHEN_MOTION'
CHOICE='SIDE_ROOTED_SERVICES'
SOLVER=30
LIMIT=720
CAP=64*1024*1024
DENIED={k:False for k in ('accepted','qualified','display_allowed','delivery_allowed','production_supported')}
PUBLIC_BLOBS={'studies/guest_compound_candidate_p27.py':'ec24ca95f7fe70a7878510f890bce21bc142ae3d',
 'app/local_integration/guest_master_p11.py':'3bac2538375766a97d237d06faae9b28ef0f0d9a',
 'studies/p25_bound_evidence.py':'d071e85959fa67ceb9b9bd7fde60c3ff1067f029'}
CONFIG_KEYS={'parent_archive','parent_cause','guest_receipt','guest_matrix','parent_decision'}
MOD={'CURRENT_PROGRAM_SUITABILITY':'current_programme_evaluator','KITCHEN_GUEST_PATH_SEPARATION':'source_guest_route_evaluator',
     'CONTINUOUS_USEFUL_LIVING':'source_living_evaluator','NONFUNCTIONAL_WALL_EXCLUSION':'source_wall_function_evaluator'}

def need(ok,code):
 if not ok:raise ValueError(code)
def enc(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(v):return sha(enc(v))
def hexn(v,n=64):return type(v)is str and re.fullmatch('[a-f0-9]{'+str(n)+'}',v) is not None
def unique(rows):
 d={}
 for k,v in rows:
  need(k not in d,'P28_DUPLICATE_JSON');d[k]=v
 return d
def bad(_):raise ValueError('P28_NONFINITE_JSON')
def float_token(s):
 v=float(s);need(math.isfinite(v),'P28_NONFINITE_JSON');return v
def decode(b):return json.loads(b,object_pairs_hook=unique,parse_constant=bad,parse_float=float_token)
def private_dir(p):return p.is_absolute() and p.resolve()==p and p.is_dir() and p.stat().st_uid==os.getuid() and stat.S_IMODE(p.stat().st_mode)==0o700
def read(p):
 need(p.is_absolute() and p.resolve()==p,'P28_INPUT_PATH')
 with os.fdopen(os.open(p,os.O_NOFOLLOW|os.O_NONBLOCK|os.O_RDONLY),'rb')as f:
  st=os.fstat(f.fileno());need(stat.S_ISREG(st.st_mode) and st.st_uid==os.getuid() and not st.st_mode&0o077 and 0<=st.st_size<=CAP,'P28_PRIVATE_FILE')
  b=f.read(CAP+1);need(len(b)==st.st_size,'P28_FILE_CHANGED')
 return b
def write(p,v,*,native=False):
 b=(json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode() if native else enc(v))
 tmp=p.with_name('.'+p.name+'.partial')
 with tmp.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 os.link(tmp,p,follow_symlinks=False);tmp.unlink();need(read(p)==b,'P28_WRITE_READBACK')
 return sha(b)
def config(path,want):
 b=read(path);need(hexn(want) and sha(b)==want,'P28_INDEPENDENT_EXTERNAL_MANIFEST')
 v=decode(b)
 need(type(v)is dict and set(v)=={'schema','files'} and v['schema']=='P28_EXTERNAL_PRIVATE_INPUTS_V1'
  and type(v['files'])is dict and set(v['files'])==CONFIG_KEYS,'P28_EXTERNAL_MANIFEST_SHAPE')
 for w in v['files'].values():
  need(type(w)is dict and set(w)=={'path','sha256'} and type(w['path'])is str and hexn(w['sha256'])
   and Path(w['path']).is_absolute(),'P28_EXTERNAL_ENTRY_SHAPE')
 return v
def all_inputs(conf):
 out={}
 for key,row in conf['files'].items():
  b=read(Path(row['path']));need(sha(b)==row['sha256'],'P28_EXTERNAL_BYTES')
  out[key]=b
 return out
def require_origin(fn,path):
 need(Path(inspect.getsourcefile(fn)).resolve()==path,'P28_CALLABLE_SOURCE')
def state(frozen):
 import engine114,guard400,search114,constructor127,construction_replay127,evaluate_pair127
 import planned_witness_support108 as support,planned_witness_contract108 as c
 import guest_compound_candidate_p27 as guest,guest_master_p11 as master,p25_bound_evidence as p25,current_four_decision as decision
 from same_version_front_rear_contract import FREEZE,ENGINE_REVISION
 paths={str(SELF.relative_to(BASE)),*PUBLIC_BLOBS,*support.PINS,
 'app/local_integration/planned_witness_contract108.py','app/local_integration/planned_witness_support108.py',
 'app/local_integration/compound_panel_candidate108.py','app/local_integration/source_fit_profile207.py',
 'app/local_integration/protected_repair_contract.py','app/local_integration/explicit_pair_redirection.py',
 'app/local_integration/program_profile_registry.py',*frozen}
 out={}
 for rel in sorted(paths):
  f=BASE/rel;need(f.resolve()==f and f.is_relative_to(BASE),'P28_SOURCE_PATH')
  b=f.read_bytes()
  if rel in PUBLIC_BLOBS:need(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==PUBLIC_BLOBS[rel],'P28_STAGED_PUBLISHED_SOURCE')
  if rel in frozen:need(sha(b)==frozen[rel],'P28_PARENT_FROZEN_SOURCE')
  out[rel]=sha(b)
 require_origin(c.freeze,LOCAL/'planned_witness_contract108.py')
 require_origin(c.check_child,LOCAL/'planned_witness_contract108.py')
 require_origin(guest.propose,BASE/'studies/guest_compound_candidate_p27.py')
 require_origin(master.entry_source,LOCAL/'guest_master_p11.py')
 require_origin(p25.verify,BASE/'studies/p25_bound_evidence.py')
 require_origin(decision.assemble,LOCAL/'current_four_decision.py')
 for fn,n in ((constructor127.build,'constructor127.py'),(constructor127.context,'constructor127.py'),
  (construction_replay127.verify,'construction_replay127.py'),(evaluate_pair127.evaluate,'evaluate_pair127.py'),(search114.propose,'search114.py')):
  require_origin(fn,ENGINE/n)
 for k,n in MOD.items():
  mod=__import__(n);require_origin(mod.assess,LOCAL/(n+'.py'))
 need(engine114.revision()==ENGINE_REVISION and guard400.guard(FREEZE)==12991 and support.source_guard(),'P28_FROZEN_ENGINE')
 return {'selected':out,'p25':p25.source_state('FRONT_REAR'),'engine_revision':ENGINE_REVISION}

def read_parent(values):
 import live_program_scheduler as live
 with zipfile.ZipFile(io.BytesIO(values['parent_archive']))as z:
  info=z.infolist();names=z.namelist()
  need(len(names)==len(set(names)) and len(names)<=64 and sum(v.file_size for v in info)<=CAP and z.testzip()is None,'P28_ARCHIVE_INVENTORY')
  m=decode(z.read('manifest.json')); rows=m['members']
  need(set(rows)|{'manifest.json'}==set(names) and 'manifest.json'not in rows,'P28_ARCHIVE_MANIFEST')
  data={}
  for n,w in rows.items():
   b=z.read(n);need(len(b)==w['size'] and sha(b)==w['sha256'],'P28_ARCHIVE_MEMBER')
   data[n]=b
 read_e=lambda n:decode(data['evidence/'+n+'.json'])
 rq=read_e('request');b=read_e('runtime-bundle');complete=read_e('child-complete');d=read_e('decision')
 need(live.bind_completed(complete,rq,b,d)is True and bytes.fromhex(rq['body_hex'])==BODY and hexn(rq['nonce'],32),'P28_PARENT_ORIGINAL_REQUEST')
 pkt=b['packet'];ctx=b['context'];tr=ctx['construction_trace'];m=pkt['world_model'];ph=b['reports']['physical'];rep=b['reports']['replay']
 mh=digest(m);p26=decode(values['parent_cause']);p27=decode(values['guest_receipt']);p25=decode(values['parent_decision'])
 need(pkt['family']==tr['family']=='FRONT_REAR' and digest(tr['raw'])==digest(RAW)
  and mh==b['model_digest']==tr['model_hash']==p26['parent_model_digest']==p27['parent_model_digest'],'P28_PARENT_MODEL')
 need(p26['v3_selected_causes']==[CAUSE] and p26['v3_certificate_digest']==p27['cause_certificate']
  and digest(ph)==b['report_digests']['physical']==p26['retained_original_physical_digest']
  and ph['status']=='FAIL' and rep['verified']is True and rep['model_hash']==mh and rep['trace_hash']==digest(tr),'P28_PARENT_CAUSE_LEDGER')
 need(p27['new_candidate_solved'] is False and p27['matrix_files']['guest_operator_sha256']==sha(values['guest_matrix'])
  and p27['retention']['panel_segments']==7 and p27['retention']['panel_rows']==35 and p27['retention']['optimizer_calls']==0,'P28_PARENT_MATRIX_LEDGER')
 join=p26['v3_scoped_operator_data_contract']
 need(join['contract_digest']==p27['parent_contract_digest'] and join['operator_contract_digest']==p27['operator_contract_digest'],'P28_PARENT_OPERATOR_JOIN')
 v=p25['receipt']
 need(v['model_digest']==mh and v['state']=='BLOCKED' and v['evidence_consistency_verified']is True
  and all(v[k]is False for k in ('accepted','qualified','display_allowed','delivery_allowed')),'P28_PARENT_DECISION_LEDGER')
 return {'request':rq,'bundle':b,'p26':p26,'p27':p27,'p25':p25}
def freeze_parent(arch):
 import planned_witness_contract108 as c
 b=arch['bundle'];q=arch['request'];a=arch['p26'];r=arch['p27']
 pkt=b['packet'];ctx=b['context'];props=ctx['construction_trace']['proposals'];ph=b['reports']['physical'];m=pkt['world_model']
 ss=a['source_hashes_same_c5ee_and_current_afb']
 need(type(ss)is dict and ss and all(type(k)is str and hexn(v)for k,v in ss.items()),'P28_PARENT_SOURCE_SET')
 reason=c.diagnose(m,props,RAW['L'],ph,ctx)
 need(reason['selected_causes']==[CAUSE] and digest(reason)==r['cause_certificate'],'P28_REDERIVED_CAUSE')
 rows=[x for x in reason['rows'] if x['established'] and x['cause']==CAUSE and x['route']=='guest_dining']
 need(len(rows)==2 and sorted(x['unit']for x in rows)==['A','B'],'P28_PARENT_BOTH_ROUTES')
 vv=c.freeze(RAW,pkt,ctx,props,ph,reason,ss,q['nonce'])
 c.bind_parent(vv,RAW,pkt,ctx,props,ph,reason,ss,q['nonce'])
 op=c.candidate_contract(vv)
 need(digest(vv)==r['parent_contract_digest'] and digest(op)==r['operator_contract_digest'],'P28_REDERIVED_OPERATOR')
 return reason,vv,op

def matrix_bytes(data):
 import numpy as np
 with np.load(io.BytesIO(data),allow_pickle=False)as z:
  keys={'data','indices','indptr','matrix_shape','objective','variable_integrality','variable_lower','variable_upper','row_lower','row_upper','metadata_utf8','specs_utf8'}
  need(set(z.files)==keys,'P28_MATRIX_FILE_SET')
  return {k:z[k] for k in keys}
def matrix_scope(a):
 need(a['matrix_shape'].tolist()==[4718,3534],'P28_MATRIX_PRODUCTION_DIMENSIONS')
 rows=decode(a['metadata_utf8'].tobytes())
 counts={}
 for r in rows:
  k=r['group']
  if k.startswith('p27_guest_panel_'):counts[k]=counts.get(k,0)+1
 need(len(rows)==4718 and counts=={'p27_guest_panel_common_guest_root':5,'p27_guest_panel_dining_east':15,'p27_guest_panel_sofa1_use':15},'P28_GUEST_ONLY_ROW_SCOPE')
def exact_matrix(a,args):
 import numpy as np
 x=args['constraints'];A=x.A.tocsr();bounds=args['bounds']
 raw={'data':A.data,'indices':A.indices,'indptr':A.indptr,'matrix_shape':np.array(A.shape),
  'objective':args['c'],'variable_integrality':args['integrality'],'variable_lower':bounds.lb,'variable_upper':bounds.ub,'row_lower':x.lb,'row_upper':x.ub}
 for k,v in raw.items():
  w=np.asarray(v);p=a[k]
  # SciPy aliases some dtypes; compare canonical signed integers/IEEE bytes, including signed zero.
  integer=k in ('indices','indptr','matrix_shape','variable_integrality')
  if integer:need(w.dtype.kind in 'iu' and p.dtype.kind in 'iu','P28_MATRIX_INTEGER_TYPE')
  else:need(w.dtype.kind in 'iuf' and p.dtype.kind in 'iuf','P28_MATRIX_NUMERIC_TYPE')
  typ='<i8' if integer else '<f8'
  need(w.shape==p.shape and w.astype(typ).tobytes()==p.astype(typ).tobytes(),'P28_ACTUAL_SOLVER_MATRIX_MISMATCH')
 return {'match':True,'shape':list(A.shape),'arrays':len(raw)}
def classify_child(proposal,proof):
 from front_rear_runtime_adapter import proposal_disposition
 s=proposal_disposition(proposal);starts=proof['starts']
 need(type(starts)is dict and set(starts)==set(proof['returns'])=={'operator','milp','highs'} and
  all(type(x)is int and x in (0,1)for x in (*starts.values(),*proof['returns'].values())) and
  starts==proof['returns'] and starts['operator']==1 and starts['milp']==starts['highs'],'P28_WORKER_CALL_COUNTS')
 if starts['milp']==0:
  need(s=='NO_PROPOSAL_IN_THIS_PROGRAM' and proposal.get('reason')=='ROOM_OR_CORE_BOUND_CONFLICT','P28_PRE_SOLVER_REJECTION')
  return 'BOUND_CONFLICT_NO_OPTIMIZER'
 j=proof.get('solver_status');i=proof.get('incumbent')
 need(type(j)is int and j==proposal.get('solver_status') and type(i)is bool and proposal.get('budget_seconds')==SOLVER
  and proof.get('matrix',{}).get('match') is True,'P28_SOLVER_METADATA')
 if s=='PROPOSAL_ONLY':
  need(j in (0,1) and i is True,'P28_WITNESS_STATUS')
  return 'WITNESS'
 if s=='ROUNDED_PROPOSAL_REJECTED':
  need(j in (0,1) and i is True,'P28_ROUNDING_METADATA')
  return 'ROUNDED_WITNESS_REJECTED'
 if s=='SEARCH_TIMEOUT_NO_WITNESS':
  need(j==1 and i is False,'P28_TIMEOUT_METADATA')
  return 'SOLVER_TIMEOUT_NO_WITNESS'
 need(s=='NO_PROPOSAL_IN_THIS_TOPOLOGY' and j in (2,3,4) and i is False,'P28_NO_WITNESS_METADATA')
 return 'BOUNDED_NO_WITNESS'if j==2 else'SOLVER_FAULT_NO_WITNESS'
def actual_routes(model):
 units=model['units']
 if [u.get('id')for u in units]!=['A','B']:return False
 return all(type(u.get('scenario_routes')) is dict and type(u['scenario_routes'].get('guest_dining')) is list
  and len(u['scenario_routes']['guest_dining'])>=2 for u in units)
def resolve(parent,child_result,protection,model):
 need(type(protection)is dict and protection.get('protected_verified')is True,'P28_PROTECTED_CHILD')
 target=[x for x in child_result['rows'] if x['cause']==CAUSE and x.get('route')=='guest_dining']
 yes=(actual_routes(model) and len(target)==2 and sorted(x['unit']for x in target)==['A','B'] and all(
  x['state']=='ACTUAL_STORED_PATH_CLEAR_ORIGINAL_PROFILE' and type(x.get('original_missing_route_count'))is int and
  x['original_missing_route_count']==0 for x in target))
 success=(yes and child_result['selected_causes']==[] and parent['selected_causes']==[CAUSE])
 return {'state':'BOTH_ACTUAL_STORED_GUEST_ROUTES_RESOLVED_NO_ADMISSION' if success else'CHILD_NOT_PROVEN_TARGET_RESOLVED',
  'fresh_both_stored_guest_dining_clear':yes,'no_new_supported_cause':child_result['selected_causes']==[],
  'protected_verified':True,'quality_claim':False,**DENIED}

def collect(folder,nonce,parent,reason,contract,proposal):
 import constructor127,construction_replay127,evaluate_pair127
 import planned_witness_contract108 as c,planned_witness_support108 as support
 import front_rear_runtime_adapter as fr,current_four_decision as d
 import p25_bound_evidence as p25
 from core_choice_pair_study import bind_program
 from program_profile_registry import lookup
 prop,tr=fr.proposal_transport(proposal)
 props={'A':prop,'B':copy.deepcopy(prop)}
 write(folder/'proposal-transport.json',tr)
 write(folder/'child-proposals.json',props,native=True)
 pkt=fr.transport(constructor127.build(RAW,'FRONT_REAR',props['A'],props['B']))[0]
 ctx=fr.transport(constructor127.context(RAW,pkt,props))[0]
 m=pkt['world_model'];mh=digest(m)
 write(folder/'child-packet-context.json',{'packet':pkt,'context':ctx,'model_digest':mh},native=True)
 bind_program(m,lookup('PROGRAM_2BED_V1'))
 need(fr.packet_binding(pkt,ctx,RAW,prop)==mh and mh!=parent['bundle']['model_digest'],'P28_NEW_CHILD_PACKET_BINDING')
 pin=digest([pkt,ctx,props])
 rp=construction_replay127.verify(m,ctx)
 write(folder/'original-replay.json',rp)
 ph=evaluate_pair127.evaluate(pkt,ctx)
 write(folder/'original-physical.json',ph)
 need(rp['verified'] is True and rp['model_hash']==mh and rp['trace_hash']==digest(ctx['construction_trace'])
  and ph['model_hash']==mh and digest(ph['multiproposal_provenance127'])==digest(rp),'P28_CHILD_ORIGINAL_BINDING')
 originals={'replay':rp,'physical':ph}
 b={'schema':'P28_CHILD_BOUND_EVALUATION_BUNDLE_V1','engine_revision':rp['source_revision'],'packet':pkt,'context':ctx,'model_digest':mh,
    'reports':originals,'report_digests':{k:digest(v)for k,v in originals.items()},**DENIED}
 write(folder/'child-bound-bundle.json',b,native=True)
 bpin=digest(b);current={};all_validation_errors={}
 # Canonical V1 order, including after JSON checkpoint.
 need(list(MOD)==list(d.SCHEMAS),'P28_CRITERION_ORDER')
 for cid,module in MOD.items():
  mod=__import__(module)
  try:
   r=mod.assess(b)
   write(folder/(cid+'.json'),r)
   current[cid]=r
   c.validate_current_report(r,mh)
   support.bind_current(module,r,b)
   need(digest(b)==bpin,'P28_CHILD_REPORT_MUTATION')
  except Exception as error:
   all_validation_errors[cid]={'type':type(error).__name__,'code':safe_error(error)}
 write(folder/'current-validation.json',all_validation_errors)
 report_checks={}
 # Always retain the child and all actual reports, even when protection fails.
 try:
  protect=c.check_child(contract,pkt,props);write(folder/'child-protection.json',protect)
 except Exception as err:
  protect=None;report_checks['protection']=safe_error(err)
 try:
  ch=c.diagnose(m,props,RAW['L'],ph,ctx);write(folder/'child-cause.json',ch)
  vr=c.resolution(reason,ch);write(folder/'v3-resolution.json',vr)
 except Exception as err:
  ch=None;report_checks['target_diagnostics']=safe_error(err)
 write(folder/'child-report-checks.json',report_checks)
 need(digest([pkt,ctx,props])==pin and digest(b)==bpin,'P28_CHILD_EVIDENCE_MUTATION')
 if all_validation_errors or set(current)!=set(MOD) or ch is None or protect is None:
  return {'state':'CHILD_RETAINED_REQUIRED_CHECKS_UNVERIFIED','model_digest':mh,'cause_repair_verified':False,**DENIED}
 decide=d.assemble(b,current,{k:digest(v)for k,v in current.items()})
 write(folder/'decision-v1.json',decide,native=True)
 anchors={'schema':p25.PIN_SCHEMA,'bundle_digest':bpin,'assessment_digests':{k:digest(v)for k,v in current.items()},'v1_decision_digest':digest(decide)}
 h=write(folder/'child-worker-evidence-anchors.json',{'nonce':nonce,'anchors':anchors,'canonical_anchor_sha256':digest(anchors)})
 out=resolve(reason,ch,protect,m)
 need(out['fresh_both_stored_guest_dining_clear']==vr['all_target_causes_resolved'],'P28_RESOLUTION_REDERIVATION')
 return {'state':out['state'],'model_digest':mh,'cause_repair_verified':out['state']=='BOTH_ACTUAL_STORED_GUEST_ROUTES_RESOLVED_NO_ADMISSION',
  'anchor_file_sha256':h,**DENIED}
def safe_error(e):
 v=str(e)
 # Only own coded validation conditions; private tracebacks are never public/CLI output.
 return v if re.fullmatch('P28_[A-Z0-9_]+',v) else 'SCOPED_CHILD_STAGE_UNVERIFIED'
def started_worker(folder):
 import guest_compound_candidate_p27 as guest, search114,compound_panel_candidate108,cause_directed_candidate108,source_fit_candidate207
 import scipy.optimize as opt,scipy.optimize._milp as sm
 need(private_dir(folder) and private_dir(folder.parent),'P28_WORKER_DIRECTORY')
 launch=decode(read(folder/'launch.json'));deadline=launch['deadline'];nonce=launch['nonce']
 need(hexn(nonce,32) and launch['start']<=time.monotonic()<deadline and deadline-launch['start']==LIMIT,'P28_WORKER_DEADLINE')
 conf=config(Path(launch['input_config']),launch['input_config_sha256']);values=all_inputs(conf)
 parent=read_parent(values);frozen=parent['p26']['source_hashes_same_c5ee_and_current_afb']
 src=state(frozen);need(digest(src)==launch['selected_source_digest'],'P28_WORKER_SOURCE')
 arrays=matrix_bytes(values['guest_matrix']);matrix_scope(arrays)
 proof={'schema':'P28_WORKER_EXECUTION_V1','nonce':nonce,'input_config_sha256':launch['input_config_sha256'],
  'starts':dict.fromkeys(('operator','milp','highs'),0),'returns':dict.fromkeys(('operator','milp','highs'),0),'faults':[]}
 watches={guest.propose.__code__:'operator',sm.milp.__code__:'milp',sm._highs_wrapper.__code__:'highs'}
 forbidden={m.propose.__code__ for m in (search114,compound_panel_candidate108,cause_directed_candidate108,source_fit_candidate207)}
 need(guest.milp.__code__ is opt.milp.__code__ is sm.milp.__code__,'P28_WATCHED_MILP_ALIAS')
 expected_op=parent['p27']['operator_contract_digest']
 def check(code,_):
  f=sys._getframe(1);l=f.f_locals
  try:
   need(code not in forbidden,'P28_NO_PARENT_OR_FALLBACK_PROPOSER')
   name=watches[code]
   need(proof['starts'][name]==0 and time.monotonic()<deadline,'P28_DUPLICATE_OR_LATE_CALL')
   if name=='operator':
    need(f.f_back.f_code is started_worker.__code__ and l['diagnostic_capture']is None and l['fixed_witness']is None
     and l['bedrooms']==2 and l['variant']==0 and l['ordered_macro']is False and l['topology']==CHOICE
     and l['organization_profile']=='UNRESTRICTED' and l['sleep_roles']==['double','twin']
     and l['time_limit']==SOLVER and l['enabled_causes']==['KITCHEN_GUEST_MOTION']
     and digest(l['core'])==digest(parent['bundle']['packet']['core']) and digest(l['parent_contract'])==expected_op,'P28_SOLVE_OPERATOR_SCOPE')
   elif name=='milp':
    need(f.f_back.f_code is guest.propose.__code__ and l['options']=={'time_limit':SOLVER,'mip_rel_gap':.02,'presolve':True}
     and deadline-time.monotonic()>=SOLVER,'P28_SOLVER_OPTIONS')
    proof['matrix']=exact_matrix(arrays,l)
    proof['matrix']['reviewed_input_sha256']=sha(values['guest_matrix'])
   else:need(f.f_back.f_code is sm.milp.__code__ and proof.get('matrix',{}).get('match')is True,'P28_HIGHS_MATRIX_GUARD')
   write(folder/(name+'-start.json'),{'clock':time.monotonic(),'nonce':nonce,'call':name,
    **({'matrix':proof['matrix']} if name=='milp' else {})})
   proof['starts'][name]+=1
  except Exception as e:
   proof['faults'].append(safe_error(e));raise
 def finish(code,_,v):
  name=watches[code];proof['returns'][name]+=1
  if name=='milp':proof.update(solver_status=int(v.status),incumbent=v.x is not None)
 mm=sys.monitoring;e=mm.events;i=4
 mm.use_tool_id(i,'P28 one exact child optimizer')
 mm.register_callback(i,e.PY_START,check);mm.register_callback(i,e.PY_RETURN,finish)
 for code in watches:mm.set_local_events(i,code,e.PY_START|e.PY_RETURN)
 for code in forbidden:mm.set_local_events(i,code,e.PY_START)
 try:
  reason,contract,operator=freeze_parent(parent)
  write(folder/'parent-rederived-cause.json',reason);write(folder/'parent-rederived-contract.json',contract)
  write(folder/'parent-operator-translation.json',operator)
  need(time.monotonic()+SOLVER<deadline,'P28_NO_TIME_FOR_ONE_CHILD')
  proposal=guest.propose(parent['bundle']['packet']['core'],2,time_limit=SOLVER,variant=0,sleep_roles=['double','twin'],
    ordered_macro=False,topology=CHOICE,parent_contract=operator,enabled_causes=operator['enabled_causes'])
  # np.float64 coordinates use exact JSON-compatible scalars; retain before full gates.
  write(folder/'solver-proposal-observed.json',proposal,native=True)
  kind=classify_child(proposal,proof)
  result=collect(folder,nonce,parent,reason,contract,proposal) if kind=='WITNESS' else {
    'state':'CHILD_'+kind,'model_digest':None,'cause_repair_verified':False,**DENIED}
  result.update(disposition=kind)
 except Exception as err:
  result={'state':'FAILED_CLOSED_PARTIAL_PRIVATE_ONLY','cause_repair_verified':False,
   'error':safe_error(err),'type':type(err).__name__,**DENIED}
 finally:
  for code in set(watches)|forbidden:mm.set_local_events(i,code,0)
  mm.free_tool_id(i)
 need(state(frozen)==src and all_inputs(conf)==values and time.monotonic()<deadline,'P28_WORKER_SOURCE_OR_CUTOFF')
 proof.update(result=result,source_digest=digest(src),worker_end=time.monotonic(),files=files(folder,exclude={'worker-complete.json'}))
 write(folder/'worker-complete.json',proof)

def files(folder,*,exclude=frozenset()):
 out={}
 for p in sorted(folder.iterdir()):
  need(p.is_file() and not p.is_symlink(),'P28_OUTPUT_FILE_SHAPE')
  if p.name not in exclude:out[p.name]=sha(read(p))
 return out
def final_bind(folder,launch,conf,values,src,at):
 import p25_bound_evidence as p25
 import planned_witness_contract108 as c
 worker=decode(read(folder/'worker-complete.json'));nonce=launch['nonce']
 need(worker['schema']=='P28_WORKER_EXECUTION_V1' and worker['nonce']==nonce and worker['input_config_sha256']==launch['input_config_sha256']
  and worker['source_digest']==digest(src) and launch['start']<=worker['worker_end']<=at<launch['deadline']
  and worker['files']==files(folder,exclude={'worker-complete.json','outside-parent-process-observed.json','child-p25-private.json'}),'P28_WORKER_EVIDENCE_READBACK')
 result=worker['result'];state_name=result['state']
 if state_name in ('BOTH_ACTUAL_STORED_GUEST_ROUTES_RESOLVED_NO_ADMISSION','CHILD_NOT_PROVEN_TARGET_RESOLVED'):
  get=lambda n:decode(read(folder/(n+'.json')))
  need(worker['faults']==[] and classify_child(get('solver-proposal-observed'),worker)=='WITNESS','P28_READBACK_WITNESS')
  ab=read(folder/'child-worker-evidence-anchors.json')
  need(sha(ab)==result['anchor_file_sha256'],'P28_ARCHIVAL_ANCHOR_BYTES')
  anchor=decode(ab);pins=anchor['anchors']
  need(anchor['nonce']==nonce and digest(pins)==anchor['canonical_anchor_sha256'],'P28_ARCHIVAL_ANCHOR_NONCE')
  b=get('child-bound-bundle');ds=get('decision-v1');assess={k:get(k)for k in MOD}
  pkt=get('child-packet-context');props=get('child-proposals')
  need(digest(pkt['packet'])==digest(b['packet']) and digest(pkt['context'])==digest(b['context'])
   and digest(props)==digest(b['context']['construction_trace']['proposals'])
   and digest(get('original-replay'))==b['report_digests']['replay']
   and digest(get('original-physical'))==b['report_digests']['physical'],'P28_READBACK_ORIGINAL_PACKET')
  # External to the verifier: worker-witnessed digests/nonce already checked
  # against the authenticated local launch and terminal proof before invocation.
  v=p25.verify(b,assess,ds,pins,anchor['canonical_anchor_sha256'])
  need(v['evidence_consistency_verified']is True and v['state']=='BLOCKED' and v['model_digest']==result['model_digest'] and
   all(v[k]is False for k in p25.AUTH+('execution_authenticity_verified','product_coverage_verified')),'P28_P25_NONADMISSION')
  parent=get('parent-rederived-cause');ct=get('parent-rederived-contract');child=get('child-cause')
  cp=c.check_child(ct,b['packet'],props)
  need(digest(cp)==digest(get('child-protection')) and digest(c.resolution(parent,child))==digest(get('v3-resolution')),'P28_READBACK_CHILD_PROTECTION')
  need(resolve(parent,child,cp,b['packet']['world_model'])['state']==state_name,'P28_READBACK_RESOLUTION')
  write(folder/'child-p25-private.json',v)
 elif state_name.startswith('CHILD_') and result.get('model_digest') is None:
  kind=classify_child(decode(read(folder/'solver-proposal-observed.json')),worker)
  need(worker['faults']==[] and state_name=='CHILD_'+kind and kind!='WITNESS','P28_READBACK_NO_WITNESS')
 need(state(read_parent(values)['p26']['source_hashes_same_c5ee_and_current_afb'])==src
  and all_inputs(conf)==values and time.monotonic()<launch['deadline'],'P28_FINAL_SOURCE_OR_CUTOFF')
 return {'schema':'P28_PRIVATE_TERMINAL_V1',**result,'nonce':nonce,'parent_was_regenerated':False,
  'child_solver_calls':worker['starts']['milp'],'worker_reaped_at':at,'outer_deadline':launch['deadline'],
  'independent_scoped_p25_receipt':(folder/'child-p25-private.json').exists(),**DENIED}
class Cutoff(BaseException):pass
def execute(root,path,want,start,deadline):
 import uuid
 conf=config(path,want);values=all_inputs(conf);parent=read_parent(values)
 src=state(parent['p26']['source_hashes_same_c5ee_and_current_afb'])
 launch={'schema':'P28_PRIVATE_LAUNCH_V1','start':start,'deadline':deadline,'nonce':uuid.uuid4().hex,'input_config':str(path),
  'input_config_sha256':want,'selected_source_digest':digest(src)}
 write(root/'launch.json',launch)
 proc=None;timed=False
 need(time.monotonic()+SOLVER<deadline,'P28_BEFORE_WORKER_BUDGET')
 with (root/'worker.stdout').open('xb')as out,(root/'worker.stderr').open('xb')as err:
  mask=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM,signal.SIGTERM,signal.SIGINT})
  try:
   try:proc=subprocess.Popen([sys.executable,'-B',str(SELF),'--worker',str(root)],cwd=BASE,start_new_session=True,stdout=out,stderr=err)
   finally:signal.pthread_sigmask(signal.SIG_SETMASK,mask)
   try:proc.wait(timeout=max(0,deadline-time.monotonic()))
   except subprocess.TimeoutExpired:timed=True
  finally:
   if proc is not None and proc.poll()is None:
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    proc.wait()
 at=time.monotonic()
 write(root/'outside-parent-process-observed.json',{'at':at,'exit':proc.returncode,'timed_out':timed,'wait_completed':proc.poll()is not None})
 need(proc.returncode==0 and not timed and at<deadline,'P28_CHILD_PROCESS_OR_CUTOFF')
 return final_bind(root,launch,conf,values,src,at)
def stop_safe(root,deadline,run):
 def clock(*_):raise Cutoff()
 def stop(*_):raise KeyboardInterrupt()
 signal.signal(signal.SIGALRM,clock);signal.signal(signal.SIGTERM,stop)
 signal.setitimer(signal.ITIMER_REAL,max(.000001,deadline-time.monotonic()))
 try:
  try:
   v=run()
   if time.monotonic()>=deadline:raise Cutoff()
   write(root/'receipt.json',v)
   if time.monotonic()>=deadline:raise Cutoff()
  except Exception as e:v={'state':'FAILED_CLOSED_PARTIAL_PRIVATE_ONLY','error':safe_error(e),'type':type(e).__name__,**DENIED}
 except Cutoff:v={'state':'DEADLINE_PRIVATE_PARTIAL_ONLY',**DENIED}
 except KeyboardInterrupt:v={'state':'INTERRUPTED_PRIVATE_PARTIAL_ONLY',**DENIED}
 finally:signal.setitimer(signal.ITIMER_REAL,0)
 if v['state'] in ('FAILED_CLOSED_PARTIAL_PRIVATE_ONLY','DEADLINE_PRIVATE_PARTIAL_ONLY','INTERRUPTED_PRIVATE_PARTIAL_ONLY'):
  if (root/'receipt.json').exists():os.replace(root/'receipt.json',root/'late-forensic-receipt.json')
  write(root/'terminal-unverified.json',v)
 return v
def main():
 start=time.monotonic();os.umask(0o077)
 a=argparse.ArgumentParser(description=__doc__)
 g=a.add_mutually_exclusive_group(required=True);g.add_argument('--private-output',type=Path);g.add_argument('--worker',type=Path)
 a.add_argument('--inputs',type=Path);a.add_argument('--inputs-sha256')
 args=a.parse_args()
 if args.worker is not None:
  need(args.inputs is None and args.inputs_sha256 is None,'P28_WORKER_ARGS');started_worker(args.worker);return
 o=args.private_output
 need(args.inputs is not None and hexn(args.inputs_sha256) and private_dir(o.parent) and o.resolve()==o,'P28_PRIVATE_SETUP')
 o.mkdir(mode=0o700,exist_ok=False)
 v=stop_safe(o,start+LIMIT,lambda:execute(o,args.inputs,args.inputs_sha256,start,start+LIMIT))
 print(json.dumps({'state':v['state'],**DENIED},sort_keys=True))
if __name__=='__main__':main()
