"""One fresh HTTP request; public output is counts/enums/hashes only."""
import http.client,json,sys,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
from request_trace_server109 import server
s=server();t=threading.Thread(target=s.serve_forever,daemon=True);t.start()
try:
 c=http.client.HTTPConnection('127.0.0.1',s.server_address[1],timeout=255)
 c.request('POST','/api/public/plan',b'{"W":"18","L":"22","n":2}',{'Content-Type':'application/json'})
 response=c.getresponse();result=json.loads(response.read());c.close()
 print(json.dumps({'http_status':response.status,'result':result},sort_keys=True,allow_nan=False),flush=True)
 assert response.status==200
 r=result['study_result'];assert r['receipt_verified']is True and r['source_integrity_verified']is True
 assert r['child_count']==0 and r['attempt_count']==1 and r['state']in('BLOCKED_NO_SUPPORTED_CAUSE','BLOCKED_REPAIR_CONTROLLER_ADAPTER','BLOCKED_NO_PARENT_PROPOSAL')
 assert all(r[k]is False for k in('accepted','qualified','display_allowed','delivery_allowed'))
finally:s.shutdown();s.server_close();t.join()
