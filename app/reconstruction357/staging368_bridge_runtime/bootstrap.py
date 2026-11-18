"""Stdlib-only closed run path and preimport closure checks."""
import json,hashlib,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent

def digest(x):
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def verify_freeze(expected):
 if len(expected)!=64:raise ValueError('BRIDGE_FREEZE_NOT_RELEASED')
 p=HERE/'source_freeze.json';data=p.read_bytes()
 if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('BRIDGE_EXTERNAL_FREEZE')
 f=json.loads(data)
 for n,h in f['files'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('BRIDGE_SOURCE_DRIFT:'+n)
 return f

def run_folder(run_id):
 if type(run_id)is not str or str(uuid.UUID(run_id))!=run_id:raise ValueError('CANONICAL_RUN_ID_REQUIRED')
 root=ROOT/'review368_runs';p=root/run_id
 if p.is_symlink()or p.resolve().parent!=root.resolve()or not p.is_dir():raise ValueError('FIXED_RUN_FOLDER_REQUIRED')
 return p

def read_inputs(folder,run_id):
 for n in('request.json','result.json'):
  if (folder/n).is_symlink():raise ValueError('SYMLINK_INPUT')
 request=json.loads((folder/'request.json').read_text());raw=json.loads((folder/'result.json').read_text())
 if set(request)!={'run_id','envelope'}or request['run_id']!=run_id:raise ValueError('REQUEST_RUN_BINDING')
 if raw.get('schema')!='FINAL_PIPELINE368_RUN'or raw.get('generation_run_id')!=run_id or raw.get('status')!='REVIEWED_NOT_QUALIFIED':raise ValueError('COMPLETED_RAW_PIPELINE_REQUIRED')
 return request,raw,{n:hashlib.sha256((folder/n).read_bytes()).hexdigest()for n in('request.json','result.json')}

def write_once(path,value):
 with path.open('x')as f:json.dump(value,f,ensure_ascii=False,indent=2)

def completed(s):
 return s.get('reason')=='COMPLETED'and type(s.get('worker_returncode'))is int and s['worker_returncode']==0 and s.get('cleanup_verified')is True and s.get('worker_reaped')is True and s.get('unresolved')==[]
