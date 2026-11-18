"""Explicit, provisional study contract. Input coverage is not output coverage."""
from fractions import Fraction as F
import hashlib,json,re
from decimal import Decimal,localcontext
def S(x):
 x=F(x)
 with localcontext()as ctx:
  ctx.prec=max(60,len(str(x.numerator))+len(str(x.denominator))+5)
  return format(Decimal(x.numerator)/Decimal(x.denominator),"f")
GRID=F('0.005');BODY=F('.7');EXT=F('.25');WALL=F('.15')
TRANS=str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩٫','01234567890123456789.')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def parse(raw):
 if not isinstance(raw,dict) or not {'W','L','n'}<=set(raw) or set(raw)-{'W','L','n','requested_count','bedrooms_per_unit','program'}:raise ValueError('INPUT_FIELDS')
 vals=[]
 for k in ('W','L','n'):
  s=str(raw[k]).translate(TRANS).strip()
  if not re.fullmatch(r'\d+(?:\.\d+)?',s):raise ValueError('INVALID_DECIMAL_'+k)
  vals.append(F(s))
 W,L,n=vals
 if not 5<=W<=45 or not 5<=L<=45:raise ValueError('OUTSIDE_REQUESTED_INPUT_DOMAIN')
 if n!=2:raise ValueError('PROGRAM_UNIT_COUNT_NOT_IMPLEMENTED_NOT_GEOMETRIC_INFEASIBILITY')
 from schedule123 import requested_count
 requested_count(raw)
 return W,L,2

def full_band_core_first(W,L):
 # First connected common graph, with explicit preserved stair/lift clear sizes.
 # Horizontal central band is one search topology, not a claim to all topologies.
 d=F('2.75');y=(L-d)/2;stair=[F('.4'),y+F('.15'),F('4.95'),y+d-F('.15')]
 lift=[W-F('2.05'),y+d-F('1.8'),W-F('.4'),y+d-F('.15')]
 left=F('5.1');right=W-F('2.2');door_x=left+F('.7')
 if right-left<F('2.65') or y-F('.15')<=F('.25'):return None
 return {'kind':'CONNECTED_CENTRAL_BAND_SEED','band':['.25',S(y),S(W-F('.25')),S(y+d)],'stair':list(map(S,stair)),'lift':list(map(S,lift)),
 'lobby':[[S(left),S(y),S(right),S(y+d)],[S(right),S(y),S(W-F('.25')),S(y+F('.8'))]],
 'entry_centers':{'A':[S(door_x),S(y-F('.075'))],'B':[S(door_x),S(y+d+F('.075'))]},
 'units':{'A':['.25','.25',S(W-F('.25')),S(y-F('.15'))],'B':['.25',S(y+d+F('.15')),S(W-F('.25')),S(L-F('.25'))]},
 'assumptions':['Stair/lift clear rectangles preserve source dimensions; structural/vertical circulation certification is not established.','Only one central-band topology is currently implemented. Failure is not global infeasibility.','Common graph begins at modeled stair/lift doors on this storey, not a proven street entrance.']}

def program(W,L,core,raw):
 q=core['units']['A'];area=(F(str(q[2]))-F(str(q[0])))*(F(str(q[3]))-F(str(q[1])))
 nested=raw.get('program')
 if nested is not None and (not isinstance(nested,dict)or set(nested)-{'bedrooms_per_unit'}):raise ValueError('PROGRAM_FIELDS')
 requested=(nested or {}).get('bedrooms_per_unit',raw.get('bedrooms_per_unit'))
 if nested and 'bedrooms_per_unit'in raw and F(str(requested).translate(TRANS))!=F(str(raw['bedrooms_per_unit']).translate(TRANS)):raise ValueError('PROGRAM_ALIAS_CONFLICT')
 if requested is not None:
  b=F(str(requested).translate(TRANS))
  if b.denominator!=1 or not 1<=b<=4:raise ValueError('PROGRAM_BEDROOM_COUNT_OUTSIDE_PROVISIONAL_IMPLEMENTATION')
  choices=[int(b)];basis='explicit_request'
 else:
  target=max(1,min(4,int(area/F(55))));choices=list(dict.fromkeys([target]+list(range(1,5))))
  basis='provisional_search_1_to_4_not_owner_final_program'
 return {'bedroom_choices':choices,'basis':basis,'same_count_in_both_units':True,'fixed_body_m':'.7','fixed_furniture':'Reference physical sizes, never scaled; room border/free area may vary.',
 'limits':['Room dimension bounds are provisional search preferences: bedroom modules 5.45–7.0 by 3.6–5.0 m plus real lateral 1.0m approach; bath 3.15–4.3 by 2.25–3.1; kitchen 2.35–3.6 by 3.05–4.2; dining 2.65–3.8 by 2.5–3.5. Bounds are not regulations or global infeasibility certificates.','Automatic initial bedroom target is floor(unit area / 55 m²), clamped to 1–4; all searched program choices are disclosed.','One to four bedrooms is a temporary search policy, not a law or impossibility bound.','All requested input dimensions remain exact; interior search lattice is5mm.','Living ratio45–55% is a preference indicator, not proof of usability.','D07 assigns spatial-program selection to the system. The current area/55 and four-bedroom cap are provisional engine limitations, not owner-approved capacity rules; failure to find an appropriate automatic program is not geometric infeasibility or a requirement to question the owner.']}


def core_first(W,L):
 """Compact central-band alternative, same actual clear stair/lift dimensions.
 Outside-band wings belong to the two units, not invented rooms or courtyard.
 """
 old=full_band_core_first(W,L)
 if old is None:return None
 C=(W-F('9.45'))/2;R=C+F('9.45');y=F(old['band'][1]);yt=F(old['band'][3]);mid=(y+yt)/2
 if C<F('.25')or R>W-F('.25'):return None
 stair=[C+F('.15'),y+F('.15'),C+F('4.7'),yt-F('.15')]
 lift=[C+F('7.65'),yt-F('1.8'),R-F('.15'),yt-F('.15')]
 left=C+F('4.85');right=C+F('7.5');entry=left+F('.7')
 own={}
 for uid in ('A','B'):
  box=old['units'][uid];lo=F(box[3])if uid=='A'else mid+F('.075');hi=mid-F('.075')if uid=='A'else F(box[1])
  own[uid]=[box]
  for a,b in ((F('.25'),C),(R,W-F('.25'))):
   if a<b and lo<hi:own[uid].append(list(map(S,[a,lo,b,hi])))
 return {**old,'kind':'COMPACT_CONNECTED_CENTRAL_CORE118','stair':list(map(S,stair)),'lift':list(map(S,lift)),'lobby':[list(map(S,[left,y,right,yt])),list(map(S,[right,y,R-F('.15'),y+F('.8')]))],'entry_centers':{'A':[S(entry),S(y-F('.075'))],'B':[S(entry),S(yt+F('.075'))]},'unit_ownership':own,'core_extent_x':[S(C),S(R)],'outside_band_unit_separator_y':[S(mid-F('.075')),S(mid+F('.075'))],'assumptions':old['assumptions']+['Compact 9.45m central core alternative preserves clear stair4.55x2.45 and lift1.65x1.65; outside-band wings are exact unit-owned floor, not promised useful rooms.','Old full-band topology preserved for comparison; centered entry shift can require different functional placement.']}
