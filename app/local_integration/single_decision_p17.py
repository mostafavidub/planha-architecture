"""Same-model n1 report consistency and non-delivery policy. Not P25 approval."""
import copy
from single_model_p15 import digest,require,AUTH
from single_evaluation_p17 import bind_bundle,source_audit
from current_four_decision import error_markers,decide,SCHEMAS as BASE_SCHEMAS
SCHEMAS={k:'SINGLE_P17_'+v for k,v in BASE_SCHEMAS.items()}
def require_current_integrity(reports):
 require(type(reports)is dict and set(reports)==set(SCHEMAS),'P17_FOUR_SET')
 for r in reports.values():require(type(r)is dict and r.get('integrity_verified')is True,'P17_CURRENT_INTEGRITY')
def assemble(bundle,reports,expected):
 require_current_integrity(reports)
 before=source_audit();pin=digest([bundle,reports,expected]);replay=bind_bundle(bundle)
 mh=bundle['model_digest'];physical=bundle['reports']['physical'];ph=digest(physical)
 require(set(reports)==set(SCHEMAS)==set(expected),'P17_FOUR_SET')
 rows=[];states={}
 for cid,r in reports.items():
  require(r.get('integrity_verified')is True,'P17_CURRENT_INTEGRITY')
  require(r.get('schema')==SCHEMAS[cid] and r.get('criterion')==cid,'P17_CURRENT_SCHEMA')
  require(r.get('current_domain_policy')=='SINGLE_CURRENT_DOMAIN_P17_V1','P17_CURRENT_POLICY')
  require(r.get('model_digest')==mh and digest(r)==expected[cid],'P17_CURRENT_DIGEST')
  require(all(r.get(k)is False for k in AUTH),'P17_CURRENT_AUTHORITY')
  rr=r['reports']['replay'] if cid=='CURRENT_PROGRAM_SUITABILITY' else r['replay']
  require(digest(rr)==digest(replay),'P17_CURRENT_REPLAY')
  require(r['source_physical_digest']==ph and digest(r['source_physical_report'])==ph,'P17_CURRENT_PHYSICAL')
  require(r['retained_historical_physical_digest']==bundle['report_digests']['historical_physical'] and digest(r['retained_historical_physical_report'])==bundle['report_digests']['historical_physical'],'P17_HISTORICAL_RETENTION')
  require(digest(r['single_source_snapshot'])==digest(before),'P17_CURRENT_SOURCE')
  if cid=='CURRENT_PROGRAM_SUITABILITY':
   require(set(r['reports'])==set(r['report_digests']),'P17_PROGRAMME_REPORT_SET')
   for k,v in r['reports'].items():require(digest(v)==r['report_digests'][k],'P17_PROGRAMME_SUBREPORT')
   require(not r.get('report_mutations'),'P17_PROGRAMME_MUTATION')
  markers=error_markers({k:v for k,v in r.items() if k not in ('source_physical_report','retained_historical_physical_report')})
  state='FAIL' if r['state']=='FAIL' else 'EVALUATOR_ERROR' if markers else r['state']
  require(state in ('PASS','FAIL','UNKNOWN','NOT_EVALUATED','EVALUATOR_ERROR'),'P17_CURRENT_STATE')
  states[cid]=state;rows.append({'criterion':cid,'state':state,'report_digest':expected[cid],'execution_error_count':len(markers)})
 decision=decide(physical,states)
 if bundle['reports']['access']['state']!='PASS_SCOPED_OWNERSHIP_ACCESS':decision['blockers'].append('SINGLE_ACCESS_NOT_VERIFIED')
 # This scope has no P25 delivery implementation. Never convert that policy into a fake physical failure.
 if any(r['execution_error_count']for r in rows) and 'EVALUATOR_ERROR'not in decision['blockers']:decision['blockers'].append('EVALUATOR_ERROR')
 decision['state']='BLOCKED'
 decision['blockers']=list(dict.fromkeys(decision['blockers']+['P25_DELIVERY_NOT_IMPLEMENTED']))
 out={'schema':'SINGLE_DECISION_P17_V1','model_digest':mh,'physical_digest':ph,'historical_physical_digest':bundle['report_digests']['historical_physical'],
      'report_digests':copy.deepcopy(expected),'criteria':rows,'decision':decision,'integrity_verified':True,'source_snapshot':before,
      'scope':'All four computations executed on one source-bound P15 model; their remaining quality/profile limitations unchanged',**{k:False for k in AUTH}}
 require(digest([bundle,reports,expected])==pin and source_audit()==before,'P17_DECISION_MUTATION')
 return out
