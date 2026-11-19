"""Exact standing-body attribution to declared residual and circulation floors.
Diagnostic only: no room relabeling or continuous-living approval.
"""
from fractions import Fraction as F
from contract114 import digest
from checker114 import rect,covered,intersects
from geometry114 import cells
from guest_four_route_diagnostic import center,same_point

def area(regions):
    return sum((F(q[2])-F(q[0]))*(F(q[3])-F(q[1]))for q in cells(regions,[]))

def assess(m):
    body=F(m['profile']['body_m']);h=body/2
    if body<=0:raise ValueError('BODY_PROFILE_REQUIRED')
    before=digest(m);rows=[]
    for u in m['units']:
        seats=u['public_program']['capacity']['living_seats']
        ids={k for k,v in u['fixture_metadata'].items()if v['kind']in('sofa1','sofa2','armchair1','armchair2')}
        if not ids or len(seats)!=len(ids)or {s['fixture_id']for s in seats}!=ids:raise ValueError('SEAT_INVENTORY')
        walls=list(m['walls'].values());panels=[o['open_panel']for o in m['operations']['doors']]
        fixtures=[q for k,q in u['fixtures'].items()if not u['fixture_metadata'][k].get('walkable')]
        occupied=[s['occupied_body']for s in seats]
        dining=[]
        for op in m['operations']['dining_chairs']:
            if op['unit']!=u['id']:continue
            a,b=rect(op['closed_rect']),rect(op['open_rect'])
            dining += [[str(min(a[0],b[0])),str(min(a[1],b[1])),str(max(a[2],b[2])),str(max(a[3],b[3]))],op['occupied_body']]
        kitchen=[]
        for op in m['operations']['kitchen']:
            if op['unit']==u['id']:kitchen+=op['motion_envelopes']+[x['actor_rect']for x in op['workstations']]
        if not dining or not kitchen:raise ValueError('ACTUAL_OPERATION_INVENTORY')
        private=sum([rs for k,rs in u['rooms'].items()if k.startswith('bed')or k in('bath','private_circulation')],[])
        physical_groups={'walls':walls,'open_panels':panels,'fixtures':fixtures,'occupied_seats':occupied,'dining_states':dining,'kitchen_operations':kitchen,'private_floor':private}
        living=cells(u['rooms']['living'],walls)
        circulation=cells(u['rooms']['entry_circulation'],walls)
        public=cells(u['rooms']['living']+u['rooms']['entry_circulation'],walls)
        for seat in seats:
            fid=seat['fixture_id'];aid=seat['access_activity_id'];point=center(u['activities'][aid])
            if not same_point(u['routes'][aid][-1],point):raise ValueError('ACTUAL_SEAT_ACTIVITY_ENDPOINT')
            x,y=map(F,point);q=(x-h,y-h,x+h,y+h);body_rect=list(map(str,q))
            outside=cells([body_rect],living);outside_public=cells([body_rect],public)
            blockers={name:[i for i,r in enumerate(rs)if intersects(q,rect(r))]for name,rs in physical_groups.items()}
            blockers={k:v for k,v in blockers.items()if v}
            in_living=body*body-area(outside);in_public=body*body-area(outside_public)
            in_circ=body*body-area(cells([body_rect],circulation))
            if covered(q,list(map(rect,living)))!=(not outside):raise ValueError('INDEPENDENT_LIVING_COVERAGE_DISAGREEMENT')
            if covered(q,list(map(rect,public)))!=(not outside_public):raise ValueError('INDEPENDENT_PUBLIC_COVERAGE_DISAGREEMENT')
            rows.append({'unit':u['id'],'fixture_id':fid,'activity_id':aid,'endpoint':point,'body_m':str(body),'body_rect':body_rect,'body_area_m2':str(body*body),
                'in_declared_living_m2':str(in_living),'in_declared_circulation_m2':str(in_circ),'in_public_union_m2':str(in_public),
                'outside_declared_living_parts':outside,'outside_public_union_parts':outside_public,
                'body_fully_in_living':not outside,'body_fully_in_public_union':not outside_public,
                'physical_state_blockers':blockers,
                'floor_digest':digest({'living':living,'circulation':circulation,'public':public})})
    if digest(m)!=before:raise ValueError('ENDPOINT_DIAGNOSTIC_MUTATED_MODEL')
    return {'schema':'V25_LIVING_ENDPOINT_FLOOR_ATTRIBUTION_V1','model_digest':before,'rows':rows,
        'CONTINUOUS_USEFUL_LIVING':'UNKNOWN','accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
        'scope':'Exact source standing-body floor attribution and actual conservative state collisions. Attribution to circulation is not approval to relabel it living, useful-area proof, or all-route connectivity.'}
