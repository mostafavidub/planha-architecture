"""P14 explicit P1/n2 FRONT_REAR study. Never a public scheduler/fallback."""
import argparse,copy,hashlib,inspect,json,os
from pathlib import Path
from fractions import Fraction as F
from front_rear_runtime_adapter import ROOT,ENGINE,AUTHORITY,transport,source_audit,verify_reports,proposal_disposition
from same_version_front_rear_contract import ENGINE_REVISION,digest
from one_bed_pair_source_study import normalize_proposal,program_bind
from current_programme_evaluator import placed,rect
from producer_provenance import snapshot,require_unchanged
import current_four_decision as four
from program_profile_registry import lookup

PROGRAMME='PROGRAM_1BED_V1'
CID='CURRENT_PROGRAM_SUITABILITY'
P1_SCHEMA='P14_ONE_BED_PAIR_PROGRAMME_STUDY_V1'
RAW={'W':'18','L':'20','n':2,'requested_count':1}
SOLVER_SECONDS=30
SOURCES={
 CID:{'app/local_integration/one_bed_pair_p14.py','app/local_integration/one_bed_pair_source_study.py',
      'app/local_integration/current_programme_evaluator.py','app/local_integration/program_profile_registry.py',
      'app/local_integration/current_entry_boundary_x03.py','specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json'}
}
PATHS=set.union(*four.REQUIRED_SOURCES.values(),*SOURCES.values())|{'app/local_integration/'+k for k in
 ('current_four_decision.py','front_rear_runtime_adapter.py','same_version_front_rear_contract.py','producer_provenance.py')}
MODS={'bed1':'PRIVATE_ROOM_MODULE116','bath':'BATHROOM_MODULE117','kitchen':'KITCHEN_MODULE117'}
ALWAYS_FALSE={k:False for k in AUTHORITY}

def need(ok,code):
 if not ok:raise ValueError(code)

def prepare(body):
 from current_entry_boundary_x03 import public_request
 env,raw=public_request(body)
 need(digest(raw)==digest(RAW),'P14_ONLY_18X20_N2')
 profile=lookup(PROGRAMME)
 need(profile['approval']['status']=='APPROVED_DESIGN_PROGRAM','P14_APPROVAL')
 return {'schema':'P14_EXPLICIT_PRIVATE_STUDY_REQUEST_V1','body_sha256':hashlib.sha256(body).hexdigest(),
  'raw':raw,'envelope':env,'programme':profile,'programme_digest':digest(profile),
  'family':'FRONT_REAR','variant':0,'solver_seconds':SOLVER_SECONDS,**ALWAYS_FALSE}

def select_fit(assessment):
 cap=assessment['reports']['capacity'];rows=cap['evidence']['units']
 need(type(cap['errors']) is list and all(type(e) is dict for e in cap['errors']) and type(rows) is list
      and all(type(r) is dict and r['unit'] in ('A','B') and type(r['residents_study']) is int
       and r['residents_study']==2 and type(r['actual_places']['sleeping_places']) is int
       and r['actual_places']['sleeping_places']>=0 for r in rows)
      and len({r['unit']for r in rows})==len(rows),'P14_TYPED_CAPACITY_EVIDENCE')
 # Physical collisions, malformed evaluator data and missing quality evidence
 # are not proof of a rule violation for this newer programme-quality layer.
 proven=any(r.get('code')=='ACTUAL_CAPACITY_SHORTFALL' and r.get('unit') in ('A','B')
   and r.get('group') in ('sleeping_places','dining_seats','living_seats') for r in cap['errors']) or any(
   r['actual_places']['sleeping_places']!=2 for r in rows)
 return 'FAIL' if proven else 'UNKNOWN'

