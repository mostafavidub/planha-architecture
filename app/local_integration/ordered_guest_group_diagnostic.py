"""Existential ordered source-profile route study, never natural-layout approval."""
from fractions import Fraction as F
from review_cycle import digest
from kitchen_guest_review import rect,sweeps
from guest_four_route_diagnostic import center,same_point
from living_connectivity_diagnostic import direction_changes
from local_seating_group_diagnostic import assess as group_assess,bounds

def assess(model):
    from geometry114 import cells,route
    from checker114 import covered
    from shared_geometry137 import local_polyline_clear
    mh=digest(model);group=group_assess(model,actor_scenario='OTHER_SEATS_OCCUPIED')
    result={'schema':'V25_ORDERED_GUEST_GROUP_STUDY_V1','model_digest':mh,'group_study':group,'units':[],'state':'UNKNOWN_NATURAL_GUEST_ORGANIZATION','accepted':False,'display_allowed':False,'delivery_allowed':False,'qualified':False,'scope':'Existence of an explicitly routed living-group visit before dining. A deliberate detour is not proof of natural first-living organization, axis quality, ergonomics or whole PRD.'}
    try:
        body=F(model['profile']['body_m'])
        if body<=0:raise ValueError('SOURCE_PROFILE_REQUIRED')
        for u in model['units']:
            uid=u['id'];g=next(x for x in group['units'] if x['unit']==uid)
            row={'unit':uid,'state':'NO_COMPLETE_ORDERED_WITNESS','legs':[]}
            result['units'].append(row)
            if g['state']!='LOCAL_SHARED_BODY_ACCESS_WITNESS_ONLY':
                row['reason']='NO_SOURCE_BOUND_LOCAL_GROUP_WITNESS';continue
            witness=next(a for a in g['attempts'] if len(a['routes'])==len(g['actual_seat_ids']) and all(r['path'] for r in a['routes']))
            shared=center(witness['body_rect']);dest=u['public_program']['destinations']
            living=center(u['activities'][dest['guest_living']['activity_id']]);dining=center(u['activities'][dest['guest_dining']['activity_id']])
            if dest['guest_living']['fixture_id'] not in g['actual_seat_ids']:raise ValueError('LIVING_DESTINATION_OUTSIDE_ACTUAL_GROUP')
            if not same_point(u['scenario_routes']['guest_living'][-1],living) or not same_point(u['scenario_routes']['guest_dining'][-1],dining):raise ValueError('SOURCE_DESTINATION_BINDING')
            walls=list(model['walls'].values())+[o['open_panel'] for o in model['operations']['doors']]
            private=sum([qs for name,qs in u['rooms'].items() if name.startswith('bed') or name in ('private_circulation','bath')],[])
            box=bounds(u['ownership']);floor=cells(u['ownership'],walls+private);outside=cells([box],floor)
            obstacles=walls+private+outside+[q for k,q in u['fixtures'].items() if not u['fixture_metadata'][k].get('walkable')]
            seats=u['public_program']['capacity']['living_seats'];obstacles += [s['occupied_body'] for s in seats]
            chairs=[]
            for op in model['operations']['dining_chairs']:
                if op['unit']==uid:chairs += [bounds([op['closed_rect'],op['open_rect']]),op['occupied_body']]
            operations=[o for o in model['operations']['kitchen'] if o['unit']==uid]
            if len(operations)!=1 or not chairs:raise ValueError('OPERATION_SCENARIO_INVENTORY')
            op=operations[0]
            if len(op.get('motion_envelopes',[]))!=6 or not op.get('workstations'):raise ValueError('KITCHEN_OPERATION_EVIDENCE')
            obstacles+=chairs+op['motion_envelopes']+[w['actor_rect'] for w in op['workstations']]+[u['activities']['kitchen_work']]
            row.update(actual_living_fixture=dest['guest_living']['fixture_id'],actual_living_activity=dest['guest_living']['activity_id'],actual_dining_fixture=dest['guest_dining']['fixture_id'],actual_dining_activity=dest['guest_dining']['activity_id'],shared_body_rect=witness['body_rect'],source_body_m=str(body),obstacle_digest=digest(obstacles))
            cases=[('entry_to_actual_living',u['entry_point'],living),('living_to_shared_group',living,shared),('shared_group_to_actual_dining',shared,dining)]
            for name,start,end in cases:
                path,why=route(start,end,box,obstacles,body=str(body));leg={'id':name,'start':start,'end':end,'path':path,'reason':why}
                row['legs'].append(leg)
                if not path:continue
                if not same_point(path[0],start) or not same_point(path[-1],end) or not local_polyline_clear(path,str(body),box,obstacles):raise ValueError('ORDERED_ROUTE_GEOMETRY')
                if any(not covered(b,list(map(rect,floor))) for b in sweeps(path,body)):raise ValueError('ORDERED_ROUTE_FLOOR')
                leg.update(length_m=str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1])) for a,b in zip(path,path[1:]))),turns=direction_changes(path))
            if len(row['legs'])==3 and all(x['path'] for x in row['legs']):row['state']='EXISTS_ORDERED_GUEST_ROUTE_ONLY'
        if digest(model)!=mh:raise ValueError('MODEL_CHANGED')
        result['remaining']=['Natural principal circulation and guest-first-living organization not proved by a forced detour','Furniture orientation/conversation and useful living area unqualified','Door scenario completeness and source profile ergonomics remain open','No nonfunctional-wall counterfactual closure']
    except (KeyError,ValueError,TypeError,IndexError,StopIteration) as e:result['missing']=[type(e).__name__+':'+str(e)]
    return result
