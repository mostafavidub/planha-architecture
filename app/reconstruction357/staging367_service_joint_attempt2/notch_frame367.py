"""Source-derived exterior junction wall; no ownership-only repair."""
from fractions import Fraction as F

def outer_right(core,thickness):
 t=F(thickness)
 if core.get('kind')!='COMPACT_CORE_SOUTH_LIFT_NOTCH367' or t!=F('.15'):raise ValueError('UNSUPPORTED_NOTCH_SOURCE')
 y,Y=F(core['band'][1]),F(core['band'][3]);right=F(core['core_extent_x'][1]);lift=list(map(F,core['lift']));floor=list(map(F,core['notch367']['new_A_floor_ownership']))
 if right-t!=lift[2] or floor[2]!=lift[2] or floor[1]!=y-t:raise ValueError('EXTERIOR_JUNCTION_SOURCE_MISMATCH')
 return [right-t,y-t,right,Y]
