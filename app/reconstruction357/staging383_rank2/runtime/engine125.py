"""One-profile left/right experimental generator; no capacity/coverage claim."""
import time
from contract114 import parse,S,digest
from engine114 import revision,_eligible
from schedule123 import requested_count
from constructor125 import build,context
from frame_contract125 import local_core
from search114 import propose
from evaluate_world125 import evaluate_world

def validate_raw(raw):
 if not isinstance(raw,dict) or set(raw)!={'W','L','n','requested_count'}:raise ValueError('REQUEST_FIELDS')
 W,L,n=parse(raw)
 if n!=2:raise ValueError('CURRENT_SCOPE_N2_ONLY')
 return W,L,n,requested_count(raw)

def check_candidate(c,raw):
 W,L,n,_=validate_raw(raw);p=c['world_packet']
 if c['model']!=p['world_model'] or c['model']['inputs']!=[S(W),S(L),n]:raise ValueError('WORLD_INPUT_MODEL_BINDING')
 ctx=c['generation_context'];t=ctx['construction_trace']
 if t['raw']!=raw or t['source_revision']!=revision():raise ValueError('SOURCE_INPUT_BINDING')
 g=evaluate_world(p['local_model'],p['world_model'],p['core'],ctx)
 if not _eligible(g):raise ValueError('INDEPENDENT_GATE_NOT_ADMITTED')
 if digest(g)!=digest(c['gate']):raise ValueError('GATE_RECEIPT_CHANGED')
 return c

def run(raw,budget_seconds=3):
 start=time.monotonic();W,L,n,count=validate_raw(raw);rev=revision()
 out={'schema':'GENERAL125_RESPONSE_V1','requested_count':count,'admitted_count':0,'distinct_count':0,'shortfall':count,'candidates':[],'internal_proposals':[],'accepted':False,'release':False,'engine_revision':rev,'input_exact':{'W':S(W),'L':S(L),'n':n},'scope':'EXPERIMENTAL_N2_LEFT_RIGHT_ONE_DOUBLE_PER_UNIT_ONLY','program_assumptions':{'bedrooms_per_unit':1,'occupants_per_unit':2,'capacity_suitability_verified':False},'verified_architectural_diversity':False,'organization_count':0,'organization_shortfall':count,'limits':['One actual profile, not requested six organizations.','No capacity optimality or general architectural quality claim.','Light and ventilation excluded from MVP.'],'search_evidence':{'solver_calls':0,'per_call_seconds':min(3,float(budget_seconds)),'max_calls':1,'budget_scope':'Solver limit only; assembly and complete validation finish without interruption. Total timing separately reported.'}}
 try:core=local_core(W,L)
 except ValueError as e:return dict(out,status='NO_ADMITTED_LAYOUT',reason=str(e),not_global_infeasibility=True,total_seconds=time.monotonic()-start)
 t=time.monotonic();p=propose(core,1,time_limit=min(3,float(budget_seconds)),variant=1,sleep_roles=['double'],topology='FRAME125_SERVICE_SIDE');out['search_evidence'].update(solver_calls=1,search_seconds=time.monotonic()-t,proposal_status=p.get('status'));out['proposal_evidence']=p
 if p.get('status')!='PROPOSAL_ONLY':return dict(out,status='NO_ADMITTED_LAYOUT',reason=p.get('status'),not_global_infeasibility=True,total_seconds=time.monotonic()-start)
 t=time.monotonic();packet=build(raw,p);ctx=context(raw,p,packet);out['search_evidence']['assembly_seconds']=time.monotonic()-t
 t=time.monotonic();g=evaluate_world(packet['local_model'],packet['world_model'],packet['core'],ctx);out['search_evidence']['validation_seconds']=time.monotonic()-t
 c={'model':packet['world_model'],'world_packet':packet,'generation_context':ctx,'gate':g,'accepted':False,'release':False};out['internal_proposals']=[c]
 if revision()!=rev:return dict(out,status='SOURCE_CHANGED_DURING_RUN',total_seconds=time.monotonic()-start)
 if _eligible(g):out.update(candidates=[c],admitted_count=1,distinct_count=1,shortfall=count-1,organization_count=1,organization_shortfall=count-1,status='LIMITED_DRAFT_SET')
 else:out.update(status='NO_ADMITTED_LAYOUT',reason='INDEPENDENT_WORLD_GATE',errors=g['errors'],pending=g['pending'])
 out['total_seconds']=time.monotonic()-start
 return out
