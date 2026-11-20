"""Explicit loopback current study launcher. No historical dynamic-module launch.
Existing standalone legacy scripts remain executable, not accepted current entries.
"""
import argparse,hashlib,importlib,inspect,json
from pathlib import Path
from current_entry_boundary_x03 import ROOT,parser_guard,source_snapshot,need
SERVICES={
 'PUBLIC_WLN_18X20':('public_wln_server','0f5743a527a6a2832d6c03aad6f8daa5b94b77ba'),
 'REQUEST_TRACE_18X22':('request_trace_server109','fbe215097b43c576ff3c97d44e741cea3d0de834')}
DIAGNOSTICS_BLOB='4dba239c1484c6eda7985cde0b590680ec9ed3f3'
def diagnostics_guard():
 path=ROOT/'app/local_integration/public_input_errors403.py';data=path.read_bytes()
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==DIAGNOSTICS_BLOB,'CURRENT_DIAGNOSTICS_SOURCE_CHANGED')
 module=importlib.import_module('public_input_errors403')
 need(Path(inspect.getsourcefile(module.parse_public_errors)).resolve()==path.resolve(),'CURRENT_DIAGNOSTICS_IMPORT_PATH')
 module.guard()
 return hashlib.sha256(data).hexdigest()
def withholding_guard():
 path=ROOT/'app/local_integration/http_withholding_x04.py';data=path.read_bytes()
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()=='5207b00d3e30ac1a194a6605d50c26fd554f5c0d','CURRENT_WITHHOLDING_SOURCE_CHANGED')
 module=importlib.import_module('http_withholding_x04')
 need(Path(inspect.getsourcefile(module.Boundary)).resolve()==path.resolve() and Path(inspect.getsourcefile(module.Boundary.execute)).resolve()==path.resolve(),'CURRENT_WITHHOLDING_IMPORT_PATH')
 return hashlib.sha256(data).hexdigest()
def evidence_guard():
 path=ROOT/'app/local_integration/http_evidence_x07.py';data=path.read_bytes()
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()=='5d3579b01f10e3692aa01d23f9cc0d31e62e3aa8','CURRENT_EVIDENCE_SOURCE_CHANGED')
 module=importlib.import_module('http_evidence_x07')
 for fn in (module.run_bound,module.consume,module.guard):
  need(Path(inspect.getsourcefile(fn)).resolve()==path.resolve(),'CURRENT_EVIDENCE_IMPORT_PATH')
 module.guard()
 return hashlib.sha256(data).hexdigest()
P17_PINS={"stop_observation_p01.py":"e5421221179a78ad8e313a5e86ba8e000bc26b79","public_program_dispatch_p17.py":"65a9b9cb4a77925e442837429a5fa1e176860d2d","public_wln_server.py":"0f5743a527a6a2832d6c03aad6f8daa5b94b77ba","single_current_programme_evaluator_p17.py":"7ac2f8efcddab91bba747b7e232393ef6bda45a3","single_decision_p17.py":"717362f62c8eaef45ae065d0770d5517c44b7bbe","single_evaluation_p17.py":"23956db2458c1d0c416c5c39a24ec3b521766845","single_physical_p17.py":"16a16f20af2603ea67a2cb631954342462fe73a0","single_runtime_p17.py":"ca33f86aa6ca0d23aa59fa366698c268f9c7c936","single_source_guest_route_evaluator_p17.py":"e32189f2de3cea1545fba2c391468565dc4a0353","single_source_living_evaluator_p17.py":"cee0eb2d5262b99b553f38ef11c3a77a03e1cb10","single_source_wall_function_evaluator_p17.py":"8beab5c8b68d50458fd8edb10de3608ec5c1b2ca"}
def single_guard():
 observed={}
 for name,pin in P17_PINS.items():
  path=ROOT/'app/local_integration'/name;data=path.read_bytes()
  need(not path.is_symlink() and hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==pin,'SINGLE_SOURCE_CHANGED')
  observed[name]=hashlib.sha256(data).hexdigest()
 module=importlib.import_module('public_program_dispatch_p17')
 path=ROOT/'app/local_integration/public_program_dispatch_p17.py'
 for fn in (module.preflight,module.run_bound,module.is_single):
  need(Path(inspect.getsourcefile(fn)).resolve()==path.resolve(),'SINGLE_DISPATCH_IMPORT_PATH')
 return observed

