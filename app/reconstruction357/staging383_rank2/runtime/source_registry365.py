"""Isolated383 finite-portal registry: exact family replay, no borrowed365 authority.
Legacy module name is retained only for cloned reviewer's imports.
"""
import time,subprocess,sys,json,copy
from pathlib import Path
from contract114 import digest
HERE=Path(__file__).resolve().parent.parent;_TOKEN=object()
class CurrentContext(dict):
 def __init__(self,token,payload,proof,deadline):
  if token is not _TOKEN:raise ValueError('INTERNAL_CONTEXT_ONLY')
  super().__init__(copy.deepcopy(payload));self._token=token;self._proof=copy.deepcopy(proof);self._deadline=deadline;self._digest=digest(self)
def verify_context(model,context):
 errors=[]
 if not isinstance(context,CurrentContext) or context._token is not _TOKEN:errors.append('LIVE_CONTEXT_REQUIRED')
 else:
  if time.monotonic()>context._deadline:errors.append('LIVE_CONTEXT_EXPIRED')
  if digest(context)!=context._digest:errors.append('CONTEXT_MUTATED')
  if digest(model)!=context._proof['model_hash']:errors.append('CURRENT_MODEL_MISMATCH')
 return {'verified':not errors,'errors':errors,'pending':[],
         'scope':'REGISTERED_FINITE_PORTALS383_REPLAY_ONLY','proof':context._proof if not errors else None}
def resolve(record,deadline):
 if type(record)is not dict or record.get('trace',{}).get('schema')!='FINITE_PORTALS383_SOURCE_TRACE_V1':raise ValueError('UNREGISTERED_DERIVED_RECORD_SCHEMA')
 remaining=deadline-time.monotonic()
 if remaining<=0:raise ValueError('DEADLINE')
 p=subprocess.run([sys.executable,'-B',str(HERE/'source383.py')],input=json.dumps(record),text=True,capture_output=True,timeout=remaining)
 if p.returncode:raise ValueError('DERIVED_REPLAY_FAILED:'+p.stdout[-2000:]+p.stderr[-500:])
 proof=json.loads(p.stdout);c=record['candidate']
 checks={'input_record_digest':digest(record),'outer_trace_digest':digest(record['trace']),
         'candidate_digest':digest(c),'model_hash':digest(c['model']),'packet_digest':digest(c['packet'])}
 if proof.get('verified')is not True or any(proof.get(k)!=v for k,v in checks.items()):raise ValueError('CURRENT_DERIVED_REPLAY_BINDING')
 payload=payload_for(record,proof)
 return CurrentContext(_TOKEN,payload,proof,deadline)

def payload_for(record,proof):
 c=record['candidate']
 return {'operation':'experimental_finite_portals383','inputs':copy.deepcopy(c['model']['inputs']),
          'construction_trace':{'schema':proof['schema'],'raw':copy.deepcopy(proof['raw']),
             'family':'FRONT_REAR','model_hash':proof['model_hash']},
          'frame_core125':copy.deepcopy(c['packet']['core']),'frame_local129':copy.deepcopy(c['packet']['local_model'])}
