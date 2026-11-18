"""Exact width-aware diagnostic, not full kitchen usability or PRD closure.
Uses the source body's width and kitchen activity/motion regions. Does not
reinterpret that hypothetical profile as a universal architectural minimum.
"""
from fractions import Fraction as F
from review_cycle import digest

def rect(value):
    if not isinstance(value,list) or len(value)!=4 or any(type(x)not in(str,int)for x in value):
        raise ValueError('EXACT_RECT_REQUIRED')
    r=tuple(map(F,value))
    if r[0]>=r[2]or r[1]>=r[3]:raise ValueError('EMPTY_RECT')
    return r

def sweeps(path,body):
    if not isinstance(path,list)or len(path)<2:raise ValueError('GUEST_PATH_MISSING')
    points=[]
    for p in path:
        if not isinstance(p,list)or len(p)!=2 or any(type(x)not in(str,int)for x in p):raise ValueError('EXACT_POINT_REQUIRED')
        points.append(tuple(map(F,p)))
    out=[];h=body/2
    for a,b in zip(points,points[1:]):
        if a==b:continue
        if a[0]!=b[0]and a[1]!=b[1]:raise ValueError('ORTHOGONAL_PATH_REQUIRED')
        out.append((min(a[0],b[0])-h,min(a[1],b[1])-h,max(a[0],b[0])+h,max(a[1],b[1])+h))
    if not out:raise ValueError('GUEST_PATH_EMPTY')
    return out

def assess(model):
    out={'schema':'MAC_KITCHEN_GUEST_DIAGNOSTIC_V1','model_digest':digest(model),'state':'UNKNOWN','units':[],
         'display_allowed':False,'accepted':False,'delivery_allowed':False,
         'scope':'Source-profile guest living/dining sweeps versus declared kitchen floor, activity and motion envelopes only; no whole kitchen use, all guest destinations, programme suitability or regulatory approval.'}
    try:
        body=F(model['profile']['body_m'])
        if body<=0:raise ValueError('INVALID_BODY_WIDTH')
        units=model['units'];ids=[u['id']for u in units]
        if not ids or len(ids)!=len(set(ids)):raise ValueError('UNIT_INVENTORY')
        for u in units:
            uid=u['id'];ops=[o for o in model['operations']['kitchen']if o['unit']==uid]
            if len(ops)!=1:raise ValueError('KITCHEN_OPERATION_INVENTORY')
            op=ops[0];floor=u['rooms']['kitchen'];motion=op['motion_envelopes']
            if not floor or not motion:raise ValueError('KITCHEN_REGIONS_MISSING')
            zones=[('kitchen_floor',rect(r))for r in floor]+[('kitchen_work',rect(u['activities']['kitchen_work']))]+[('kitchen_motion',rect(r))for r in motion]
            rows=[]
            for name in ('guest_living','guest_dining'):
                path=u['scenario_routes'][name]
                if path[0]!=u['entry_point']:raise ValueError('GUEST_ENTRY_BINDING')
                hits=[];ss=sweeps(path,body)
                for i,s in enumerate(ss):
                    for zone,r in zones:
                        q=(max(s[0],r[0]),max(s[1],r[1]),min(s[2],r[2]),min(s[3],r[3]))
                        if q[0]<q[2]and q[1]<q[3]:hits.append({'segment':i,'zone':zone,'intersection':list(map(str,q))})
                rows.append({'route':name,'swept_segments':len(ss),'collisions':hits,'state':'FAIL_INTERSECTION'if hits else'PASS_SCOPED_SEPARATION'})
            out['units'].append({'unit':uid,'body_m':str(body),'kitchen_floor_area_m2':str(sum((r[2]-r[0])*(r[3]-r[1])for r in map(rect,floor))),'routes':rows})
        out['state']='FAIL_INTERSECTION'if any(r['collisions']for u in out['units']for r in u['routes'])else'PASS_SCOPED_SEPARATION'
    except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError)as e:
        out['missing']=[str(e)]
    return out
