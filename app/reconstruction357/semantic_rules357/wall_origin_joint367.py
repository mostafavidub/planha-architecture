"""362 exact source geometry adapter; callable only after SOURCE_JOINT367 artifact gate."""
import ast,types,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect
ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'staging367_service_joint_attempt2';SRC=ROOT/'planha_general150_runtime_work'
def load_origin(record):
 trace=record['trace'];c=record['candidate'];m=c['model']
 if trace['schema']!='SOURCE_SERVICE_JOINT367_TRACE_V1'or trace['model_digest']!=digest(m)or trace['candidate_digest']!=digest(c):raise ValueError('SOURCE_JOINT367_RECORD_BINDING')
 for name,sha in trace['source_inventory'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SOURCE_JOINT367_ORIGIN_SOURCE_DRIFT')
 data=(ROOT/'staging365_service_grammar/candidate365.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!='8807b7f2e8ba841d8e1a38ba6787f72161c9d04f64d69e71112859be92976ad9':raise ValueError('FIXED_PARENT_RECORD_SHA')
 import json
 parent=json.loads(data)
 if digest(parent)!=trace['parent_record_digest']:raise ValueError('PARENT_RECORD_CHAIN')
 actual_trace=dict(trace);actual_trace['proposal']=parent['trace']['proposal'];actual_trace['proposal_origin_record_digest']=digest(parent)
 return c,m,actual_trace

def base(record):
 c,m,t=load_origin(record);path=HERE/'assemble367.py';data=path.read_bytes()
 if t['source_inventory'].get(str(path.relative_to(ROOT)))!=hashlib.sha256(data).hexdigest():raise ValueError('CURRENT_SOURCE_CONSTRUCTOR_PIN')
 tree=ast.parse(data);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='assemble');stop=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='uid'and any(isinstance(x,ast.FunctionDef)and x.name=='tr'for x in n.body));fn.body=fn.body[:stop]+[ast.Return(value=ast.Name(id='m',ctx=ast.Load()))];mod=types.ModuleType('_prefix365');mod.__file__=str(path);sys.path.insert(0,str(SRC));sys.path.insert(0,str(HERE));exec(compile(ast.fix_missing_locations(tree),str(path),'exec'),mod.__dict__)
 raw=c['request'];out=mod.assemble(F(raw['W']),F(raw['L']),c['packet']['core'],t['proposal'])
 return out,{'file':'staging367_service_joint_attempt2/assemble367.py','sha256':hashlib.sha256(data).hexdigest(),'selector':'Executed source367 constructor prefix with current joint core and pinned original source proposal; no fresh or functional role inference'}

def hall(record):
 c,m,t=load_origin(record);path=HERE/'private_branch_hall367.py';data=path.read_bytes();key=str(path.relative_to(ROOT))
 if t['source_inventory'].get(key)!=hashlib.sha256(data).hexdigest():raise ValueError('SOURCE_BRANCH_HALL_PIN')
 if t['proposal']['ordered_macro']['kind']!='PARALLEL_TWINS_BRANCH146':raise ValueError('SOURCE_PRIVATE_BRANCH_REQUIRED')
 tree=ast.parse(data);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='install');stop=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.Assign)and any(isinstance(z,ast.Name)and z.id=='gross'for z in n.targets));fn.body=fn.body[:stop];mod=types.ModuleType('_hall_service365');mod.__file__=str(path);sys.path.insert(0,str(SRC));sys.path.insert(0,str(HERE));exec(compile(ast.fix_missing_locations(tree),str(path),'exec'),mod.__dict__);out={'walls':{},'wall_hosts':{},'source_wall_hosts':{}}
 for uid in ('A','B'):mod.install(out,{'id':uid},c['packet']['core'],t['proposal'],F(c['request']['L']))
 for wid,q in out['walls'].items():
  if rect(q)!=rect(m['walls'][wid])or rect(q)!=rect(m['wall_hosts'][wid]):raise ValueError('REBUILT_BRANCH_HALL_GEOMETRY')
 return out,{'file':key,'sha256':hashlib.sha256(data).hexdigest(),'selector':'Executed source367 branch install prefix with current core.branch_end367 and original program transform','not_necessity_proof':True}
