"""Current domain boundary, not Python isolation or product admission.
Frozen direct calls remain historical primitives. No caller capability grants dispatch.
"""
import copy,hashlib,importlib,inspect,json,sys
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
VERSION='CURRENT_ENTRY_DOMAIN_X03_V1'
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
SOURCE_PINS={
 "app/local_integration/public_wln_contract.py": "80fd2b2710342735dc35e484c9b0da790995d830",
 "app/local_integration/dimension_contract.py": "058502cd97b5131908b82fdbdba34c62d3376ea3",
 "app/local_integration/core_choice_pair_study.py": "4ed751238583d63ec2d9bb570bccbb9b0802cd3c",
 "app/local_integration/source_fit_candidate207.py": "8f56cc4cba74bd8c184bb6f820e60971911e4b44",
 "app/local_integration/program_profile_registry.py": "af549f86f39e2e57554cd48e0ffdea54d5444262",
 "app/local_integration/front_rear_runtime_adapter.py": "92ce916b71bb05f0087e2527a51dd8de4d40a676",
 "app/reconstruction357/planha_general150_runtime_work/contract114.py": "a2631c6a38a43b8d423edf82ad8d526ced1b8196",
 "app/reconstruction357/planha_general150_runtime_work/constructor127.py": "beb67bf4b08a65242305519a678eef94fef3fad6"
}
REGISTRY={
 'SOURCE_FIT207_COMPACT_PAIR':{'mode':'CURRENT_STUDY','input':'PUBLIC_WLN_V3','family':'FRONT_REAR','programme':'PROGRAM_2BED_V1','unit_count':2},
 'CONSTRUCTOR127_COMPACT_PAIR':{'mode':'CURRENT_STUDY','input':'PUBLIC_WLN_V3','family':'FRONT_REAR','programme':'PROGRAM_2BED_V1','unit_count':2}}
def need(ok,code):
 if not ok:raise ValueError(code)
