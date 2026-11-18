"""Loopback-only experimental HTTP service. No changes to prior servers or databases."""
import argparse,json,hashlib
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import engine128
from service128 import Service
from reference128.render import encode as svg
from reference128.export_dxf import encode as dxf
from export_audit118 import audit_exports
ROOT=Path(__file__).resolve().parent

def revision():
 files=sorted(p for p in ROOT.rglob('*') if p.is_file() and (p.suffix=='.py' or (p.parent==ROOT and p.suffix=='.json') or p==ROOT/'reference128/index.html' or p.parent==ROOT/'references') and '__pycache__'not in p.parts and 'evidence'not in p.parts and 'audit_integration114'not in p.parts)
 return hashlib.sha256(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files},sort_keys=True).encode()).hexdigest()

def checked_artifact(candidate,kind):
 """Additional serialized-file checks after the independently admitted model.
 Does not relax gate: both serializers call admitted(), and service freshly
 evaluates model/source binding before invoking this function.
 """
 rev=revision();sb=svg(candidate,rev);db=dxf(candidate,rev)
 audit=audit_exports(candidate['model'],sb,db,rev)
 if audit['status']!='PASS_LIMITED':raise ValueError('SERIALIZED_EXPORT_AUDIT_FAILED:'+','.join(audit['errors']))
 if revision()!=rev:raise ValueError('SOURCE_CHANGED_DURING_EXPORT')
 if kind not in ('svg','dxf'):raise ValueError('ARTIFACT_TYPE')
 return sb if kind=='svg'else db

def main():
 a=argparse.ArgumentParser();a.add_argument('--port',type=int,default=8128);a.add_argument('--db',default=str(ROOT/'drafts128.sqlite'));a.add_argument('--budget',type=float,default=26);args=a.parse_args()
 service=Service(args.db,engine128.runtime,engine128.check_candidate,revision,{'svg':lambda c:checked_artifact(c,'svg'),'dxf':lambda c:checked_artifact(c,'dxf')},args.budget)
 class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
   if self.path=='/':b=(ROOT/'reference128/index.html').read_bytes();mime='text/html; charset=utf-8'
   elif self.path=='/health':b=json.dumps({'service':'GENERAL128_EXPERIMENTAL','source_revision':revision(),'solver_budget_seconds':args.budget,'not_final_acceptance':True}).encode();mime='application/json'
   else:self.send_error(404);return
   self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
  def do_POST(self):
   try:
    size=int(self.headers.get('Content-Length',0))
    if size<2 or size>65536:raise ValueError('REQUEST_SIZE')
    r=json.loads(self.rfile.read(size));p=service.handle(self.path,r)
   except Exception as e:p={'status':'REQUEST_FAILED','reason':str(e),'accepted':False}
   b=json.dumps(p,ensure_ascii=False).encode();self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
if __name__=='__main__':main()
