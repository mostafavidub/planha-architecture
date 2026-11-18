"""TEST_ONLY geometry and receipt fixtures; none are natural production failures."""
import copy,json,unittest,zipfile
from pathlib import Path
import operator369 as op

ROOT=Path(__file__).resolve().parents[1]

def fixture():
    units=[]
    for uid,off in [('A',0),('B',30)]:
        def r(a,b,c,d):return list(map(str,(a+off,b,c+off,d)))
        units.append({'id':uid,'ownership':[r(0,0,20,20)],'rooms':{'living':[r(0,0,20,20)]},
            'fixtures':{'sofa1':r(2,2,4,3),'sofa2':r(3,2,5,3)},
            'activities':{'sofa1_front':r(2,3,4,4),'sofa2_front':r(3,3,5,4)}})
    m={'inputs':['26','28',2],'program':{'bedrooms':3},'profile':{'body_m':'.7'},'units':units}
    request={'W':'26','L':'28','n':2,'requested_count':2}
    c={'request':request,'request_digest':op.digest(request),'model':m,'model_digest':op.digest(m),
       'packet':{'family':'FRONT_REAR','core':{'frozen':'core'},'world_model':m,'local_model':copy.deepcopy(m)}}
    t={'schema':op.SCHEMA,'candidate_digest':op.digest(c),'model_digest':op.digest(m),'source_inventory':{},
       'proposal':{'status':'PROPOSAL_ONLY','generation_method':'TEST_FIXTURE_NOT_SOLVER',
        'solver_status':0,'solver_message':'TEST_ONLY','variables':1,'constraints':1,'seconds':0,
        'rectangles':{'sofa1_use':['2','2','4','4'],'sofa2_use':['3','2','5','4']},'bedrooms':3}}
    record={'candidate':c,'trace':t};fresh={'fresh_checker_executed':True,'source_unchanged':True,
      'provenance':{'verified':True,'TEST_ONLY':True},'expected_method_registry':{'built_before_evaluate':True},
      'input_record_digest':op.digest(record),'outer_trace_digest':op.digest(t),'model_digest':op.digest(m),
      'raw_report':{'model_hash':op.digest(m),'status':'FAIL','pending':[],
                    'errors':[{'code':'FIXTURE_COLLISION','fixtures':['sofa1','sofa2']} for _ in range(2)]}}
    binding={'run_id':'test-run','candidate_id':'test-parent','review_id':'test-review',
             'model_digest':op.digest(m),'record_digest':op.digest(record),'fresh_digest':op.digest(fresh)}
    return record,fresh,binding

def resign_fresh(fresh,binding):binding['fresh_digest']=op.digest(fresh)

