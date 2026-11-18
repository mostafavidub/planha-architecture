"""Seat access connectivity witnesses; never labels residual floor useful living.
Two explicit studies distinguish source-classified residual from conceptual public union.
Neither modifies the model or grants display, delivery, programme or ergonomic authority.
"""
from fractions import Fraction as F
from review_cycle import digest
from kitchen_guest_review import rect,sweeps
from guest_four_route_diagnostic import center,same_point

def area_union(rectangles):
    from geometry114 import cells
    return sum((F(r[2])-F(r[0]))*(F(r[3])-F(r[1])) for r in cells(rectangles,[]))
def assess(model):
    result={'schema':'V25_CONNECTED_SEAT_ACCESS_STUDY_V1','model_digest':digest(model),'state':'UNKNOWN_CONTINUOUS_USEFUL_LIVING','units':[],'accepted':False,'display_allowed':False,'delivery_allowed':False,'qualified':False,'scope':'Source-profile geometric seat-access study; no useful-area or full continuous-living approval'}
    try:
        from geometry114 import cells,route
        from checker114 import covered
        body=F(model['profile']['body_m'])
        if body<=0:raise ValueError('PROFILE_REQUIRED')
        result['source_profile']=model['profile']
        for u in model['units']:
            seats=u['public_program']['capacity']['living_seats']
            expected={k for k,v in u['fixture_metadata'].items() if v['kind'] in ('sofa1','sofa2','armchair1','armchair2')}
            if not expected or len(seats)!=len(expected) or {s['fixture_id'] for s in seats}!=expected:raise ValueError('LIVING_SEAT_INVENTORY')
            endpoints=[];used=[]
            for s in seats:
                fid=s['fixture_id'];act=u['activities'][s['access_activity_id']];path=u['routes'].get(s['access_activity_id'])
                endpoint=center(act)
                if not path or not same_point(path[-1],endpoint):raise ValueError('SEAT_STANDING_BINDING')
                endpoints.append({'fixture_id':fid,'activity_id':s['access_activity_id'],'point':endpoint})
                used += [u['fixtures'][fid],act]
            walls=list(model['walls'].values())+[op['open_panel'] for op in model['operations']['doors']]
            fixtures=[q for k,q in u['fixtures'].items() if not u['fixture_metadata'][k].get('walkable')]
            occupied=[s['occupied_body'] for s in seats]
            dining=[]
            for chair in model['operations']['dining_chairs']:
                if chair['unit']!=u['id']:continue
                a,b=rect(chair['closed_rect']),rect(chair['open_rect'])
                dining += [[str(min(a[0],b[0])),str(min(a[1],b[1])),str(max(a[2],b[2])),str(max(a[3],b[3]))],chair['occupied_body']]
            kitchen=[]
            for op in model['operations']['kitchen']:
                if op['unit']==u['id']:
                    if not op.get('motion_envelopes') or not op.get('workstations'):raise ValueError('KITCHEN_EVIDENCE_MISSING')
                    kitchen += op['motion_envelopes']+[x['actor_rect'] for x in op['workstations']]
            if not kitchen or not dining:raise ValueError('SIMULTANEOUS_OPERATION_EVIDENCE_MISSING')
            private=sum([rs for k,rs in u['rooms'].items() if k.startswith('bed') or k in ('bath','private_circulation')],[])
            base_obstacles=walls+fixtures+occupied+dining+kitchen+private
            owner=u['ownership'];box=owner[0]
            if len(owner)!=1:raise ValueError('UNSUPPORTED_MULTI_OWNER_BOX')
            studies=[]
            for label,floor in [('DECLARED_RESIDUAL_LIVING',u['rooms']['living']),('CONCEPTUAL_PUBLIC_UNION_PROBE',u['rooms']['living']+u['rooms']['entry_circulation'])]:
                floor=cells(floor,walls);outside=cells(owner,floor);obstacles=base_obstacles+outside
                paths=[];all_bands=[]
                anchor=endpoints[0]
                for target in endpoints[1:]:
                    path,reason=route(anchor['point'],target['point'],box,obstacles,body=str(body))
                    row={'from_fixture':anchor['fixture_id'],'to_fixture':target['fixture_id'],'path':path,'reason':reason,'state':'NO_WITNESS_IN_THIS_STUDY'}
                    if path:
                        if not same_point(path[0],anchor['point']) or not same_point(path[-1],target['point']):raise ValueError('SEAT_ROUTE_ENDPOINT')
                        bands=sweeps(path,body)
                        if not bands:raise ValueError('EMPTY_SEAT_ROUTE')
                        for band in bands:
                            if not covered(band,list(map(rect,floor))):raise ValueError('SEAT_ROUTE_OUTSIDE_ACTUAL_UNION')
                            for o in map(rect,obstacles):
                                if max(band[0],o[0])<min(band[2],o[2]) and max(band[1],o[1])<min(band[3],o[3]):raise ValueError('SEAT_ROUTE_COLLISION')
                        all_bands += [[str(v) for v in q] for q in bands]
                        row.update(state='PASS_WIDTH_AWARE_SEAT_ACCESS_ONLY',length_m=str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1])) for a,b in zip(path,path[1:]))),turns=max(0,len(path)-2),width_m=str(body))
                    paths.append(row)
                connected=bool(paths) and all(p['path'] for p in paths)
                footprint=cells(used+all_bands,[])
                studies.append({'label':label,'state':'CONNECTED_SEAT_ACCESS_SOURCE_PROFILE' if connected else 'NO_CONNECTED_SEAT_WITNESS_THIS_STUDY','floor_digest':digest(floor),'floor_area_m2':str(area_union(floor)),'floor_cells':floor,'obstacle_digest':digest(obstacles),'seat_endpoints':endpoints,'paths':paths,'declared_used_footprint_m2':str(area_union(footprint)),'footprint_not_useful_area':True,'reclassification_performed':False})
            result['units'].append({'unit':u['id'],'classification':u.get('public_floor_classification'),'studies':studies,'owner_area_m2':str(area_union(owner))})
        result['remaining']=['Source body profile remains hypothetical, not ergonomically approved','Connected standing points are not a coherent seating-group or continuous useful-area proof','Compare route length/turns/bottlenecks with shorter organization; no arbitrary acceptance threshold','All simultaneous activity scenarios and functional rectangles remain to be proved','Public-union probe is not a source living reclassification']
    except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError) as e:
        result['missing']=[type(e).__name__+':'+str(e)]
    return result