def digest(v):
 return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def source_snapshot():
 out={}
 for path,pin in SOURCE_PINS.items():
  data=(ROOT/path).read_bytes()
  need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==pin,'CURRENT_BOUNDARY_SOURCE_CHANGED')
  out[path]=hashlib.sha256(data).hexdigest()
 out['app/local_integration/current_entry_boundary_x03.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 return out
def imported(module,name,path):
 fn=getattr(module,name)
 need(Path(inspect.getsourcefile(fn)).resolve()==(ROOT/path).resolve(),'CURRENT_BOUNDARY_IMPORT_PATH')
 return fn
def parser_guard():
 before=source_snapshot()
 import public_wln_contract,dimension_contract
 imported(public_wln_contract,'parse_public','app/local_integration/public_wln_contract.py')
 imported(public_wln_contract,'verify_public','app/local_integration/public_wln_contract.py')
 imported(public_wln_contract,'engine_raw','app/local_integration/public_wln_contract.py')
 imported(dimension_contract,'parse','app/local_integration/dimension_contract.py')
 imported(dimension_contract,'_number','app/local_integration/dimension_contract.py')
 return before
def public_request(body):
 before=parser_guard()
 from public_wln_contract import parse_public,verify_public,engine_raw
 e=parse_public(body);verify_public(body,e)
 raw=engine_raw(e)
 need(source_snapshot()==before,'CURRENT_BOUNDARY_SOURCE_CHANGED')
 return e,raw
def check_model_domain(model):
 """Domain only, not ownership, original raw, or provenance."""
 before=parser_guard()
 need(type(model)is dict,'CURRENT_MODEL_OBJECT_REQUIRED')
 v=model.get('inputs')
 need(type(v)is list and len(v)==3,'CURRENT_MODEL_INPUTS_REQUIRED')
 from public_wln_contract import parse_public
 e=parse_public(json.dumps({'W':v[0],'L':v[1],'n':v[2]},allow_nan=False).encode())
 need(e['canonical_request']['unit_count']==2,'UNSUPPORTED_CURRENT_MODEL_UNIT_COUNT')
 need(source_snapshot()==before,'CURRENT_BOUNDARY_SOURCE_CHANGED')
 return {'version':VERSION,'model_input_digest':digest(v),'input_valid':True,
         'qualification_established':False,**{k:False for k in AUTH}}
def check_raw_domain(raw):
 before=parser_guard()
 need(type(raw)is dict,'CURRENT_RAW_OBJECT_REQUIRED')
 from dimension_contract import parse
 from public_wln_contract import parse_public
 # Internal diagnostic schema remains separate from the public three-field body.
 e=parse(json.dumps(raw,allow_nan=False).encode())
 parse_public(json.dumps({k:raw[k]for k in ('W','L','n')},allow_nan=False).encode())
 need(source_snapshot()==before,'CURRENT_BOUNDARY_SOURCE_CHANGED')
 return e
def entry(identifier):
 need(type(identifier)is str and identifier in REGISTRY,'UNREGISTERED_CURRENT_ENTRY_DISABLED')
 return copy.deepcopy(REGISTRY[identifier])
def prepare(identifier,body):
 rule=entry(identifier);e,raw=public_request(body);before=source_snapshot()
 sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration')]
 coremod=importlib.import_module('core_choice_pair_study')
 selected=imported(coremod,'selected_core','app/local_integration/core_choice_pair_study.py')
 profilemod=importlib.import_module('program_profile_registry')
 lookup=imported(profilemod,'lookup','app/local_integration/program_profile_registry.py')
 profile=lookup(rule['programme']);core,_=selected(raw,'FRONT_REAR_COMPACT118')
 need(source_snapshot()==before,'CURRENT_BOUNDARY_SOURCE_CHANGED')
 return {'schema':VERSION,'entry':identifier,'rule':rule,'envelope':e,'raw':raw,
         'core':core,'profile':profile,'sources':before,**{k:False for k in AUTH}}
def validate_prepared(prepared,body):
 need(type(prepared)is dict,'CURRENT_REQUEST_BINDING')
 expected=prepare(prepared.get('entry'),body)
 need(digest(prepared)==digest(expected),'CURRENT_REQUEST_BINDING')
 return expected
def propose_current(body,*,seconds=3,variant=0,guest_entry_panel=False):
 need(type(seconds)is int and 1<=seconds<=30,'STUDY_BUDGET')
 need(type(variant)is int and 0<=variant<=2,'STUDY_VARIANT')
 need(type(guest_entry_panel)is bool,'P11_INTERNAL_FLAG')
 p=prepare('SOURCE_FIT207_COMPACT_PAIR',body);pin=digest(p)
 producer=importlib.import_module('source_fit_candidate207')
 call=imported(producer,'propose','app/local_integration/source_fit_candidate207.py')
 try:
  kwargs={'guest_entry_panel':True} if guest_entry_panel else {}
  return call(copy.deepcopy(p['core']),2,time_limit=seconds,variant=variant,
       sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES',**kwargs)
 finally:
  need(digest(p)==pin and source_snapshot()==p['sources'],'CURRENT_BOUNDARY_MUTATED')
def construct_current(body,proposals):
 p=prepare('CONSTRUCTOR127_COMPACT_PAIR',body)
 need(type(proposals)is dict and set(proposals)=={'A','B'},'PAIR_PROPOSALS_REQUIRED')
 for proposal in proposals.values():
  need(type(proposal)is dict and type(proposal.get('bedrooms'))is int and proposal['bedrooms']==2
       and digest(proposal.get('sleep_roles'))==digest(['double','twin']),'CURRENT_PROGRAMME_BINDING')
 original=digest(proposals);pin=digest(p);ctor=importlib.import_module('constructor127')
 build=imported(ctor,'build','app/reconstruction357/planha_general150_runtime_work/constructor127.py')
 context=imported(ctor,'context','app/reconstruction357/planha_general150_runtime_work/constructor127.py')
 try:
  packet=build(p['raw'],'FRONT_REAR',copy.deepcopy(proposals['A']),copy.deepcopy(proposals['B']))
  need(digest(packet['core'])==digest(p['core']),'CURRENT_CORE_BINDING')
  model=packet['world_model'];check_model_domain(model)
  need(all(F(model['inputs'][i])==F(p['raw'][a])for i,a in enumerate(('W','L'))) and type(model['inputs'][2])is int and model['inputs'][2]==p['raw']['n'],'CURRENT_MODEL_REQUEST_MISMATCH')
  ctx=context(p['raw'],packet,copy.deepcopy(proposals))
  need(digest(ctx['construction_trace']['raw'])==digest(p['raw'])and ctx['construction_trace']['model_hash']==digest(model),'CURRENT_CONTEXT_BINDING')
  return {'packet':packet,'context':ctx,'boundary_version':VERSION,'boundary_scope':'DOMAIN_SOURCE_PAIR_BINDING_NOT_QUALIFICATION',**{k:False for k in AUTH}}
 finally:
  need(digest(proposals)==original and digest(p)==pin and source_snapshot()==p['sources'],'CURRENT_BOUNDARY_MUTATED')
def bind_current_evidence(body,model,report,expected_model_digest,expected_report_digest):
 """Consistency, not authenticity from caller hashes."""
 before=source_snapshot();e,raw=public_request(body);check_model_domain(model)
 need(digest(model)==expected_model_digest and digest(report)==expected_report_digest,'CURRENT_EVIDENCE_DIGEST_MISMATCH')
 need(type(report)is dict and report.get('model_hash')==expected_model_digest,'CURRENT_REPORT_MODEL_BINDING')
 need(all(F(model['inputs'][i])==F(raw[a])for i,a in enumerate(('W','L')))and type(model['inputs'][2])is int and model['inputs'][2]==raw['n'],'CURRENT_MODEL_REQUEST_MISMATCH')
 need(source_snapshot()==before,'CURRENT_BOUNDARY_SOURCE_CHANGED')
 return {'schema':VERSION,'state':'DOMAIN_BOUND_ONLY_NOT_ADMISSION','request_digest':e['canonical_request_digest'],
    'model_digest':expected_model_digest,'report_digest':expected_report_digest,'source_digest':digest(before),
    'historical_report_status_retained':report.get('status'),'authenticity_verified':False,
    'frozen_legacy_execution_disabled':False,'packaging_isolation':'NOT_IMPLEMENTED',**{k:False for k in AUTH}}
