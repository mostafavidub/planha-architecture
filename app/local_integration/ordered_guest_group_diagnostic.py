"""Existential ordered source-profile route study, never natural-layout approval."""
from fractions import Fraction as F
from review_cycle import digest
from kitchen_guest_review import rect,sweeps
from guest_four_route_diagnostic import center,same_point
from living_connectivity_diagnostic import direction_changes
from local_seating_group_diagnostic import assess as group_assess,bounds

def first_positive_body_contact(path,width,regions):
    """Exact infimum distance of positive body/rectangle overlap; tangency excluded."""
    if F(width)<=0 or len(path)<2 or not any(list(map(F,a))!=list(map(F,b)) for a,b in zip(path,path[1:])):raise ValueError('NONZERO_ROUTE_AND_POSITIVE_BODY_REQUIRED')
    half=F(width)/2;travelled=F(0);best=None
    for pa,pb in zip(path,path[1:]):
        a,b=list(map(F,pa)),list(map(F,pb));delta=[b[i]-a[i] for i in range(2)]
        length=abs(delta[0])+abs(delta[1])
        if delta[0] and delta[1]:raise ValueError('CONTACT_PATH_NOT_ORTHOGONAL')
        if not length:continue
        for q in map(rect,regions):
            low,high=F(0),F(1);possible=True
            for axis in (0,1):
                lo,hi=q[axis]-half,q[axis+2]+half
                if delta[axis]==0:
                    if not lo<a[axis]<hi:possible=False;break
                else:
                    t0,t1=(lo-a[axis])/delta[axis],(hi-a[axis])/delta[axis]
                    low=max(low,min(t0,t1));high=min(high,max(t0,t1))
            if possible and low<high:
                d=travelled+length*low
                best=d if best is None else min(best,d)
        travelled+=length
    return None if best is None else str(best)

def assess(model,physical_review):
    from geometry114 import cells,route
    from checker114 import covered
    from shared_geometry137 import local_polyline_clear
    mh=digest(model)
    if not isinstance(physical_review,dict) or physical_review.get('model_hash')!=mh or physical_review.get('status')!='PASS_CONCEPT_SCOPED_REVIEW' or physical_review.get('errors')!=[] or physical_review.get('pending')!=[]:raise ValueError('FRESH_PHYSICAL_PASS_SAME_MODEL_REQUIRED')
    origin=physical_review.get('multiproposal_provenance127',{})
    if origin.get('verified')is not True or origin.get('model_hash')!=mh or origin.get('errors')!=[] or origin.get('pending')!=[]:raise ValueError('SOURCE_VERIFIED_MODEL_REQUIRED')
    group=group_assess(model,actor_scenario='OTHER_SEATS_OCCUPIED')
    result={'schema':'V25_ORDERED_GUEST_GROUP_STUDY_V1','model_digest':mh,'fresh_physical_review_digest':digest(physical_review),'precondition':'Caller supplied fresh source-verified physical PASS for identical model; workflow independently reconstructs/evaluates','kitchen_scenario':'Actual work activity + workstation actors + six conservative source motions; not whole kitchen-floor exclusion, not replacement for frozen guest gate','group_study':group,'units':[],'state':'UNKNOWN_NATURAL_GUEST_ORGANIZATION','accepted':False,'display_allowed':False,'delivery_allowed':False,'qualified':False,'scope':'Existence of an explicitly routed living-group visit before dining. A deliberate detour is not proof of natural first-living organization, axis quality, ergonomics or whole PRD.'}
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
            selected=next(z for z in u['public_program']['capacity']['living_seats'] if z['fixture_id']==dest['guest_living']['fixture_id'])
            if selected['access_activity_id']!=dest['guest_living']['activity_id']:raise ValueError('LIVING_ACTIVITY_SOURCE_BINDING')
            from public_program_audit118 import bind_operation_destination
            import inspect
            from pathlib import Path
            from parametric_worker import ENGINE
            if Path(inspect.getsourcefile(bind_operation_destination)).resolve()!=(ENGINE/'public_program_audit118.py').resolve():raise ValueError('DINING_BINDING_IMPORT')
            row['dining_source_binding']=bind_operation_destination(u,dest['guest_dining'],tuple(map(F,dining)))
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
            direct,reason=route(u['entry_point'],dining,box,obstacles,body=str(body))
            row['direct_dining_comparison']={'path':direct,'reason':reason,'scope':'Same-obstacle route proposal, not certified principal route or globally shortest'}
            if direct:
                if not same_point(direct[0],u['entry_point']) or not same_point(direct[-1],dining) or not local_polyline_clear(direct,str(body),box,obstacles):raise ValueError('DIRECT_ROUTE_GEOMETRY')
                if any(not covered(b,list(map(rect,floor))) for b in sweeps(direct,body)):raise ValueError('DIRECT_ROUTE_FLOOR')
                living_activities=[u['activities'][seat['access_activity_id']] for seat in seats]
                table_id=u['dining_module_placement']['id_map']['table']
                dining_material=chairs+[u['fixtures'][table_id]]
                contact=first_positive_body_contact(direct,body,dining_material)
                if contact is not None:raise ValueError('DIRECT_ROUTE_DINING_OCCUPANCY_COLLISION')
                row['direct_dining_comparison'].update(length_m=str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1])) for a,b in zip(direct,direct[1:]))),turns=direction_changes(direct),first_living_access_activity_contact_m=first_positive_body_contact(direct,body,living_activities),first_declared_dining_floor_contact_m=first_positive_body_contact(direct,body,u['rooms']['dining']),dining_occupied_material_contact_m=contact)

        if digest(model)!=mh:raise ValueError('MODEL_CHANGED')
        result['remaining']=['Natural principal circulation and guest-first-living organization not proved by a forced detour','Furniture orientation/conversation and useful living area unqualified','Door scenario completeness and source profile ergonomics remain open','No nonfunctional-wall counterfactual closure']
    except (KeyError,ValueError,TypeError,IndexError,StopIteration) as e:result['missing']=[type(e).__name__+':'+str(e)]
    return result
