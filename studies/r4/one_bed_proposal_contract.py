"""Draft one-bedroom proposal syntax contract only. Never a feasibility/admission gate.
Input is already-normalized builtin JSON, NOT raw numpy-bearing solver output.
Caller must separately verify lossless role-limited transport, sources and origin.
"""
import json,hashlib,math
KEYS=set(["organization_profile","organization_topology","objective_profile","capacity_profile","sleep_roles","status","solver_status","solver_message","solver_seconds","budget_seconds","bedrooms","variant","variables","binary_separation_variables","constraints","no_global_infeasibility_claim","rectangles","roles","network_paths","bed_door_sides","private_module_contract","network_scope"])
ROLES={"bed1":"private_room","bath":"service","kitchen":"open_room","dining":"open_room","sofa1_use":"furniture_use","sofa2_use":"furniture_use","chair1_use":"furniture_use","chair2_use":"furniture_use","entry_apron":"reserved_entry"}
TERMINALS=(set(ROLES)-{"dining","entry_apron"})|{"dining_west","dining_east","dining_front","dining_back"}
def need(v,code):
    if not v:raise ValueError(code)
def strict(v):
    if type(v)is dict:
        need(all(type(k)is str for k in v),"JSON_KEYS")
        for x in v.values():strict(x)
    elif type(v)is list:
        for x in v:strict(x)
    else:need(type(v)in(str,int,float,bool,type(None)) and(type(v)is not float or math.isfinite(v)),"JSON_TYPE")
def digest(v):
    strict(v);return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
def number(v):return type(v)in(int,float) and math.isfinite(v)
def check(p):
    r={"schema":"R4_ONE_BED_PROPOSAL_SHAPE_DRAFT_V1","proposal_shape_verified":False,"origin_verified":False,"physical_verified":False,"accepted":False,"qualified":False,"display_allowed":False,"delivery_allowed":False,"errors":[]}
    try:
        before=digest(p);need(type(p)is dict and set(p)==KEYS,"PROPOSAL_FIELDS")
        expected={"bedrooms":1,"sleep_roles":["double"],"capacity_profile":"LEGACY_SOURCE_PROGRAM","status":"PROPOSAL_ONLY","organization_profile":"UNRESTRICTED","organization_topology":"SIDE_ROOTED_SERVICES","variant":0,"no_global_infeasibility_claim":True}
        for k,v in expected.items():need(digest(p[k])==digest(v),"PROGRAM_SCOPE:"+k)
        for k in ("solver_status","variables","binary_separation_variables","constraints"):need(type(p[k])is int,"INTEGER:"+k)
        for k in ("solver_seconds","budget_seconds"):need(number(p[k]) and p[k]>=0,"TIME:"+k)
        for k in ("objective_profile","solver_message","private_module_contract","network_scope"):need(type(p[k])is str,"TEXT:"+k)
        need(digest(p["roles"])==digest(ROLES),"SOURCE_ROLES")
        need(type(p["rectangles"])is dict and set(p["rectangles"])==set(ROLES),"RECTANGLE_INVENTORY")
        for q in p["rectangles"].values():
            need(type(q)is list and len(q)==4 and all(number(v)for v in q),"RECTANGLE_TYPE")
            need(q[0]<q[2] and q[1]<q[3],"RECTANGLE_EXTENT")
        need(type(p["bed_door_sides"])is dict and set(p["bed_door_sides"])=={"bed1"} and type(p["bed_door_sides"]["bed1"])is str and p["bed_door_sides"]["bed1"]in("left","right"),"DOOR_SIDE")
        need(type(p["network_paths"])is dict and set(p["network_paths"])==TERMINALS,"TERMINAL_INVENTORY")
        for path in p["network_paths"].values():
            need(type(path)is list and len(path)==5,"PATH_LENGTH")
            for point in path:need(type(point)is list and len(point)==2 and all(number(v)for v in point),"PATH_POINT")
        need(digest(p)==before,"INPUT_MUTATION")
        r.update(proposal_shape_verified=True,proposal_digest=before,rectangle_count=len(ROLES),terminal_count=len(TERMINALS),design_persons_reference=2,unit_count_reference=2)
    except(ValueError,TypeError,KeyError,IndexError,OverflowError,RecursionError)as e:r["errors"].append(type(e).__name__+":"+str(e))
    r["not_checked"]=["SOLVER_STATUS_COUNT_SEMANTICS_NOT_CHECKED","SOURCE_MARKER_SEMANTICS_NOT_CHECKED","ROLE_LIMITED_NUMERIC_TRANSPORT_NOT_PERFORMED","SOURCE_PIN_RUNTIME_VERIFICATION","SOLVER_ORIGIN","RECTANGLE_CLEARANCE_OR_CONSTRAINTS","SOURCE_MODULE_INSTANCE_GEOMETRY","WHOLE_MODEL_AND_CURRENT_CRITERIA","AUTOMATIC_SELECTION_OR_FALLBACK","QUALITY_AND_ERGONOMICS"]
    return r
