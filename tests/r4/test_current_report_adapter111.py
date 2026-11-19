import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'app/local_integration'))
import current_report_adapter111 as x
import obligation_admission111 as a

def fixture():
    b={k:str(i+1)*64 for i,k in enumerate(a.BINDINGS)}
    b['coverage_digest']=a.digest(a.coverage_contract())
    p={'model_hash':b['model_digest'],'status':'FAIL','errors':['SYNTHETIC_PHYSICAL_FAILURE'],
       'pending':['SYNTHETIC_PENDING'],'original_pending':['SYNTHETIC_HISTORY']}
    replay={'model_hash':b['model_digest'],'verified':True,'source_revision':x.ENGINE_REVISION}
    current={}
    for cid,schema in x.SCHEMAS.items():
        r={'schema':schema,'criterion':cid,'model_digest':b['model_digest'],
           'state':'UNKNOWN','integrity_verified':True,
           'source_snapshot':x.source_snapshot(cid),**{k:False for k in a.AUTH}}
        if cid=='CURRENT_PROGRAM_SUITABILITY':
            r.update(historical_physical_report=copy.deepcopy(p),historical_physical_digest=a.digest(p),
                     reports={'replay':copy.deepcopy(replay)},inventory=[])
        else:
            r.update(original_physical_report=copy.deepcopy(p),original_physical_digest=a.digest(p),replay=copy.deepcopy(replay))
            if cid=='NONFUNCTIONAL_WALL_EXCLUSION':r['walls']=[{'source_id':'SYNTHETIC_WALL','state':'UNKNOWN'}]
            else:r['units']=[{'unit':'A','scope':'SYNTHETIC_SUBSTUDY'},{'unit':'B','scope':'SYNTHETIC_SUBSTUDY'}]
        current[cid]=r
    return {'physical':p,'replay':replay,'current':current},b
def run(raw,b):return x.adapt(raw,a.digest(raw),b,a.digest(b))
class AdapterTests(unittest.TestCase):
    def test_source_shaped_not_live_and_preserved(self):
        raw,b=fixture();out=run(raw,b)
        self.assertTrue(out['consistency_verified'])
        self.assertEqual(out['raw_reports'],raw)
        self.assertFalse(out['live_execution_verified'])
        self.assertTrue(all(out[k] is False for k in a.AUTH))
        self.assertEqual(len(out['decision']['rows']),51)
    def test_aggregate_pass_never_unit_pass(self):
        raw,b=fixture()
        for r in raw['current'].values():r['state']='PASS'
        out=run(raw,b)
        self.assertTrue(out['consistency_verified'])
        self.assertTrue(all(r['reported_state']=='UNKNOWN' for r in out['decision']['rows']))
    def test_fail_error_both_retained_without_unit_propagation(self):
        raw,b=fixture();cid=next(iter(x.SCHEMAS))
        raw['current'][cid].update(state='FAIL',findings=[{'kind':'EVALUATOR_OR_SOURCE_BINDING_ERROR'}])
        out=run(raw,b);codes={r['code'] for r in out['decision']['blockers']}
        self.assertTrue({'RETAINED_AGGREGATE_CURRENT_FAIL','SOURCE_OR_EVALUATOR_ERROR','RETAINED_PHYSICAL_FAIL'}<=codes)
        self.assertEqual(out['raw_reports'],raw)
    def test_rehashed_wrong_model(self):
        raw,b=fixture();raw['current'][next(iter(x.SCHEMAS))]['model_digest']='f'*64
        self.assertEqual(run(raw,b)['state'],'EVIDENCE_ERROR')
    def test_wrong_physical_copy(self):
        raw,b=fixture();raw['current']['CONTINUOUS_USEFUL_LIVING']['original_physical_report']['errors']=[]
        self.assertEqual(run(raw,b)['state'],'EVIDENCE_ERROR')
    def test_source_changed_or_removed_rehashed(self):
        for mode in ('changed','removed'):
            raw,b=fixture();snap=raw['current']['CONTINUOUS_USEFUL_LIVING']['source_snapshot'];key=next(iter(snap))
            if mode=='changed':snap[key]='f'*64
            else:del snap[key]
            self.assertEqual(run(raw,b)['state'],'EVIDENCE_ERROR')
    def test_duplicate_unit_or_missing_unit(self):
        raw,b=fixture();r=raw['current']['CONTINUOUS_USEFUL_LIVING'];r['units'].append(copy.deepcopy(r['units'][0]))
        self.assertEqual(run(raw,b)['state'],'EVIDENCE_ERROR')
        raw,b=fixture();raw['current']['CONTINUOUS_USEFUL_LIVING']['units']=[]
        out=run(raw,b);self.assertTrue(out['consistency_verified'])
        self.assertTrue(all(z['reported_state']=='UNKNOWN' for z in out['decision']['rows']))
    def test_stale_pin_preserves_raw(self):
        raw,b=fixture();pin=a.digest(raw);raw['physical']['pending'].append('SYNTHETIC_NEW')
        out=x.adapt(raw,pin,b,a.digest(b))
        self.assertEqual(out['state'],'EVIDENCE_ERROR');self.assertEqual(out['raw_reports'],raw)
    def test_replay_wrong_revision_rehashed(self):
        raw,b=fixture();raw['replay']['source_revision']='stale'
        self.assertEqual(run(raw,b)['state'],'EVIDENCE_ERROR')
    def test_physical_error_or_unknown_status_is_evidence_error(self):
        for state in ('ERROR','EVALUATOR_ERROR','NEW_STATE',None):
            raw,b=fixture();raw['physical'].update(status=state,errors=[])
            out=run(raw,b)
            self.assertEqual(out['state'],'EVIDENCE_ERROR')
            self.assertEqual(out['raw_reports'],raw)
    def test_authority_and_unknown_state(self):
        for field,value in (('qualified',True),('state','NEW_STATE')):
            raw,b=fixture();raw['current'][next(iter(x.SCHEMAS))][field]=value
            self.assertEqual(run(raw,b)['state'],'EVIDENCE_ERROR')
if __name__=='__main__':unittest.main()
