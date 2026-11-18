"""New engineering comparator358, NOT recovered PARETO_CIRC or live authority.
Caller must supply independently bound exact per-unit/scenario metric readsets.
This pure helper cannot establish eligibility, scope closure, or acceptance.
"""
from fractions import Fraction
DIRECTIONS={'exclusive_circulation_area_m2':'min','path_length_m':'min','turn_count':'min','bottleneck_count':'min','functional_capacity':'max','useful_area_m2':'max','ownership_area_m2':'max'}
def compare(baseline,alternative,required):
    out={'schema':'ENGINEERING358_COMPONENTWISE_COMPARISON','canonical_PARETO_CIRC':False,'rule_acceptance':False,'global_optimum':False}
    # required keyed by exact unit/scenario/target/metric, no averaging allowed.
    if not required or set(baseline)!=set(required) or set(alternative)!=set(required):
        return dict(out,state='UNKNOWN',reason='METRIC_INVENTORY_NOT_EXACT')
    better=[];worse=[];equal=[]
    for key,definition in required.items():
        metric=definition.get('metric'); direction=DIRECTIONS.get(metric)
        if direction is None or not definition.get('source_pointer') or not definition.get('unit') or not definition.get('scenario') or definition.get('role') not in ('objective','protected'):
            return dict(out,state='UNKNOWN',reason='METRIC_DEFINITION_OR_PROVENANCE_MISSING',key=key)
        pair=[]
        for rows in (baseline,alternative):
            row=rows[key]
            if type(row) is not dict or row.get('value') is None or not row.get('readset_digest') or row.get('definition')!=definition:
                return dict(out,state='UNKNOWN',reason='MISSING_OR_UNMATCHED_METRIC',key=key)
            v=row['value']
            if type(v)not in(str,int): return dict(out,state='UNKNOWN',reason='EXACT_VALUE_REQUIRED',key=key)
            try: v=Fraction(v)
            except (ValueError,ZeroDivisionError):return dict(out,state='UNKNOWN',reason='INVALID_RATIONAL',key=key)
            if v<0:return dict(out,state='UNKNOWN',reason='NEGATIVE_PHYSICAL_METRIC',key=key)
            pair.append(v)
        a,b=pair
        (equal if a==b else better if ((b<a) if direction=='min' else (b>a)) else worse).append(key)
    return dict(out,state='MEASURED_VECTOR_ONLY',strictly_dominates=any(required[k]['role']=='objective' for k in better) and not worse,improved=better,degraded=worse,equal=equal,eligibility='NOT_ESTABLISHED_BY_THIS_HELPER')

def partial_dominance(baseline,alternative,required):
    """Strong-Kleene conjunction: one proved deterioration refutes dominance.
    Unknown data never becomes acceptance. All fully comparable dimensions must
    be present before TRUE; FALSE needs only one valid objective counterexample.
    """
    unknown=[];better=[];worse=[]
    for key,definition in required.items():
        one=compare({key:baseline[key]} if key in baseline else {},{key:alternative[key]} if key in alternative else {},{key:definition})
        if one['state']=='UNKNOWN': unknown.append({'key':key,'reason':one['reason']});continue
        better.extend(one['improved']);worse.extend(one['degraded'])
    objective_worse=[k for k in worse if required[k]['role']=='objective']
    # A worsening protected constraint also refutes dominance when measured.
    value='FALSE' if worse else 'UNKNOWN' if unknown or not required else 'TRUE' if any(required[k]['role']=='objective'for k in better)else 'FALSE'
    return {'dominance':value,'worsened_objectives':objective_worse,'worsened_dimensions':worse,'improved_dimensions':better,'unknown_dimensions':unknown,'rule_acceptance':False,'scope':'PARTIAL_ORDER_LOGIC_ONLY_NOT_COMPONENT_PURPOSE_OR_FINITE_COVERAGE'}
