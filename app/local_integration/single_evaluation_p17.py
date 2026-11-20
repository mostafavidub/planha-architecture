"""P17 fixed-family evidence binding. No n2 bypass, quality waiver or delivery."""
import copy,hashlib,inspect,json,sys
from pathlib import Path
import single_model_p15 as producer
from single_model_p15 import ROOT,ENGINE,LOCAL,RAW,FAMILY,AUTH,digest,require
from front_rear_runtime_adapter import source_audit as original_audit
from program_profile_registry import lookup
SOURCE_PINS={"app/local_integration/current_programme_evaluator.py":"99ada55f405e0c205d1a431469d1faae55a149dd","app/local_integration/source_guest_route_evaluator.py":"17fb50e08d153aee4aa2ecd4fa4d13928f522a4e","app/local_integration/source_living_evaluator.py":"2f368ae2a1d5db32d7163076f90eb5a7e991f76f","app/local_integration/source_wall_function_evaluator.py":"84233b6bba2c4835af5e59c203ecf51a6765b8e0"}
DERIVED_NAMES=["single_current_programme_evaluator_p17.py","single_source_guest_route_evaluator_p17.py","single_source_living_evaluator_p17.py","single_source_wall_function_evaluator_p17.py"]
def blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
def source_audit():
 base=producer.snapshot()
 for rel,pin in SOURCE_PINS.items():
  path=ROOT/rel
  require(not path.is_symlink() and blob(path.read_bytes())==pin,'P17_BASE_SOURCE_CHANGED')
 import single_assembler_p15,single_access_p15
 for fn,name in ((producer.replay,'single_model_p15.py'),(producer.construct,'single_model_p15.py'),(producer.assemble,'single_assembler_p15.py'),(verify,'single_evaluation_p17.py')):
  require(Path(inspect.getsourcefile(fn)).resolve()==(LOCAL/name).resolve(),'P17_CALLABLE_SOURCE')
 for mod,name in ((producer,'single_model_p15.py'),(single_assembler_p15,'single_assembler_p15.py'),(single_access_p15,'single_access_p15.py')):
  require(Path(mod.__file__).resolve()==(LOCAL/name).resolve(),'P17_ACTUAL_SOURCE_PATH')
 names=['single_evaluation_p17.py','single_physical_p17.py','single_decision_p17.py','single_runtime_p17.py','public_program_dispatch_p17.py','public_wln_server.py',*DERIVED_NAMES]
 observed={}
 for name in names:
  path=LOCAL/name;require(not path.is_symlink(),'P17_SOURCE_SYMLINK')
  observed[name]=hashlib.sha256(path.read_bytes()).hexdigest()
  mod=sys.modules.get(name[:-3])
  if mod is not None:
   require(Path(mod.__file__).resolve()==path.resolve(),'P17_SHADOW_MODULE')
   own={'single_physical_p17.py':('evaluate','verify_context'),'single_decision_p17.py':('assemble',),'single_runtime_p17.py':('worker','run_bound','read'),'public_program_dispatch_p17.py':('preflight','run_bound','is_single')}
   for attr in (('assess',)if name in DERIVED_NAMES else own.get(name,())):
    require(Path(inspect.getsourcefile(getattr(mod,attr))).resolve()==path.resolve(),'P17_ACTUAL_EVALUATOR_PATH')
 collection={}
 for rel in ('studies/p17_http_single.py','.github/workflows/p17-single-api.yml','studies/p17_evaluator_derivatives.json'):
  path=ROOT/rel;require(not path.is_symlink(),'P17_COLLECTION_SYMLINK');collection[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
 return {'p15':base,'p17':observed,'collection':collection}
def verify(model,context):
 before=source_audit();pin=digest([model,context])
 require(type(context)is dict and set(context)=={'schema','raw','proposal','core','programme_digest'},'P17_CONTEXT_SCHEMA')
 require(context['schema']=='SINGLE_ORIGIN_CONTEXT_P17_V1','P17_CONTEXT_VERSION')
 require(digest(context['raw'])==digest(RAW),'P17_RAW_BINDING')
 require(digest(context['core'])==digest(producer.core(RAW)),'P17_CORE_BINDING')
 require(context['programme_digest']==digest(lookup('PROGRAM_2BED_V1')),'P17_PROGRAMME_BINDING')
 require(model.get('schema')==FAMILY and model.get('contract_version')=='p15-single-v1','P17_MODEL_SCHEMA')
 require(digest(model['inputs'])==digest(['18','20',1]),'P17_MODEL_INPUT_TYPED')
 require(type(model['units'])is list and [u['id']for u in model['units']]==['A'],'P17_MODEL_UNITS')
 require(all(model.get(k)is False for k in AUTH),'P17_AUTHORITY')
 report=producer.replay(model,context['raw'],context['proposal'])
 require(report['verified']is True,'P17_REPLAY_MISMATCH')
 require(digest([model,context])==pin and source_audit()==before,'P17_REPLAY_MUTATION')
 return {**report,'schema':'SINGLE_ORIGIN_REPLAY_P17_V1','model_hash':report['model_digest'],'context_digest':digest(context)}
def context(raw,proposal):
 return {'schema':'SINGLE_ORIGIN_CONTEXT_P17_V1','raw':copy.deepcopy(raw),'proposal':copy.deepcopy(proposal),'core':producer.core(raw),'programme_digest':digest(lookup('PROGRAM_2BED_V1'))}
def bind_bundle(bundle):
 before=source_audit();pin=digest(bundle)
 require(bundle.get('schema')=='SINGLE_EVALUATION_BUNDLE_P17_V1','P17_BUNDLE_SCHEMA')
 model=bundle['packet']['world_model'];mh=digest(model)
 require(bundle['model_digest']==mh,'P17_MODEL_DIGEST')
 require(set(bundle['reports'])=={'physical','historical_physical','access','replay'},'P17_ORIGINAL_REPORT_SET')
 require(set(bundle['report_digests'])==set(bundle['reports']),'P17_REPORT_DIGEST_SET')
 for name,report in bundle['reports'].items():
  require(digest(report)==bundle['report_digests'][name],'P17_REPORT_DIGEST')
  require(report.get('model_hash',report.get('model_digest'))==mh,'P17_REPORT_MODEL_BINDING')
 require(bundle['reports']['physical'].get('schema')=='SINGLE_PHYSICAL_P17_V1','P17_PHYSICAL_VERSION')
 import single_physical_p17 as physical
 ph=bundle['reports']['physical']
 require(ph.get('integrity_verified')is True and all(ph.get(k)is False for k in AUTH),'P17_PHYSICAL_INTEGRITY')
 require(ph.get('checker_version')==physical.VERSION and ph.get('status')in('FAIL','NOT_EVALUATED','PASS_CONCEPT_SCOPED_REVIEW'),'P17_PHYSICAL_STATE')
 require(type(ph.get('errors'))is list and all(type(x)is dict for x in ph['errors']) and type(ph.get('pending'))is list and all(type(x)is str for x in ph['pending']),'P17_PHYSICAL_REPORT_TYPES')
 require(digest(ph['source_snapshot'])==digest(physical.source_guard()),'P17_PHYSICAL_SOURCE')
 phcontext={'schema':'SINGLE_P17_PHYSICAL_CONTEXT_V1','raw':bundle['context']['raw'],'proposal':bundle['context']['proposal']}
 require(digest(ph['replay'])==digest(physical.verify_context(model,phcontext)),'P17_PHYSICAL_REPLAY')
 require(bundle['reports']['access'].get('schema')=='SINGLE_UNIT_OWNERSHIP_ACCESS_P15_V1','P17_ACCESS_VERSION')
 require(bundle['reports']['replay'].get('schema')=='SINGLE_ORIGIN_REPLAY_P17_V1','P17_REPLAY_VERSION')
 current=verify(model,bundle['context'])
 require(digest(current)==digest(bundle['reports']['replay']),'P17_REPLAY_REPORT_BINDING')
 require(digest(bundle)==pin and source_audit()==before,'P17_BIND_MUTATION')
 return current
