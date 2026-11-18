"""Pure study geometry, not an app gate or source authenticity validator."""
from fractions import Fraction as F

def rect(q):
    a,b,c,d=map(F,q)
    if a>=c or b>=d: raise ValueError('NONPOSITIVE_RECTANGLE')
    return a,b,c,d

def overlaps(a,b):
    return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])

def additional_body_witness(uses, fixtures, body_size):
    """Find square outside all use/fixture interiors, inside tight six-use bbox.
    Candidate corner enumeration is exact for axis-aligned rectangles. Touching
    edges permitted here; real physical policy still applies. No route claim.
    """
    if len(uses)!=6: raise ValueError('SIX_USES_REQUIRED')
    s=F(body_size)
    if s<=0: raise ValueError('POSITIVE_SOURCE_BODY_SIZE_REQUIRED')
    us=[rect(q) for q in uses]; obs=us+[rect(q) for q in fixtures]
    box=(min(q[0] for q in us),min(q[1] for q in us),max(q[2] for q in us),max(q[3] for q in us))
    x0,y0,x1,y1=box
    xs={x0,x1-s}; ys={y0,y1-s}
    # Forbidden lower-left intervals are (obstacle.left-s, obstacle.right).
    for a,b,c,d in obs: xs.update((a-s,c));ys.update((b-s,d))
    for x in sorted(xs):
        for y in sorted(ys):
            q=(x,y,x+s,y+s)
            if x0<=x and y0<=y and x+s<=x1 and y+s<=y1 and not any(overlaps(q,o) for o in obs):
                return q
    return None

def local_polyline_clear(points, body_size, group, obstacles):
    """Validate supplied orthogonal center path by exact swept square union.
    Does not search paths or authorize crossing other actors' activities.
    Caller must supply the scenario-specific obstacle set.
    """
    s=F(body_size)
    if s<=0: raise ValueError('POSITIVE_SOURCE_BODY_SIZE_REQUIRED')
    if not points: return False
    h=s/2; g=rect(group); os=[rect(q) for q in obstacles]
    ps=[tuple(map(F,p)) for p in points]
    segments=list(zip(ps,ps[1:])) or [(ps[0],ps[0])]
    for (x,y),(u,v) in segments:
        if x!=u and y!=v: return False
        q=(min(x,u)-h,min(y,v)-h,max(x,u)+h,max(y,v)+h)
        if not(g[0]<=q[0] and g[1]<=q[1] and q[2]<=g[2] and q[3]<=g[3]):return False
        if any(overlaps(q,o) for o in os):return False
    return True