class Tests(unittest.TestCase):
    def test_source_proposal_is_real_translation_not_verdict_change(self):
        r,f,b=fixture();before=op.digest(r);p=op.propose(r,f,b)
        self.assertEqual(p['status'],'RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED')
        self.assertNotEqual(p['proposal']['rectangles'],r['trace']['proposal']['rectangles'])
        self.assertEqual(op.digest(r),before);self.assertFalse(p['live_authority'])
        self.assertFalse(p['solver_used']);self.assertNotIn('solver_status',p['proposal'])
        self.assertFalse(p['accepted']);self.assertEqual(p['proposal']['bedrooms'],3)
    def test_fresh_pass_not_rejection(self):
        r,f,b=fixture();f['raw_report']['status']='PASS';resign_fresh(f,b)
        with self.assertRaisesRegex(ValueError,'FAIL_REQUIRED'):op.propose(r,f,b)
    def test_pending_not_waived(self):
        r,f,b=fixture();f['raw_report']['pending']=['unknown'];resign_fresh(f,b)
        with self.assertRaisesRegex(ValueError,'FAIL_REQUIRED'):op.propose(r,f,b)
    def test_foreign_fresh_digest(self):
        r,f,b=fixture();f['seconds']=0
        with self.assertRaisesRegex(ValueError,'FRESH_DIGEST'):op.propose(r,f,b)
    def test_fresh_other_model_even_resigned(self):
        r,f,b=fixture();f['raw_report']['model_hash']='different';resign_fresh(f,b)
        with self.assertRaisesRegex(ValueError,'FAIL_REQUIRED'):op.propose(r,f,b)
    def test_second_error_not_ignored(self):
        r,f,b=fixture();f['raw_report']['errors'].append({'code':'OTHER'});resign_fresh(f,b)
        with self.assertRaisesRegex(ValueError,'ONLY_SAME_PAIR'):op.propose(r,f,b)
    def test_no_source_compound_relabel(self):
        r,f,b=fixture();r['trace']['proposal']['rectangles']['sofa1_use']=['0','0','1','1']
        r['trace']['candidate_digest']=op.digest(r['candidate']);f['input_record_digest']=op.digest(r)
        f['outer_trace_digest']=op.digest(r['trace']);b['record_digest']=op.digest(r);resign_fresh(f,b)
        with self.assertRaisesRegex(ValueError,'COMPOUND_NOT_BOUND'):op.propose(r,f,b)
    def test_joint_unsupported_not_coerced(self):
        r,f,b=fixture();r['trace']['schema']='SOURCE_SERVICE_JOINT367_TRACE_V1'
        with self.assertRaisesRegex(ValueError,'UNSUPPORTED_CURRENT'):op.propose(r,f,b)
    def test_exact_ownership_hole(self):
        self.assertFalse(op.union_contains(tuple(map(op.F,['0','0','3','1'])),
            [tuple(map(op.F,['0','0','1','1'])),tuple(map(op.F,['2','0','3','1']))]))
    def test_float_rect_rejected(self):
        with self.assertRaises(ValueError):op.rect([0.,0,1,1])
    def test_new_candidate_lineage_and_program_unchanged(self):
        r,f,b=fixture();p=op.propose(r,f,b);child=copy.deepcopy(r)
        for frame in ('local_model','world_model'):
            child['candidate']['packet'][frame]['units'][0]['fixtures']['sofa1']=['0','2','2','3']
        child['candidate']['model']=copy.deepcopy(child['candidate']['packet']['world_model'])
        child['candidate']['model_digest']=op.digest(child['candidate']['model'])
        child['trace']={'schema':'BALANCED_SOURCE_REPAIR369_TRACE_V1','parent_record_digest':op.digest(r),
            'proposal_digest':p['proposal_digest'],'candidate_digest':op.digest(child['candidate']),
            'model_digest':op.digest(child['candidate']['model'])}
        line=op.bind_reconstructed(r,p,child,b['run_id'])
        self.assertNotEqual(line['candidate_id'],b['candidate_id']);self.assertIsNone(line['review_id'])
        self.assertEqual(line['parent_review_id'],b['review_id']);self.assertTrue(line['fresh_review_required'])
        child['candidate']['packet']['local_model']['program']['bedrooms']=2
        child['trace']['candidate_digest']=op.digest(child['candidate'])
        with self.assertRaisesRegex(ValueError,'PROTECTED_DATA_CHANGED'):op.bind_reconstructed(r,p,child,b['run_id'])
    def test_noop_child_rejected(self):
        r,f,b=fixture();p=op.propose(r,f,b)
        child=copy.deepcopy(r);child['trace']={'schema':'BALANCED_SOURCE_REPAIR369_TRACE_V1',
            'parent_record_digest':op.digest(r),'proposal_digest':p['proposal_digest'],
            'candidate_digest':op.digest(child['candidate']),'model_digest':op.digest(child['candidate']['model'])}
        with self.assertRaisesRegex(ValueError,'NO_MODEL_CHANGE'):op.bind_reconstructed(r,p,child,b['run_id'])
    def test_live_path_never_accepts_serialized_claim(self):
        self.assertEqual(op.execute_live(*fixture())['status'],'BLOCKED')
    def test_real_successful_records_do_not_authorize_repair(self):
        with zipfile.ZipFile(ROOT/'independent368actual/checkpoint368_actual_one_shot.zip') as z:
            base='368_actual_evidence/program_receipts/bridge_run/'
            for kind in ('balanced','joint'):
                r=json.loads(z.read(base+kind+'/constructed.json'));f=json.loads(z.read(base+kind+'/fresh.json'))
                b={'run_id':'actual-run','candidate_id':'actual-candidate','review_id':'actual-review',
                   'model_digest':op.digest(r['candidate']['model']),'record_digest':op.digest(r),'fresh_digest':op.digest(f)}
                with self.assertRaises(ValueError):op.propose(r,f,b)

if __name__=='__main__':unittest.main(verbosity=2)
