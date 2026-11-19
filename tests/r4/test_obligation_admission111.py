import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'app/local_integration'))
import obligation_admission111 as a

def fixture():
    c = a.coverage_contract()
    b = {k: str(i + 1) * 64 for i, k in enumerate(a.BINDINGS)}
    b['coverage_digest'] = a.digest(c)
    rows = [{'obligation': x['obligation'], 'subject': x['subject'], 'state': 'PASS',
             'errors': [], 'pending': [], 'missing': []} for x in c['obligations']]
    report = {'schema': 'OBLIGATION_EVIDENCE111_V1', 'binding': copy.deepcopy(b),
              'rows': rows, 'errors': [], 'pending': [], **{k: False for k in a.AUTH}}
    return c, b, {'synthetic': report}
def run(c, b, reports, pins=None):
    return a.admission(c, a.digest(c), b, a.digest(b), reports,
                       pins if pins is not None else {k: a.digest(v) for k, v in reports.items()})
def codes(out):
    return {r['code'] for r in out['blockers']}

class AdmissionTests(unittest.TestCase):
    def test_fixed_inventory_and_units(self):
        c, b, r = fixture()
        self.assertEqual(len(c['obligations']), 51)
        for u in ('A', 'B'):
            self.assertEqual({x['obligation'] for x in c['obligations'] if x['subject'] == u},
                             set(a.CURRENT_IDS) | {'CALIBRATED_UNIT_QUALITY'})
        out = run(c, b, r)
        self.assertTrue(out['consistency_verified'])
        self.assertIn('APPLICABILITY_UNKNOWN', codes(out))
        self.assertFalse(out['declared_conditions_complete'])
        self.assertTrue(all(out[k] is False for k in a.AUTH))
    def test_four_pass_only_missing_other_obligations(self):
        c,b,r = fixture()
        r['synthetic']['rows'] = [x for x in r['synthetic']['rows'] if x['obligation'] in a.CURRENT_IDS]
        out=run(c,b,r)
        self.assertIn('MISSING_EVIDENCE',codes(out))
        self.assertFalse(out['qualified'])
    def test_caller_rehashed_policy_deletion_rejected(self):
        c,b,r=fixture(); c['obligations'].pop(); b['coverage_digest']=a.digest(c)
        r['synthetic']['binding']=copy.deepcopy(b)
        self.assertEqual(run(c,b,r)['state'],'EVIDENCE_ERROR')
    def test_caller_cannot_clear_conditional_or_claim_product(self):
        for field in ('conditional','product','unit'):
            c,b,r=fixture()
            if field=='conditional': c['obligations'][0]['applicability']='EXCLUDED'; c['obligations'][0]['exclusion_evidence_digest']='f'*64
            elif field=='product': c['whole_product_coverage_verified']=True
            else: c['units']=['A']
            b['coverage_digest']=a.digest(c);r['synthetic']['binding']=copy.deepcopy(b)
            self.assertEqual(run(c,b,r)['state'],'EVIDENCE_ERROR')
    def test_fail_and_error_both_preserved(self):
        c,b,r=fixture(); row=r['synthetic']['rows'][0]
        row['state']='FAIL'; row['errors']=['synthetic error']; row['pending']=['synthetic pending']
        out=run(c,b,r)
        self.assertTrue({'NECESSARY_FAIL','EVALUATOR_ERROR','NECESSARY_PENDING'}<=codes(out))
        self.assertEqual(out['observed_reports'],r)
    def test_all_state_dispositions(self):
        expected={'PASS':None,'FAIL':'NECESSARY_FAIL','UNKNOWN':'NECESSARY_UNKNOWN',
                  'NOT_EVALUATED':'NECESSARY_NOT_EVALUATED','ERROR':'EVALUATOR_ERROR'}
        for state, reason in expected.items():
            c,b,r=fixture();r['synthetic']['rows'][0]['state']=state
            out=run(c,b,r); self.assertTrue(out['consistency_verified'])
            if reason:self.assertIn(reason,codes(out))
    def test_each_binding_mismatch_rehashed_report(self):
        for k in a.BINDINGS:
            c,b,r=fixture();r['synthetic']['binding'][k]='f'*64
            self.assertEqual(run(c,b,r)['state'],'EVIDENCE_ERROR')
    def test_stale_report_digest_preserves_observed(self):
        c,b,r=fixture();pins={k:a.digest(v) for k,v in r.items()}
        r['synthetic']['rows'][0]['state']='UNKNOWN'
        out=run(c,b,r,pins)
        self.assertEqual(out['state'],'EVIDENCE_ERROR')
        self.assertEqual(out['observed_reports'],r)
    def test_each_forged_authority(self):
        for key in a.AUTH:
            c,b,r=fixture();r['synthetic'][key]=True
            self.assertEqual(run(c,b,r)['state'],'EVIDENCE_ERROR')
    def test_duplicate_and_wrong_unit(self):
        for mode in ('duplicate','unit','unknown'):
            c,b,r=fixture()
            if mode=='duplicate': r['synthetic']['rows'].append(copy.deepcopy(r['synthetic']['rows'][0]))
            elif mode=='unit': r['synthetic']['rows'][0]['subject']='C'
            else:r['synthetic']['rows'][0]['obligation']='invented'
            self.assertEqual(run(c,b,r)['state'],'EVIDENCE_ERROR')
    def test_missing_kinds_remain_distinct(self):
        c,b,r=fixture();r['synthetic']['rows'][0]['missing']=list(a.CODES)
        self.assertTrue(set(a.CODES)<=codes(run(c,b,r)))
    def test_malformed_state_and_diagnostics(self):
        for v in (None,True,'NEW_STATE'):
            c,b,r=fixture();r['synthetic']['rows'][0]['state']=v
            self.assertEqual(run(c,b,r)['state'],'EVIDENCE_ERROR')
        for field in ('errors','pending','missing'):
            c,b,r=fixture();del r['synthetic']['rows'][0][field]
            self.assertEqual(run(c,b,r)['state'],'EVIDENCE_ERROR')
    def test_typed_json_and_input_unchanged(self):
        c,b,r=fixture(); before=a.digest([c,b,r])
        run(c,b,r);self.assertEqual(before,a.digest([c,b,r]))
        r['synthetic']['rows'][0]['errors']=(1,)
        out=a.admission(c,a.digest(c),b,a.digest(b),r,{})
        self.assertEqual(out['state'],'EVIDENCE_ERROR')
        self.assertEqual(out['observed_report_preservation'],'NOT_ESTABLISHED')
        self.assertNotIn('observed_reports',out)
    def test_conditional_and_stage_applicability_not_invented(self):
        c,b,r=fixture()
        self.assertEqual({x['obligation'] for x in c['obligations'] if x['applicability']=='UNRESOLVED'},a.UNRESOLVED_APPLICABILITY)
    def test_global_errors_not_hidden_by_pass_rows(self):
        c,b,r=fixture();r['synthetic']['errors']=['synthetic evaluator failure']
        self.assertIn('EVALUATOR_ERROR',codes(run(c,b,r)))
if __name__ == '__main__':
    unittest.main()
