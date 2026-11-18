"""Fresh context/raw/exterior D4 binding for Q04; never necessity approval."""
from fractions import Fraction as F
from frame_audit125 import digest,equal,rectangle,evaluate_core

def examine(m,context):
 errors=[];w={}
 try:
  from source_registry_joint367 import CurrentContext,verify_context
  if isinstance(context,CurrentContext) and not verify_context(m,context)['verified']:raise ValueError('REGISTERED_CONTEXT_INVALID')
  if not isinstance(context,dict):raise ValueError('WORKFLOW_CONTEXT_REQUIRED')
  raw=context['construction_trace']['raw'];trace=context['construction_trace']
  if not equal(m['inputs'],[raw['W'],raw['L'],raw['n']]):raise ValueError('ACTUAL_RAW_INPUT_BINDING')
  if m.get('frame_binding125'):
   core=context['frame_core125'];local=context['frame_local129'];T=core['world_from_local'];fb=m['frame_binding125']
   a=evaluate_core(core)
   if a['errors']:raise ValueError('ACTUAL_CORE_FRAME:'+str(a['errors']))
   if trace.get('family')!='LEFT_RIGHT':raise ValueError('TRACE_FAMILY')
   if not equal(m['inputs'],core['physical_core_model']['inputs'])or not equal(local['inputs'],core['solver_inputs']):raise ValueError('FRAME_INPUTS')
   for k,v in [('local_model_hash',digest(local)),('model_hash',digest(m)),('core_hash',digest(core))]:
    if trace.get(k)!=v:raise ValueError('TRACE_HASH:'+k)
   if fb.get('local_model_hash')!=digest(local)or fb.get('core_contract_hash')!=digest(core)or not equal(fb.get('world_from_local'),T):raise ValueError('WORLD_FRAME_RECEIPT')
   if set(m['walls'])!=set(local['walls']):raise ValueError('WALL_INVENTORY')
   for name,r in local['walls'].items():
    if not equal(rectangle(r,T),m['walls'][name]):raise ValueError('ACTUAL_WALL_D4:'+name)
   w={'local_model_hash':digest(local),'world_model_hash':digest(m),'core_hash':digest(core),'world_from_local':T};base=local
  else:
   if trace.get('family') not in (None,'FRONT_REAR'):raise ValueError('UNFRAMED_FAMILY')
   if trace.get('model_hash') and trace['model_hash']!=digest(m):raise ValueError('TRACE_HASH:model_hash')
   base=m;w={'world_model_hash':digest(m),'frame':'FRONT_REAR_NATIVE'}
  W,L=map(F,base['inputs'][:2]);walls=base['walls'];left,right,front,back=[tuple(map(F,walls[k]))for k in ('left','right','front','back')]
  if not all(len(r)==4 and r[0]<r[2]and r[1]<r[3]for r in (left,right,front,back)):raise ValueError('EXTERIOR_RECTANGLE')
  if not(left[0]==0 and right[2]==W and front[1]==0 and back[3]==L):raise ValueError('EXTERIOR_DIMENSION_BINDING')
  if not(left[1]==right[1]==0 and left[3]==right[3]==L and front[0]==back[0]==left[2]and front[2]==back[2]==right[0]):raise ValueError('EXTERIOR_SHELL_GEOMETRY')
 except(KeyError,ValueError,TypeError,IndexError)as ex:errors.append('CIRCULATION148_FRAME:'+str(ex))
 return {'errors':errors,'pending':[],'witness':w,'scope':'Actual raw/frame/walls binding only; no historical or internal necessity proof.'}