def inventory(model,profile,catalog):
 from dining_inventory119 import counts
 program_bind(model,profile)
 need(model['fixture_catalog_hash']==digest(catalog),'P14_CATALOG_BINDING')
 rows=[]
 for u in model['units']:
  uid=u['id'];fs=u['fixtures'];parts=[p for p in model['module_placements'] if p['unit_id']==uid]
  need(len(parts)==3 and {p['room_id']for p in parts}==set(MODS),'P14_P1_MODULE_INVENTORY')
  need([k for k in sorted(u['rooms']) if k.startswith('bed')]==['bed1'],'P14_ONE_BEDROOM_PER_UNIT')
  fids=set();aids=set()
  for p in parts:
   mod=p['module'];need(mod['schema']==MODS[p['room_id']] and digest(mod)==p['module_hash'],'P14_MODULE_SOURCE')
   for category,seen in (('fixtures',fids),('activities',aids)):
    for key,q in mod['unit'][category].items():
     target=p['id_map'][key]
     need(target not in seen and placed(q,p['transform'])==rect(u[category][target]),'P14_SOURCE_INSTANCE_BINDING')
     if category=='fixtures':
      need(u['fixture_metadata'][target]['kind']==mod['unit']['fixture_metadata'][key]['kind'],'P14_SOURCE_FIXTURE_KIND')
     seen.add(target)
  dining=u['dining_module_placement'];dm=dining['module']
  need(counts(u)=={'dining_table':1,'dining_chair_front':2,'dining_chair_back':2},'P14_SOURCE_DINING')
  dset=set(dining['id_map'].values());need(not dset&fids,'P14_DINING_ALIAS')
  fids|=dset
  for seat in dm['seating']['instances']:
   aid='dining_'+seat['id'][5:]
   need(aid not in aids and placed(seat['rise_transfer']['standing_body'],dining['transform'])==rect(u['activities'][aid]),'P14_DINING_STANDING')
   aids.add(aid)
  for fid in profile['source_inventory']['living_items']:
   a,b,c,d=rect(fs[fid]);kind=u['fixture_metadata'][fid]['kind'];r=catalog['types'][kind]
   need(kind==fid and fid not in fids and sorted((c-a,d-b))==sorted((F(r['width_m']),F(r['depth_m']))),'P14_LIVING_SOURCE_DIMENSIONS')
   fids.add(fid);aid=fid+'_front';need(aid not in aids,'P14_LIVING_ACTIVITY_ALIAS')
   rect(u['activities'][aid]);aids.add(aid)
  need(set(fs)==fids and set(u['fixture_metadata'])==fids,'P14_WHOLE_FIXTURE_INVENTORY')
  md=u['fixture_metadata'];beds={k for k,v in md.items()if v['kind']in('bed','single_bed')}
  closets={k for k,v in md.items()if v['kind']=='closet'}
  cap=u['public_program']['capacity']
  need(beds=={'bed1.bed'} and closets=={'bed1.closet'} and type(cap['residents']) is int and cap['residents']==2,'P14_SLEEP_CLOSET_PROGRAMME')
  rows.append({'unit':uid,'design_persons':2,'fixtures':len(fids),'source_activities':len(aids),
     'registered_dining_places':4,'registered_living_instances':4,'closet_instances':1,
     'excess_seating_not_automatic_reject_or_capacity_upgrade':True,'clothing_volume':'NOT_VERIFIED'})
 return rows

