"""Loopback-only experimental HTTP service. No changes to prior servers or databases."""
import argparse,json,hashlib
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import engine114
from service115 import Service
from reference115.render import encode as svg
from reference115.export_dxf import encode as dxf
ROOT=Path(__file__).resolve().parent

def revision():
 files=sorted(p for p in ROOT.rglob('*') if p.is_file() and (p.suffix=='.py' or p in [ROOT/'fixture_catalog114.json', ROOT/'reference115/index.html'] or p.parent==ROOT/'references') and '__pycache__'not in p.parts and 'evidence'not in p.parts and 'audit_integration114'not in p.parts)
 return hashlib.sha256(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files},sort_keys=True).encode()).hexdigest()

def main():
 a=argparse.ArgumentParser();a.add_argument('--port',type=int,default=8115);a.add_argument('--db',default=str(ROOT/'drafts115.sqlite'));a.add_argument('--budget',type=float,default=15);args=a.parse_args()
 service=Service(args.db,engine114.run,engine114.check_candidate,revision,{'svg':lambda c:svg(c,revision()),'dxf':lambda c:dxf(c,revision())},args.budget)
 class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
   if self.path=='/':b=(ROOT/'reference115/index.html').read_bytes();mime='text/html; charset=utf-8'
   elif self.path=='/health':b=json.dumps({'service':'GENERAL115_EXPERIMENTAL','source_revision':revision(),'solver_budget_seconds':args.budget,'not_final_acceptance':True}).encode();mime='application/json'
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
