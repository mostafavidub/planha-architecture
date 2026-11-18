"""Ordered SOURCE_SERVICE_JOINT367 reconstruction. No borrowed verdicts.
Stage1 branch-end proof before any entry/core changes. Stage2 actual notch source
assembly. Stage3 recompute operation domains on stage2, then select and rebuild.
"""
import json,hashlib,copy,sys,time
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'planha_general150_runtime_work'));sys.path.insert(0,str(ROOT/'semantic_rules357'))
from contract114 import digest
from assemble367 import assemble
from core_notch367 import derive
from operation_domain367 import domains
from selector367 import select
from branch_end_guard366_v5 import propose,compare_constructed
from modules_spatial import rect,difference
RECORD_SHA='8807b7f2e8ba841d8e1a38ba6787f72161c9d04f64d69e71112859be92976ad9'
SCHEMA='SOURCE_SERVICE_JOINT367_TRACE_V1'
def original():
 data=(ROOT/'staging365_service_grammar/candidate365.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!=RECORD_SHA:raise ValueError('FIXED_PARENT_CHANGED')
 r=json.loads(data)
 if r['trace']['schema']!='SOURCE_SERVICE_ANCHOR365_TRACE_V1':raise ValueError('PARENT_SCHEMA')
 return r

def original_parameters(r):
 m=r['candidate']['model'];ops={o['id']:o for o in m['openings']}
 return {'entry_x':{u:r['candidate']['packet']['core']['entry_centers'][u][0]for u in('A','B')},'slide_direction':{u:1 for u in('A','B')},'portal_y':{s:str((F(ops[s+'.entry']['rect'][1])+F(ops[s+'.entry']['rect'][3]))/2)for s in('stair','lift')}}

def protect(before,after,*,ownership_equal):
 for key in('inputs','program','profile','module_placements','module_ports'):
  if digest(before[key])!=digest(after[key]):raise ValueError('PROTECTED_MODEL:'+key)
 if [u['id']for u in before['units']]!=[u['id']for u in after['units']]:raise ValueError('UNIT_INVENTORY')
 for a,b in zip(before['units'],after['units']):
  for key in('fixtures','activities'):
   if digest(a[key])!=digest(b[key]):raise ValueError('PROTECTED_ASSET:'+a['id']+':'+key)
  aa=list(map(rect,a['ownership']));bb=list(map(rect,b['ownership']))
  if difference(aa,bb)or(ownership_equal and difference(bb,aa)):raise ValueError('PROTECTED_OWNERSHIP')
  for name in a['rooms']:
   if name.startswith('bed'):
    aa=list(map(rect,a['rooms'][name]));bb=list(map(rect,b['rooms'][name]))
    if difference(aa,bb)or difference(bb,aa):raise ValueError('BEDROOM_FLOOR_CHANGED')
 return {'status':'EXACT_DECLARED_DATA_PROTECTION_ONLY','ownership_policy':'EQUAL'if ownership_equal else'PER_UNIT_SET_NONDECREASE','functional_approval':False}

def assert_notch_entry(core,selection):
 hostend=F(core['notch367']['A_horizontal_boundary_end']);x=F(selection['entry_x']['A']);direction=selection['slide_direction']['A']
 if direction not in(-1,1):raise ValueError('SOURCE_SLIDE_DIRECTION')
 right=x+(F('1.95')if direction==1 else F('.65'))
 if right>hostend:raise ValueError('SELECTED_ENTRY_RAIL_EXCEEDS_NOTCH_HOST')
 return True

def build(*,stage_sink=None):
 r=original();base=r['candidate'];raw=base['request'];proposal=copy.deepcopy(r['trace']['proposal']);basecore=base['packet']['core'];W,L=F(raw['W']),F(raw['L']);events=[]
 def emit(name,data):
  events.append({'stage':name,**data})
  if stage_sink:stage_sink(name,data)
 # The guard is a source-bound proposal, not permission to patch final model.
 bp=propose(r);core=copy.deepcopy(basecore);core['branch_end367']={x['unit']:x['derived_end']for x in bp['units']};core['service_balanced367']=original_parameters(r);core['branch_only_original_operations367']=True
 branch=assemble(W,L,core,proposal)
 if stage_sink:stage_sink('BRANCH_MODEL_BUILT',{'model':branch})
 branchproof=compare_constructed(r,bp,branch);protect(base['model'],branch,ownership_equal=True)
 emit('BRANCH_RECONSTRUCTION',{'model_digest':digest(branch),'proposal':bp,'protection':branchproof})
 # Source notch built BEFORE deriving the new domain. Old operation feasibility
 # never serves as evidence for this changed host/floor geometry.
 notch=derive(core);notch.pop('branch_only_original_operations367');notchmodel=assemble(W,L,notch,proposal)
 if stage_sink:stage_sink('NOTCH_MODEL_BUILT',{'model':notchmodel})
 protect(branch,notchmodel,ownership_equal=False)
 emit('NOTCH_RECONSTRUCTION',{'model_digest':digest(notchmodel),'core_digest':digest(notch),'function':'UNKNOWN_UNTIL_OWN_REVIEW'})
 dr={'status':'COMPLETED_PURE_OPERATION_DOMAIN','domains':domains(notchmodel),'source_unchanged':True}
 intermediate={'candidate':{'model':notchmodel,'packet':{'core':notch}}};selection=select(intermediate,dr);assert_notch_entry(notch,selection)
 emit('JOINT_PARAMETER_SELECTION',{'model_digest':digest(notchmodel),'domain':dr,'selection':selection})
 finalcore=copy.deepcopy(notch);finalcore['service_balanced367']=selection
 for u in('A','B'):finalcore['entry_centers'][u][0]=selection['entry_x'][u]
 model=assemble(W,L,finalcore,proposal)
 if stage_sink:stage_sink('FINAL_MODEL_BUILT',{'model':model})
 protection=protect(notchmodel,model,ownership_equal=True)
 if basecore['stair']!=finalcore['stair']or basecore['lift']!=finalcore['lift']:raise ValueError('CORE_ASSET_CHANGED')
 packet={'family':'FRONT_REAR','world_model':model,'local_model':copy.deepcopy(model),'core':finalcore,'admission_claim':False};candidate={'request':raw,'request_digest':digest(raw),'packet':packet,'model':model,'model_digest':digest(model)}
 emit('FINAL_RECONSTRUCTION',{'model_digest':digest(model),'protection':protection,'route_failures':model['route_failures']})
 return candidate,{'branch_proposal':bp,'selection':selection,'stages':events,'parent_record_digest':digest(r),'role_approval':False}

def inventory():
 files=list(HERE.glob('*.py'))+list(HERE.glob('*.json'))
 rt=ROOT/'planha_general150_runtime_work';files+=list(rt.glob('*.py'))+list(rt.glob('*.json'))+[p for p in(rt/'references').rglob('*')if p.is_file()]
 frozen=json.loads((ROOT/'semantic_rules357/branch_end_guard366_v5_source_freeze.json').read_text())['files']
 files += [ROOT/n for n in frozen]+[ROOT/'semantic_rules357/branch_end_guard366_v5.py',ROOT/'semantic_rules357/branch_end_guard366_v5_source_freeze.json',ROOT/'staging365_service_grammar/candidate365.json']
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(set(files))}

def construct(*,stage_sink=None):
 before=inventory();candidate,details=build(stage_sink=stage_sink)
 if inventory()!=before:raise ValueError('SOURCE_CHANGED')
 trace={'schema':SCHEMA,'candidate_digest':digest(candidate),'model_digest':candidate['model_digest'],'packet_digest':digest(candidate['packet']),'source_inventory':before,**details}
 return {'candidate':candidate,'trace':trace,'accepted':False,'delivery_allowed':False}
def replay(trace):
 if trace.get('schema')!=SCHEMA or trace.get('source_inventory')!=inventory():raise ValueError('TRACE_SOURCE_BINDING')
 r=construct()
 if digest(r['trace'])!=digest(trace):raise ValueError('FULL_TRACE_REPLAY_MISMATCH')
 return r
