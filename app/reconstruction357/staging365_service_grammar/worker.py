"""One bounded proposal, explicit source365 build and full-trace replay. No fresh."""
import json,time
from contract import HERE,check_pins,validate_request,verify_program,source_inventory
from adapter365 import construct,replay
from coarse_branch365 import propose
from constructor129 import frame

def main():
 pins=check_pins();raw=validate_request(pins['raw']);before=source_inventory()
 def emit(phase,**kw):print(json.dumps({'phase':phase,**kw}),flush=True)
 core,_=frame(raw,'FRONT_REAR')
 emit('solver_begin',solver_calls=1,solver_limit_seconds=3)
 start=time.monotonic();p=propose(core,time_limit=3,gap_bodies=2)
 emit('solver_end',seconds=time.monotonic()-start,status=p.get('status'))
 (HERE/'proposal365.json').write_text(json.dumps(p,indent=2))
 if p.get('status')!='PROPOSAL_ONLY':emit('STOP_NO_PROPOSAL',status=p.get('status'),not_global_infeasibility=True);return
 verify_program(p);emit('source_build_begin');record=construct(raw,p)
 (HERE/'candidate365_unreplayed.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
 emit('independent_reconstruction_begin');rebuilt=replay(record['trace'])
 if source_inventory()!=before:raise ValueError('SOURCE_CHANGED')
 record['replay']={'status':'EXACT_FULL_TRACE_REBUILT','model_digest':rebuilt['candidate']['model_digest'],'fresh':False,'live_authority':False}
 (HERE/'candidate365.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
 emit('BUILD_AND_REPLAY_COMPLETE_NOT_ADMITTED',model_digest=record['candidate']['model_digest'],fresh_calls=0,retry=0)
if __name__=='__main__':main()
