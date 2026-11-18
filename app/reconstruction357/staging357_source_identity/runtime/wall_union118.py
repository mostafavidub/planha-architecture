"""Exact physical solid union and source aliases; no deletion of source walls.
Overlapping source descriptions refer to one physical region. This does not
certify finish specification or connection; independent checker decides both.
"""
from fractions import Fraction as F
from geometry114 import cells,Q
from contract114 import digest

def bind_physical_wall_union(m):
 walls=m['walls'];solid=cells(list(walls.values()),[]);parts={f'physical_wall_{i}':q for i,q in enumerate(solid)}
 def overlaps(a,b):return max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])
 aliases={k:[pid for pid,q in parts.items()if overlaps(Q(r),Q(q))]for k,r in walls.items()}
 m['physical_wall_network']={'schema':'EXACT_SOURCE_WALL_UNION118','source_wall_hash':digest(walls),'solids':parts,'source_aliases':aliases,'source_walls_preserved':True,'method':'Exact orthogonal union; alias intersections must reconstruct each source wall, no material added.','faces':'Coordinates are the modeled finished-face geometry used by body/opening checks; actual finish build-up not established.','finish_profile_status':'NOT_EVALUATED','accepted':False}
 return m
