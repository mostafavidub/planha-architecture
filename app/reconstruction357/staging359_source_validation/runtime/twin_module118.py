"""Actual two-single-bed program. New source profile, never half a double bed."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from bedroom_module116 import build as double_build
from contract114 import S,digest
from geometry114 import route,Q
P=Path(__file__).resolve().parent

def build(width,depth):
 W,H=F(str(width)),F(str(depth))
 if W<F('5.45')or H<F('4.5'):raise ValueError('TWIN_CURRENT_MODULE_BOUNDS_NOT_GLOBAL_INFEASIBILITY')
 m=double_build(width,depth);u=m['unit'];seq=lambda q:list(map(S,q))
 u['fixtures'].pop('bed1.bed');u['fixture_metadata'].pop('bed1.bed')
 for k in ['bed1.bed_front','bed1.bed_back','bed1.changing']:u['activities'].pop(k)
 for key,y in [('bedA',F('.9')),('bedB',F('2.7'))]:
  q=(W-F(2),y,W-F('.1'),y+F('.9'));fid='bed1.'+key
  u['fixtures'][fid]=seq(q);u['fixture_metadata'][fid]={'kind':'single_bed','rotation_deg':0,'source_profile':'A9_F5_SINGLE_BED_0.9x1.9','design_person_places':1,'capacity_is_design_scenario_not_actual_population':True}
  u['activities'][fid+'_front']=seq((q[0],q[1]-F('.9'),q[2],q[1]));u['activities'][fid+'_back']=seq((q[0],q[3],q[2],q[3]+F('.9')))
 u['activities']['bed1.changing']=seq((W-F('.8'),F('3.7'),W-F('.1'),F('4.4')))
 u['routes']={};u['route_targets']={};fail=[];start=(F('-.55'),F('.7'));obs=list(m['walls'].values())+list(u['fixtures'].values())+[m['operations']['doors'][0]['open_panel']]
 for k,q in u['activities'].items():
  q=Q(q);end=((q[0]+q[2])/2,(q[1]+q[3])/2);p,why=route(start,end,[-1,0,W,H],obs);u['route_targets'][k]=seq(end)
  if p:u['routes'][k]=p
  else:fail.append({'route':k,'reason':why})
 m['schema']='PRIVATE_TWIN_ROOM_MODULE118';m['contract_version']='PRIVATE_TWIN_SOURCE_A9_V1';m['input_program'].update(sleep_role='twin',single_beds=2,design_person_places=2)
 m['sleep_profile']={'id':'A9_F5_SINGLE_BED_0.9x1.9','source_file':'references/CAPACITY_PROGRAM118_SOURCE.json','source_sha256':hashlib.sha256((P/'references/CAPACITY_PROGRAM118_SOURCE.json').read_bytes()).hexdigest(),'source_line':378,'physical_size_m':['.9','1.9'],'allowed_rotation':True,'scale_allowed':False,'target_fixture_ids':['bed1.bedA','bed1.bedB'],'capacity_basis':'Two actual single-bed instances, one design person each; all operations remain to be independently checked.'}
 m['route_failures']=fail;m['source_binding']['producer_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();m['source_binding']['double_module_base_source_sha256']=hashlib.sha256((P/'bedroom_module116.py').read_bytes()).hexdigest();return m
