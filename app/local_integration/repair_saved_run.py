"""Explicit local continuation of one saved natural rejection; hard150s, no delivery."""
import argparse,json,os,signal,subprocess,sys,uuid,time
from pathlib import Path
from repair_saved_worker import load_source,BASE,SCHEMA
from dimension_contract import _pairs,_nonfinite,parse,InputError

def repair(body,cancelled=None):
    try:
        args=json.loads(body,object_pairs_hook=_pairs,parse_constant=_nonfinite)
        if type(args)is not dict or set(args)!={'run_id','candidate_id'}:raise ValueError('REPAIR_REQUEST_FIELDS')
        original,_,_=load_source(args['run_id'],args['candidate_id'])
    except InputError as error:
        return error.status,{"schema":SCHEMA,"outcome":"INVALID_INPUT","code":error.code,"field":error.field,"accepted":False,"delivery_allowed":False}
    except (ValueError,KeyError,TypeError,OSError,RecursionError):
        return 422,{'schema':SCHEMA,'outcome':'INVALID_REPAIR_SOURCE','code':'VERIFIED_NATURAL_REJECTION_REQUIRED','accepted':False,'delivery_allowed':False}
    return execute(args['run_id'],args['candidate_id'],original,cancelled)

def execute(source_run,candidate_id,body,cancelled=None):
    try:parse(body)
    except InputError as error:
        return error.status,{"schema":SCHEMA,"outcome":"INVALID_INPUT","code":error.code,"field":error.field,"accepted":False,"delivery_allowed":False}
    run_id=str(uuid.uuid4());folder=BASE/run_id;folder.mkdir(parents=True,exist_ok=False);(folder/'request.json').write_bytes(body)
    try:
        w=subprocess.Popen([sys.executable,'-B',str(Path(__file__).with_name('repair_saved_worker.py')),source_run,candidate_id,run_id],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    except OSError as error:
        result={'schema':SCHEMA,'outcome':'DEPENDENCY_UNAVAILABLE','code':'REPAIR_WORKER_START_FAILED','run_id':run_id,'accepted':False,'delivery_allowed':False}
        (folder/'stderr.txt').write_text(type(error).__name__);(folder/'result.json').write_text(json.dumps(result));(folder/'lifecycle.json').write_text(json.dumps({'pid':None,'worker_started':False,'returncode':None,'wait_completed':True,'http_status':503}))
        return 503,result
    def stopped(status,outcome,code):
        try:os.killpg(w.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        out,err=w.communicate()
        return status,{'schema':SCHEMA,'outcome':outcome,'code':code,'run_id':run_id,'accepted':False,'delivery_allowed':False},err
    deadline=time.monotonic()+150
    while True:
        if cancelled is not None and cancelled():
            status,result,err=stopped(499,'CANCELLED','REQUEST_DISCONNECTED');break
        remaining=deadline-time.monotonic()
        if remaining<=0:
            status,result,err=stopped(504,'EXECUTION_TIMEOUT','BOUNDED_REPAIR_TIMEOUT');break
        try:out,err=w.communicate(timeout=min(.25,remaining))
        except subprocess.TimeoutExpired:continue
        try:
            if w.returncode:raise ValueError('REPAIR_WORKER_FAILED')
            result=json.loads(out)
            if result['run_id']!=run_id or result['parent_run_id']!=source_run or result['accepted']is not False or result['delivery_allowed']is not False:raise ValueError('REPAIR_RESPONSE_BINDING')
            from dimension_contract import verify
            verify(body,result['envelope'])
            if len(result['candidates'])!=1:raise ValueError('REPAIR_COUNT')
            receipt=result['candidates'][0]['repair_receipt']
            if receipt['parent_run_id']!=source_run or receipt['parent_candidate_id']!=candidate_id or receipt['test_only']is not False or receipt['natural_failure']is not True:raise ValueError('REPAIR_PARENT_BINDING')
            result['original_request_body']=body.decode('utf-8');status=200
        except (ValueError,KeyError,TypeError):
            status=500;result={'schema':SCHEMA,'outcome':'EXECUTION_ERROR','code':'REPAIR_WORKER_FAILED','run_id':run_id,'accepted':False,'delivery_allowed':False}
        break
    (folder/'stderr.txt').write_bytes(err);(folder/'result.json').write_text(json.dumps(result,ensure_ascii=False,allow_nan=False));(folder/'lifecycle.json').write_text(json.dumps({'pid':w.pid,'returncode':w.returncode,'wait_completed':w.poll()is not None,'http_status':status}))
    if status==200:
        try:
            from run_history import summary
            summary(run_id)
        except (ValueError,KeyError,TypeError,OSError):
            status=500;result={'schema':SCHEMA,'outcome':'EXECUTION_ERROR','code':'REPAIR_RECORD_VERIFICATION_FAILED','run_id':run_id,'accepted':False,'delivery_allowed':False}
            (folder/'result.json').write_text(json.dumps(result));(folder/'lifecycle.json').write_text(json.dumps({'pid':w.pid,'returncode':w.returncode,'wait_completed':True,'http_status':status}))
    return status,result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',required=True);p.add_argument('--candidate',required=True);args=p.parse_args()
    status,result=repair(json.dumps({'run_id':args.run,'candidate_id':args.candidate}).encode())
    print(json.dumps({'run_id':result.get('run_id'),'status':status,'outcome':result['outcome'],'receipt':result.get('candidates',[{}])[0].get('repair_receipt')}),flush=True)
    if status!=200:sys.exit(1)
if __name__=='__main__':main()
