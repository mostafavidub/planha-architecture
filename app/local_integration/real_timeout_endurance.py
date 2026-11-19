"""Real wall-clock timeout endurance for owned controlled workers.
Launch target and evidence directory are substituted; deadlines, clocks, killpg,
communicate/reap and lifecycle persistence are actual production paths.
Not geometry generation, full HTTP/UI races or descendant-process proof.
"""
import json,os,signal,subprocess,sys,tempfile,time,datetime
from pathlib import Path
from unittest.mock import patch
import generation_gateway as generation
import repair_saved_run as repair
BODY=b'{"W":"25","L":"25","n":2,"requested_count":1}'

def run_one(module,is_repair):
    real_popen=subprocess.Popen;real_clock=time.monotonic;children=[];dispatch=[]
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def launch(argv,**kwargs):
        dispatch.append({'interpreter_is_active':argv[0]==sys.executable,'requested_new_session':kwargs.get('start_new_session')is True})
        assert argv[0]==sys.executable and kwargs.get('start_new_session')is True
        p=real_popen([sys.executable,'-B','-c','import time;time.sleep(300)'],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        assert os.getpgid(p.pid)==p.pid
        children.append(p);return p
    with tempfile.TemporaryDirectory()as tmp,patch.object(module,'BASE'if is_repair else'ROOT',Path(tmp)),patch.object(module.subprocess,'Popen',side_effect=launch):
        assert module.time.monotonic is real_clock
        begin=real_clock()
        status,result=module.execute('controlled-parent','controlled-candidate',BODY)if is_repair else module.generate(BODY)
        elapsed=real_clock()-begin
        assert module.time.monotonic is real_clock
        assert len(children)==1 and status==504 and result['outcome']=='EXECUTION_TIMEOUT'
        assert result['accepted']is False and result['delivery_allowed']is False
        assert 149<=elapsed<=180,('ACTUAL_TIMEOUT_DURATION',elapsed)
        worker=children[0];assert worker.returncode==-signal.SIGKILL and worker.poll()==-signal.SIGKILL
        try:os.killpg(worker.pid,0)
        except ProcessLookupError:group_absent=True
        else:raise AssertionError('OWNED_GROUP_REMAINS')
        folder=(Path(tmp)if is_repair else Path(tmp)/'app/local_integration/evidence/requests')/result['run_id']
        life=json.loads((folder/'lifecycle.json').read_text())
        saved=json.loads((folder/'result.json').read_text())
        assert life['pid']==worker.pid and life['returncode']==-signal.SIGKILL and life['wait_completed']is True and life['http_status']==504
        assert saved==result and (folder/'request.json').read_bytes()==BODY and (folder/'stderr.txt').is_file()
        return {'case':'repair_execute'if is_repair else'generation','started_at':started,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'elapsed_real_seconds':elapsed,'nominal_deadline_seconds':150,'controlled_sleep_seconds':300,
            'clock_accelerated':False,'dispatch':dispatch,'status':status,'outcome':result['outcome'],
            'worker_returncode':worker.returncode,'wait_completed':life['wait_completed'],'owned_process_group_absent':group_absent,
            'lifecycle_and_result_persisted':True,'accepted':False,'delivery_allowed':False,
            'scope':'Real deadline branch with controlled single owned subprocess and temporary evidence. Production worker dispatch body replaced, no geometry or full HTTP/UI proof.'}

def run():
    rows=[]
    for module,is_repair in ((generation,False),(repair,True)):
        row=run_one(module,is_repair);rows.append(row);print('ENDURANCE_CASE '+json.dumps(row),flush=True)
    return {'schema':'V25_REAL_TIMEOUT_ENDURANCE_V1','operation_start':'2026-11-19T01:09:46Z','operation_deadline':'2026-11-19T04:09:46Z','rows':rows,
        'status':'PASS_TWO_REAL_TIMEOUT_PATHS_ONLY','whole_cycle_verified':False,'qualified':False,'accepted':False,'delivery_allowed':False,
        'remaining':['Actual successful geometry and redesign are separate evidence','Full HTTP disconnect/cancellation timing and every UI race are not covered','Controlled single-process groups do not prove arbitrary descendant process behavior']}
if __name__=='__main__':
    Path('timeout-endurance.json').write_text(json.dumps(run(),indent=2))
