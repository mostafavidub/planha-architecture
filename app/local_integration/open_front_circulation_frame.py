"""New-origin raw/core/exterior binding; no historical trace adapter or necessity claim."""
from fractions import Fraction as F
from contract114 import digest
def examine(m,context):
 errors=[];w={}
 try:
  from open_front_world_origin import verify
  if not isinstance(context,dict):raise ValueError('NEW_STUDY_CONTEXT_REQUIRED')
  packet=context['study_packet'];trace=context['study_trace']
  origin=verify(packet,trace)
  if digest(m)!=digest(packet['world_model']):raise ValueError('NEW_STUDY_MODEL_BINDING')
  raw=trace['raw']
  if list(map(F,m['inputs']))!=[F(raw['W']),F(raw['L']),F(raw['n'])]:raise ValueError('ACTUAL_RAW_INPUT_BINDING')
  if m.get('frame_binding125'):raise ValueError('NEW_STUDY_TRANSPOSED_FRAME_NOT_SUPPORTED')
  if trace.get('family')!='FRONT_REAR':raise ValueError('NEW_STUDY_FRAME_FAMILY')
  W,L=map(F,m['inputs'][:2]);walls=m['walls'];left,right,front,back=[tuple(map(F,walls[k]))for k in ('left','right','front','back')]
  if not all(len(r)==4 and r[0]<r[2]and r[1]<r[3]for r in (left,right,front,back)):raise ValueError('EXTERIOR_RECTANGLE')
  if not(left[0]==0 and right[2]==W and front[1]==0 and back[3]==L):raise ValueError('EXTERIOR_DIMENSION_BINDING')
  if not(left[1]==right[1]==0 and left[3]==right[3]==L and front[0]==back[0]==left[2]and front[2]==back[2]==right[0]):raise ValueError('EXTERIOR_SHELL_GEOMETRY')
  w={'world_model_hash':digest(m),'frame':'FRONT_REAR_NATIVE','new_origin':origin}
 except(KeyError,ValueError,TypeError,IndexError)as ex:errors.append('OPEN_FRONT_CIRCULATION_FRAME:'+str(ex))
 return {'errors':errors,'pending':[],'witness':w,'scope':'Exact new-origin replay plus actual raw/native exterior binding only. All original exterior conditions retained; transposed frames unsupported. No circulation necessity proof.'}