def binding(bundle):
 originals=bundle['reports'];model=bundle['packet']['world_model'];packet=bundle['packet'];context=bundle['context'];trace=context['construction_trace']
 mh=digest(model);expect=bundle['request'];raw=expect['raw'];profile=expect['programme']
 need(bundle['schema']=='P14_P1_N2_ORIGINAL_RUNTIME_BUNDLE_V1','P14_BUNDLE_SCHEMA')
 need(digest(expect)==digest(prepare(bytes.fromhex(bundle['request_body_hex']))),'P14_REQUEST_BINDING')
 program_bind(model,profile)
 need(digest(profile)==expect['programme_digest']==digest(lookup(PROGRAMME)),'P14_REGISTRY_BINDING')
 need(bundle['model_digest']==mh==digest(packet['local_model'])==trace['model_hash']==trace['local_model_hash']
   and packet['family']==trace['family']=='FRONT_REAR' and packet['admission_claim'] is False,'P14_MODEL_FRAME')
 need(bundle['engine_revision']==trace['source_revision']==ENGINE_REVISION and digest(trace['raw'])==digest(raw)
   and digest(model['inputs'])==digest([raw['W'],raw['L'],2]) and digest(context['inputs'])==digest(model['inputs'])
   and digest(packet['core'])==trace['core_hash'],'P14_ORIGINAL_FRAME')
 from constructor127 import frame
 need(Path(inspect.getsourcefile(frame)).resolve()==ENGINE/'constructor127.py','P14_FRAME_SOURCE_PATH')
 selected_core,_=frame(copy.deepcopy(raw),'FRONT_REAR')
 need(digest(selected_core)==trace['core_hash'],'P14_SELECTED_CORE_BINDING')
 need(context['operation']=='generate_from_dimensions' and context['baseline_model_hash'] is None and context['existing_plan_id'] is None,'P14_ORIGINAL_CONTEXT')
 props=trace['proposals'];p,_=normalize_proposal(bundle['proposal'])
 need(p['status']=='PROPOSAL_ONLY' and set(props)=={'A','B'} and digest(props['A'])==digest(p)==digest(props['B']),'P14_EXACT_P1_PROPOSAL')
 wanted={u:digest(p)for u in ('A','B')}
 need(digest(wanted)==digest(trace['unit_proposal_hashes'])==digest(packet['unit_proposal_hashes']),'P14_PROPOSAL_ASSIGNMENT')
 need(set(originals)==set(bundle['report_digests'])=={'replay','physical'},'P14_ORIGINAL_REPORT_SET')
 verify_reports(originals,bundle['report_digests'])
 replay=originals['replay'];physical=originals['physical']
 need(replay['verified'] is True and not replay['errors'] and not replay['pending'] and replay['source_revision']==ENGINE_REVISION
      and replay['model_hash']==mh and replay['trace_hash']==digest(trace),'P14_REPLAY_BINDING')
 need(physical['model_hash']==mh and physical['accepted'] is False and physical['release'] is False
      and type(physical['errors']) is list and type(physical['pending']) is list
      and digest(physical['multiproposal_provenance127'])==digest(replay),'P14_PHYSICAL_BINDING')
 need(all(bundle[k] is False for k in AUTHORITY),'P14_BUNDLE_AUTHORITY')
 need(type(bundle['source_snapshot']) is dict and set(bundle['source_snapshot'])==PATHS,'P14_RUNTIME_SOURCE_SET')
 require_unchanged(ROOT,bundle['source_snapshot'])
 return model,mh,replay,physical

def assess_programme(bundle):
 import program_capacity_audit118 as cap
 model,mh,replay,physical=binding(bundle)
 need(Path(inspect.getsourcefile(cap.examine)).resolve()==ENGINE/'program_capacity_audit118.py','P14_CAPACITY_SOURCE_PATH')
 inputs=digest(bundle);sources=snapshot(ROOT,sorted(SOURCES[CID]));engine=source_audit()
 result={'schema':P1_SCHEMA,'criterion':CID,'current_domain_policy':'CURRENT_ENTRY_DOMAIN_X03_V1',
  'programme_id':PROGRAMME,'profile_digest':bundle['request']['programme_digest'],'model_digest':mh,
  'historical_physical_report':copy.deepcopy(physical),'historical_physical_digest':digest(physical),
  'reports':{'replay':copy.deepcopy(replay)},'state':'UNKNOWN','findings':[],**ALWAYS_FALSE}
 try:
  catalogue=json.loads((ENGINE/'fixture_catalog114.json').read_bytes())
  result['inventory']=inventory(model,bundle['request']['programme'],catalogue)
  measured=cap.examine(model);result['reports']['capacity']=copy.deepcopy(measured)
  need(measured['evidence']['model_hash']==mh,'P14_CAPACITY_MODEL')
  result['findings']=[{'kind':'MISSING_PROFILE','code':'CALIBRATED_ROOM_AND_UNIT_QUALITY'},
    {'kind':'MISSING_EVIDENCE','code':'CLOTHING_STORAGE_VOLUME_AND_COMPLETE_SIMULTANEITY'},
    {'kind':'NOT_EVALUATED','code':'AP07_SEPARATE_LOWER_PROGRAMME_COMPARISON'}]
  result['state']=select_fit(result)
 except (KeyError,IndexError,ValueError,TypeError,ArithmeticError) as ex:
  result['findings'].append({'kind':'EVALUATOR_OR_SOURCE_BINDING_ERROR','type':type(ex).__name__,'detail':str(ex)})
  result['state']='UNKNOWN'
 require_unchanged(ROOT,sources)
 need(digest(bundle)==inputs and source_audit()==engine,'P14_PROGRAMME_SOURCE_OR_INPUT_CHANGED')
 result['source_snapshot']=sources;result['integrity_verified']=True
 result['report_digests']={k:digest(v)for k,v in result['reports'].items()}
 return result

