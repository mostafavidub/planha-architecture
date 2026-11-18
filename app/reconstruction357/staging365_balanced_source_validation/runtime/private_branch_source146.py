from fractions import Fraction as F
from contract114 import S

def build(core,variant=1):
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);ox=ex-F('6.25');oy=y0
 if ox<x0 or ox+F('10.8')>x1 or y1-y0<F('9.65'):return None
 local={'bed1':['6.9','.15','10.5','5.6'],'bed2':['.15','.15','5.6','4.65'],'bed3':['.15','4.8','5.6','9.3']}
 rects={k:list(map(S,[ox+F(a),oy+F(b),ox+F(c),oy+F(d)]))for k,(a,b,c,d)in local.items()}
 return {'kind':'PARALLEL_TWINS_BRANCH146','origin':list(map(S,[ox,oy])),'rectangles':rects,'bed_door_sides':{'bed1':'top','bed2':'right','bed3':'right'},'private_interface_center_x':S(ex),'scope':'Parallel source twins and perpendicular rotated double with actual branch hall; independent admission required'}
