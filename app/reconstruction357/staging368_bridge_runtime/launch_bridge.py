"""Pinned launcher: exclusively owns the semantic child and its cleanup."""
import sys,json,hashlib,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE_SHA='5e757cf39d98cd6f54c18c09f3eef5d9ff1cab3ed0e43580ed319a995ea3694a'
BOOTSTRAP_SHA='6a2c4e091198f80af20ef216c951566e0ad44bffba6018f2c80d294428330cf2'
p=HERE/'bootstrap.py'
if hashlib.sha256(p.read_bytes()).hexdigest()!=BOOTSTRAP_SHA:raise ValueError('BOOTSTRAP_PREIMPORT')
from bootstrap import ROOT,verify_freeze,run_folder,read_inputs,write_once,digest,completed
verify_freeze(FREEZE_SHA)
run_id=sys.argv[1];folder=run_folder(run_id);request,raw,before=read_inputs(folder,run_id)
write_once(folder/'bridge_started.json',{'generation_run_id':run_id,'limit_seconds':60,'source_freeze_sha256':FREEZE_SHA,'raw_pipeline_digest':digest(raw)})
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from supervisor import supervise
s=supervise([sys.executable,'-B',str(HERE/'worker.py'),run_id,FREEZE_SHA,BOOTSTRAP_SHA],60,evidence_directory=folder)
write_once(folder/'bridge_supervision.json',s)
verify_freeze(FREEZE_SHA)
if before!={n:hashlib.sha256((folder/n).read_bytes()).hexdigest()for n in before}:raise ValueError('BRIDGE_INPUT_CHANGED')
if not completed(s)or not(folder/'bridge_result.json').is_file():raise SystemExit(1)
r=json.loads((folder/'bridge_result.json').read_text())
if r.get('generation_run_id')!=run_id or r.get('raw_pipeline_digest')!=digest(raw)or r.get('request_digest')!=digest(request)or r.get('source_unchanged')is not True or r.get('source_freeze_sha256')!=FREEZE_SHA:raise ValueError('BRIDGE_RECEIPT_BINDING')
# Derived report remains distinct from immutable physical pipeline result.
write_once(folder/'final_result.json',{'schema':'DERIVED_FINAL_REPORT368','generation_run_id':run_id,'raw_pipeline_digest':digest(raw),'bridge_receipt_digest':digest(r),'supervision_digest':digest(s),'qualified_set':r['bridge_result'],'accepted':False,'delivery_allowed':False})
