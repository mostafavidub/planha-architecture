"""Local shared seating-group diagnostic only, never a historical gate.
General actual inventory, not the historical six-use marker. A tight group
rectangle is a restricted study domain, never useful area or global infeasibility.
"""
from fractions import Fraction as F
import time
from review_cycle import digest
from kitchen_guest_review import rect,sweeps
from guest_four_route_diagnostic import center,same_point
from living_connectivity_diagnostic import direction_changes
def bounds(rs):
    qs=list(map(rect,rs))
    if not qs:raise ValueError('RECTANGLE_INVENTORY_REQUIRED')
    return [str(min(q[0] for q in qs)),str(min(q[1] for q in qs)),str(max(q[2] for q in qs)),str(max(q[3] for q in qs))]
def hit(a,b):return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
def assess(model):
    from geometry114 import cells,route
    from checker114 import covered
    from shared_geometry137 import local_polyline_clear
    result={'schema':'V25_LOCAL_SHARED_SEATING_STUDY_V1','model_digest':digest(model),'units':[],'state':'UNKNOWN_COHERENT_USEFUL_LIVING','accepted':False,'display_allowed':False,'delivery_allowed':False,'qualified':False,'historical_shared_gate_invoked':False,'scope':'Restricted actual-seat group witness; no ergonomic, useful-area, programme, historical marker or global-infeasibility claim'}
    try:
        body=F(model['profile']['body_m'])
        if body<=0:raise ValueError('SOURCE_PROFILE_REQUIRED')
        for u in model['units']:
            started=time.monotonic();seats=u['public_program']['capacity']['living_seats']
            expected={k for k,v in u['fixture_metadata'].items() if v['kind'] in ('sofa1','sofa2','armchair1','armchair2')}
            if len(expected)<2 or len(seats)!=len(expected) or {s['fixture_id'] for s in seats}!=expected:raise ValueError('ACTUAL_SEAT_INVENTORY')
            seatmap={s['fixture_id']:s for s in seats};ids=sorted(expected)
            uses={k:bounds([u['fixtures'][k],u['activities'][seatmap[k]['access_activity_id']]]) for k in ids}
            group=bounds(list(uses.values()));g=rect(group)
            walls=list(model['walls'].values())+[x['open_panel'] for x in model['operations']['doors']]
            floor=cells(u['rooms']['living']+u['rooms']['entry_circulation'],walls)
            outside=cells([group],floor)
            protected={k:q for k,q in u['fixtures'].items() if k not in expected and not u['fixture_metadata'][k].get('walkable')}
            obstacles=walls+list(u['fixtures'].values())+[s['occupied_body'] for s in seats]+outside
            for op in model['operations']['kitchen']:
                if op['unit']==u['id']:obstacles+=op['motion_envelopes']+[s['actor_rect'] for s in op['workstations']]
            for chair in model['operations']['dining_chairs']:
                if chair['unit']==u['id']:obstacles += [bounds([chair['closed_rect'],chair['open_rect']]),chair['occupied_body']]
            private=sum([qs for name,qs in u['rooms'].items() if name.startswith('bed') or name in ('private_circulation','bath')],[])
            obstacles+=private
            activities={k:u['activities'][seatmap[k]['access_activity_id']] for k in ids}
            allq=list(map(rect,obstacles+list(uses.values())))
            xs={g[0],g[2]-body};ys={g[1],g[3]-body}
            for a,b,c,d in allq:xs.update([a-body,c]);ys.update([b-body,d])
            free=[]
            for x in sorted(xs):
                if not g[0]<=x<=g[2]-body:continue
                for y in sorted(ys):
                    if not g[1]<=y<=g[3]-body:continue
                    q=(x,y,x+body,y+body)
                    if not any(hit(q,o) for o in allq) and covered(q,list(map(rect,floor))):free.append(q)
            free.sort(key=lambda q:(abs((q[0]+q[2])-(g[0]+g[2]))+abs((q[1]+q[3])-(g[1]+g[3])),q))
            row={'unit':u['id'],'actual_seat_ids':ids,'group_search_domain':group,'group_domain_not_useful_area':True,'source_body_m':str(body),'candidate_count':len(free),'candidate_limit':3,'time_budget_seconds':20,'nonseating_fixture_crossings':[k for k,q in protected.items() if hit(g,rect(q))],'attempts':[],'state':'NO_LOCAL_SHARED_WITNESS_IN_BOUNDED_STUDY'}
            for q in free[:3]:
                if time.monotonic()-started>20:row['budget_exhausted']=True;break
                point=center(list(map(str,q)));attempt={'body_rect':list(map(str,q)),'routes':[]}
                for k in ids:
                    target=center(activities[k]);obs=obstacles+[r for other,r in activities.items() if other!=k]
                    path,reason=route(point,target,group,obs,body=str(body))
                    entry={'fixture_id':k,'activity_id':seatmap[k]['access_activity_id'],'path':path,'reason':reason}
                    if path:
                        if not same_point(path[0],point) or not same_point(path[-1],target) or not local_polyline_clear(path,str(body),group,obs):raise ValueError('LOCAL_SHARED_ROUTE_BINDING')
                        if any(not covered(band,list(map(rect,floor))) for band in sweeps(path,body)):raise ValueError('LOCAL_SHARED_ROUTE_OUTSIDE_FLOOR')
                        entry.update(length_m=str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1])) for a,b in zip(path,path[1:]))),turns=direction_changes(path))
                    attempt['routes'].append(entry)
                row['attempts'].append(attempt)
                if len(attempt['routes'])==len(ids) and all(r['path'] for r in attempt['routes']):
                    row['state']='LOCAL_SHARED_BODY_ACCESS_WITNESS_ONLY';break
            result['units'].append(row)
        result['remaining']=['Witness does not approve seating conversation/orientation or comfort','Tight bbox is only a restricted search domain; failure is not global impossibility','Other standing-seat activities conservatively occupied simultaneously','No programme or useful-area qualification; no historical gate marker synthesized']
    except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError) as e:result['missing']=[type(e).__name__+':'+str(e)]
    return result
