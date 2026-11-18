"""Process-local authority for a fixed replay, never deserializable authority."""
import time,subprocess,sys,json,copy,hashlib
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
 return {'verified':not errors,'errors':errors,'pending':[],'scope':'REGISTERED_SOURCE_REPLAY_ONLY','proof':context._proof if not errors else None}

def resolve(record,deadline):
 if type(record)is not dict or type(record.get('trace'))is not dict or record['trace'].get('schema')!='TRANSLATED_PRIVATE357_SOURCE_TRACE_V1':raise ValueError('UNREGISTERED_RECORD_SCHEMA')
 remaining=deadline-time.monotonic()
 if remaining<=0:raise ValueError('DEADLINE')
 p=subprocess.run([sys.executable,str(HERE/'replay_worker.py')],input=json.dumps(record),text=True,capture_output=True,timeout=remaining)
 if p.returncode:raise ValueError('REPLAY_FAILED:'+p.stdout[-2000:]+p.stderr[-500:])
 proof=json.loads(p.stdout)
 if proof.get('verified')is not True or proof['input_record_digest']!=digest(record) or proof['outer_trace_digest']!=digest(record['trace']):raise ValueError('REPLAY_RECORD_BINDING')
 c=record['candidate']
 if proof['candidate_digest']!=digest(c) or proof['model_hash']!=digest(c['model']) or proof['packet_digest']!=digest(c['packet']):raise ValueError('CURRENT_PACKET_BINDING')
 payload={'operation':'experimental_source357','inputs':copy.deepcopy(c['model']['inputs']),'construction_trace':{'schema':proof['schema'],'raw':copy.deepcopy(proof['raw']),'family':'FRONT_REAR','model_hash':proof['model_hash']},'frame_core125':copy.deepcopy(c['packet']['core']),'frame_local129':copy.deepcopy(c['packet']['local_model'])}
 return CurrentContext(_TOKEN,payload,proof,deadline)
