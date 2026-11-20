import http.client,importlib,json,sys,threading,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'engine'),str(ROOT/'frontend')]
import current_entry_launch_x03 as launch
class LauncherTests(unittest.TestCase):
 def test_unknown_historical_aliases_never_import(self):
  for name in ('frontend','backend','engine','current','latest','contract114','server390','../server','validation_server',True):
   with patch.object(launch.importlib,'import_module')as call:
    with self.assertRaisesRegex(ValueError,'HISTORICAL_SERVICE_CURRENT_DISABLED'):launch.server(name)
    call.assert_not_called()
 def test_two_real_http_interfaces_bounds_types_zero_dispatch(self):
  for service,module_name in (('PUBLIC_WLN_18X20','public_wln_server'),('REQUEST_TRACE_18X22','request_trace_server109')):
   s=launch.server(service);thread=threading.Thread(target=s.serve_forever,daemon=True);thread.start()
   module=importlib.import_module(module_name);dispatch='run_live'if module_name=='public_wln_server'else'run'
   # Existing trace server invokes run() for unsupported input as well; its
   # actual preflight path must stop before make_request/Popen, not a fake result.
   target=patch.object(module,'run_live',side_effect=AssertionError('DISPATCH_FORBIDDEN'))if dispatch=='run_live'else patch('request_trace109.make_request',side_effect=AssertionError('DISPATCH_FORBIDDEN'))
   try:
    with target as called:
     cases=[]
     for axis in ('W','L'):
      for value in ('5','25','4.999','25.001',True,None,'NaN'):
       raw={'W':'18','L':'22','n':2};raw[axis]=value
       cases.append((json.dumps(raw).encode(),409 if value in ('5','25')else 422))
     cases += [(b'{"W":18,"W":19,"L":22,"n":2}',422),(b'{"W":NaN,"L":22,"n":2}',422),
       (b'{"W":18,"L":Infinity,"n":2}',422),(b'{"W":18,"L":22,"n":true}',422),
       (b'{"W":18,"L":22,"n":2,"capability":true}',422),(b'{"W":18,"L":22,"n":1}',409)]
     for raw,status in cases:
      conn=http.client.HTTPConnection('127.0.0.1',s.server_port,timeout=5)
      conn.request('POST','/api/public/plan',body=raw,headers={'Content-Type':'application/json','Host':'127.0.0.1:'+str(s.server_port)})
      response=conn.getresponse();payload=json.loads(response.read());conn.close()
      self.assertEqual(response.status,status)
      self.assertIsNot(payload.get('qualified'),True);self.assertIsNot(payload.get('delivery_allowed'),True)
     called.assert_not_called()
   finally:s.shutdown();s.server_close();thread.join(timeout=5);self.assertFalse(thread.is_alive())
 def test_changed_server_after_factory_closes_socket(self):
  import public_wln_server
  original_read=Path.read_bytes;original_factory=public_wln_server.ThreadingHTTPServer
  objects=[];reads=[0]
  target=ROOT/'app/local_integration/public_wln_server.py'
  def read(path):
   data=original_read(path)
   if path==target:
    reads[0]+=1
    if objects:return data+b' changed' # mutate only after factory, independent of extra preflight reads
   return data
  def factory(*args,**kwargs):
   obj=original_factory(*args,**kwargs);objects.append(obj);return obj
  with patch.object(Path,'read_bytes',read),patch.object(public_wln_server,'ThreadingHTTPServer',factory):
   with self.assertRaisesRegex(ValueError,'CURRENT_SERVICE_CHANGED_DURING_STARTUP'):launch.server('PUBLIC_WLN_18X20')
  self.assertEqual(len(objects),1);self.assertEqual(objects[0].socket.fileno(),-1)
 def test_port_and_source_guard(self):
  for port in (True,-1,65536):
   with self.assertRaisesRegex(ValueError,'LOOPBACK_PORT_REQUIRED'):launch.server('PUBLIC_WLN_18X20',port)
  with patch.dict(launch.SERVICES,{'PUBLIC_WLN_18X20':('public_wln_server','0'*40)}):
   with self.assertRaisesRegex(ValueError,'CURRENT_SERVICE_SOURCE_CHANGED'):launch.server('PUBLIC_WLN_18X20')
if __name__=='__main__':unittest.main()
