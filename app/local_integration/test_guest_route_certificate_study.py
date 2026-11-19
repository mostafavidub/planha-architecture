import copy,pathlib,sys,unittest
sys.path[:0]=[str(pathlib.Path(__file__).resolve().parent),str(pathlib.Path(__file__).resolve().parents[1]/'reconstruction357/planha_general150_runtime_work')]
from guest_route_certificate_study import certify,overlay,digest,disposition,verify_report
def fixture():
 s={'parts':[['0','0','4','4']],'owner':[['0','0','4','4']],'box':['0','0','4','4'],'obstacles':[],'labels':[],'roles':['living'],'body':'.7'}
 r={'path':[['1','1'],['3','1']],'start':['1','1'],'end':['3','1'],'state':'PASS_SOURCE_PROFILE_ROUTE_ONLY','body_m':'.7','floor_roles':s['roles'],'floor_digest':digest(s['parts']),'ownership_digest':digest(s['owner']),'domain_box':s['box'],'obstacle_digest':digest([]),'obstacle_count':0,'id':'entry_living'}
 return r,s
class Certificates(unittest.TestCase):
 def test_exact_capacity_sweep_certificate(self):
  r,s=fixture();c=certify(r,s,digest(r['path']))
  self.assertEqual(c['capacity']['maximum_uniform_axis_aligned_square_width_m'],'2')
  self.assertTrue(c['capacity']['independent_certificate']['at_capacity_clear'])
 def intrusion(self,label):
  r,s=fixture();s['obstacles']=[['1.5','.8','2.5','1.2']];s['labels']=[label]
  r.update(obstacle_digest=digest(s['obstacles']),obstacle_count=1)
  with self.assertRaisesRegex(ValueError,'ROUTE_OBSTACLE_COLLISION'):certify(r,s,digest(r['path']))
 def test_fridge_intrusion(self):self.intrusion('kitchen_motion:4')
 def test_drawer_intrusion(self):self.intrusion('kitchen_motion:0')
 def test_floor_hole(self):
  r,s=fixture();s['parts']=[['0','0','1.5','4'],['2.5','0','4','4']];r['floor_digest']=digest(s['parts'])
  with self.assertRaisesRegex(ValueError,'ROUTE_DOMAIN_COVERAGE'):certify(r,s,digest(r['path']))
 def test_path_hash_mismatch(self):
  r,s=fixture();old=digest(r['path']);r['path'][0][0]='1.1'
  with self.assertRaisesRegex(ValueError,'PATH_DIGEST'):certify(r,s,old)
 def test_scenario_mismatch(self):
  r,s=fixture();s['obstacles']=[['3','3','4','4']];s['labels']=['kitchen_motion:4']
  with self.assertRaisesRegex(ValueError,'SCENARIO_BINDING'):certify(r,s,digest(r['path']))
 def test_body_profile_not_invented(self):
  r,s=fixture();s['body']='.6'
  with self.assertRaisesRegex(ValueError,'SOURCE_BODY'):certify(r,s,digest(r['path']))
 def test_source_error_not_relabelled_no_witness(self):
  self.assertEqual(disposition({'state':'UNKNOWN_EVALUATOR_OR_BINDING_ERROR'}),'SOURCE_EVALUATOR_OR_BINDING_ERROR')
  self.assertEqual(disposition({'state':'NO_WITNESS_IN_THIS_CONSERVATIVE_SCENARIO'}),'NO_SOURCE_WITNESS_CERTIFICATE_NOT_EVALUATED')
 def test_source_report_mutation_final_guard(self):
  r={'state':'UNKNOWN','rows':[]};pin=digest(r);r['rows'].append({'state':'PASS'})
  with self.assertRaisesRegex(ValueError,'SOURCE_REPORT_MUTATION'):verify_report(r,pin)
 def test_overlay_only_same_path_not_product(self):
  r,s=fixture();c=certify(r,s,digest(r['path']));v=overlay('A',r,s,c,'a'*64)
  self.assertIn('DIAGNOSTIC REVIEW ONLY / NOT QUALIFIED',v);self.assertIn('<polyline',v)
  self.assertNotIn('<script',v);self.assertNotIn('href=',v)
  import xml.etree.ElementTree as ET
  self.assertEqual(ET.fromstring(v).tag,'{http://www.w3.org/2000/svg}svg')
if __name__=='__main__':unittest.main()
