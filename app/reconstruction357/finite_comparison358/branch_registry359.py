"""Explicit source-backed finite work inventory; not an exhaustion certificate."""
from build_ledger import *
import ast

def callable_pointer(path,name):
 p=ROOT/path;tree=ast.parse(p.read_text());node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name==name)
 return {'file':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'callable':name,'lines':[node.lineno,node.end_lineno]}
def registry():
 branches=[]
 for ident,path,fn,state,reason in [
 ('LAYOUT_ROW358_FIXED_PROPOSAL','staging358_comparative/row_adapter358.py','construct','EVALUATED','Actual source-bound 358; same exact brief/profile; negative area objective versus359'),
 ('LAYOUT_SIDECAR357_FIXED_PROPOSAL','staging357_comparative/translated_adapter.py','construct','EVALUATED','Actual source-bound357; negative source route objective versus359'),
 ('LAYOUT_ROW351_SAVED_PROPOSAL','planha_general150_runtime_work/constructor129.py','build','EVALUATED','Recovered fixed351 candidate, source provenance retained; negative source route objective versus359'),
 ('LAYOUT_HALL_CLAMP359_FIXED_LINEAGE','staging359_hall_clamp/adapter359.py','construct','EVALUATED_SELF_TIE','Current359, same exact fixed358 proposal, one bounded reconstruction'),
 ('CORE_FULL_BAND114_FIXED_INPUT','planha_general150_runtime_work/contract114.py','core_first','PROTECTED_DOMAIN_EXCLUDED','Source full-band primitive measured independently; exact ownership loss forbids this conservative comparative domain, not intrinsic invalidity'),
 ('CORE_NOTCH360_FIXED_LINEAGE','staging360_core_notch/adapter360.py','construct','UNKNOWN_ELIGIBILITY','Actual360 exists; source/fresh/intrinsic and objective review pending. Must not erase from current finite work domain'),
 ('DOOR_RELOCATION_STANDALONE','staging359_hall_clamp/adapter359.py','construct','UNSUPPORTED_REGISTERED_PRODUCER','Current fixed-lineage adapter takes no door position/host/profile parameters; source module openings regenerated unchanged. General source233 OP_EDIT_OPENING is specification, not an implemented standalone branch'),
 ('LAYOUT_OTHER_SOURCE_TOPOLOGIES','planha_general150_runtime_work/constructor129.py','build','STOPPED_UNASSESSED_SOURCE_DOMAIN','Source constructor has additional topology/family dispatches; this finite current-candidate cohort is not their exhaustion proof. No silent claim all source variants were attempted')]:
  branches.append({'id':ident,'source':callable_pointer(path,fn),'state':state,'reason':reason,'shared_constraints':{'raw':'exact W26 L28 n2 requested_count2','frame':'FRONT_REAR only in current fixed lineage','program':'double/twin/twin three bedrooms per unit','profile':'source asset/body dimensions unchanged','owner_exclusions':'lighting/ventilation and technical core approval excluded'},'applicability':'CURRENT_SOURCE_SUPPORTED_WORK_INVENTORY_NOT_GLOBAL_DISPATCH_EXHAUSTION'})
 core=branches[4];p=ROOT/'planha_general150_runtime_work/contract114.py';tree=ast.parse(p.read_text());names=[n.name for n in tree.body if isinstance(n,ast.FunctionDef)];core['source']['available_callables']=names
 return {'schema':'SOURCE_BACKED_FINITE_BRANCH_REGISTRY359_V2','version':2,'branches':branches,'scope_closed':False,'unknown_or_stopped_branch_ids':[b['id']for b in branches if b['state'].startswith(('UNKNOWN','STOPPED'))],'counted_evaluated_candidate_ids':['baseline351','translated357','row358','clamped359'],'current_model':'cb516cd81801438b7d920c3e3f0a56f98c22fae1e3ba03718d9dc2f8724b1b12','policy':'No branch omitted because unsupported/unknown; exact finite source operator bounds must be independently registered before a finite completeness claim. No infinite parameter search or global optimum assertion.','parent_acceptance':False}
if __name__=='__main__':
 x=registry();Path(__file__).with_name('branch_registry_actual359_v2.json').write_text(json.dumps(x,ensure_ascii=False,indent=2));print(x['unknown_or_stopped_branch_ids'])
