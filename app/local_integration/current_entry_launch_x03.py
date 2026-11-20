"""Explicit loopback current study launcher. No historical dynamic-module launch.
Existing standalone legacy scripts remain executable, not accepted current entries.
"""
import argparse,hashlib,importlib,inspect,json
from pathlib import Path
from current_entry_boundary_x03 import ROOT,parser_guard,source_snapshot,need
SERVICES={
 'PUBLIC_WLN_18X20':('public_wln_server','8fe1afe174b621e57cabbe38f576ca93bc7890c3'),
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
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()=='706c33b6dc8f793f423d89dffa43c4ff71ffa79c','CURRENT_WITHHOLDING_SOURCE_CHANGED')
 module=importlib.import_module('http_withholding_x04')
 need(Path(inspect.getsourcefile(module.Boundary)).resolve()==path.resolve() and Path(inspect.getsourcefile(module.Boundary.execute)).resolve()==path.resolve(),'CURRENT_WITHHOLDING_IMPORT_PATH')
 return hashlib.sha256(data).hexdigest()
def evidence_guard():
 path=ROOT/'app/local_integration/http_evidence_x07.py';data=path.read_bytes()
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()=='b23153874b7a4b2f10f170afcd38c6d4238cb852','CURRENT_EVIDENCE_SOURCE_CHANGED')
 module=importlib.import_module('http_evidence_x07')
 for fn in (module.run_bound,module.consume,module.guard):
  need(Path(inspect.getsourcefile(fn)).resolve()==path.resolve(),'CURRENT_EVIDENCE_IMPORT_PATH')
 module.guard()
 return hashlib.sha256(data).hexdigest()
P17_PINS={"public_program_dispatch_p17.py":"ce4f2772a1ffd353556735003bfd128465a03adf","public_wln_server.py":"8fe1afe174b621e57cabbe38f576ca93bc7890c3","single_current_programme_evaluator_p17.py":"7ac2f8efcddab91bba747b7e232393ef6bda45a3","single_decision_p17.py":"dc7d5ab899c315a6aae3f636c50dcc94aaebaddd","single_evaluation_p17.py":"1c01902a836e69b22327b32287f28837fbb6e862","single_physical_p17.py":"16a16f20af2603ea67a2cb631954342462fe73a0","single_runtime_p17.py":"6f30a919954e693c98068ee45900f7efd817263a","single_source_guest_route_evaluator_p17.py":"e32189f2de3cea1545fba2c391468565dc4a0353","single_source_living_evaluator_p17.py":"cee0eb2d5262b99b553f38ef11c3a77a03e1cb10","single_source_wall_function_evaluator_p17.py":"8beab5c8b68d50458fd8edb10de3608ec5c1b2ca"}
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

def server(identifier,port=0):
 need(type(identifier)is str and identifier in SERVICES,'UNREGISTERED_OR_HISTORICAL_SERVICE_CURRENT_DISABLED')
 need(type(port)is int and 0<=port<=65535,'LOOPBACK_PORT_REQUIRED')
 before=parser_guard();diagnostic_pin=diagnostics_guard();name,pin=SERVICES[identifier]
 withholding_pin=withholding_guard() if identifier=='PUBLIC_WLN_18X20' else None
 evidence_pin=evidence_guard() if identifier=='PUBLIC_WLN_18X20' else None
 single_pin=single_guard() if identifier=='PUBLIC_WLN_18X20' else None
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
