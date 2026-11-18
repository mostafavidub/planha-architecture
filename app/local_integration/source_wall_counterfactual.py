"""Source-bound wall removal probes only; never a constructed/admitted model."""
import copy
from fractions import Fraction as F
from review_cycle import digest

def bound_source(model,source_id):
    if source_id not in model['walls']:raise ValueError('SOURCE_WALL_ID_REQUIRED_NOT_PHYSICAL_ALIAS')
    matches=[]
    for placement in model['module_placements']:
        module=placement['module']
        ids=[placement['id_map'][k] for k in module['walls']]
        if len(set(ids))!=len(ids):raise ValueError('SOURCE_WALL_MAP_NOT_INJECTIVE')
        if digest(module)!=placement['module_hash']:raise ValueError('SOURCE_MODULE_DIGEST')
        for local_id,q in module['walls'].items():
            if placement['id_map'][local_id]!=source_id:continue
            mat=[[F(str(v)) for v in row] for row in placement['transform']['matrix']];t=list(map(F,placement['transform']['translation']))
            if len(mat)!=2 or any(len(row)!=2 for row in mat) or any(sum(abs(v) for v in row)!=1 for row in mat) or any(sum(abs(mat[i][j]) for i in range(2))!=1 for j in range(2)):raise ValueError('SOURCE_RIGID_TRANSFORM')
            a,b,c,d=map(F,q);pts=[(mat[0][0]*x+mat[0][1]*y+t[0],mat[1][0]*x+mat[1][1]*y+t[1]) for x in (a,c) for y in (b,d)]
            actual=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)]
            if actual!=list(map(F,model['walls'][source_id])):raise ValueError('SOURCE_WALL_GEOMETRY_BINDING')
            matches.append({'unit_id':placement['unit_id'],'room_id':placement['room_id'],'module_hash':placement['module_hash'],'module_schema':module['schema'],'local_source_id':local_id,'transform':placement['transform']})
    if len(matches)!=1:raise ValueError('UNIQUE_SOURCE_MODULE_WALL_REQUIRED')
    return matches[0]

def assess(model,physical_review,source_id,expected_model_digest):
    mh=digest(model)
    if mh!=expected_model_digest:raise ValueError('EXPECTED_PARENT_HASH')
    if physical_review.get('model_hash')!=mh or physical_review.get('status')!='PASS_CONCEPT_SCOPED_REVIEW' or physical_review.get('errors')!=[] or physical_review.get('pending')!=[]:raise ValueError('FRESH_PHYSICAL_PASS_REQUIRED')
    origin=physical_review.get('multiproposal_provenance127',{})
    if origin.get('verified')is not True or origin.get('model_hash')!=mh or origin.get('errors')!=[] or origin.get('pending')!=[]:raise ValueError('SOURCE_VERIFIED_PARENT_REQUIRED')
    binding=bound_source(model,source_id)
    if model['physical_wall_network']['source_wall_hash']!=digest(model['walls']):raise ValueError('BASE_WALL_NETWORK_BINDING')
    from geometry114 import cells,Q,area
    from privacy115 import closure_gaps
    from checker114 import check_whole_privacy117
    from guest_four_route_diagnostic import assess as guest_routes
    before=list(model['walls'].values());after=[q for k,q in model['walls'].items() if k!=source_id]
    removed=cells(before,after);released=sum((area(Q(q)) for q in removed),F(0))
    probe=copy.deepcopy(model);del probe['walls'][source_id]
    oldunion=list(map(Q,cells(before,[])));newunion=list(map(Q,cells(after,[])))
    closure=[]
    for u in model['units']:
        for name,regions in u['rooms'].items():
            if not name.startswith('bed'):continue
            role=u['id']+'.'+name
            openings=[Q(o['rect']) for o in model['openings'] if role in o.get('connects',[])]
            b=closure_gaps(list(map(Q,regions)),oldunion,openings);a=closure_gaps(list(map(Q,regions)),newunion,openings)
            closure.append({'room':u['id']+'.'+name,'before_gaps':b,'after_gaps':a})
    base_routes=guest_routes(model);probe_routes=guest_routes(probe)
    privacy_before=check_whole_privacy117(model);privacy_after=check_whole_privacy117(probe)
    assert digest(model)==mh
    assert digest(probe['units'])==digest(model['units']) and digest(probe['operations'])==digest(model['operations'])
    return {'schema':'V25_SOURCE_WALL_PROBE_V1','scope':'COUNTERFACTUAL_DIAGNOSTIC_ONLY_NOT_CONSTRUCTED_MODEL','base_model_digest':mh,'fresh_physical_review_digest':digest(physical_review),'source_id':source_id,'source_rect':model['walls'][source_id],'source_binding':binding,'physical_aliases':model['physical_wall_network']['source_aliases'][source_id],'removed_material_cells':removed,'free_geometric_gain_m2':str(released),'material_union_unchanged':not cells(before,after) and not cells(after,before),'useful_area_gain':'NOT_PROVEN','closure_metric':'Coarse boundary edge coverage only; unchanged edge list does not prove unchanged missing interval or all function','closure':closure,'baseline_routes':base_routes,'probe_routes':probe_routes,'privacy_before':privacy_before,'privacy_after':privacy_after,'state':'UNKNOWN_NONFUNCTIONAL_WALL_EXCLUSION','accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'remaining':['A source role and removal consequence do not prove optimal placement or absence of an alternative','Room/operation inventories fixed; no layout benefit or useful area assumed','Probe never fed into full historical provenance checker or returned as a constructed model']}
