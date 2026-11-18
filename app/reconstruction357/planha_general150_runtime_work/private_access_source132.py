from fractions import Fraction as F
from contract114 import S

def build(core,variant=2):
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);ox=ex-F('6.15');oy=y0
 if ox<x0 or ox+F('12.5')>x1 or y1-y0<F('10.15'):return None
 local={'bed1':['.15','.15','5.6','3.75'],'bed2':['.15','3.9','5.6','8.4'],'bed3':['6.9','4.8','12.35','9.3']}
 rects={k:list(map(S,[ox+F(a),oy+F(b),ox+F(c),oy+F(d)]))for k,(a,b,c,d)in local.items()}
 return {'kind':'STAGGER_ACCESS132','origin':list(map(S,[ox,oy])),'rectangles':rects,'bed_door_sides':{'bed1':'right','bed2':'right','bed3':'left'},'private_interface_center_x':S(ox+F('6.25')),'scope':'Left stacked double/twin facing raised upper twin with real lower service bay, source-size unchanged; experimental not accepted'}
