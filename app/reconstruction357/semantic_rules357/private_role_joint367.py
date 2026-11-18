"""Own-source joint367 intrinsic private connector role. Necessity stays separate."""
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,intersection,difference,union_area
from guest_closure import transformed_rect
from circulation_role_joint367 import evaluate as inventory

def source_port_cross_sections(private,ports,body):
 allowed=[];joins=[]
 for p in ports:
  q=rect(p['source_port_region']);dims=(q[2]-q[0],q[3]-q[1])
  if dims[0]==dims[1]:raise ValueError('AMBIGUOUS_SOURCE_PORT_AXIS_STOP')
  axis=0 if dims[0]>dims[1]else 1;normal=1-axis
  for c in private:
   if not intersection(c,q)or c[normal+2]-c[normal]!=1 or F(body)>1:continue
   z=list(c);z[axis]=max(c[axis],q[axis]);z[axis+2]=min(c[axis+2],q[axis+2])
   if z[axis]<z[axis+2]:allowed.append(tuple(z));joins.append({'source_port_digest':p['source_port_digest'],'actual_port_digest':p['actual_port_digest'],'source_module_digest':p['source_module_digest'],'source_corridor_cell':list(map(str,c)),'supporting_margin_cross_section':list(map(str,z))})
 return allowed,joins

def evaluate(record,review):
 out=inventory(record,review);m=record['candidate']['model']
 for row in out['units']:
  uid=row['unit'];u=next(u for u in m['units']if u['id']==uid);private=list(map(rect,u['rooms']['private_circulation']));ports=[]
  for p in m['module_placements']:
   if p['unit_id']!=uid or not p['room_id'].startswith('bed'):continue
   if digest(p['module'])!=p['module_hash']:raise ValueError('SOURCE_PRIVATE_MODULE_HASH')
   for sp in p['module']['external_ports']:
    oid=p['id_map'][sp['opening_id']];a=[x for x in m['module_ports']if x['opening_id']==oid]
    if len(a)!=1 or transformed_rect(sp['rect'],p['transform'])!=rect(a[0]['rect']):raise ValueError('SOURCE_PRIVATE_PORT_BINDING')
    ports.append({'opening_id':oid,'source_port_region':a[0]['rect'],'source_port_digest':digest(sp),'actual_port_digest':digest(a[0]),'source_module_digest':p['module_hash']})
  if {p['opening_id']for p in ports}!={uid+'.bed'+str(i)+'.entry'for i in(1,2,3)}:raise ValueError('COMPLETE_PRIVATE_SOURCE_PORT_INVENTORY')
  allowed,joins=source_port_cross_sections(private,ports,m['profile']['body_m']);direct=[z for p in ports for q in private if(z:=intersection(rect(p['source_port_region']),q))];res=[rect(q)for c in row['private_circulation_components']for q in c['unsupported_margin_regions']];left=difference(res,direct+allowed)
  required=all(c['required_targets_served']for c in row['private_circulation_components'])
  row['source_connector_margin_proof']={'status':'PASS_SCOPED_SOURCE_PORT_AND_TRANSVERSE_CORRIDOR_MARGIN'if not left and required else'UNKNOWN_UNBOUND_PRIVATE_MARGIN','source_ports':ports,'cross_section_joins':joins,'remaining_m2':str(union_area(left)),'remaining_regions':[list(map(str,q))for q in left],'engineering_assumption':'Registered source367 branch corridors are exactly one metre clear; full transverse corridor margin may serve a checked actual source approach without tiling by body sweep. No longitudinal extension beyond its source approach is covered.','necessity_claimed':False}
  row['intrinsic_private_role_status']='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE'if not left and required and not row['untargeted_terminal_extensions']else'UNKNOWN_SOURCE_BRANCH_COMPONENT_ROLE'
 out['schema']='JOINT367_OWN_FRESH_PRIVATE_COMPONENT_ROLE';out['status']='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE'if all(r['intrinsic_private_role_status'].startswith('PASS_')for r in out['units'])else'UNKNOWN_PRIVATE_ROLE';out['parent_complete']=False
 return out
