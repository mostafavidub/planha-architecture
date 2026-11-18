"""Pure test compiles exact event/result expressions from frozen pipeline source.
No pipeline.execute, solver, producer or checker is executed here.
"""
import ast,copy,json,sys,time,uuid,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'staging368_final_pipeline/pipeline.py'
sys.path.insert(0,str(P.parent))
from request_contract368 import parse_json
from state_machine import event_view,final_view
class Protocol(unittest.TestCase):
 def setUp(self):
  self.tree=ast.parse(P.read_text());self.fn=next(x for x in self.tree.body if isinstance(x,ast.FunctionDef)and x.name=='execute');self.r=str(uuid.uuid4());self.e=parse_json('{"W":"26","L":"28","n":"2","requested_count":"2"}')
 def test_actual_nested_event_callback(self):
  f=next(x for x in self.fn.body if isinstance(x,ast.FunctionDef)and x.name=='event');events=[];received=[];errors=[];checks=[];ns={'run_id':self.r,'events':events,'on_event':lambda e:received.append(event_view(e,self.r)),'copy':copy,'callback_errors':errors,'check_request':lambda:checks.append(True)}
  exec(compile(ast.Module(body=[f],type_ignores=[]),str(P),'exec'),ns)
  ns['event'](kind='balanced',phase='construct',status='STARTED');ns['event'](kind='balanced',phase='construct',status='COMPLETED',candidate_id='c',review_id=None);ns['event'](kind='balanced',phase='review',status='COMPLETED',candidate_id='c',review_id=str(uuid.uuid4()))
  self.assertEqual(len(received),3);self.assertEqual(errors,[]);self.assertIsNone(received[1]['review_id']);self.assertEqual(len(checks),3)
 def test_actual_result_expression(self):
  node=next(x for x in self.fn.body if isinstance(x,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='out'for t in x.targets));ns={'run_id':self.r,'e':self.e,'status':'REVIEWED_NOT_QUALIFIED','members':[],'events':[],'callback_errors':[],'time':time,'started':time.monotonic()};result=eval(compile(ast.Expression(node.value),str(P),'eval'),ns)
  self.assertEqual(result['state'],result['status']);self.assertEqual(final_view(result,self.e,self.r)['state'],'REVIEWED_NOT_QUALIFIED');self.assertFalse(result['accepted'])
 def test_worker_import_resolution_prefers_pipeline(self):
  source=(Path(__file__).with_name('pipeline_worker.py')).read_text();self.assertIn("sys.path[:0]=[str(ROOT/'staging368_final_pipeline'),str(HERE)]",source)
if __name__=='__main__':unittest.main()
