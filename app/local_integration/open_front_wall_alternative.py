"""Same-program source-built kitchen wall alternative, not all-wall approval."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import inspect
from contract114 import digest
from open_front_kitchen_study import ROOT

EXPECTED_ROUTES={'entry_living','entry_dining','entry_WC','living_dining'}
def route_map(study):
    if study.get('missing'):raise ValueError('GUEST_STUDY_INCOMPLETE')
    units=study.get('units',[])
    if len(units)!=2 or {u['unit']for u in units}!={'A','B'}:raise ValueError('GUEST_UNIT_INVENTORY')
    out={}
    for u in units:
        routes=u['routes']
        if len(routes)!=4 or {r['id']for r in routes}!=EXPECTED_ROUTES:raise ValueError('FOUR_ROUTE_INVENTORY')
        for r in routes:out[(u['unit'],r['id'])]=r
    return out

def compare_routes(before,after):
    from living_connectivity_diagnostic import direction_changes
    if digest(before['source_profile'])!=digest(after['source_profile']):raise ValueError('COMPARISON_PROFILE_CHANGED')
    a,b=route_map(before),route_map(after);rows=[]
    if set(a)!=set(b):raise ValueError('COMPARISON_ROUTE_INVENTORY')
    for key in sorted(a):
        old,new=a[key],b[key]
        if digest([old['start'],old['end'],old['body_m']])!=digest([new['start'],new['end'],new['body_m']]):raise ValueError('COMPARISON_ENDPOINT_OR_BODY_CHANGED')
        row={'unit':key[0],'route':key[1],'start':old['start'],'end':old['end'],'body_m':old['body_m'],
             'before_state':old['state'],'after_state':new['state'],'both_have_width_witness':bool(old['path'])and bool(new['path'])}
        if row['both_have_width_witness']:
            row.update(before_length_m=old['length_m'],after_length_m=new['length_m'],
                length_delta_m=str(F(new['length_m'])-F(old['length_m'])),
                before_turns=direction_changes(old['path']),after_turns=direction_changes(new['path']))
        rows.append(row)
    return rows

def compare_living(before,after):
    rows=[]
    for study in (before,after):
        if study.get('missing') or len(study.get('units',[]))!=2 or {u['unit']for u in study['units']}!={'A','B'}:
            raise ValueError('LIVING_COMPARISON_INCOMPLETE')
    au={u['unit']:u for u in before['units']};bu={u['unit']:u for u in after['units']}
    labels={'DECLARED_RESIDUAL_LIVING','CONCEPTUAL_PUBLIC_UNION_PROBE'}
    for uid in sorted(au):
        a={s['label']:s for s in au[uid]['studies']};b={s['label']:s for s in bu[uid]['studies']}
        if len(au[uid]['studies'])!=2 or len(bu[uid]['studies'])!=2 or set(a)!=labels or set(b)!=labels:raise ValueError('LIVING_SCOPE_INVENTORY')
        for label in sorted(labels):
            x,y=a[label],b[label]
            for key in ('anchor_fixture_id','target_fixture_ids','seat_endpoints'):
                if digest(x[key])!=digest(y[key]):raise ValueError('LIVING_TARGET_BINDING')
            if not x['target_fixture_ids']:raise ValueError('EMPTY_LIVING_TARGETS')
            xp={(p['from_fixture'],p['to_fixture']):p for p in x['paths']}
            yp={(p['from_fixture'],p['to_fixture']):p for p in y['paths']}
            if len(xp)!=len(x['paths']) or len(yp)!=len(y['paths']) or set(xp)!=set(yp):raise ValueError('LIVING_PATH_INVENTORY')
            paths=[]
            for key in sorted(xp):
                o,n=xp[key],yp[key];row={'from_fixture':key[0],'to_fixture':key[1],'before_state':o['state'],'after_state':n['state']}
                if o['path']and n['path']:
                    if o['width_m']!=n['width_m']:raise ValueError('LIVING_BODY_PROFILE_CHANGED')
                    row.update(length_delta_m=str(F(n['length_m'])-F(o['length_m'])),before_turns=o['turns'],after_turns=n['turns'])
                paths.append(row)
            rows.append({'unit':uid,'scope':label,'before_state':x['state'],'after_state':y['state'],
                'before_floor_area_m2':x['floor_area_m2'],'after_floor_area_m2':y['floor_area_m2'],
                'area_not_proven_useful':True,'paths':paths})
    return rows

def assess(packet,trace,baseline_packet,baseline_context):
    from open_front_evaluator import assess as evaluate
    from guest_four_route_diagnostic import assess as guests
    from living_connectivity_diagnostic import assess as living
    from producer_provenance import snapshot,require_unchanged
    for fn,filename in [(evaluate,'open_front_evaluator.py'),(guests,'guest_four_route_diagnostic.py'),(living,'living_connectivity_diagnostic.py')]:
        if Path(inspect.getsourcefile(fn)).resolve()!=Path(__file__).with_name(filename).resolve():raise ValueError('WALL_ALTERNATIVE_CALLABLE_PATH')
    sources=snapshot(ROOT,['app/local_integration/open_front_wall_alternative.py'])
    bundle=digest([packet,trace,baseline_packet,baseline_context])
    review=evaluate(packet,trace,baseline_packet,baseline_context)
    if review['errors'] or review['status']!='UNKNOWN_REQUIRED_STUDY':raise ValueError('ALTERNATIVE_FRESH_STUDY_ERRORS')
    old,new=baseline_packet['world_model'],packet['world_model']
    removed=set(old['walls'])-set(new['walls']);added=set(new['walls'])-set(old['walls'])
    if removed!={'A.kitchen.front.right','B.kitchen.front.right'} or added:raise ValueError('ALTERNATIVE_WALL_DELTA')
    if any(digest(old['walls'][k])!=digest(new['walls'][k])for k in set(old['walls'])&set(new['walls'])):raise ValueError('OTHER_WALL_CHANGED')
    for key in ('inputs','program','profile'):
        if digest(old[key])!=digest(new[key]):raise ValueError('ALTERNATIVE_PROGRAM_PROFILE_CHANGED')
    if len(old['units'])!=len(new['units']):raise ValueError('ALTERNATIVE_UNITS_CHANGED')
    for a,b in zip(old['units'],new['units']):
        for key in ('id','fixtures','fixture_metadata','activities'):
            if digest(a[key])!=digest(b[key]):raise ValueError('ALTERNATIVE_ACTUAL_INVENTORY_CHANGED:'+key)
    before_guests=guests(deepcopy(old));after_guests=review['current_functional']['guest_four_route_study']
    before_living=living(deepcopy(old));after_living=review['current_functional']['living_connectivity_study']
    if before_guests['model_digest']!=digest(old)or before_living['model_digest']!=digest(old):raise ValueError('BASELINE_DIAGNOSTIC_BINDING')
    if after_guests['model_digest']!=digest(new)or after_living['model_digest']!=digest(new):raise ValueError('ALTERNATIVE_DIAGNOSTIC_BINDING')
    for study in (before_living,after_living):
        if study.get('missing') or len(study.get('units',[]))!=2 or {u['unit']for u in study['units']}!={'A','B'}:
            raise ValueError('LIVING_COMPARISON_INCOMPLETE')
    comparison=compare_routes(before_guests,after_guests)
    living_comparison=compare_living(before_living,after_living)
    if digest([packet,trace,baseline_packet,baseline_context])!=bundle:raise ValueError('WALL_ALTERNATIVE_INPUT_MUTATED')
    require_unchanged(ROOT,review['source_snapshot'])
    require_unchanged(ROOT,sources)
    return {'schema':'OPEN_FRONT_SAME_PROGRAM_WALL_ALTERNATIVE_STUDY_V1',
      'baseline_model_digest':digest(old),'model_digest':digest(new),
      'removed_source_wall_ids':sorted(removed),'remaining_source_wall_count':len(new['walls']),
      'source_snapshot':sources,'fresh_evaluator':review,
      'released_physical_material_m2':review['boundary_comparison']['released_physical_material_m2'],
      'route_comparisons':comparison,'living_comparisons':living_comparison,'before_guest_study':before_guests,'after_guest_study':after_guests,
      'before_living_connectivity':before_living,'after_living_connectivity':after_living,
      'status':'COMPARISON_EXECUTED_CURRENT_WALL_RULE_UNKNOWN',
      'NONFUNCTIONAL_WALL_EXCLUSION':'UNKNOWN','whole_physical_verified':False,
      'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,
      'remaining':['Only two specified kitchen source-wall pieces compared, not every remaining wall',
        'A width-witness on fixed source profile is not ergonomic or principal organization approval',
        'Physical material released is not useful area; unchanged or shorter route is not necessity proof',
        'Cohesive furnishing, current programme suitability and full current Q11 remain unresolved'],
      'scope':'Real independently source-built alternative with exact inventory and fresh checks; no detached wall deletion, old-schema masquerade, global optimality or delivery.'}
