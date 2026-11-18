import copy,json,unittest
from pathlib import Path
from fractions import Fraction as F
from checker114 import check_module_placements,digest
from named_checks118 import public_named_scenarios
P=Path('evidence/correction120/prefreeze_typed_kitchen_case5_assembly_only.json')
def fixture():return json.loads(P.read_text())['model']
def port(m):return next(p for p in m['module_ports']if p['role_id']=='A.kitchen_public_access')
def centered(q,c):
 q=list(map(F,q));x,y=map(F,c);w,h=q[2]-q[0],q[3]-q[1];return list(map(str,[x-w/2,y-h/2,x+w/2,y+h/2]))
def mutations(m):
 rows=[]
 a=copy.deepcopy(m);a['units'][0]['fixtures']['dining_table']=centered(a['units'][0]['fixtures']['dining_table'],port(a)['center']);rows.append(('table_body',a,'KITCHEN_PORT_BODY_ACTUAL_OCCUPIED_COLLISION'))
 a=copy.deepcopy(m);op=next(z for z in a['operations']['dining_chairs']if z['unit']=='A');op['occupied_body']=centered(op['occupied_body'],port(a)['center']);rows.append(('occupied_seat_body',a,'KITCHEN_PORT_BODY_ACTUAL_OCCUPIED_COLLISION'))
 a=copy.deepcopy(m);a['logical_regions']['A.kitchen_public_access']['source_roles'].append('bed1');rows.append(('bedroom_in_union',a,'MODULE_TYPED_PUBLIC_ROLE'))
 a=copy.deepcopy(m);o=next(z for z in a['openings']if z['id']=='A.bed1.entry');o['connects']=['A.kitchen_public_access'if z=='A.public_access'else z for z in o['connects']];rows.append(('bed_opening_cross_use',a,'MODULE_TYPED_PUBLIC_ROLE'))
 return rows
class Actual(unittest.TestCase):
 def test_actual(self):
  m=fixture();r=check_module_placements(m);self.assertEqual(r['errors'],[]);self.assertEqual(r['pending'],[]);self.assertEqual(public_named_scenarios(m)['status'],'PASS_LIMITED')
 def test_mutations(self):
  for name,m,code in mutations(fixture()):
   r=check_module_placements(m);self.assertTrue(any(e['code']==code for e in r['errors']),name)
 def test_guest_through_table(self):
  m=fixture();u=m['units'][0];p=u['scenario_routes']['guest_dining'];s,t=p[0],p[-1];q=list(map(F,u['fixtures']['dining_table']));c=[str((q[0]+q[2])/2),str((q[1]+q[3])/2)];pts=[s,[c[0],s[1]],c,[t[0],c[1]],t];u['scenario_routes']['guest_dining']=[v for i,v in enumerate(pts)if i==0 or v!=pts[i-1]];self.assertEqual(public_named_scenarios(m)['status'],'FAIL')
if __name__=='__main__':unittest.main()
