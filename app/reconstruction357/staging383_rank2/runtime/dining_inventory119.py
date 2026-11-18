"""Source-bound physical dining inventory, independent of bedroom count.
Four installed chairs do not prove four design occupants or operational success.
"""
from fractions import Fraction as F
from collections import Counter

def counts(unit):
 from public_program_audit118 import digest,examine_dining_module
 p=unit['dining_module_placement'];m=p['module']
 six=m.get('schema')=='SIX_PLACE_PLANAR_SOURCE_STUDY_V1'
 keys={'table',*('chair_'+n for n in('front_left','front_right','back_left','back_right','left','right'))}if six else{'table','chair_west','chair_east','chair_front','chair_back'}
 if m.get('schema')not in('DINING_CAPACITY_MODULE118_PROPOSAL','SIX_PLACE_PLANAR_SOURCE_STUDY_V1') or set(m['fixtures'])!=keys:raise ValueError('DINING_SOURCE_SCHEMA_INVENTORY')
 if m['seating']['requested_places']!=(6 if six else 4) or m['seating']['distinct_chair_count']!=(6 if six else 4):raise ValueError('DINING_SOURCE_FOUR_DISTINCT_INSTANCES')
 if digest(m)!=p['module_hash'] or examine_dining_module(m)['errors']:raise ValueError('DINING_SOURCE_GEOMETRY_HASH')
 ids=p['id_map']
 if set(ids)!=keys or len(set(ids.values()))!=len(keys):raise ValueError('DINING_SOURCE_ID_MAP')
 mat=[[F(str(v))for v in row]for row in p['transform']['matrix']];t=[F(str(v))for v in p['transform']['translation']]
 if len(mat)!=2 or len(t)!=2 or any(len(r)!=2 for r in mat) or any(v not in(-1,0,1)for r in mat for v in r) or any(sum(abs(v)for v in r)!=1 for r in mat) or any(sum(abs(mat[i][j])for i in range(2))!=1 for j in range(2)):raise ValueError('DINING_SOURCE_ISOMETRY')
 result=Counter()
 for key,r in m['fixtures'].items():
  x,y,X,Y=map(F,r);pts=[tuple(sum(mat[i][j]*v[j]for j in range(2))+t[i]for i in range(2))for v in((x,y),(x,Y),(X,y),(X,Y))];expected=(min(v[0]for v in pts),min(v[1]for v in pts),max(v[0]for v in pts),max(v[1]for v in pts))
  if tuple(map(F,unit['fixtures'][ids[key]]))!=expected:raise ValueError('DINING_ACTUAL_SOURCE_RECT')
  kind=('dining_table6'if six else'dining_table')if key=='table'else'dining_chair_front'if key in(('chair_front_left','chair_front_right','chair_left')if six else('chair_west','chair_front'))else'dining_chair_back'
  if unit['fixture_metadata'][ids[key]]['kind']!=kind:raise ValueError('DINING_ACTUAL_SOURCE_KIND')
  result[kind]+=1
 actual={k for k,v in unit['fixture_metadata'].items()if v.get('kind')in result}
 if actual!=set(ids.values()):raise ValueError('DINING_EXTRA_OR_MISSING_INSTANCE')
 return result
