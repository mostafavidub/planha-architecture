"""Pre-import frozen member inspection; not a selected-set issuer."""
import json,hashlib,types,builtins
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent
FREEZE_SHA='f30ff8992921a222e4cc0fd40dd8d198ce3cd8e27815a6839c5c1ea1c9326bbb'
def _capture():
 data=(P/'member_boundary_freeze.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!=FREEZE_SHA:raise ValueError('BOUNDARY_FREEZE_CHANGED')
 manifest=json.loads(data);captured={}
 for n,h in manifest['files'].items():
  d=(ROOT/n).read_bytes()
  if hashlib.sha256(d).hexdigest()!=h:raise ValueError('PREIMPORT_SOURCE_CHANGED:'+n)
  if n in ('staging367_selected_set/selection_v2.py','staging367_selected_set/balanced_member_binding.py'):captured[Path(n).stem]=d
 return data,manifest,captured

def inspect_balanced():
 try:
  initial,manifest,captured=_capture();loaded={}
  def load(name):
   if name in loaded:return loaded[name]
   if name not in captured:raise ValueError('UNREGISTERED_PROJECT_IMPORT')
   m=types.ModuleType('_selected_boundary_'+name);m.__file__=str(P/(name+'.py'));loaded[name]=m
   def imp(n,g=None,l=None,fromlist=(),level=0):
    if level==0 and n in captured:return load(n)
    return builtins.__import__(n,g,l,fromlist,level)
   m.__dict__['__builtins__']={**vars(builtins),'__import__':imp};exec(compile(captured[name],m.__file__,'exec'),m.__dict__);return m
  result=load('balanced_member_binding').inspect_registered_member()
  after,_,_=_capture()
  if after!=initial:raise ValueError('POSTIMPORT_FREEZE_CHANGED')
  result['boundary_scope']='PINNED_STORED_CONCEPT_REVIEW_ONLY_NOT_SELECTED_SET'
  return result
 except (ValueError,KeyError,TypeError,IndexError,OSError)as e:return {'status':'UNKNOWN','missing':[str(e)],'membership_authority':False,'qualified_selected_count':0,'request_fulfilled':False,'accepted':False,'delivery_allowed':False}
