"""Current validated primitive computation; scoped closures only."""
import time,importlib,copy
from gate387 import D,validate_views
_CACHE=None
def evaluate(model,raw,*,source_profile,post_fresh):
 global _CACHE
 env,res,groups=(post_fresh[k]for k in('envelope','result','groups'));validate_views(env,res)
 if D(env['packet']['world_model'])!=D(model)or D(res['raw_fresh_report'])!=D(raw):raise ValueError('CURRENT_PRIMITIVE_BINDING')
 if _CACHE is not None:return copy.deepcopy(_CACHE)
 start=time.monotonic();out={}
 for name in('living','guest','kitchen'):
  out[name+'_closure']=importlib.import_module(name+'_closure387').evaluate(env,res,groups,seconds=8 if name!='living'else 6)
 _CACHE={'source_closures':out,'seconds':time.monotonic()-start,'model_hash':D(model),'raw_hash':D(raw),'fresh_executed':False};return copy.deepcopy(_CACHE)