def capacity_guard():
 path=ROOT/'app/local_integration/programme_prefilter_p05.py';data=path.read_bytes()
 need(not path.is_symlink() and hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
  =='d4935a015d44838a7d18c51132b1756f797ea036','CURRENT_CAPACITY_SOURCE_CHANGED')
 mod=importlib.import_module('programme_prefilter_p05')
 need(all(Path(inspect.getsourcefile(fn)).resolve()==path.resolve() for fn in
  (mod.capture_http,mod.attach_http,mod.inspect_request,mod.source_guard)),'CURRENT_CAPACITY_IMPORT_PATH')
 return hashlib.sha256(data).hexdigest()

def server(identifier,port=0):
 need(type(identifier)is str and identifier in SERVICES,'UNREGISTERED_OR_HISTORICAL_SERVICE_CURRENT_DISABLED')
 need(type(port)is int and 0<=port<=65535,'LOOPBACK_PORT_REQUIRED')
 before=parser_guard();diagnostic_pin=diagnostics_guard();name,pin=SERVICES[identifier]
 withholding_pin=withholding_guard() if identifier=='PUBLIC_WLN_18X20' else None
 evidence_pin=evidence_guard() if identifier=='PUBLIC_WLN_18X20' else None
 single_pin=single_guard() if identifier=='PUBLIC_WLN_18X20' else None
 capacity_pin=capacity_guard() if identifier=='PUBLIC_WLN_18X20' else None
 path=ROOT/'app/local_integration'/ (name+'.py');data=path.read_bytes()
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==pin,'CURRENT_SERVICE_SOURCE_CHANGED')
 module=importlib.import_module(name)
 need(Path(inspect.getsourcefile(module.server)).resolve()==path.resolve()
      and Path(inspect.getsourcefile(module.Handler.do_POST)).resolve()==path.resolve(),'CURRENT_SERVICE_IMPORT_PATH')
 need(source_snapshot()==before,'CURRENT_BOUNDARY_SOURCE_CHANGED')
 # Both source-pinned factories bind 127.0.0.1 and retain their own request gates.
 server=module.server(port)
 try:
  after=path.read_bytes()
  need(hashlib.sha1(b'blob '+str(len(after)).encode()+bytes([0])+after).hexdigest()==pin,'CURRENT_SERVICE_CHANGED_DURING_STARTUP')
  need(source_snapshot()==before and diagnostics_guard()==diagnostic_pin,'CURRENT_BOUNDARY_SOURCE_CHANGED')
  if withholding_pin is not None:need(withholding_guard()==withholding_pin,'CURRENT_WITHHOLDING_CHANGED_DURING_STARTUP')
  if evidence_pin is not None:need(evidence_guard()==evidence_pin,'CURRENT_EVIDENCE_CHANGED_DURING_STARTUP')
  if single_pin is not None:need(single_guard()==single_pin,'SINGLE_SOURCE_CHANGED_DURING_STARTUP')
  if capacity_pin is not None:need(capacity_guard()==capacity_pin,'CAPACITY_SOURCE_CHANGED_DURING_STARTUP')
  return server
 except BaseException:
  server.server_close()
  raise
def main():
 p=argparse.ArgumentParser(description='Scoped studies only; no product qualification, historical launcher or dynamic target.')
 p.add_argument('--service',required=True,choices=sorted(SERVICES));p.add_argument('--port',type=int,default=0)
 a=p.parse_args();s=server(a.service,a.port)
 print(json.dumps({'state':'LOOPBACK_STUDY_ONLY','service':a.service,'port':s.server_port,'qualified':False,'delivery_allowed':False}),flush=True)
 try:s.serve_forever()
 finally:s.server_close()
if __name__=='__main__':main()
