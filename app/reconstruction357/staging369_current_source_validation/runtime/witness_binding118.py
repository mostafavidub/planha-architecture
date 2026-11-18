"""Read-only physical binding, independent of search constructor."""
from fractions import Fraction as F

def bbox(parts):
 p=[list(map(lambda v:F(str(v)),q))for q in parts]
 return [min(q[0]for q in p),min(q[1]for q in p),max(q[2]for q in p),max(q[3]for q in p)]
def binding(m,p):
 u=next(u for u in m['units']if u['id']=='A');rows=[]
 for name,q in p['rectangles'].items():
  if name in u['rooms']:actual=bbox(u['rooms'][name]);kind='actual_room_floor_envelope'
  elif name.endswith('_use'):
   f=name[:-4].replace('chair','armchair') if name.startswith('chair') else name[:-4]
   actual=bbox([u['fixtures'][f],u['activities'][f+'_front']]);kind='rigid_fixture_plus_actual_use_area'
  elif name=='entry_apron':
   rows.append({'name':name,'scope':'master reserve; actual entry panel and moving actors independently gate-checked, not an occupied room','master_rectangle':q});continue
  else:raise ValueError(name)
  target=list(map(lambda v:F(str(v)),q));rows.append({'name':name,'kind':kind,'actual':list(map(str,actual)),'master':list(map(str,target)),'equal':actual==target})
 for port in m['module_ports']:
  if not port['id'].startswith('A.'):continue
  name=port['id'].split('.')[1];actual=list(map(F,port['center']));expected=list(map(lambda x:F(str(x)),p['network_paths'][name][-1]));rows.append({'name':port['id'],'kind':'actual_module_port','actual':list(map(str,actual)),'master':list(map(str,expected)),'equal':actual==expected})
 return {'all_bound_equal':all(r.get('equal',True)for r in rows),'rows':rows,'private_internal_fixtures_operations':'Not master decision variables; independently source/module/isometry bound and whole-neighbor checked.','q11':'Current physical witness is not evidence of Q11 compliance.'}
