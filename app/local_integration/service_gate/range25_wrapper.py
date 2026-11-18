"""External launch-time HTTP pre-gate. Does not edit pinned service sources/DBs.
Historical reopen/artifact endpoints pass through unchanged. New generation
and review requests require each dimension in the exact current owner range.
"""
import io,json,re,runpy,sys,os
from pathlib import Path
from decimal import Decimal,InvalidOperation
TRANS=str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩٫','01234567890123456789.')
BANNER='<aside dir="rtl">قاعده جاری مالک: عرض و طول، هرکدام از ۵ تا ۲۵ متر شامل دو سر بازه؛ بزرگ‌تر از۲۵ خطاست. متن و شواهد نسخه‌های پیشین تاریخی‌اند، نه مجوز تولید خارج این بازه.</aside>'.encode()
def is_generation(path):
 return path=='/generate'or path.startswith('/generate-')or path=='/review-concept'
def validate(body):
 try:
  def pairs(xs):
   d={}
   for k,v in xs:
    if k in d:raise ValueError('DUPLICATE_FIELD')
    d[k]=v
   return d
  r=json.loads(body,object_pairs_hook=pairs)
  if type(r)is not dict:raise ValueError('OBJECT_REQUIRED')
  for axis in ('W','L'):
   v=r.get(axis)
   if type(v)not in(str,int):return 'EXACT_DECIMAL_REQUIRED',axis
   s=str(v).strip().translate(TRANS)
   if len(s)>64 or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',s):return 'EXACT_DECIMAL_REQUIRED',axis
   if not Decimal(5)<=Decimal(s)<=Decimal(25):return 'DIMENSION_OUT_OF_OWNER_RANGE',axis
 except (ValueError,TypeError,UnicodeError,InvalidOperation,RecursionError):return 'INVALID_JSON',None
 return None

def wrapped_handler(original):
 class Gated(original):
  def do_POST(self):
   if not is_generation(self.path):return super().do_POST()
   try:n=int(self.headers.get('Content-Length','0'))
   except ValueError:n=0
   if not 0<n<=65536:
    error=('REQUEST_SIZE',None);body=b''
   else:
    body=self.rfile.read(n);error=validate(body)if len(body)==n else('BODY_LENGTH_MISMATCH',None)
   if error:
    payload={'status':'INVALID_INPUT','outcome':'INVALID_INPUT','code':error[0],'reason':error[0],'field':error[1],'message':'عرض و طول باید هرکدام از۵تا۲۵متر باشند؛ مقدار خارج بازه رد شد.','candidates':[],'options':[],'accepted':False,'release_allowed':False,'delivery_allowed':False,'generation_started':False}
    data=json.dumps(payload,ensure_ascii=False).encode();self.send_response(422);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
   saved=self.rfile;self.rfile=io.BytesIO(body)
   try:return super().do_POST()
   finally:self.rfile=saved
  def do_GET(self):
   if self.path not in('/','/version116'):return super().do_GET()
   saved=self.wfile;capture=io.BytesIO();self.wfile=capture
   try:super().do_GET()
   finally:self.wfile=saved
   raw=capture.getvalue();head,sep,body=raw.partition(b'\r\n\r\n')
   if sep and b'text/html'in head.lower():
    body=BANNER+body;lines=[l for l in head.split(b'\r\n')if not l.lower().startswith(b'content-length:')];lines.append(b'Content-Length: '+str(len(body)).encode());raw=b'\r\n'.join(lines)+sep+body
   saved.write(raw)
 return Gated

def main():
 import http.server
 original=http.server.HTTPServer.__init__
 def init(self,address,handler,*a,**kw):
  if os.environ.get("PLANHA_GATE_TEST_PORT"):address=(address[0],int(os.environ["PLANHA_GATE_TEST_PORT"]))
  return original(self,address,wrapped_handler(handler),*a,**kw)
 http.server.HTTPServer.__init__=init
 target=Path(sys.argv[1]).resolve();sys.argv=sys.argv[1:];sys.path.insert(0,str(target.parent));runpy.run_path(str(target),run_name='__main__')
if __name__=='__main__':main()
