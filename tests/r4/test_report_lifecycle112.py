import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'app/local_integration'))
import report_lifecycle112 as l
import request_trace109 as t
import request_budget110 as budget
import current_report_adapter111 as a
from test_current_report_adapter111 import fixture as rawfixture

def fixture():
    request=t.make_request(b'{"W":"18","L":"22","n":2}');rh=t.digest(request)
    raw,b=rawfixture(); mh=raw['physical']['model_hash']
    reports={'parent_physical':raw['physical'],'parent_replay':raw['replay'],
             'parent_cause':{'model_digest':mh,'selected_causes':[]}}
    current={}
    for mod,cid in l.MODS.items():
        reports['parent_current_'+mod]=raw['current'][cid]
        current[mod]={'state':'UNKNOWN','integrity_verified':True,'missing_count':0,'evaluator_error_count':0}
    from one_bed_pair_source_study import code_counts
    p=raw['physical']
    summary={'completed':True,'integrity_verified':True,'state':'BLOCKED_NO_SUPPORTED_CAUSE',
             'request_digest':rh,'run_nonce':request['nonce'],'request_account_id':request['account_id'],
             'raw_digest':t.digest(request['preflight']['raw']),'profile_digest':request['programme_digest'],
             'request_source_digest':t.digest(request['source_snapshot']),'attempt_count':1,
             'child_observed':False,'cause_repair_verified':False,'parent_observed':True,
             'parent_model_digest':mh,'selected_causes':[],'parent_current':current,
             'parent_physical':{'status':p['status'],'errors':code_counts(p['errors']),
                'pending':code_counts(p['pending']),'not_evaluated_count':0,'out_of_scope_count':0},
             'report_digests':{k:t.digest(v) for k,v in reports.items()},**{k:False for k in t.AUTH}}
    anchor=budget.anchor(request,rh);account=budget.create(anchor)
    account,_=budget.reserve(account,t.digest(account),anchor)
    return request,rh,summary,reports,account
def write(root,summary,reports):
    (root/'summary.json').write_text(json.dumps(summary))
    (root/'reports.json').write_text(json.dumps(reports))
def consume(root,r,h,account):
    return l.consume(root,r,h,{'returncode':0,'wait_completed':True,'timed_out':False},account,t.digest(account))
class LifecycleTests(unittest.TestCase):
    def test_same_lifecycle_fullraw_consumed_then_cleanup(self):
        r,h,o,reports,account=fixture()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);write(root,o,reports)
            _,_,e=consume(root,r,h,account)
            self.assertTrue(e['safe_summary']['adapter_executed'])
            self.assertEqual(e['safe_summary']['declared_row_count'],51)
            self.assertEqual(e['private_evidence']['original_reports'],reports)
            self.assertTrue((root/'reports.json').is_file())
        self.assertFalse(root.exists())
        self.assertFalse(e['safe_summary']['durable_full_reports'])
        self.assertNotIn('original_reports',e['safe_summary'])
        self.assertFalse(e['safe_summary']['qualified'])
    def test_missing_truncated_and_summaryonly(self):
        for mode in ('missing','truncated','summaryonly','duplicate'):
            r,h,o,reports,account=fixture()
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);write(root,o,reports)
                if mode=='missing':(root/'reports.json').unlink()
                elif mode=='truncated':(root/'reports.json').write_text('{')
                elif mode=='duplicate':(root/'reports.json').write_text('{"x":1,"x":2}')
                else:(root/'reports.json').write_text(json.dumps(o))
                with self.assertRaises(l.EvidenceFailure):consume(root,r,h,account)
    def test_stale_rehashed_reports_preserved_on_error(self):
        r,h,o,reports,account=fixture();reports['parent_physical']['model_hash']='f'*64
        o['report_digests']={k:t.digest(v)for k,v in reports.items()}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);write(root,o,reports)
            with self.assertRaises(l.EvidenceFailure) as caught:consume(root,r,h,account)
            self.assertEqual(caught.exception.private_evidence['original_reports'],reports)
    def test_nonce_account_profile_source_mismatch(self):
        for key in ('run_nonce','request_account_id','profile_digest','request_source_digest','request_digest'):
            r,h,o,reports,account=fixture();o[key]='f'*64
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);write(root,o,reports)
                with self.assertRaises(l.EvidenceFailure):consume(root,r,h,account)
    def test_reservation_other_request_rejected(self):
        r,h,o,reports,account=fixture();r2=t.make_request(b'{"W":"18","L":"22","n":2}')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);write(root,o,reports)
            with self.assertRaises(l.EvidenceFailure):consume(root,r2,t.digest(r2),account)
    def test_source_mutation_rejected(self):
        r,h,o,reports,account=fixture()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);write(root,o,reports)
            with patch.object(t,'sources',return_value={}):
                with self.assertRaises(l.EvidenceFailure):consume(root,r,h,account)
    def test_report_file_changed_during_adapter_rejected(self):
        r,h,o,reports,account=fixture();real=Path.read_bytes; reads={}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);write(root,o,reports)
            def altered(path):
                if path==root/'reports.json':
                    reads[str(path)]=reads.get(str(path),0)+1
                    if reads[str(path)]==2:path.write_text('{}')
                return real(path)
            with patch.object(Path,'read_bytes',altered):
                with self.assertRaises(l.EvidenceFailure):consume(root,r,h,account)
    def test_no_parent_skips_adapter_not_fabricated(self):
        r,h,o,reports,account=fixture()
        o.update(state='BLOCKED_NO_PARENT_PROPOSAL',parent_observed=False)
        o.pop('parent_model_digest')
        reports={'parent_no_witness':{'state':'NO_PROPOSAL'}}
        o['report_digests']={k:t.digest(v)for k,v in reports.items()}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);write(root,o,reports)
            _,_,e=consume(root,r,h,account)
            self.assertFalse(e['safe_summary']['adapter_executed'])
            self.assertEqual(e['safe_summary']['state'],'SKIPPED_NO_PARENT')
            o['parent_model_digest']='a'*64;write(root,o,reports)
            with self.assertRaises(l.EvidenceFailure):consume(root,r,h,account)
    def test_preflight_scope_no_go_and_no_process(self):
        with patch('subprocess.Popen',side_effect=AssertionError('NO_PROCESS')):
            for w,length in (('18','20'),('18','22')):
                result=l.cycle_preflight(json.dumps({'W':w,'L':length,'n':2}).encode())
                self.assertEqual(result['state'],'NO_GO_COMPLETE_CYCLE')
                self.assertFalse(result['qualified'])
    def test_adapter_error_report_preserved_in_exception(self):
        r,h,o,reports,account=fixture()
        reports['parent_replay']['source_revision']='SYNTHETIC_STALE'
        o['report_digests']={k:t.digest(v)for k,v in reports.items()}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);write(root,o,reports)
            with self.assertRaises(l.EvidenceFailure) as caught:consume(root,r,h,account)
            self.assertEqual(caught.exception.private_evidence['adapter']['state'],'EVIDENCE_ERROR')
            self.assertEqual(caught.exception.private_evidence['original_reports'],reports)
    def test_final_invalidation_demotes_lifecycle(self):
        base={'receipt_verified':True,'lifecycle_admission':{'consistency_verified':True}}
        t.invalidate(base)
        self.assertNotIn('lifecycle_admission',base)
        self.assertIn('lifecycle_admission',base['observed_unverified_evidence'])
if __name__=='__main__':unittest.main()
