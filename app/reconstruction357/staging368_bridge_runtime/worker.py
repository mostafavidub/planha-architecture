"""One isolated semantic bridge evaluation. No producer or checker execution."""
import sys,hashlib,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
# Bootstrap bytes and external freeze are supplied only by pinned launcher.
run_id,freeze_sha,bootstrap_sha=sys.argv[1:]
p=HERE/'bootstrap.py'
if hashlib.sha256(p.read_bytes()).hexdigest()!=bootstrap_sha:raise ValueError('BOOTSTRAP_PREIMPORT')
from bootstrap import ROOT,verify_freeze,run_folder,read_inputs,write_once,digest
verify_freeze(freeze_sha)
folder=run_folder(run_id);request,raw,before=read_inputs(folder,run_id)
if (folder/'bridge_result.json').exists()or(folder/'final_result.json').exists():raise ValueError('BRIDGE_WRITE_ONCE')
sys.path.insert(0,str(ROOT/'staging368_semantic_bridge'))
from current_run import qualify_run
start=time.monotonic();result=qualify_run(folder,request['envelope'],raw)
verify_freeze(freeze_sha)
if before!={n:hashlib.sha256((folder/n).read_bytes()).hexdigest()for n in before}:raise ValueError('BRIDGE_MUTATED_RAW_INPUT')
if result.get('generation_run_id')!=run_id:raise ValueError('BRIDGE_OUTPUT_RUN_BINDING')
write_once(folder/'bridge_result.json',{'schema':'ISOLATED_BRIDGE368_RESULT','generation_run_id':run_id,'raw_pipeline_digest':digest(raw),'request_digest':digest(request),'input_file_hashes':before,'bridge_result':result,'seconds':time.monotonic()-start,'source_freeze_sha256':freeze_sha,'source_unchanged':True,'accepted':False,'delivery_allowed':False})
