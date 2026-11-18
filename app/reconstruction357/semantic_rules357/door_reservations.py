"""Exact existing-source door pocket / surface-mount clearance reservations.
No newly chosen clearance values and no technical hardware certification.
Must be consumed only after bound fresh door-operation proof for this model.
"""
from fractions import Fraction as F
from modules_spatial import rect,intersection,union_area,digest

def derive(model,unit_id):
 out=[]
 for op in model['operations']['doors']:
  if not any(s.get('unit')==unit_id for s in op.get('states',[])):continue
  oid=op['opening_id'];kind=op['kind']
  if kind=='pocket_source113':
   pocket=rect(op['pocket']);out.append({'opening_id':oid,'kind':'SOURCE113_EXISTING_POCKET_RESERVATION','region':list(map(str,pocket)),'operation_digest':digest(op),'authority':'Fresh source113 door operation; existing source pocket rectangle, not newly expanded clearance','technical_approval':False})
  elif kind=='sliding_linear'and op.get('mount',{}).get('kind')=='surface':
   mount=op['mount'];host_id=mount['host_wall_id'];host=rect(model['wall_hosts'][host_id]);closed,opened,rail=rect(op['closed_panel']),rect(op['open_panel']),rect(op['rail_envelope'])
   width,height=host[2]-host[0],host[3]-host[1]
   if width==height:raise ValueError('AMBIGUOUS_SOURCE_HOST_NORMAL')
   normal=0 if width<height else 1;along=1-normal;thickness=F(mount['panel_thickness_m']);offset=F(mount['offset_m'])
   if offset<=0 or thickness<=0:raise ValueError('POSITIVE_SOURCE_MOUNT_PROFILE')
   if closed[normal+2]-closed[normal]!=thickness or opened[normal+2]-opened[normal]!=thickness:raise ValueError('SOURCE_PANEL_THICKNESS')
   if closed[normal]!=opened[normal]or closed[normal+2]!=opened[normal+2]:raise ValueError('SOURCE_LINEAR_MOUNT_AXIS')
   expected=(min(closed[0],opened[0]),min(closed[1],opened[1]),max(closed[2],opened[2]),max(closed[3],opened[3]))
   if rail!=expected:raise ValueError('SOURCE_RAIL_SWEEP')
   if not(host[along]<=rail[along]and rail[along+2]<=host[along+2]):raise ValueError('RAIL_EXCEEDS_SOURCE_HOST')
   gap=list(rail)
   if mount['face']=='min':
    if host[normal]-rail[normal+2]!=offset:raise ValueError('SOURCE_MOUNT_OFFSET')
    gap[normal]=rail[normal+2];gap[normal+2]=host[normal]
   elif mount['face']=='max':
    if rail[normal]-host[normal+2]!=offset:raise ValueError('SOURCE_MOUNT_OFFSET')
    gap[normal]=host[normal+2];gap[normal+2]=rail[normal]
   else:raise ValueError('SOURCE_MOUNT_FACE')
   out.append({'opening_id':oid,'kind':'EXACT_SOURCE_SURFACE_MOUNT_OFFSET_RESERVATION','region':list(map(str,gap)),'operation_digest':digest(op),'host_id':host_id,'host_geometry_digest':digest(model['wall_hosts'][host_id]),'source_offset_m':str(offset),'source_panel_thickness_m':str(thickness),'authority':'Actual bound source mount offset, checked against both rail and host; no invented margin','technical_approval':False})
 return out
