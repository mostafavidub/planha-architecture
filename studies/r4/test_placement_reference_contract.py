"""Synthetic detached fixtures only. Prepared NOT_RUN; no source-built model."""
import copy,unittest
from placement_reference_contract import check,digest
def fixture():
    m={"walls":{},"wall_hosts":{},"module_placements":[],"units":[]}
    for uid in ("A","B"):
        mod={"schema":"KITCHEN_MODULE117","walls":{"back":["0","0","1","1"]},"wall_hosts":{"host":["0","0","1","1"]},"unit":{"fixtures":{"sink":["0","0","1","1"]},"activities":{"sink_use":["0","0","1","1"]}}}
        ids={"back":uid+".back","host":uid+".host","sink":"sink","sink_use":"sink_use"}
        m["walls"][uid+".back"]=["0","0","1","1"];m["wall_hosts"][uid+".host"]=["0","0","1","1"]
        dm={"schema":"DINING_CAPACITY_MODULE118_PROPOSAL","fixtures":{"table":["0","0","1","1"],"chair_west":["0","0","1","1"]}}
        tr={"matrix":[[1,0],[0,1]],"translation":["0","0"]}
        u={"id":uid,"rooms":{"kitchen":[]},"fixtures":{"sink":["0","0","1","1"],"dining_table":["0","0","1","1"],"dining_chair_west":["0","0","1","1"]},"activities":{"sink_use":["0","0","1","1"]},"dining_module_placement":{"module":dm,"module_hash":digest(dm),"transform":copy.deepcopy(tr),"id_map":{"table":"dining_table","chair_west":"dining_chair_west"},"capacity_status":"NOT_EVALUATED_OCCUPIED_RISE_PENDING"}}
        m["units"].append(u)
        m["module_placements"].append({"module":mod,"module_hash":digest(mod),"transform":tr,"id_map":ids,"unit_id":uid,"room_id":"kitchen","geometry_scope":"synthetic reference-only fixture"})
    return m
class References(unittest.TestCase):
    def bad(self,mutator,code):
        m=fixture();mutator(m);r=check(m)
        self.assertFalse(r["reference_verified"]);self.assertTrue(any(code in x for x in r["errors"]),r)
    def test_same_local_ids_in_distinct_units_allowed(self):
        r=check(fixture());self.assertTrue(r["reference_verified"]);self.assertFalse(r["qualified"])
    def test_duplicate_unit(self):self.bad(lambda m:m["units"][1].update(id="A"),"UNIT_ID")
    def test_missing_field(self):self.bad(lambda m:m["module_placements"][0].pop("room_id"),"PLACEMENT_FIELDS")
    def test_bad_reference(self):self.bad(lambda m:m["module_placements"][0]["id_map"].update(sink="absent"),"DANGLING_REFERENCE")
    def test_cross_unit_global_wall_claim(self):self.bad(lambda m:m["module_placements"][1]["id_map"].update(back="A.back"),"MULTIPLE_SOURCE_OWNERS")
    def test_duplicate_instance(self):self.bad(lambda m:m["module_placements"].append(copy.deepcopy(m["module_placements"][0])),"DUPLICATE_PLACEMENT_INSTANCE")
    def test_boolean_matrix_is_not_integer(self):self.bad(lambda m:m["module_placements"][0]["transform"]["matrix"][0].__setitem__(0,True),"MATRIX_TYPE")
    def test_float_matrix_is_not_integer(self):self.bad(lambda m:m["module_placements"][0]["transform"]["matrix"][0].__setitem__(0,1.0),"MATRIX_TYPE")
    def test_singular_matrix(self):self.bad(lambda m:m["module_placements"][0]["transform"].update(matrix=[[1,0],[1,0]]),"NOT_SIGNED_PERMUTATION")
    def test_numeric_translation_rejected(self):self.bad(lambda m:m["module_placements"][0]["transform"]["translation"].__setitem__(0,0),"TRANSLATION_TYPE")
    def test_source_hash_type_mutation(self):self.bad(lambda m:m["module_placements"][0]["module"]["walls"]["back"].__setitem__(0,0),"MODULE_HASH")
    def test_dining_mapping_separate(self):self.bad(lambda m:m["units"][0]["dining_module_placement"]["id_map"].update(table="sink"),"DINING_SOURCE_MAPPING")
    def test_dining_status_no_capacity_approval(self):self.bad(lambda m:m["units"][0]["dining_module_placement"].update(capacity_status="PASS"),"DINING_CAPACITY_SCOPE")
    def test_extra_record_field(self):self.bad(lambda m:m["module_placements"][0].update(accepted=True),"PLACEMENT_FIELDS")
    def test_geometry_mutation_explicitly_not_covered(self):
        m=fixture();m["units"][0]["fixtures"]["sink"]=["99","99","100","100"]
        r=check(m);self.assertTrue(r["reference_verified"]);self.assertIn("GEOMETRIC_PLACEMENT_EQUALITY",r["not_checked"]);self.assertFalse(r["accepted"])
    def test_json_identity_not_python_equality(self):
        self.assertNotEqual(digest(1),digest(1.0));self.assertNotEqual(digest(False),digest(0))
if __name__=="__main__":unittest.main()