def decision(bundle,reports,expected_digests):
 model,mh,replay,physical=binding(bundle);pin=digest([bundle,reports,expected_digests])
 need(set(reports)==set(expected_digests)==set(four.SCHEMAS),'P14_FOUR_CRITERIA')
 rows=[];effective={};checked={}
 for name in sorted(four.SCHEMAS):
  row=reports[name];pg=name==CID
  need(digest(row)==expected_digests[name] and row['model_digest']==mh and row['criterion']==name
       and row['schema']==(P1_SCHEMA if pg else four.SCHEMAS[name])
       and row['current_domain_policy']=='CURRENT_ENTRY_DOMAIN_X03_V1','P14_ASSESSMENT_DIGEST_DOMAIN')
  need(all(row[k] is False for k in AUTHORITY),'P14_ASSESSMENT_AUTHORITY')
  need(digest(row['reports']['replay']if pg else row['replay'])==digest(replay),'P14_ASSESSMENT_REPLAY')
  original=row['historical_physical_report'] if pg else row['original_physical_report']
  ph=row['historical_physical_digest'] if pg else row['original_physical_digest']
  need(ph==digest(original)==digest(physical),'P14_ASSESSMENT_PHYSICAL')
  if pg:
   need(row['programme_id']==PROGRAMME and row['profile_digest']==bundle['request']['programme_digest'],'P14_ASSESSMENT_REGISTRY')
   need(set(row['reports'])==set(row['report_digests']) and set(row['reports']) in ({'replay'},{'replay','capacity'}),'P14_PROGRAMME_REPORT_SET')
   verify_reports(row['reports'],row['report_digests'])
   cap=row['reports'].get('capacity')
   if cap is not None:need(cap['evidence']['model_hash']==mh and row['state']==select_fit(row),'P14_CAPACITY_STATE_BINDING')
   else:need(row['state']=='UNKNOWN' and bool(four.error_markers(row)),'P14_PROGRAMME_MISSING_MEASUREMENT')
  ss=row['source_snapshot']
  need(set(ss)==(SOURCES[CID]if pg else four.REQUIRED_SOURCES[name]),'P14_ASSESSMENT_SOURCE_SET')
  require_unchanged(ROOT,ss);checked.update(ss)
  state=row['state'];need(state in ('PASS','FAIL','UNKNOWN','NOT_EVALUATED'),'P14_ASSESSMENT_STATE')
  errs=four.error_markers(row)
  effective[name]='FAIL' if state=='FAIL' else 'EVALUATOR_ERROR' if errs else state
  rows.append({'criterion':name,'reported_state':state,'effective_state':effective[name],'error_markers':errs})
 require_unchanged(ROOT,checked)
 need(digest([bundle,reports,expected_digests])==pin,'P14_DECISION_MUTATION')
 verdict=four.decide(physical,effective)
 if any(r['error_markers'] for r in rows) and 'EVALUATOR_ERROR' not in verdict['blockers']:
  verdict['blockers'].append('EVALUATOR_ERROR')
 return {'schema':'P14_P1_N2_FOUR_CRITERIA_DECISION_V1','model_digest':mh,'original_physical_digest':digest(physical),
  'programme_digest':bundle['request']['programme_digest'],'assessment_digests':copy.deepcopy(expected_digests),
  'criteria':rows,'decision':verdict,'integrity_verified':True,**ALWAYS_FALSE}

