"""Process-local memoization of *computed* independent reports, never caller receipts.
Key includes complete model/context and current source revision. No persistence.
"""
from collections import OrderedDict
from copy import deepcopy
import hashlib,json,threading

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
class GateCache:
 def __init__(self,limit=8):
  if not isinstance(limit,int)or limit<1:raise ValueError('CACHE_LIMIT')
  self.limit=limit;self._entries=OrderedDict();self.computations=0;self.hits=0;self._lock=threading.RLock()
 def clear(self):
  with self._lock:self._entries.clear()
 def evaluate(self,model,context,source_revision,evaluator,*,force=False):
  if not isinstance(source_revision,str)or not source_revision:raise ValueError('SOURCE_REVISION_REQUIRED')
  mh=digest(model);ch=digest(context);key=(source_revision,mh,ch)
  with self._lock:
   if not force and key in self._entries:
    self.hits+=1;self._entries.move_to_end(key);return deepcopy(self._entries[key])
  m=deepcopy(model);c=deepcopy(context);report=evaluator(m,c)
  with self._lock:self.computations+=1
  if digest(m)!=mh or digest(c)!=ch:raise ValueError('INDEPENDENT_EVALUATOR_MUTATED_INPUT')
  if not isinstance(report,dict)or report.get('model_hash')!=mh:raise ValueError('INDEPENDENT_REPORT_MODEL_BINDING')
  with self._lock:
   self._entries[key]=deepcopy(report);self._entries.move_to_end(key)
   while len(self._entries)>self.limit:self._entries.popitem(last=False)
  return deepcopy(report)
