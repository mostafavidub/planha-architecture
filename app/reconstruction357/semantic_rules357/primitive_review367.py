"""Direct source-closure runner, deliberately no parent/engine import or dispatch."""
from pathlib import Path
import types,builtins,json,hashlib,time
HERE=Path(__file__).resolve().parent
MANIFEST_SHA='8d932d853e4afeea35741e83cbc0ab5f9586095092f704ea913ca13e668aa91e'
PROFILES={'SOURCE_JOINT367':'method_registry_source367.json'}
def evaluate(model,raw,*,source_profile,post_fresh):
 data=(HERE/'primitive_review367_manifest.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!=MANIFEST_SHA:raise ValueError('PRIMITIVE_MANIFEST_CHANGED')
 manifest=json.loads(data);loaded={}
 def load(name):
  if name in loaded:return loaded[name]
  file=name+'.py';data=(HERE/file).read_bytes()
  if hashlib.sha256(data).hexdigest()!=manifest['files'].get(file):raise ValueError('PRIMITIVE_SOURCE_CHANGED:'+name)
  mod=types.ModuleType(name);mod.__file__=str(HERE/file);loaded[name]=mod
  def imp(n,g=None,l=None,fromlist=(),level=0):
   if n=='engine' or n.startswith('closure_room_program'):raise ValueError('FORBIDDEN_PARENT_REENTRY')
   if level==0 and n+'.py'in manifest['files']:return load(n)
   return builtins.__import__(n,g,l,fromlist,level)
  mod.__dict__['__builtins__']={**vars(builtins),'__import__':imp}
  exec(compile(data,mod.__file__,'exec'),mod.__dict__);return mod
 if source_profile not in PROFILES:raise ValueError('UNREGISTERED_SOURCE_PROFILE')
 registry=PROFILES[source_profile]
 if hashlib.sha256((HERE/registry).read_bytes()).hexdigest()!=manifest['files'].get(registry):raise ValueError('PRIMITIVE_REGISTRY_CHANGED')
 common=load('common');common.REGISTRY_NAME=registry;common.rows(model,raw)
 if type(post_fresh)is not dict or set(post_fresh)!={'envelope','result','groups','seconds'}:raise ValueError('CLOSED_PRIMITIVE_CONTEXT')
 e,r,g=(post_fresh[k]for k in ('envelope','result','groups'));budget=post_fresh['seconds']
 if type(budget)not in(int,float)or not 0<budget<=10:raise ValueError('PRIMITIVE_BUDGET')
 if common.digest(e['packet']['world_model'])!=common.digest(model)or common.digest(r['raw_fresh_report'])!=common.digest(raw):raise ValueError('PRIMITIVE_INPUT_BINDING')
 before=common.digest([model,raw,post_fresh]);out={};deadline=time.monotonic()+budget
 for name in ('living_closure','guest_closure','kitchen_closure'):
  remaining=deadline-time.monotonic()
  if remaining<=0:raise ValueError('PRIMITIVE_DEADLINE')
  out[name]=load(name+'367').evaluate(e,r,g,seconds=min(remaining,8))
 if common.digest([model,raw,post_fresh])!=before:raise ValueError('PRIMITIVE_INPUT_MUTATION')
 return {'source_closures':out,'parent_dispatch_executed':False,'fresh_executed':False,'delivery_allowed':False,'model_hash':common.digest(model),'raw_hash':common.digest(raw)}
