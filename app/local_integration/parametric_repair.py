"""Narrow constructor129 FRONT_REAR source repair. No physical-law claims.
Trusted internal call only; this is not an external authorization API.
"""
import copy
from fractions import Fraction as F
from review_cycle import digest
PUBLIC={'sofa1','sofa2','armchair1','armchair2','armchair3','armchair4'}

def rect(v):
    if type(v)is not list or len(v)!=4 or any(type(x)not in(str,int)for x in v):raise ValueError('EXACT_RECT_REQUIRED')
    r=tuple(map(F,v))
    if r[2]<=r[0] or r[3]<=r[1]:raise ValueError('RECT_EXTENT')
    return r

def overlap(a,b):return min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1])
def moved(r,dx,dy):return (r[0]+dx,r[1]+dy,r[2]+dx,r[3]+dy)
def contains(q,owners):
    xs=sorted({q[0],q[2]}|{x for r in owners for x in(r[0],r[2])if q[0]<x<q[2]});ys=sorted({q[1],q[3]}|{y for r in owners for y in(r[1],r[3])if q[1]<y<q[3]})
    return all(any(r[0]<=(a+b)/2<=r[2] and r[1]<=(c+d)/2<=r[3] for r in owners)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:]))
def source_key(fid):return (fid if fid.startswith('sofa')else'chair'+fid[8:])+'_use'

def protected(packet,fixture_id):
    if fixture_id not in PUBLIC:raise ValueError('UNREGISTERED_FIXTURE')
    model=packet['world_model']
    result={k:copy.deepcopy(model[k])for k in ('inputs','profile','program','common_spaces','walls','openings','concept_windows','fixture_catalog_digest')}
    result['core']=copy.deepcopy(packet['core']);result['family']=packet['family'];result['units']=[]
    for u in model['units']:
        result['units'].append({'id':u['id'],'ownership':copy.deepcopy(u['ownership']),
          'rooms':{k:copy.deepcopy(v)for k,v in u['rooms'].items()if k not in ('living','entry_circulation')},
          'fixtures':{k:copy.deepcopy(v)for k,v in u['fixtures'].items()if k!=fixture_id},
          'activities':{k:copy.deepcopy(v)for k,v in u['activities'].items()if k!=fixture_id+'_front'},
          'fixture_metadata':copy.deepcopy(u['fixture_metadata'])})
    return result

