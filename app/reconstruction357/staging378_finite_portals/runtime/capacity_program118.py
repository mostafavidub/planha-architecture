"""Source-scoped spatial program, BEFORE placement. No area/55 or cap4 rule.
This contract does not turn room area or furniture presence into capacity proof.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from contract114 import digest
P=Path(__file__).resolve().parent
SOURCE=P/'references/CAPACITY_PROGRAM118_SOURCE.json'
def contract():
 s=json.loads(SOURCE.read_text())
 return {'schema':'SOURCE_CAPACITY_PROGRAM118_V1','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source':s,'alternatives':[{'id':'A9_ONE_DOUBLE','bedrooms':1,'occupants':2,'sleep_roles':['double'],'dining_seats_required':2,'living_person_places_required':2},{'id':'A9_DOUBLE_PLUS_TWIN','bedrooms':2,'occupants':4,'sleep_roles':['double','twin'],'dining_seats_required':4,'living_person_places_required':4}], 'higher_programs':'NOT_YET_BOUND_TO_A_COMPLETE_OCCUPANCY_AND_OPERATION_PROFILE; not forbidden or globally impossible','selection':'Compare actually feasible alternatives per unit, core/organization first, then fewer rooms if necessary; never silently change n. No maximizing bedroom count without functional quality.','area_policy':'Only actual activity regions, necessary circulation and genuinely unprogrammed floor are accounted separately; remainder is not proven living capacity.','required_witnesses':['sleep places and each bed access','closet capacity and actual use','each distinct dining chair pull/rise with all other necessary seats occupied','each distinct living person place and access','guest entry to living and dining independently, excluding cooking/dining activity conflicts','kitchen work, storage and service for declared program','named scenario completeness and same-model body/operations/routes'], 'accepted':False}
def audit_inventory(model):
 c=contract();results=[]
 for u in model['units']:
  rooms=[k for k in u['rooms']if k.startswith('bed')];md=u['fixture_metadata'];beds=[k for k,v in md.items()if v['kind'] in ('bed','double_bed','single_bed')];chairs=[k for k,v in md.items()if v['kind'].startswith('dining_chair')]
  profile=next((p for p in c['alternatives']if p['bedrooms']==len(rooms)),None);errors=[];pending=[]
  if not profile:pending.append('OCCUPANCY_PROGRAM_NOT_SOURCE_BOUND_FOR_THIS_ROOM_COUNT')
  elif len(chairs)<profile['dining_seats_required']:errors.append({'code':'INSUFFICIENT_DISTINCT_DINING_CHAIRS','actual':len(chairs),'required':profile['dining_seats_required']})
  if profile and profile['bedrooms']==2:
   singles=[k for k in beds if md[k]['kind']=='single_bed']
   if len(singles)!=2:errors.append({'code':'A9_TWIN_ROOM_PROGRAM_MISMATCH','required_single_beds':2,'actual':len(singles),'double_bed_repetition_is_not_this_profile':True})
  pending+=['LIVING_PERSON_PLACE_CAPACITY_AND_ALL_ACCESS_NOT_PROVEN','DINING_ALL_OTHER_OCCUPIED_PULL_RISE_NOT_PROVEN','PROGRAM_DAY_TO_DAY_SCENARIOS_NOT_COMPLETE']
  results.append({'unit':u['id'],'bedrooms':len(rooms),'profile':profile,'actual_bed_ids':beds,'actual_dining_chair_ids':chairs,'errors':errors,'pending':pending,'accepted':False})
 return {'schema':'CAPACITY118_INVENTORY_AUDIT','model_hash':digest(model),'contract_hash':digest(c),'units':results,'accepted':False,'scope':'Inventory can disprove a program; presence alone never proves operational capacity.'}

def enumerate_alternatives(unit_area,budget_count=12):
 """Finite engineer-budget list, not an owner bedroom cap or area sufficiency test.
 Lower bound is actual minimum supported bedroom MODULE clear footprint, only
 for this implementation. Twin modules exist; whole program capacity still requires fresh gate evidence.
 """
 from itertools import product
 area=F(str(unit_area));necessary_bound=int(area/(F('5.45')*F('3.6')))
 alternatives=[]
 for count in range(1,necessary_bound+1):
  for extras in product(('twin','double'),repeat=count-1):
   roles=['double',*extras];places=[{'room':i+1,'type':r,'sleep_instances':([{'kind':'reference_double_bed','capacity_hypothesis':2}]if r=='double'else[{'kind':'A9_single_bed','capacity_hypothesis':1},{'kind':'A9_single_bed','capacity_hypothesis':1}])}for i,r in enumerate(roles)]
   occupants=sum(v['capacity_hypothesis']for p in places for v in p['sleep_instances'])
   alternatives.append({'bedrooms':count,'sleep_program':places,'design_occupants_hypothesis':occupants,'required_distinct_dining_places':occupants,'required_living_person_places':occupants,'basis':'A9 exact role pattern'if roles in (['double'],['double','twin'])else'D07 internal explicitly disclosed composition of actual bed instances, not owner-approved occupancy policy','pending':['Each sleep-instance usability and simultaneous use','Matching dining/living/clothing/day-to-day capacity']+(['Twin bedroom module implementation']if 'twin'in roles else[]),'accepted':False})
   if len(alternatives)>=budget_count:return {'alternatives':alternatives,'necessary_module_area_bound':necessary_bound,'enumeration_stop':'ENGINEERING_CANDIDATE_BUDGET_NOT_INFEASIBILITY','area_does_not_prove_placement':True}
 return {'alternatives':alternatives,'necessary_module_area_bound':necessary_bound,'enumeration_stop':'CURRENT_MODULE_BOUND','area_does_not_prove_placement':True}

def proposed_program(core,raw):
 """Pick a bounded program-search order, not a claimed optimal final program."""
 box=list(map(F,core['units']['A']));area=(box[2]-box[0])*(box[3]-box[1]);bound=int(area/(F('5.45')*F('3.6')))
 requested=(raw.get('program')or{}).get('bedrooms_per_unit',raw.get('bedrooms_per_unit'))
 if requested is not None:
  b=F(str(requested))
  if b.denominator!=1 or b<1:raise ValueError('INVALID_BEDROOM_PROGRAM')
  order=[int(b)];basis='explicit_development_program'
 else:
  order=[b for b in [3,2,1,*range(4,bound+1)]if b<=bound][:12];basis='D07_automatic_source_profile_search_order_not_final_selection'
 if not order:raise ValueError('CURRENT_MODULE_PROGRAM_BOUND_EMPTY_NOT_GLOBAL_INFEASIBILITY')
 roles={str(b):['double']+['twin']*(b-1)for b in order}
 return {'unit_clear_depth_m':str(box[3]-box[1]),'bedroom_choices':order,'sleep_roles_by_count':roles,'basis':basis,'design_occupants_by_count':{str(b):sum(2 for _ in roles[str(b)])for b in order},'capacity_basis':'Sum actual reference double-bed(2) / two A9 single-bed(1+1) instances; >2 rooms explicitly internal study composition, not owner-approved occupancy policy.','necessary_module_area_bound':bound,'same_count_in_both_units':True,'enumeration_budget_count':12,'limits':['Program enumeration is a proposal list, not the runtime schedule. Runtime-supported counts and scheduled variants are attached by the engine.','Actual scheduling and cumulative budgets are reported separately. Three-bedroom whole topology is not integrated; untried alternatives are not infeasible.','Every sleep instance and equal-capacity living/dining/clothing/day-to-day scenario needs independent proof.','No area/55 selection, owner four-bedroom cap, or residual-as-useful-living claim.','The current topology and module bounds do not prove general geometric impossibility.']}
