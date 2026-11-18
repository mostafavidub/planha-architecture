"""Local, bounded subprocess dispatch for the parametric experiment, not release."""
import json
import os
from pathlib import Path
import signal
import subprocess
import uuid
import time
from dimension_contract import InputError
from parametric_worker import ROOT,SCHEMA,prepare


def generate(body, cancelled=None):
    try:
        prepare(body)
    except InputError as error:
        return error.status,{'schema':SCHEMA,'outcome':'INVALID_INPUT' if error.status==422 else 'UNSUPPORTED','code':error.code,'field':error.field,'accepted':False,'delivery_allowed':False}
    here=Path(__file__).resolve().parent
    python=ROOT/'app/local_integration/.venv/bin/python'
    run_id=str(uuid.uuid4())
    evidence=ROOT/'app/local_integration/evidence/requests'/run_id
    evidence.mkdir(parents=True,exist_ok=False)
    (evidence/'request.json').write_bytes(body)
    try:
        worker=subprocess.Popen([str(python),'-B',str(here/'parametric_worker.py')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    except OSError as error:
        result={'schema':SCHEMA,'outcome':'DEPENDENCY_UNAVAILABLE','code':'WORKER_START_FAILED','run_id':run_id,'accepted':False,'delivery_allowed':False}
        (evidence/'stderr.txt').write_text(type(error).__name__)
        (evidence/'result.json').write_text(json.dumps(result))
        (evidence/'lifecycle.json').write_text(json.dumps({'pid':None,'worker_started':False,'returncode':None,'wait_completed':True,'http_status':503}))
        return 503,result
    cancelled_run=False
    try:
        deadline=time.monotonic()+150
        first=True
        while True:
            if cancelled is not None and cancelled():
                try:os.killpg(worker.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                stdout,stderr=worker.communicate()
                result={'schema':SCHEMA,'outcome':'CANCELLED','code':'REQUEST_DISCONNECTED','run_id':run_id,'accepted':False,'delivery_allowed':False}
                status=499
                cancelled_run=True
                break
            remaining=deadline-time.monotonic()
            if remaining<=0:raise subprocess.TimeoutExpired(worker.args,150)
            try:
                data=body if first else None;first=False
                stdout,stderr=worker.communicate(data,timeout=min(.25,remaining))
                break
            except subprocess.TimeoutExpired:
                continue
    except subprocess.TimeoutExpired:
        try:os.killpg(worker.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        stdout,stderr=worker.communicate()
        result={'schema':SCHEMA,'outcome':'EXECUTION_TIMEOUT','code':'BOUNDED_WORKER_TIMEOUT','run_id':run_id,'accepted':False,'delivery_allowed':False}
        status=504
    else:
        try:
            if cancelled_run:raise InterruptedError('REQUEST_DISCONNECTED')
            if worker.returncode:raise ValueError('WORKER_EXIT_NONZERO')
            result=json.loads(stdout)
            if result.get('schema')!=SCHEMA or result.get('accepted')is not False or result.get('delivery_allowed')is not False:raise ValueError('WORKER_RESPONSE_CONTRACT')
            # Verify request binding using the exact HTTP body, not caller identity.
            from dimension_contract import verify
            verify(body,result['envelope'])
            result['run_id']=run_id
            for candidate in result.get('candidates',[]):
                text=json.dumps(candidate['model'],ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
                import hashlib
                if hashlib.sha256(text.encode()).hexdigest()!=candidate['model_digest']:raise ValueError('MODEL_DIGEST_MISMATCH')
                candidate['model_json']=text
            status=200
        except InterruptedError:
            pass
        except (ValueError,KeyError,TypeError) as error:
            status=500
            result={'schema':SCHEMA,'outcome':'EXECUTION_ERROR','code':str(error),'run_id':run_id,'accepted':False,'delivery_allowed':False}
    (evidence/'stderr.txt').write_bytes(stderr)
    (evidence/'result.json').write_text(json.dumps(result,ensure_ascii=False,allow_nan=False))
    (evidence/'lifecycle.json').write_text(json.dumps({'pid':worker.pid,'returncode':worker.returncode,'wait_completed':worker.poll() is not None,'http_status':status}))
    return status,result
