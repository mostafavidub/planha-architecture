"""One explicitly limited ordered macro, not global search-space equivalence."""
from fractions import Fraction as F
from contract114 import S,GRID

def build(core,variant=2):
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);C,R=map(F,core['core_extent_x'])
 floorgrid=lambda x:(x//GRID)*GRID
 start=floorgrid((x0+x1-F(20))/2);bw=F('5.8');bh=F('4.8');rects={}
 for i in range(3):
  x=start+i*F('7.1');rects['bed'+str(i+1)]=[x,y0,x+bw,y0+bh]
 rects['bath']=[C,y1-F('3.1'),C+F('4.3'),y1]
 rects['kitchen']=[x0,y1-F('4.2'),x0+F('3.6'),y1]
 rects['dining']=[x0+F('4.25'),y1-F('4.7'),x0+F('9.65'),y1-F('.3')]
 dx=F('.4')if variant==0 else F(0)
 for i in(1,2):
  x=ex+F('1.7')+(i-1)*F(4)+dx;y=y1-F('3.1');rects['sofa'+str(i)+'_use']=[x,y,x+F('2.2'),y+F('1.6')]
 for i in range(4):
  x=ex+F('1.7')+(i//2)*F(4)+(i%2)*F('1.8')+dx;y=y1-F('5.3');rects['chair'+str(i+1)+'_use']=[x,y,x+F('.8'),y+F('1.5')]
 for k,r in rects.items():
  if not(x0<=r[0]<r[2]<=x1 and y0<=r[1]<r[3]<=y1):return None
 # Preserve a real rear private hall, not leftover space rebranded as useful.
 if y1-F('5.3')<y0+bh+F('1.3'):return None
 return {'kind':'ORDERED_FRONT_THREE_PRIVATE_REAR_HALL_AND_SIX_PUBLIC121','rectangles':{k:list(map(S,r))for k,r in rects.items()},'scope':'Fixed-order compact macro with parameter-derived placement; a proper restricted subset, not warm-start capability or all-domain completeness.','bed_door_sides':{'bed1':'right','bed2':'left','bed3':'left'},'private_hall_clear_depth':'1.0','private_interface_center_x':S(ex),'raw_inputs_not_rounded':True,'internal_position_grid_m':S(GRID)}