def retain_private(root,name,value):
 need(root.is_dir() and not root.is_symlink() and root.stat().st_mode&0o077==0,'P14_PRIVATE_LOCAL_DIRECTORY')
 need(type(name) is str and Path(name).name==name and name not in ('.','..'),'P14_LOCAL_FILENAME')
 data=json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()
 path=root/name;temp=root/('.'+name+'.partial')
 fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:
  with os.fdopen(fd,'wb')as f:
   f.write(data);f.flush();os.fsync(f.fileno())
  # Atomic visibility and no overwrite. Stale .partial files after a watchdog
  # stop are not accepted evidence.
  os.link(temp,path,follow_symlinks=False)
 finally:temp.unlink()
 need(path.read_bytes()==data and digest(json.loads(data))==digest(value),'P14_PERSISTED_READBACK')
 return {'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}

def run(body,root):
 """Single private attempt. Caller provides watchdog and exclusive local directory."""
 import search114,constructor127,construction_replay127,evaluate_pair127
 import source_guest_route_evaluator as guest,source_living_evaluator as living,source_wall_function_evaluator as walls
 root=Path(root)
 request=prepare(body);evidence={};stage='SOURCE'
 def save(name,data):evidence[name]=retain_private(root,name,data)
 paths=snapshot(ROOT,sorted(PATHS));source=source_audit()
 for fn,p in ((search114.propose,ENGINE/'search114.py'),(constructor127.build,ENGINE/'constructor127.py'),
   (constructor127.frame,ENGINE/'constructor127.py'),(constructor127.context,ENGINE/'constructor127.py'),
   (construction_replay127.verify,ENGINE/'construction_replay127.py'),(evaluate_pair127.evaluate,ENGINE/'evaluate_pair127.py'),
   (guest.assess,ROOT/'app/local_integration/source_guest_route_evaluator.py'),
   (living.assess,ROOT/'app/local_integration/source_living_evaluator.py'),
   (walls.assess,ROOT/'app/local_integration/source_wall_function_evaluator.py'),
   (four.decide,ROOT/'app/local_integration/current_four_decision.py'),
   (placed,ROOT/'app/local_integration/current_programme_evaluator.py'),
   (normalize_proposal,ROOT/'app/local_integration/one_bed_pair_source_study.py'),
   (program_bind,ROOT/'app/local_integration/one_bed_pair_source_study.py'),
   (lookup,ROOT/'app/local_integration/program_profile_registry.py')):
  need(Path(inspect.getsourcefile(fn)).resolve()==p,'P14_RUNTIME_IMPORT_PATH')
 raw=request['raw'];rp=digest(request)
 raw_saved={'request_body_hex':body.hex(),'request':request}
 save('request.json',raw_saved)
 try:
  core,_=constructor127.frame(raw,'FRONT_REAR');cp=digest(core);stage='PROPOSAL'
  save('attempt-open.json',{'stage':'PROPOSAL_STARTING','attempt_index':1,'core_digest':cp,
      'programme_digest':request['programme_digest'],'solver_limit_seconds':SOLVER_SECONDS,**ALWAYS_FALSE})
  result=search114.propose(copy.deepcopy(core),1,time_limit=SOLVER_SECONDS,variant=0,sleep_roles=['double'],
      ordered_macro=False,topology='SIDE_ROOTED_SERVICES')
  disposition=proposal_disposition(result)
  if disposition!='PROPOSAL_ONLY':
   observed,_=transport(result);save('proposal-observed.json',observed)
   return {'state':'NO_WITNESS_WITHIN_SINGLE_ATTEMPT','proposal_disposition':disposition,'exact_attempts':1,**ALWAYS_FALSE}
  p,receipt=normalize_proposal(result);pin=digest(p)
  save('proposal.json',p);save('proposal-transport.json',receipt)
  stage='CONSTRUCTION'
  packet=constructor127.build(copy.deepcopy(raw),'FRONT_REAR',copy.deepcopy(p),copy.deepcopy(p))
  ctx=constructor127.context(raw,packet,{'A':p,'B':copy.deepcopy(p)})
  (packet,ctx),_=transport([packet,ctx]);model=packet['world_model'];mh=digest(model)
  need(digest(request)==rp and digest(p)==pin and digest(packet['core'])==cp,'P14_CONSTRUCTOR_MUTATION_CORE')
  program_bind(model,request['programme'])
  save('packet.json',packet);save('context.json',ctx)
  stage='REPLAY'
  re=construction_replay127.verify(model,ctx);save('replay-original.json',re)
  need(re['verified'] is True and re['model_hash']==mh,'P14_REPLAY_FAILED')
  stage='PHYSICAL'
  phys=evaluate_pair127.evaluate(packet,ctx);save('physical-original.json',phys)
  bundle={'schema':'P14_P1_N2_ORIGINAL_RUNTIME_BUNDLE_V1',**raw_saved,'packet':packet,'context':ctx,
      'proposal':p,'engine_revision':ENGINE_REVISION,'model_digest':mh,'reports':{'replay':re,'physical':phys},
      'report_digests':{'replay':digest(re),'physical':digest(phys)},'source_snapshot':paths,**ALWAYS_FALSE}
  bp=digest(bundle);binding(bundle);save('runtime-bundle.json',bundle)
  stages={CID:assess_programme,'KITCHEN_GUEST_PATH_SEPARATION':guest.assess,
       'CONTINUOUS_USEFUL_LIVING':living.assess,'NONFUNCTIONAL_WALL_EXCLUSION':walls.assess}
  reports={};pins={}
  for label,call in stages.items():
   stage=label
   try:
    row=call(copy.deepcopy(bundle))
   except Exception as ex:
    save(label+'-execution-error.json',{'stage':label,'type':type(ex).__name__,'detail':str(ex)})
   else:
    save(label+'.json',row);reports[label]=copy.deepcopy(row);pins[label]=digest(row)
   need(bp==digest(bundle),'P14_FULL_REPORT_MUTATION')
  if set(reports)!=set(stages):
   return {'state':'FOUR_ASSESSMENT_EXECUTION_INCOMPLETE','reported':sorted(reports),'exact_attempts':1,
    'model_digest':mh,'physical_status':phys['status'],**ALWAYS_FALSE}
  stage='DECISION'
  read=lambda name:json.loads((root/name).read_bytes())
  durable=read('runtime-bundle.json');same={label:read(label+'.json')for label in sorted(stages)}
  need(digest(durable)==bp,'P14_RUNTIME_READBACK')
  out=decision(durable,same,pins);save('decision.json',out)
  state=('FOUR_ASSESSMENTS_WITH_EVALUATOR_ERRORS_NOT_QUALIFIED' if 'EVALUATOR_ERROR' in out['decision']['blockers']
    else 'ONE_BEDROOM_PAIR_SOURCE_STUDY_NOT_QUALIFIED')
  return {'state':state,'model_digest':mh,'exact_attempts':1,
    'physical_status':phys['status'],'physical_errors':len(phys['errors']),'physical_pending':len(phys['pending']),
    'criteria':[{'criterion':r['criterion'],'reported_state':r['reported_state'],'effective_state':r['effective_state']}for r in out['criteria']],
    'decision':out['decision'],**ALWAYS_FALSE}
 except Exception as ex:
  save('runtime-execution-error.json',{'stage':stage,'type':type(ex).__name__,'detail':str(ex)})
  return {'state':'RUNTIME_FAILED_CLOSED','stage':stage,**ALWAYS_FALSE}
 finally:
  require_unchanged(ROOT,paths)
  need(source_audit()==source,'P14_RUNTIME_SOURCE_CHANGED')
  save('evidence-index.json',{'files':copy.deepcopy(evidence),'engine':source,'local_source':paths,**ALWAYS_FALSE})

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--private-output',required=True);a=ap.parse_args()
 p=Path(a.private_output);need(p.is_absolute() and p.parent.is_dir() and not p.parent.is_symlink()
        and p.parent.stat().st_mode&0o077==0,'P14_PRIVATE_PARENT')
 old=os.umask(0o077)
 try:
  p.mkdir(mode=0o700,exist_ok=False)
  output=run(b'{"W":"18","L":"20","n":2}',p);retain_private(p,'summary.json',output)
  print(json.dumps(output,sort_keys=True,ensure_ascii=False))
 finally:os.umask(old)
if __name__=='__main__':main()
