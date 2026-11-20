"""P15: genuine one-unit top-core family, separate from frozen pair engines."""
import copy,hashlib,inspect,json,math,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
LOCAL=ROOT/'app/local_integration'
sys.path[:0]=[str(ENGINE),str(LOCAL)]
from public_wln_contract import parse_public,verify_public
from front_rear_runtime_adapter import source_audit,proposal_transport,transport
from program_profile_registry import lookup
from contract114 import S
from single_assembler_p15 import assemble
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
FAMILY='SINGLE_FRONT_TOP_CORE_P15_V1'
RAW={'W':'18','L':'20','n':1}
def require(ok,code):
 if not ok:raise ValueError(code)
def digest(v):
 def check(x):
  require(type(x)in(dict,list,str,int,float,bool,type(None)),'JSON_TYPE')
  if type(x)is float:require(math.isfinite(x),'NONFINITE')
  if type(x)is dict:
   require(all(type(k)is str for k in x),'JSON_KEY')
   for z in x.values():check(z)
  if type(x)is list:
   for z in x:check(z)
 check(v)
 return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def preflight(body):
 e=parse_public(body);verify_public(body,e);c=e['canonical_request']
 n=c['unit_count']
 # Verified public envelope retains exact numerator/denominator; no float conversion.
 w,l=(F(int(c['dimensions_m'][a]['numerator']),int(c['dimensions_m'][a]['denominator'])) for a in ('W','L'))
 normalized={'W':S(w),'L':S(l),'n':n}
 return {'input_valid':True,'execution_ready':normalized==RAW and type(n)is int,
         'state':'READY_SINGLE_FAMILY_P15'if normalized==RAW and type(n)is int else'UNSUPPORTED_SINGLE_FAMILY_P15',
         'raw':normalized,'envelope':e,'programme':lookup('PROGRAM_2BED_V1'),**{k:False for k in AUTH}}
def core(raw):
 require(digest(raw)==digest(RAW),'UNSUPPORTED_SINGLE_FAMILY_P15')
 W,L=F(raw['W']),F(raw['L']);t=F('.15');e=F('.25');y=L-e-F('2.75');yt=L-e
 entry=F('5.8')
 return {'schema':'SINGLE_TOP_CORE_OWNERSHIP_P15_V1','kind':FAMILY,
  'band':list(map(S,[e,y,W-e,yt])),
  'stair':list(map(S,[F('.4'),y+t,F('4.95'),yt-t])),
  'lift':list(map(S,[W-F('2.05'),yt-F('1.8'),W-F('.4'),yt-t])),
  'lobby':[list(map(S,[F('5.1'),y,W-F('2.2'),yt])),list(map(S,[W-F('2.2'),y,W-e,y+F('.8')]))],
  'units':{'A':list(map(S,[e,e,W-e,y-t]))},
  'unit_ownership':{'A':[list(map(S,[e,e,W-e,y-t]))]},
  'entry_centers':{'A':[S(entry),S(y-t/2)]},
  'source_dimensions':{'stair':['4.55','2.45'],'lift':['1.65','1.65'],'body_m':'.7'},
  'scope':'One-unit top shared core built directly. Stair/lift rectangles and this-storey access only; no technical, legal or vertical approval.'}
def snapshot():
 original=source_audit()
 import search114,entry117,single_assembler_p15
 for mod,fn,path in [(search114,search114.propose,ENGINE/'search114.py'),(entry117,entry117.install,ENGINE/'entry117.py'),(single_assembler_p15,assemble,Path(__file__).with_name('single_assembler_p15.py'))]:
  require(Path(mod.__file__).resolve()==path.resolve() and Path(inspect.getsourcefile(fn)).resolve()==path.resolve(),'ACTUAL_SOURCE_PATH')
 paths=[Path(__file__),Path(__file__).with_name('single_assembler_p15.py'),Path(__file__).with_name('single_access_p15.py'),ROOT/'studies/p15_single_model.py',ROOT/'.github/workflows/p15-single-model.yml']
 require(all(not p.is_symlink() for p in paths),'SOURCE_SYMLINK')
 return {'original_source':original,'p15_sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}}
def construct(raw,proposal):
 c=core(raw)
 require(proposal['bedrooms']==2 and type(proposal['bedrooms'])is int and proposal['sleep_roles']==['double','twin'],'PROGRAMME_BINDING')
 m=assemble(F(raw['W']),F(raw['L']),c,proposal)
 require(m['inputs']==['18','20',1] and type(m['inputs'][2])is int,'MODEL_INPUT')
 require([u['id']for u in m['units']]==['A'],'MODEL_UNIT_COUNT')
 m['entry_access_reservation']={'unit':'A','rect':copy.deepcopy(proposal['rectangles']['entry_apron']),'source':'search114 reserved_entry: same-source proposal rectangle, not useful-room classification'}
 m['construction_identity']={'family':FAMILY,'raw_digest':digest(raw),'core_digest':digest(c),
  'proposal_digest':digest(proposal),'programme_digest':digest(lookup('PROGRAM_2BED_V1')),
  'unit_assignment':{'A':digest(proposal)},'pair_built_then_filtered':False}
 m.update({k:False for k in AUTH})
 return m
def replay(model,raw,proposal):
 # Independent invocation of deterministic construction, NOT original replay127.
 original=digest(model);rebuilt=construct(copy.deepcopy(raw),copy.deepcopy(proposal))
 return {'schema':'SINGLE_CONSTRUCTION_REPLAY_P15_V1','model_digest':original,
  'reconstructed_digest':digest(rebuilt),'verified':original==digest(rebuilt),
  'scope':'Exact same-source reassembly, not independent physical approval',**{k:False for k in AUTH}}
