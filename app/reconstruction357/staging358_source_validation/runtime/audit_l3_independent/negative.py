from check import *
m=json.loads((P/'evidence_l3_primitive131/model.json').read_text());cases=[]
def trial(name,fn):
 x=copy.deepcopy(m);fn(x);r=check(x);cases.append({'name':name,'rejected':bool(r['errors']),'errors':r['errors']})
trial('scaled_fixture',lambda x:x['units'][0]['fixtures']['bed1.bedA'].__setitem__(2,'3'))
trial('stale_actor',lambda x:x['operations']['doors'][0]['states'][0]['actor_rect'].__setitem__(0,'0'))
trial('stale_hand',lambda x:x['operations']['closets'][0]['panels'][0]['continuous_actor_segments'][0]['hand_end'].__setitem__(0,'0'))
trial('source_hash_changed',lambda x:x['module_placements'][0].__setitem__('module_hash','0'))
trial('wall_duplicate',lambda x:x['physical_wall_network']['solids'].__setitem__('duplicate',x['physical_wall_network']['solids']['physical_wall_0']))
trial('alias_omitted',lambda x:x['physical_wall_network']['source_aliases'].pop('A.bed1.front'))
trial('actual_corridor_obstacle',lambda x:x['walls'].__setitem__('injected',['5.8','2','6.7','2.2']))
trial('boundary_removed',lambda x:x['walls'].pop('A.private_l3.right_exposed'))
trial('route_shortcut',lambda x:x['private_domains'][0]['paths']['A.bed2'].__setitem__(1,['7','4.65']))
trial('room_double_count',lambda x:x['units'][0]['rooms']['public_interface'].append(x['private_domains'][0]['parts'][0]))
trial('absent_quadrant_relabel',lambda x:x['private_domains'][0]['parts'].append(['6.9','3.9','12.35','9.3']))
trial('port_fabricated',lambda x:x['module_ports'][0]['center'].__setitem__(0,'7'))
assert all(c['rejected']for c in cases),cases
(P/'audit_l3_independent/negatives.json').write_text(json.dumps({'count':len(cases),'all_rejected':True,'cases':cases},indent=2));print(len(cases),'negative cases rejected')
