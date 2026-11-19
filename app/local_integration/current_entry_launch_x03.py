"""Explicit loopback current study launcher. No historical dynamic-module launch.
Existing standalone legacy scripts remain executable, not accepted current entries.
"""
import argparse,hashlib,importlib,inspect,json
from pathlib import Path
from current_entry_boundary_x03 import ROOT,parser_guard,source_snapshot,need
SERVICES={
 'PUBLIC_WLN_18X20':('public_wln_server','b3cb9e9ad0ef34349d3c6740f6285f95b865371a'),
 'REQUEST_TRACE_18X22':('request_trace_server109','fbe215097b43c576ff3c97d44e741cea3d0de834')}
DIAGNOSTICS_BLOB='4dba239c1484c6eda7985cde0b590680ec9ed3f3'
def diagnostics_guard():
 path=ROOT/'app/local_integration/public_input_errors403.py';data=path.read_bytes()
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==DIAGNOSTICS_BLOB,'CURRENT_DIAGNOSTICS_SOURCE_CHANGED')
 module=importlib.import_module('public_input_errors403')
 need(Path(inspect.getsourcefile(module.parse_public_errors)).resolve()==path.resolve(),'CURRENT_DIAGNOSTICS_IMPORT_PATH')
 module.guard()
 return hashlib.sha256(data).hexdigest()
def server(identifier,port=0):
 need(type(identifier)is str and identifier in SERVICES,'UNREGISTERED_OR_HISTORICAL_SERVICE_CURRENT_DISABLED')
 need(type(port)is int and 0<=port<=65535,'LOOPBACK_PORT_REQUIRED')
 before=parser_guard();diagnostic_pin=diagnostics_guard();name,pin=SERVICES[identifier]
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
