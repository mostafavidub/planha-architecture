"""Draft R4-2.09 placement reference contract. NOT_RUN; not an origin/geometry gate.
Source-module hashes only bind supplied content, not its authenticity.
Dining is a separate per-unit placement, not a module_placements entry.
"""
import hashlib,json,math
from fractions import Fraction
SCHEMA="R4_PLACEMENT_REFERENCES_DRAFT_V1"
SUPPORTED={"PRIVATE_ROOM_MODULE116","PRIVATE_TWIN_ROOM_MODULE118","BATHROOM_MODULE117","KITCHEN_MODULE117"}
FIELDS={"module","module_hash","transform","id_map","unit_id","room_id","geometry_scope"}
DINING_FIELDS={"module","module_hash","transform","id_map","capacity_status"}
def require(ok,code):
    if not ok: raise ValueError(code)
def strict(v):
    if type(v) is dict:
        require(all(type(k) is str for k in v),"JSON_KEY")
        for x in v.values(): strict(x)
    elif type(v) is list:
        for x in v: strict(x)
    else: require(type(v) in (str,int,float,bool,type(None)) and (type(v) is not float or math.isfinite(v)),"JSON_TYPE")
def digest(v):
    strict(v)
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def transform(t):
    require(type(t) is dict and set(t)=={"matrix","translation"},"TRANSFORM_FIELDS")
    a=t["matrix"]
    require(type(a) is list and len(a)==2 and all(type(r) is list and len(r)==2 and all(type(x) is int and x in (-1,0,1) for x in r) for r in a),"MATRIX_TYPE")
    require(all(sum(a[k][i]*a[k][j] for k in range(2))==int(i==j) for i in range(2) for j in range(2)),"NOT_SIGNED_PERMUTATION")
    require(type(t["translation"]) is list and len(t["translation"])==2 and all(type(x) is str for x in t["translation"]),"TRANSLATION_TYPE")
    for x in t["translation"]: Fraction(x)
def check(model):
    out={"schema":SCHEMA,"reference_verified":False,"accepted":False,"qualified":False,"display_allowed":False,"delivery_allowed":False,"errors":[],"scope":"Supplied-record structure, hash, D4 type and typed ID-reference cardinality only; no source authenticity or geometric equality."}
    try:
        before=digest(model)
        units=model["units"]
        require(type(units) is list,"UNITS_TYPE")
        by={}
        for u in units:
            require(type(u["id"]) is str and u["id"] in ("A","B") and u["id"] not in by,"UNIT_ID")
            by[u["id"]]=u
        require(set(by)=={"A","B"},"UNIT_INVENTORY")
        require(type(model["module_placements"]) is list,"PLACEMENT_LIST")
        require(bool(model["module_placements"]),"EMPTY_MODULE_PLACEMENT_INVENTORY")
        instances=set();claimed=set();unvalidated=[]
        def bind(mapping,source,target,namespace,uid,instance):
            require(type(source) is dict and type(target) is dict,"REFERENCE_DICTIONARY")
            seen=set()
            for sid in source:
                require(sid in mapping and type(mapping[sid]) is str,"MISSING_TYPED_REFERENCE")
                tid=mapping[sid]
                require(tid in target,"DANGLING_REFERENCE")
                require(tid not in seen,"NONINJECTIVE_REFERENCE")
                seen.add(tid)
                # Global walls and per-unit objects are distinct namespaces.
                key=(namespace,uid if namespace in ("fixtures","activities") else None,tid)
                require(key not in claimed,"MULTIPLE_SOURCE_OWNERS")
                claimed.add(key)
        for p in model["module_placements"]:
            require(type(p) is dict and set(p)==FIELDS,"PLACEMENT_FIELDS")
            uid=p["unit_id"];room=p["room_id"]
            require(type(uid) is str and uid in by and type(room) is str,"PLACEMENT_ID")
            require((uid,room) not in instances,"DUPLICATE_PLACEMENT_INSTANCE")
            instances.add((uid,room))
            require(room in by[uid]["rooms"],"ROOM_REFERENCE")
            require(type(p["geometry_scope"]) is str and bool(p["geometry_scope"]),"GEOMETRY_SCOPE")
            mod=p["module"]
            require(type(mod) is dict and mod.get("schema") in SUPPORTED,"MODULE_SCHEMA")
            require(type(p["module_hash"]) is str and p["module_hash"]==digest(mod),"MODULE_HASH")
            transform(p["transform"])
            ids=p["id_map"];require(type(ids) is dict and all(type(k) is str and type(v) is str for k,v in ids.items()),"ID_MAP_TYPE")
            for kind in ("walls","wall_hosts"):
                bind(ids,mod[kind],model[kind],kind,uid,room)
            for kind in ("fixtures","activities"):
                bind(ids,mod["unit"][kind],by[uid][kind],kind,uid,room)
            checked=set(mod["walls"])|set(mod["wall_hosts"])|set(mod["unit"]["fixtures"])|set(mod["unit"]["activities"])
            unvalidated.append({"unit":uid,"room":room,"unvalidated_id_map_keys":sorted(set(ids)-checked)})
        dining_count=0
        for uid,u in by.items():
            p=u["dining_module_placement"]
            require(type(p) is dict and set(p)==DINING_FIELDS,"DINING_PLACEMENT_FIELDS")
            mod=p["module"]
            require(type(mod) is dict and mod.get("schema")=="DINING_CAPACITY_MODULE118_PROPOSAL","DINING_SCHEMA")
            require(type(p["module_hash"]) is str and p["module_hash"]==digest(mod),"DINING_HASH")
            transform(p["transform"])
            ids=p["id_map"];require(type(ids) is dict and all(type(k) is str and type(v) is str for k,v in ids.items()),"DINING_MAP_TYPE")
            expected={k:("dining_table" if k=="table" else "dining_"+k) for k in mod["fixtures"]}
            require(digest(ids)==digest(expected),"DINING_SOURCE_MAPPING")
            bind(ids,mod["fixtures"],u["fixtures"],"fixtures",uid,"dining")
            require(p["capacity_status"]=="NOT_EVALUATED_OCCUPIED_RISE_PENDING","DINING_CAPACITY_SCOPE")
            # Activities are generated separately by assemble114, NOT dining id_map.
            dining_count+=1
        require(digest(model)==before,"INPUT_MUTATION")
        out.update(reference_verified=True,module_instances=len(instances),dining_instances=dining_count,counts_scope="PRESENT_RECORDS_ONLY_NOT_COMPLETENESS",unvalidated_id_map_keys=unvalidated)
    except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError,RecursionError,UnicodeError) as e:
        out["errors"].append(type(e).__name__+":"+str(e))
    out["not_checked"]=["MODULE_INVENTORY_COMPLETENESS","EMBEDDED_MODULE_CONTENT_COMPLETENESS","UNVALIDATED_EXTRA_ID_MAP_REFERENCES","SOURCE_AUTHENTICITY","GEOMETRIC_PLACEMENT_EQUALITY","OPENING_PORT_ROLE_REFERENCES","OPERATIONS_STATES","DINING_ACTIVITY_BINDING","MATERIAL_ALIAS_UNION","WHOLE_SCHEMA","PHYSICAL_OR_CURRENT_CRITERIA"]
    return out
