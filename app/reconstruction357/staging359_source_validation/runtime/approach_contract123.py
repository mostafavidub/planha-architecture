"""Conservative placement reservation, not an owner simultaneity rule.
Public-room names do not establish free floor. Preserve the complete source
chair actor trajectory separately from static/occupied/pull obstacles.
"""
from fractions import Fraction as F

def dining_actor_sweeps(module):
    out=[]
    for seat in module['seating']['instances']:
        for i,seg in enumerate(seat['rise_transfer']['segments']):
            a,b=([F(str(x)) for x in seg[k]] for k in ('actor_start','actor_end'))
            # Rigid axis-aligned translation: this bbox is the exact swept
            # rectangle for these axis-aligned source motions.
            if (a[2]-a[0],a[3]-a[1]) != (b[2]-b[0],b[3]-b[1]):
                raise ValueError('NONRIGID_DINING_ACTOR')
            if a[0]!=b[0] and a[1]!=b[1]:
                raise ValueError('NON_AXIS_ALIGNED_DINING_ACTOR')
            out.append((seat['id']+':'+str(i),[min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])]))
    return out

def bedroom_role(uid):
    return {'unit':uid,'kind':'BEDROOM_PUBLIC_APPROACH123',
            'source_roles':['living','entry_circulation','dining'],
            'reservation_policy':'SEPARATE_BEDROOM_APRON_FROM_DINING_ACTOR_SWEEPS',
            'policy_scope':'conservative search construction; not a universal simultaneity requirement'}
