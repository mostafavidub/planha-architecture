"""Exact clearance of an already witnessed fixed orthogonal polyline, not global routing."""
from fractions import Fraction as F
from review_cycle import digest
from kitchen_guest_review import rect
from guest_four_route_diagnostic import assess as guest_assess

def fixed_polyline_capacity(path,box,obstacles):
    b=list(map(F,box))
    if len(path)<2:raise ValueError('NONZERO_ORTHOGONAL_ROUTE_REQUIRED')
    limits=[];moving=False
    for index,(pa,pb) in enumerate(zip(path,path[1:])):
        a,c=list(map(F,pa)),list(map(F,pb))
        if a[0]!=c[0] and a[1]!=c[1]:raise ValueError('NON_ORTHOGONAL_ROUTE')
        if a==c:continue
        moving=True;seg=[min(a[0],c[0]),min(a[1],c[1]),max(a[0],c[0]),max(a[1],c[1])]
        for label,distance in [('left',seg[0]-b[0]),('bottom',seg[1]-b[1]),('right',b[2]-seg[2]),('top',b[3]-seg[3])]:
            if distance<0:raise ValueError('CENTER_ROUTE_OUTSIDE_BOUND')
            limits.append((distance,{'segment':index,'kind':'ownership_boundary','edge':label}))
        for oi,q in enumerate(map(rect,obstacles)):
            dx=max(q[0]-seg[2],seg[0]-q[2],F(0));dy=max(q[1]-seg[3],seg[1]-q[3],F(0))
            limits.append((max(dx,dy),{'segment':index,'kind':'obstacle','obstacle_index':oi,'rect':list(map(str,q))}))
    if not moving:raise ValueError('NONZERO_ORTHOGONAL_ROUTE_REQUIRED')
    distance=min(d for d,_ in limits)
    return {'schema':'FIXED_POLYLINE_LINF_CLEARANCE_V1','maximum_uniform_axis_aligned_square_width_m':str(2*distance),'limiting_constraints':[x for d,x in limits if d==distance],'scope':'Exact fixed-path source-scenario geometric capacity only; not best rerouted path, human turning/comfort, door-state completeness or regulatory minimum','accepted':False}

def assess(model,physical_review):
    mh=digest(model)
    if physical_review.get('model_hash')!=mh or physical_review.get('status')!='PASS_CONCEPT_SCOPED_REVIEW' or physical_review.get('errors')!=[] or physical_review.get('pending')!=[]:raise ValueError('FRESH_PHYSICAL_PASS_SAME_MODEL_REQUIRED')
    study=guest_assess(model);result={'schema':'V25_FIXED_GUEST_CLEARANCE_STUDY_V1','model_digest':mh,'fresh_review_digest':digest(physical_review),'guest_study_digest':digest(study),'units':[],'state':'UNKNOWN_FULL_GUEST_AND_ERGONOMIC_CLOSURE','accepted':False,'delivery_allowed':False,'qualified':False}
    if study.get('missing'):result['missing']=study['missing'];return result
    for u in model['units']:
        uid=u['id'];source=next(s for s in study['units'] if s['unit']==uid);box=u['ownership'][0]
        op=next(o for o in model['operations']['kitchen'] if o['unit']==uid)
        zones=[u['activities']['kitchen_work']]+op['motion_envelopes']+[s['actor_rect'] for s in op['workstations']]
        walls=list(model['walls'].values())+[x['open_panel'] for x in model['operations']['doors']]
        chairs=[]
        for chair in model['operations']['dining_chairs']:
            if chair['unit']!=uid:continue
            a,b=rect(chair['closed_rect']),rect(chair['open_rect'])
            chairs += [[str(min(a[0],b[0])),str(min(a[1],b[1])),str(max(a[2],b[2])),str(max(a[3],b[3]))],chair['occupied_body']]
        private=sum([v for k,v in u['rooms'].items() if k.startswith('bed') or k=='private_circulation'],[])
        routes=[]
        for source_route in source['routes']:
            name=source_route['id']
            fixtures=[q for k,q in u['fixtures'].items() if not u['fixture_metadata'][k].get('walkable') and not(name=='entry_WC' and k=='WC_iranian')]
            obstacles=walls+fixtures+chairs+private+zones
            if digest(obstacles)!=source_route['obstacle_digest']:raise ValueError('SCENARIO_OBSTACLE_BINDING')
            row={'id':name,'path':source_route['path'],'source_body_m':source_route['body_m'],'obstacle_digest':digest(obstacles)}
            if source_route['path']:
                row['capacity']=fixed_polyline_capacity(source_route['path'],box,obstacles)
                if F(row['capacity']['maximum_uniform_axis_aligned_square_width_m'])<F(source_route['body_m']):raise ValueError('CAPACITY_CONTRADICTS_SOURCE_WITNESS')
            else:row['state']='NO_ROUTE_WITNESS_NOT_GLOBAL_INFEASIBILITY'
            routes.append(row)
        result['units'].append({'unit':uid,'scenario':source['scenario'],'routes':routes})
    assert digest(model)==mh
    return result
