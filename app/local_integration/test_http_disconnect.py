"""Real loopback HTTP disconnect through unchanged Handler/generation paths.
Only child launch target and evidence ROOT are substituted. No mocked disconnect,
clock, cancellation callback, kill or reap. Not geometry or repair HTTP coverage.
"""
import http.client,json,os,signal,socket,subprocess,sys,tempfile,threading,time
from pathlib import Path
from unittest.mock import patch
from http.server import HTTPServer
import generation_gateway as generation
from validation_server import Handler
BODY=b'{"W":"25","L":"25","n":2,"requested_count":1}'

def wait_until(predicate,seconds,label):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        value=predicate()
        if value:return value
        time.sleep(.02)
    raise AssertionError(label)

def request(port,method,path,body=None):
    c=http.client.HTTPConnection('127.0.0.1',port,timeout=5)
    try:
        c.request(method,path,body=body,headers={'Content-Type':'application/json'}if body else {})
        r=c.getresponse();return r.status,json.loads(r.read())
    finally:c.close()

def run():
    real_popen=subprocess.Popen;real_clock=time.monotonic
    children=[];dispatch=[];client=None;server=None;thread=None
    with tempfile.TemporaryDirectory()as tmp:
        root=Path(tmp);ready=root/'worker-ready'
        def launch(argv,**kwargs):
            assert argv[0]==sys.executable and kwargs.get('start_new_session')is True
            assert Path(argv[2]).name=='parametric_worker.py'
            dispatch.append({'interpreter_is_active':True,'requested_new_session':True,'requested_worker':Path(argv[2]).name})
            p=real_popen([sys.executable,'-B','-c',
                'from pathlib import Path;import time,sys;Path(sys.argv[1]).write_text("ready");time.sleep(300)',str(ready)],
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            children.append(p)
            assert os.getpgid(p.pid)==p.pid
            return p
        with patch.object(generation,'ROOT',root),patch.object(generation.subprocess,'Popen',side_effect=launch):
            try:
                assert generation.time.monotonic is real_clock
                server=HTTPServer(('127.0.0.1',0),Handler)
                thread=threading.Thread(target=server.serve_forever,kwargs={'poll_interval':.05},daemon=True)
                thread.start();port=server.server_port
                hs,h=request(port,'GET','/health')
                assert hs==200 and h['accepted']is False and h['delivery_allowed']is False
                client=socket.create_connection(('127.0.0.1',port),timeout=5)
                raw=(b'POST /generate HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: application/json\r\nContent-Length: '+str(len(BODY)).encode()+b'\r\n\r\n'+BODY)
                client.sendall(raw)
                wait_until(lambda:len(children)==1 and ready.is_file(),10,'REAL_WORKER_NOT_READY')
                worker=children[0]
                folders=list((root/'app/local_integration/evidence/requests').iterdir())
                assert len(folders)==1;folder=folders[0]
                # More than several production .25-second cancellation polls while
                # the completed request socket remains connected and idle.
                hold_start=real_clock()
                while real_clock()-hold_start<1.25:
                    assert worker.poll()is None and not(folder/'result.json').exists()
                    time.sleep(.05)
                held=real_clock()-hold_start
                disconnected=real_clock()
                client.shutdown(socket.SHUT_RDWR);client.close();client=None
                def persisted():
                    try:
                        return json.loads((folder/'lifecycle.json').read_text())
                    except (FileNotFoundError,json.JSONDecodeError):return None
                life=wait_until(persisted,10,'DISCONNECT_LIFECYCLE_NOT_PERSISTED')
                elapsed=real_clock()-disconnected
                result=json.loads((folder/'result.json').read_text())
                assert len(children)==1 and life['pid']==worker.pid
                assert life['http_status']==499 and life['wait_completed']is True
                assert life['returncode']==-signal.SIGKILL and worker.poll()==-signal.SIGKILL
                try:os.killpg(worker.pid,0)
                except ProcessLookupError:group_absent=True
                else:raise AssertionError('OWNED_PROCESS_GROUP_REMAINS')
                assert result['outcome']=='CANCELLED' and result['code']=='REQUEST_DISCONNECTED'
                assert result['accepted']is False and result['delivery_allowed']is False
                assert result['run_id']==folder.name and (folder/'request.json').read_bytes()==BODY
                assert (folder/'stderr.txt').is_file()
                hs,h=request(port,'GET','/health')
                assert hs==200 and h['accepted']is False and h['delivery_allowed']is False
                bad=b'{"W":"26","L":"25","n":2,"requested_count":1}'
                badstatus,badresult=request(port,'POST','/generate',bad)
                assert badstatus in(409,422) and badresult['accepted']is False and badresult['delivery_allowed']is False
                assert len(children)==1 and len(list(folder.parent.iterdir()))==1
                assert generation.time.monotonic is real_clock
                report={'schema':'V25_REAL_HTTP_GENERATION_DISCONNECT_V1','status':'PASS_CONTROLLED_GENERATION_HTTP_DISCONNECT_ONLY',
                    'connected_idle_seconds':held,'disconnect_to_persisted_seconds':elapsed,
                    'actual_worker_ready':True,'cancelled_while_connected':False,'persisted_http_status':499,
                    'worker_returncode':worker.returncode,'wait_completed':True,'owned_process_group_absent':group_absent,
                    'post_disconnect_health_status':hs,'out_of_domain_status':badstatus,'out_of_domain_result':badresult,
                    'worker_launch_count':len(children),'dispatch':dispatch,'request_result_lifecycle_persisted':True,
                    'clock_accelerated':False,'disconnect_mocked':False,'accepted':False,'qualified':False,'delivery_allowed':False,
                    'scope':'Real TCP disconnect and production Handler cancellation with one controlled owned sleeping worker and temporary storage. 499 is persisted, not received by the disconnected client. No geometry, repair HTTP, descendant-process or all-race proof.'}
            finally:
                if client is not None:client.close()
                for p in children:
                    if p.poll()is None:
                        try:os.killpg(p.pid,signal.SIGKILL)
                        except ProcessLookupError:pass
                    p.wait(timeout=5)
                if server is not None:
                    server.shutdown();server.server_close()
                if thread is not None:
                    thread.join(timeout=5)
                    assert not thread.is_alive(),'HTTP_SERVER_THREAD_REMAINS'
                for p in children:
                    for stream in (p.stdin,p.stdout,p.stderr):
                        if stream is not None:stream.close()
        report['server_stopped_after_test']=True
        return report
