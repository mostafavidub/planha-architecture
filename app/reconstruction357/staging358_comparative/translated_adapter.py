"""New357 source assembly/replay. Not recovered old354 source or verdict."""
import sys,json,copy,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'planha_general150_runtime_work';sys.path.insert(0,str(ROOT))
from contract114 import digest
from constructor129 import build,context

def sources():
 return {str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted([*ROOT.glob('*.py'),*ROOT.glob('*.json'),*(q for q in(ROOT/'references').rglob('*')if q.is_file()),*Path(__file__).parent.glob('*.py')])}
def construct(raw,proposal):
 if proposal['generation_method']!='ANCHORED_TRANSLATED_PRIVATE357_REQUIRES_REPLAY_AND_FRESH':raise ValueError('PRODUCER_SCOPE')
 if proposal['sleep_roles']!=['double','twin','twin']or proposal['bedrooms']!=3:raise ValueError('PROGRAM')
 from packing_validator import verify as verify_packing
 check=verify_packing(raw,proposal)
 if check['errors']:raise ValueError('INDEPENDENT_PACKING_FAILED:'+str(check['errors']))
 before=sources();packet=build(copy.deepcopy(raw),'FRONT_REAR',copy.deepcopy(proposal));ctx=context(raw,proposal,packet)
 candidate={'request':raw,'request_digest':digest(raw),'packet':packet,'model':packet['world_model'],'model_digest':digest(packet['world_model']),'generation_context':ctx}
 manifest=json.loads(Path(__file__).with_name('source_manifest.json').read_text())
 trace={'schema':'TRANSLATED_PRIVATE357_SOURCE_TRACE_V1','raw':raw,'proposal':proposal,'model_digest':candidate['model_digest'],'candidate_digest':digest(candidate),'source_inventory':before,'source_manifest_digest':digest(manifest),'requires_fresh':True,'accepted':False}
 if before!=sources():raise ValueError('SOURCE_CHANGED')
 return {'candidate':candidate,'trace':trace,'accepted':False}
def replay(trace):
 if trace['source_inventory']!=sources():raise ValueError('SOURCE_DRIFT')
 result=construct(trace['raw'],trace['proposal'])
 if digest(result['candidate'])!=trace['candidate_digest']:raise ValueError('EXACT_REPLAY_MISMATCH')
 return {'status':'EXACT_RECONSTRUCTION_ONLY','candidate':result['candidate'],'accepted':False}
if __name__=='__main__':
 b=json.loads((BASE/'actual_run/actual_response.json').read_text());p=json.loads(Path(__file__).with_name('anchored_proposal357.json').read_text());x=construct(b['raw'],p);Path(__file__).with_name('anchored_candidate357.json').write_text(json.dumps(x,ensure_ascii=False,indent=2));print(x['candidate']['model_digest'],len(x['candidate']['model']['route_failures']))
