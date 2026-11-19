"""Synthetic adversarial binding/preservation tests, NOT whole-model provenance."""
import copy,json,unittest
import front_rear_runtime_adapter as a
def fixture():
 raw={'W':'18','L':'20','n':2,'requested_count':1}
 proposal={'status':'PROPOSAL_ONLY','bedrooms':2,'sleep_roles':['double','twin']}
 m={'inputs':['18','20',2],'program':{'bedrooms_per_unit':2,'units':2,'sleep_roles':['double','twin'],'capacity_profile':'LEGACY_SOURCE_PROGRAM','design_occupants_per_unit':4,'provisional':True},'accepted':False,'release_allowed':False}
 packet={'family':'FRONT_REAR','local_model':copy.deepcopy(m),'world_model':m,'core':{'test_only':True},'unit_proposal_hashes':{'A':a.digest(proposal),'B':a.digest(proposal)},'admission_claim':False}
 trace={'schema':'CONSTRUCTION_TRACE127_PAIR_V1','family':'FRONT_REAR','raw':copy.deepcopy(raw),'proposals':{'A':copy.deepcopy(proposal),'B':copy.deepcopy(proposal)},'unit_proposal_hashes':copy.deepcopy(packet['unit_proposal_hashes']),'model_hash':a.digest(m),'local_model_hash':a.digest(m),'core_hash':a.digest(packet['core']),'source_revision':a.ENGINE_REVISION}
 ctx={'operation':'generate_from_dimensions','baseline_model_hash':None,'existing_plan_id':None,'inputs':copy.deepcopy(m['inputs']),'construction_trace':trace}
 return packet,ctx,raw,proposal
def resign(p,c):
 c['construction_trace']['model_hash']=a.digest(p['world_model'])
 c['construction_trace']['local_model_hash']=a.digest(p['local_model'])
 c['construction_trace']['core_hash']=a.digest(p['core'])
class RuntimeAdversarial(unittest.TestCase):
 def test_synthetic_binding_is_not_replay(self):
  p,c,r,q=fixture();self.assertEqual(a.packet_binding(p,c,r,q),a.digest(p['world_model']))
  self.assertNotIn('verified',p)
 def test_exact_program_int_float(self):
  for key,value in [('units',2.0),('bedrooms_per_unit',2.0),('design_occupants_per_unit',4.0),('provisional',1)]:
   p,c,r,q=fixture()
   for k in ('world_model','local_model'):p[k]['program'][key]=value
   resign(p,c)
   with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
 def test_boolean_authority_not_zero(self):
  p,c,r,q=fixture();p['admission_claim']=0
  with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
  p,c,r,q=fixture()
  for k in ('world_model','local_model'):p[k]['accepted']=0
  resign(p,c)
  with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
 def test_input_mutation(self):
  for field,value in [('n',2.0),('W','20'),('requested_count',True)]:
   p,c,r,q=fixture();c['construction_trace']['raw'][field]=value
   with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
 def test_origin_wrong_schema_family_revision(self):
  for field,value in [('schema','CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1'),('family','LEFT_RIGHT'),('source_revision','0'*64)]:
   p,c,r,q=fixture();c['construction_trace'][field]=value
   with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
 def test_proposal_assignment_changed(self):
  p,c,r,q=fixture();c['construction_trace']['proposals']['B']['bedrooms']=1
  with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
 def test_raw_request_to_model_mismatch(self):
  p,c,r,q=fixture()
  for k in ('world_model','local_model'):p[k]['inputs'][2]=2.0
  c['inputs']=['18','20',2.0];resign(p,c)
  with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
 def test_local_world_and_digest(self):
  for target in ('core','world_model','local_model'):
   p,c,r,q=fixture();p[target]['mutation']=True
   with self.assertRaises(ValueError):a.packet_binding(p,c,r,q)
 def test_report_original_survives_downstream_mutation(self):
  reports={};live={};pins={}
  physical={'errors':['E'],'pending':['P'],'original_pending':['O'],'not_evaluated':['N'],'out_of_scope':[{'code':'Q'}]}
  a.preserve_report(reports,live,pins,'physical',physical)
  def synthetic_downstream(report):report['errors'].clear();report['pending'].append('MUTATION')
  synthetic_downstream(physical)
  with self.assertRaises(ValueError):a.verify_reports(live,pins)
  a.verify_reports(reports,pins)
  self.assertEqual(reports['physical']['errors'],['E']);self.assertEqual(reports['physical']['pending'],['P'])
  json.dumps(reports,allow_nan=False)
 def test_noncanonical_report_mutation_original_serializable(self):
  for value in (float('nan'),object()):
   reports={};live={};pins={};physical={'errors':[]}
   a.preserve_report(reports,live,pins,'physical',physical)
   physical['bad']=value
   with self.assertRaises((ValueError,TypeError)):a.verify_reports(live,pins)
   self.assertTrue(a.observed_digest(physical).startswith('UNHASHABLE_INTEGRITY_ERROR'))
   json.dumps({'original':reports,'observed':a.observed_copy(physical)},allow_nan=False)
 def test_noncanonical_new_report_not_admitted(self):
  originals={};live={};pins={}
  with self.assertRaises(ValueError):a.preserve_report(originals,live,pins,'x',{'nan':float('nan')})
  self.assertEqual(originals,{})
 def test_noncanonical_packet_observation(self):
  p,c,r,q=fixture();original=copy.deepcopy(p);p['world_model']['bad']=object()
  self.assertTrue(a.observed_digest(p).startswith('UNHASHABLE_INTEGRITY_ERROR'))
  json.dumps({'packet':original,'observed':a.observed_copy(p)},allow_nan=False)
 def test_transport_nonfinite_and_nonjson(self):
  for value in (float('nan'),float('inf'),object(),{1:'bad'},set()):
   with self.assertRaises((ValueError,TypeError)):a.transport(value)
  import numpy as np
  with self.assertRaises(ValueError):a.transport(np.float64(1.5))
 def test_transport_preserves_int_float_bool_distinctions(self):
  values=[0,False,2,2.0]
  out,receipt=a.transport(values)
  self.assertEqual([type(x) for x in out],[int,bool,int,float])
  self.assertNotEqual(a.digest(0),a.digest(False));self.assertNotEqual(a.digest(2),a.digest(2.0))
 def test_unknown_status_rejected(self):
  for status in (None,False,2,'PASS','ERROR','SOURCE_CONFLICT'):
   with self.assertRaises(ValueError):a.proposal_disposition({'status':status})
 def test_preflight_invalid_budget_never_imports_solver(self):
  for seconds in (True,0,-1,float('nan'),float('inf'),'3',61):
   with self.assertRaises(ValueError):a.run(b'{}',solver_seconds=seconds)
 def test_invalid_public_or_case_before_live(self):
  for body in (b'{"W":18,"L":20,"n":2,"bedrooms":2}',b'{"W":26,"L":20,"n":2}',b'{"W":20,"L":18,"n":2}'):
   with self.assertRaises(ValueError):a.run(body,solver_seconds=1)
if __name__=='__main__':unittest.main()
