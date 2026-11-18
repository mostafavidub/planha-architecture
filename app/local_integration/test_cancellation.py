"""Real owned sleep-worker cancellation in temp storage; not geometry generation."""
import json,sys,socket,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import generation_gateway as gateway
from validation_server import Handler
class Cancellation(unittest.TestCase):
 def test_disconnect_stops_owned_worker_and_reaps(self):
  real_popen=subprocess.Popen;children=[]
  def launch(*args,**kw):
   p=real_popen([sys.executable,'-B','-c','import time;time.sleep(30)'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);children.append(p);return p
  with tempfile.TemporaryDirectory()as tmp,patch.object(gateway,'ROOT',Path(tmp)),patch.object(gateway.subprocess,'Popen',side_effect=launch):
   calls=[0]
   def cancelled():calls[0]+=1;return calls[0]>=2
   status,r=gateway.generate(b'{"W":"25","L":"25","n":2,"requested_count":1}',cancelled=cancelled)
   self.assertEqual(status,499);self.assertEqual(r['outcome'],'CANCELLED');self.assertFalse(r['delivery_allowed']);self.assertIsNotNone(children[0].poll())
   life=json.loads((Path(tmp)/'app/local_integration/evidence/requests'/r['run_id']/'lifecycle.json').read_text());self.assertTrue(life['wait_completed']);self.assertEqual(life['http_status'],499)
 def test_open_socket_not_cancelled(self):
  a,b=socket.socketpair()
  try:
   h=Handler.__new__(Handler);h.connection=a;self.assertFalse(h.request_disconnected())
  finally:a.close();b.close()
 def test_closed_socket_cancelled(self):
  a,b=socket.socketpair();b.close()
  try:
   h=Handler.__new__(Handler);h.connection=a;self.assertTrue(h.request_disconnected())
  finally:a.close()
 def test_unread_data_not_disconnect(self):
  a,b=socket.socketpair();b.send(b'x')
  try:
   h=Handler.__new__(Handler);h.connection=a;self.assertFalse(h.request_disconnected());self.assertEqual(a.recv(1),b'x')
  finally:a.close();b.close()
if __name__=='__main__':unittest.main()
