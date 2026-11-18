import unittest,uuid,copy
from state_machine import digest,final_view

def fixture():
 run=str(uuid.uuid4());e={'canonical_request_digest':'c','raw_digest':'r','received_digest':'i','normalized_raw':{'requested_count':2}};members=[];selected=[];pairs=[]
 for kind in ('balanced','joint'):
  b={'run_id':run,'candidate_id':kind,'review_id':str(uuid.uuid4()),'model_digest':'m'+kind,'fresh_digest':'f'+kind,**{k:e[k]for k in ('canonical_request_digest','raw_digest','received_digest')}}
  base={'run_id':run,'candidate_id':kind,'review_id':b['review_id'],'model_hash':b['model_digest'],'current_fresh_digest':b['fresh_digest'],'missing':[],'verdict':'PASS'}
  quality=[dict(base,rule_id=str(i))for i in range(11)]
  q12=[{'run_id':run,'candidate_id':kind,'review_id':b['review_id'],'model_digest':b['model_digest'],'fresh_digest':b['fresh_digest'],'missing':[],'unit':u}for u in ('A','B')]
  selected.append({'binding':b,'eleven_attestations_digest':digest(quality),'q12_digest':digest(q12)})
  quality.append(dict(base,rule_id='DISTINCTNESS_AND_FAIRNESS'));members.append({'kind':kind,'binding':b,'quality':quality,'current_roles':{'q12':q12}})
  pairs.append({'kind':kind,'generation_run_id':run,'candidate_id':kind,'review_id':b['review_id'],'model_digest':b['model_digest'],'current_fresh_digest':b['fresh_digest']})
 q={**{k:e[k]for k in ('canonical_request_digest','raw_digest','received_digest')},'normalized_raw_digest':e['raw_digest'],'generation_run_id':run,'membership_authority':True,'qualified_selected_count':2,'requested_count':2,'members':selected,'pair':{'members':pairs,'pair_count':1,'source_organization_distinct':True}};q['set_digest']=digest(q)
 for m in members:m['quality'][-1]['source_closure']={'current_set_digest':q['set_digest'],'current_pair_digest':digest(q['pair']),'independent_current_q12_digest':digest(m['current_roles']['q12'])}
 return {'state':'QUALIFIED_CONCEPTUAL_SET','generation_run_id':run,'canonical_request_digest':'c','raw_digest':'r','members':members,'qualified_set':q},e,run
class Tests(unittest.TestCase):
 def test_bound(self):
  x,e,r=fixture();self.assertEqual(final_view(x,e,r)['state'],'QUALIFIED_CONCEPTUAL_SET')
 def test_wrong_set_run(self):
  x,e,r=fixture();x['qualified_set']['generation_run_id']='stale'
  with self.assertRaises(ValueError):final_view(x,e,r)
 def test_wrong_current_rule_fresh(self):
  x,e,r=fixture();x['members'][0]['quality'][0]['current_fresh_digest']='old'
  with self.assertRaises(ValueError):final_view(x,e,r)
 def test_pair_wrong_review_even_resealed(self):
  x,e,r=fixture();q=x['qualified_set'];q['pair']['members'][0]['review_id']='old';q['set_digest']=digest({k:v for k,v in q.items()if k!='set_digest'})
  with self.assertRaises(ValueError):final_view(x,e,r)
 def test_member_request_mismatch(self):
  x,e,r=fixture();x['members'][0]['binding']['raw_digest']='stale'
  with self.assertRaises(ValueError):final_view(x,e,r)
 def test_empty_or_duplicate_units(self):
  for units in ([],['A','A']):
   x,e,r=fixture();q12=x['members'][0]['current_roles']['q12'];x['members'][0]['current_roles']['q12']=[dict(q12[0],unit=u)for u in units]
   with self.assertRaises(ValueError):final_view(x,e,r)
 def test_wrong_q14_link(self):
  x,e,r=fixture();x['members'][0]['quality'][-1]['source_closure']['current_set_digest']='old'
  with self.assertRaises(ValueError):final_view(x,e,r)
 def test_missing_quality(self):
  x,e,r=fixture();x['members'][0]['quality'].pop()
  with self.assertRaises(ValueError):final_view(x,e,r)
if __name__=='__main__':unittest.main()
