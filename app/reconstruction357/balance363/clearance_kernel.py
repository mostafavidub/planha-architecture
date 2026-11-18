"""Exact fixed-centerline square-body clearance; not general path optimization."""
from fractions import Fraction as F

def number(x):
 if type(x)not in(str,int,F):raise ValueError('EXACT_NUMBER')
 return F(x)
def rect(r):
 if len(r)!=4:raise ValueError('RECTANGLE')
 a,b,c,d=map(number,r)
 if a>=c or b>=d:raise ValueError('POSITIVE_RECTANGLE')
 return a,b,c,d
def segment(a,b):
 a=tuple(map(number,a));b=tuple(map(number,b))
 if len(a)!=2 or len(b)!=2 or(a[0]!=b[0]and a[1]!=b[1]):raise ValueError('AXIS_ALIGNED_SEGMENT_REQUIRED')
 return min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1])
def distance(a,b):
 # Exact L-infinity distance between a possibly degenerate centerline segment
 # and a closed blocked rectangle. Positive-area collision starts above it.
 return max(F(0),b[0]-a[2],a[0]-b[2],b[1]-a[3],a[1]-b[3])
def maximum_width(path,frame,blocked):
 if len(path)<2:raise ValueError('AT_LEAST_TWO_POINTS')
 frame=rect(frame);obs=[(x['id'],rect(x['rect']))for x in blocked];candidates=[]
 for i,(a,b)in enumerate(zip(path,path[1:])):
  s=segment(a,b);bounds=[s[0]-frame[0],s[1]-frame[1],frame[2]-s[2],frame[3]-s[3]]
  for side,d in zip(('left','bottom','right','top'),bounds):candidates.append((d,i,'FRAME_'+side))
  for ident,o in obs:candidates.append((distance(s,o),i,ident))
 radius=min(x[0]for x in candidates)
 if radius<=0:raise ValueError('CENTERLINE_NOT_STRICTLY_FREE')
 return {'max_axis_aligned_square_width_m':str(2*radius),'limiting_witnesses':[{'segment':i,'obstacle':name,'half_width_m':str(d)}for d,i,name in candidates if d==radius],'scope':'Fixed recorded centerline, exact static blocked set and frame. Not circular-body clearance or best route, legal width, or universal profile.'}
def feasible(path,frame,blocked,width):
 w=number(width)
 if w<=0:raise ValueError('POSITIVE_WIDTH')
 limit=number(maximum_width(path,frame,blocked)['max_axis_aligned_square_width_m'])
 return w<=limit
