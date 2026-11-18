"""Transport binding to unchanged registered378 source, not a new source origin."""
import sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;W=ROOT.parent
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from request_contract368 import parse_json,verify,digest

def bind(envelope,record,fresh,run_id):
 verify(envelope)
 if type(run_id)is not str or str(uuid.UUID(run_id))!=run_id:raise ValueError('RUN_UUID')
 c=record['candidate'];t=record['trace'];p=fresh['provenance'];mh=digest(c['model'])
 if t['schema']!='FINITE_PORTALS378_SOURCE_TRACE_V1' or record.get('test_only')is not False or fresh.get('test_only')is not False:raise ValueError('GENUINE_FINITE_SOURCE_REQUIRED')
 if t['run_id']!=run_id or p['run_id']!=run_id:raise ValueError('RUN_SOURCE_REVIEW_BINDING')
 if c['request_digest']!=envelope['raw_digest']or digest(c['request'])!=envelope['raw_digest']or c['request']!=envelope['normalized_raw']:raise ValueError('REQUEST_BINDING')
 identity=digest({'run_id':run_id,'request_digest':digest(c['request']),'model_digest':mh,'trace_digest':digest(t)})
 if record['candidate_id']!=identity or p['candidate_id']!=identity:raise ValueError('CANDIDATE_IDENTITY')
 if t['selection_rank']!=1 or c['generation_context']['selection']!=t['enumeration'][1]:raise ValueError('PREDECLARED_RANK')
 # Unchanged378 binding gate recomputes current source/method registry and checks
 # complete source/current model/review provenance, without running the checker.
 sys.path.insert(0,str(ROOT/'staging378_finite_portals'))
 from source378 import repair_dispatch
 dispatch=repair_dispatch(record,fresh)
 return {'run_id':run_id,'candidate_id':identity,'raw_digest':envelope['raw_digest'],'canonical_request_digest':envelope['canonical_request_digest'],
         'received_digest':envelope['received_digest'],'transport_body_sha256':envelope.get('transport_body_sha256'),
         'review_id':fresh['review_id'],'record_digest':digest(record),'model_digest':mh,'fresh_digest':digest(fresh),'dispatch':dispatch}

def partial(state,run_id):
 return {'state':state,'transport_run_id':run_id,'test_only':False,'experimental':True,'requested_count':2,'tested_branch_count':1,'request_fulfilled':False,
         'accepted':False,'delivery_allowed':False,'qualified_selected_set':False,'semantic_state':'UNKNOWN_PENDING_VALIDATION','repair_attempted':False,
         'daylight_ventilation_scope':'EXCLUDED_FROM_MVP_NOT_EVALUATED'}
