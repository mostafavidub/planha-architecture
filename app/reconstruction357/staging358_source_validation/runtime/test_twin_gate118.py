import copy,json
from pathlib import Path
from checker114 import check_twin_module
R=Path(__file__).parent;out={}
for name in('5.45x4.5','6x4.8','6.015x4.505','6x4.8_reflected'):
 m=json.loads((R/f'evidence/twin118_{name}.json').read_text());r=check_twin_module(m);assert not r['errors']and not r['pending'];out[name]=r
m=json.loads((R/'evidence/twin118_5.45x4.5.json').read_text())
for case in('delete_second_bed','shrink_single','missing_second_access','fake_target_band','remove_actual_skin','source_profile_tamper'):
 n=copy.deepcopy(m)
 if case=='delete_second_bed':del n['unit']['fixtures']['bed1.bedB']
 if case=='shrink_single':n['unit']['fixtures']['bed1.bedB'][2]='5.3'
 if case=='missing_second_access':del n['unit']['routes']['bed1.bedB_back']
 if case=='fake_target_band':n['unit']['activities']['bed1.bedB_back']=n['unit']['activities']['bed1.bedA_front']
 if case=='remove_actual_skin':n['operations']['closets'][0]['shell_rects'].pop()
 if case=='source_profile_tamper':n['sleep_profile']['source_sha256']='0'*64
 r=check_twin_module(n);assert r['errors']or r['pending'],case;out[case]=r
(R/'evidence/independent118/twin_parameters_mutations.json').write_text(json.dumps(out,indent=2));print('Four actual twin module checks passed; six mutations rejected. Whole/occupancy acceptance not asserted.')
