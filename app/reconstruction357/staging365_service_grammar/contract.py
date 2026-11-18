"""Pre-registered single FR branch proposal; no selection/admission authority."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
RAW={'W':'26','L':'28','n':2,'requested_count':2}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_request(raw):
 if type(raw)is not dict or set(raw)!=set(RAW)or any(type(raw[k])is not type(v)or raw[k]!=v for k,v in RAW.items()):raise ValueError('FIXED_REGISTERED_REQUEST_ONLY')
 return dict(raw)
def source_inventory():
 root=ROOT/'planha_general150_runtime_work'
 return {str(p.relative_to(ROOT)):sha(p)for p in sorted([*root.glob('*.py'),*root.glob('*.json'),*(p for p in (root/'references').rglob('*')if p.is_file()),HERE/'contract.py',HERE/'worker.py',HERE/'supervisor.py',HERE/'containment.py',HERE/'adapter365.py',HERE/'service_anchor365.py',HERE/'coarse_branch365.py'])}
def check_pins():
 pins=json.loads((HERE/'runtime_preregistered.json').read_text())
 if pins['source_inventory']!=source_inventory():raise ValueError('SOURCE_CHANGED')
 baseline=ROOT/pins['raw_source_record']
 if sha(baseline)!=pins['raw_source_sha256']:raise ValueError('RAW_SOURCE_CHANGED')
 rec=json.loads(baseline.read_text());validate_request(rec['trace']['raw'])
 return pins

def verify_program(proposal):
 if proposal.get('bedrooms')!=3 or proposal.get('sleep_roles')!=['double','twin','twin']or proposal.get('ordered_macro',{}).get('kind')!='PARALLEL_TWINS_BRANCH146':raise ValueError('SOURCE_PROGRAM_OR_BRANCH_CHANGED')
 return True
