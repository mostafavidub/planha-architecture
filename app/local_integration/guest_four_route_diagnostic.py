"""Four independent width-aware route studies. Not full PRD qualification.
Uses the model's stated source profile, not an invented regulatory threshold.
Conservative simultaneous open/occupied bounds can reject a study, not all designs.
"""
from fractions import Fraction as F
from review_cycle import digest
from kitchen_guest_review import rect,sweeps

def center(r):
    a,b,c,d=rect(r)
    return [str((a+c)/2),str((b+d)/2)]

def assess(model):
    out={'schema':'V25_FOUR_GUEST_ROUTE_STUDY_V1','model_digest':digest(model),
      'state':'UNKNOWN_PRD_CLOSURE','units':[],'accepted':False,'display_allowed':False,'delivery_allowed':False,
      'scope':'Four newly constructed width-aware routes under conservative source-profile bounds. Not final guest-first-living, all door scenarios, ergonomics or programme proof.'}
    try:
        from geometry114 import route
        body=F(model['profile']['body_m'])
        if body<=0:raise ValueError('BODY_PROFILE_MISSING')
        ids=[u['id'] for u in model['units']]
        if not ids or len(ids)!=len(set(ids)):raise ValueError('UNIT_INVENTORY')
        out['source_profile']=model['profile'];out['source_profile_digest']=digest(model['profile'])
        for u in model['units']:
            uid=u['id'];entry=u['entry_point'];box=u['ownership'][0]
            dest=u['public_program']['destinations']
            targets={}
            for name in ('guest_living','guest_dining'):
                d=dest[name]
                if d['fixture_id'] not in u['fixtures']:raise ValueError('DESTINATION_FIXTURE_BINDING')
                targets[name]=center(u['activities'][d['activity_id']])
                if u['scenario_routes'][name][-1]!=targets[name]:raise ValueError('SOURCE_DESTINATION_BINDING')
            wc=center(u['activities']['WC_use'])
            if u['route_targets']['WC_use']!=wc:raise ValueError('WC_DESTINATION_BINDING')
            operations=[x for x in model['operations']['kitchen'] if x['unit']==uid]
            if len(operations)!=1:raise ValueError('KITCHEN_OPERATION_INVENTORY')
            op=operations[0]
            if not op.get('motion_envelopes') or not op.get('workstations') or not op.get('drawers') or not op.get('fridge'):
                raise ValueError('KITCHEN_OPERATION_EVIDENCE_MISSING')
            zones=[u['activities']['kitchen_work']]+op['motion_envelopes']
            # Do not prohibit the whole kitchen floor: PRD prohibits occupied work/operation regions.
            for station in op['workstations']:zones.append(station['actor_rect'])
            walls=list(model['walls'].values())+[x['open_panel'] for x in model['operations']['doors']]
            chairs=[]
            for chair in model['operations']['dining_chairs']:
                if chair['unit']!=uid:continue
                a,b=rect(chair['closed_rect']),rect(chair['open_rect'])
                chairs += [[str(min(a[0],b[0])),str(min(a[1],b[1])),str(max(a[2],b[2])),str(max(a[3],b[3]))],chair['occupied_body']]
            if not chairs:raise ValueError('CHAIR_STATE_MISSING')
            private=sum([v for k,v in u['rooms'].items() if k.startswith('bed') or k=='private_circulation'],[])
            rows=[]
            cases=[('entry_living',entry,targets['guest_living']),('entry_dining',entry,targets['guest_dining']),('entry_WC',entry,wc),('living_dining',targets['guest_living'],targets['guest_dining'])]
            for name,start,end in cases:
                fixtures=[q for k,q in u['fixtures'].items() if not u['fixture_metadata'][k].get('walkable') and not(name=='entry_WC' and k=='WC_iranian')]
                obstacles=walls+fixtures+chairs+private+zones
                path,why=route(start,end,box,obstacles,body=str(body))
                row={'id':name,'start':start,'end':end,'body_m':str(body),'obstacle_digest':digest(obstacles),'obstacle_count':len(obstacles),'path':path,'reason':why,'state':'NO_WITNESS_THIS_CONSERVATIVE_SCENARIO'}
                if path:
                    if path[0]!=start or path[-1]!=end:raise ValueError('FRESH_ROUTE_ENDPOINT_BINDING')
                    bands=sweeps(path,body)
                    for band in bands:
                        if not(F(box[0])<=band[0] and F(box[1])<=band[1] and band[2]<=F(box[2]) and band[3]<=F(box[3])):raise ValueError('FRESH_ROUTE_OUTSIDE_OWNERSHIP')
                        for obs in map(rect,obstacles):
                            if max(band[0],obs[0])<min(band[2],obs[2]) and max(band[1],obs[1])<min(band[3],obs[3]):raise ValueError('FRESH_ROUTE_COLLISION')
                    row.update(state='PASS_SOURCE_PROFILE_ROUTE_ONLY',length_m=str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1])) for a,b in zip(path,path[1:]))),segments=len(bands))
                rows.append(row)
            out['units'].append({'unit':uid,'scenario':'all open panels plus chair swept/occupied and conservative kitchen operation bounds','kitchen_operation_digest':digest(op),'routes':rows})
        out['all_four_routes_have_witness']=all(r['path'] for u in out['units'] for r in u['routes'])
        out['remaining']=['Independent source profile is hypothetical, not ergonomic approval','Guest-first-living and furnished dining axis need separate proof','Door-state scenario completeness and bottleneck/opening classification not yet closed','No continuous-living or wall counterfactual evidence']
    except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError) as e:
        out['missing']=[type(e).__name__+':'+str(e)]
    return out
