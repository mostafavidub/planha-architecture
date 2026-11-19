"""Controlled taxonomy fixtures only; no geometry generation or qualification."""
import json,tempfile,unittest,uuid
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from history_status_taxonomy import summarize
from dimension_contract import parse
BODY=b'{"W":"25","L":"25","n":2,"requested_count":1}'
def completed(states):
    return {'outcome':'EXPERIMENT_COMPLETED','accepted':False,'delivery_allowed':False,'qualified_count':0,'generated_count':0,
        'candidates':[],'envelope':parse(BODY),'attempts':[{'family':'F'+str(i),'state':s,'reason':'controlled fixture '+str(i)}for i,s in enumerate(states)]}
def write_record(base,result,body=BODY):
    rid=str(uuid.uuid4());folder=base/rid;folder.mkdir()
    result=deepcopy(result);result['run_id']=rid
    (folder/'request.json').write_bytes(body);(folder/'result.json').write_text(json.dumps(result))
    (folder/'lifecycle.json').write_text(json.dumps({'wait_completed':True,'http_status':200 if result['outcome']=='EXPERIMENT_COMPLETED'else504,'returncode':0}))
    return rid
class StatusTests(unittest.TestCase):
    def test_exact_attempt_categories(self):
        for state,want in [('UNSUPPORTED_BUNDLE_FIT','UNSUPPORTED'),('UNSUPPORTED_CURRENT_CORE_FIT','UNSUPPORTED'),
            ('NO_PROPOSAL_IN_THIS_RESTRICTED_MASTER','NO_PROPOSAL'),('NO_PROPOSAL_IN_THIS_TOPOLOGY','NO_PROPOSAL'),
            ('TIMEOUT_NO_WITNESS','TIMEOUT'),('SEARCH_TIMEOUT_NO_WITNESS','TIMEOUT'),('EXECUTION_ERROR','EXECUTION_ERROR'),
            ('NO_MYSTERY','UNKNOWN'),('FAIL_FUTURE_UNIMPLEMENTED','UNKNOWN'),('NOT_ATTEMPTED_BUDGET','UNKNOWN')]:
            with self.subTest(state=state):
                result=completed([state]);before=deepcopy(result);r=summarize(result,[])
                self.assertEqual(r['primary'],want);self.assertEqual(r['attempt_causes'][0]['state'],state)
                self.assertFalse(r['qualified']);self.assertFalse(r['global_infeasibility_proven']);self.assertEqual(result,before)
    def test_mixed_no_collapse(self):
        r=summarize(completed(['TIMEOUT_NO_WITNESS','NO_PROPOSAL_IN_THIS_TOPOLOGY','UNSUPPORTED_BUNDLE_FIT','EXECUTION_ERROR']),[])
        self.assertEqual(r['primary'],'MULTIPLE')
        self.assertEqual(r['categories'],['EXECUTION_ERROR','NO_PROPOSAL','TIMEOUT','UNSUPPORTED'])
        self.assertEqual(len(r['attempt_causes']),4)
    def test_top_outcomes_preserve_codes(self):
        for outcome,want in [('INVALID_INPUT','INVALID_INPUT'),('UNSUPPORTED','UNSUPPORTED'),('EXECUTION_TIMEOUT','TIMEOUT'),('CANCELLED','CANCELLED'),('EXECUTION_ERROR','EXECUTION_ERROR'),('DEPENDENCY_UNAVAILABLE','DEPENDENCY_UNAVAILABLE')]:
            result={'outcome':outcome,'code':'EXACT_CODE','field':'W','accepted':False,'delivery_allowed':False}
            r=summarize(result,[]);self.assertEqual(r['primary'],want);self.assertEqual(r['original_outcome'],outcome);self.assertEqual(r['original_code'],'EXACT_CODE')
    def test_candidate_states_stay_unqualified(self):
        for state,want in [('REJECTED_PHYSICAL','REJECTED'),('UNKNOWN_REVIEW','UNKNOWN'),('PHYSICAL_PASS_SEMANTIC_UNKNOWN','UNKNOWN')]:
            r=summarize(completed([]),[{'candidate_id':'fixture','state':state}]);self.assertEqual(r['primary'],want);self.assertFalse(r['qualified'])
    def test_invalid_shapes_and_authority(self):
        for change in [{'accepted':True},{'delivery_allowed':0},{'qualified_count':True},{'qualified_count':1},{'outcome':'QUALIFIED'},{'attempts':{}},{'attempts':[{'state':False}]},{'attempts':[{'state':'EXECUTION_ERROR','reason':{}}]}]:
            with self.subTest(change=change):
                with self.assertRaises(ValueError):summarize({**completed([]),**change},[])
        with self.assertRaises(ValueError):summarize(completed([]),[{'state':'QUALIFIED'}])
    def test_saved_history_retains_causes(self):
        from run_history import summary,output_gate
        with tempfile.TemporaryDirectory()as tmp:
            base=Path(tmp)
            for states,want in [(['NO_PROPOSAL_IN_THIS_TOPOLOGY'],'NO_PROPOSAL'),(['TIMEOUT_NO_WITNESS'],'TIMEOUT'),(['UNSUPPORTED_BUNDLE_FIT'],'UNSUPPORTED'),(['TIMEOUT_NO_WITNESS','EXECUTION_ERROR'],'MULTIPLE')]:
                source=completed(states);rid=write_record(base,source);r=summary(rid,base)
                self.assertEqual(r['outcome'],'EXPERIMENT_COMPLETED');self.assertEqual(r['status_taxonomy']['primary'],want)
                self.assertEqual([a['state']for a in r['status_taxonomy']['attempt_causes']],states)
                self.assertFalse(r['live_model_restored']);self.assertEqual(output_gate(rid,base)[0],403)
    def test_invalid_input_is_not_fabricated_history(self):
        import generation_gateway as gateway
        from run_history import summary
        invalid=b'{"W":false,"L":"25","n":2,"requested_count":1}'
        with tempfile.TemporaryDirectory()as tmp,patch.object(gateway,'ROOT',Path(tmp)),patch.object(gateway.subprocess,'Popen')as popen:
            status,result=gateway.generate(invalid)
            self.assertEqual(status,422);self.assertEqual(result['outcome'],'INVALID_INPUT');popen.assert_not_called()
            self.assertFalse((Path(tmp)/'app/local_integration/evidence/requests').exists())
            rid=write_record(Path(tmp),{'outcome':'INVALID_INPUT','accepted':False,'delivery_allowed':False},invalid)
            with self.assertRaises(ValueError):summary(rid,Path(tmp))
if __name__=='__main__':unittest.main()