def propose(raw,family,proposal,packet,context,review,source_revision,test_only=False):
    from current_entry_boundary_x03 import check_raw_domain
    check_raw_domain(raw)
    before=digest([raw,proposal,packet,context,review])
    if family!='FRONT_REAR' or packet.get('family')!=family:raise ValueError('UNSUPPORTED_REPAIR_FRAME')
    if proposal.get('generation_method') not in (['COARSE_BUNDLE_MILP_NOT_FULL_NETWORK_SOLVER','CONTROLLED_PARAMETRIC_COLLISION_FIXTURE_V1'] if test_only else ['COARSE_BUNDLE_MILP_NOT_FULL_NETWORK_SOLVER']):raise ValueError('UNREGISTERED_PROPOSAL_FAMILY')
    trace=context['construction_trace'];model=packet['world_model'];mh=digest(model);origin=review.get('hierarchical_provenance129',{})
    if trace['raw']!=raw or trace['proposal']!=proposal or trace['model_hash']!=mh or trace['local_model_hash']!=digest(packet['local_model']) or trace['core_hash']!=digest(packet['core']) or review.get('model_hash')!=mh:raise ValueError('CURRENT_PARENT_BINDING')
    if origin.get('verified')is not True or origin.get('model_hash')!=mh or origin.get('source_revision')!=source_revision or trace['source_revision']!=source_revision:raise ValueError('FRESH_PARENT_PROOF_REQUIRED')
    if review.get('status')!='FAIL' or review.get('pending')!=[]:raise ValueError('UNAMBIGUOUS_CURRENT_FAIL_REQUIRED')
    errors=review.get('errors');collisions=[e for e in errors if type(e)is dict and e.get('code')=='FIXTURE_COLLISION'] if type(errors)is list else []
    if not collisions:raise ValueError('DIRECT_COLLISION_REQUIRED')
    pair=collisions[0].get('fixtures')
    if type(pair)is not list or len(pair)!=2 or len(set(pair))!=2 or not set(pair)<=PUBLIC:raise ValueError('UNSUPPORTED_COLLISION_PAIR')
    if any(e.get('fixtures')!=pair for e in collisions):raise ValueError('MULTIPLE_COLLISION_PAIRS_UNSUPPORTED')
    units=packet['local_model']['units'];unit=next(u for u in units if u['id']=='A')
    if not overlap(rect(unit['fixtures'][pair[0]]),rect(unit['fixtures'][pair[1]])):raise ValueError('MISSING_GEOMETRIC_COLLISION')
    owners=list(map(rect,unit['ownership']));options=[]
    for fid,other in (pair,pair[::-1]):
        key=source_key(fid);q=rect(proposal['rectangles'][key]);fx=rect(unit['fixtures'][fid]);activity=rect(unit['activities'][fid+'_front'])
        compound=(min(fx[0],activity[0]),min(fx[1],activity[1]),max(fx[2],activity[2]),max(fx[3],activity[3]))
        if q!=compound:raise ValueError('SOURCE_COMPOUND_BINDING')
        obstacle=rect(proposal['rectangles'][source_key(other)])
        for dx,dy in ((obstacle[0]-q[2],F(0)),(obstacle[2]-q[0],F(0)),(F(0),obstacle[1]-q[3]),(F(0),obstacle[3]-q[1])):
            target=moved(q,dx,dy)
            # Four metres is a finite search budget inherited from mechanics,
            # not an architectural maximum or minimum.
            if not(dx or dy)or abs(dx)+abs(dy)>4 or not contains(target,owners):continue
            if any(overlap(target,rect(v))for k,v in proposal['rectangles'].items()if k!=key):continue
            options.append((abs(dx)+abs(dy),fid,key,dx,dy,target))
    if not options:return {'state':'UNSUPPORTED_REPAIR_NO_SAFE_FINITE_TRANSLATION','repair_attempted':False}
    _,fid,key,dx,dy,target=min(options)
    child=copy.deepcopy(proposal);child['rectangles'][key]=list(map(str,target))
    for k in ('solver_status','solver_message','variables','constraints','seconds'):child.pop(k,None)
    child['status']='PROPOSAL_ONLY';child['generation_method']='EXACT_PARAMETRIC_SEATING_TRANSLATION_V1';child['solver_used']=False
    result={'state':'RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED','proposal':child,'parent_proposal_digest':digest(proposal),'parent_model_digest':mh,'parent_review_digest':digest(review),'source_revision':source_revision,'raw_digest':digest(raw),'protected_digest':digest(protected(packet,fid)),'allowed_derived_changes':['target fixture and front activity','route/scenario geometry and targets','living/entry_circulation classification from actual route sweeps; not walls'], 'operator':{'fixture_id':fid,'source_key':key,'dx':str(dx),'dy':str(dy),'search_budget_not_physical_rule_m':4},'accepted':False,'delivery_allowed':False}
    if digest([raw,proposal,packet,context,review])!=before:raise ValueError('PARENT_MUTATED')
    result['plan_digest']=digest(result)
    return result

def verify_child(raw,parent,plan,child_packet,child_review,child_context):
    from current_entry_boundary_x03 import check_raw_domain
    check_raw_domain(raw)
    unsigned={k:v for k,v in plan.items()if k!='plan_digest'}
    if digest(unsigned)!=plan.get('plan_digest'):raise ValueError('PLAN_CHANGED')
    trace=child_context['construction_trace']
    if trace['proposal']!=plan['proposal']or trace['raw']!=raw or trace['model_hash']!=digest(child_packet['world_model']):raise ValueError('CHILD_SOURCE_PLAN_BINDING')
    if digest(raw)!=plan['raw_digest']or digest(parent['world_model'])!=plan['parent_model_digest']:raise ValueError('LINEAGE_PARENT_CHANGED')
    fid=plan['operator']['fixture_id']
    if digest(protected(child_packet,fid))!=plan['protected_digest']:raise ValueError('PROTECTED_OBJECT_CHANGED')
    mh=digest(child_packet['world_model']);origin=child_review.get('hierarchical_provenance129',{})
    if mh==plan['parent_model_digest']or child_review.get('model_hash')!=mh or origin.get('verified')is not True or origin.get('model_hash')!=mh or origin.get('source_revision')!=plan['source_revision']:raise ValueError('FRESH_CHILD_BINDING')
    return {'parent_model_digest':plan['parent_model_digest'],'child_model_digest':mh,'parent_review_digest':plan['parent_review_digest'],'child_review_digest':digest(child_review),'operator_digest':digest(plan['operator']),'raw_digest':plan['raw_digest'],'protected_unchanged':True,'accepted':False,'delivery_allowed':False}
