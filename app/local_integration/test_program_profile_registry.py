import copy,json,unittest
from program_profile_registry import lookup,list_profiles,approved_profiles,_REGISTRY_JSON
class RegistryTests(unittest.TestCase):
    def test_approved_capacity_is_not_population(self):
        self.assertEqual([p['bedrooms_per_unit'] for p in approved_profiles()],[1,2])
        for p in approved_profiles():
            self.assertEqual(p['design_persons_per_unit'],p['bedrooms_per_unit']*2)
            self.assertIs(p['capacity_means_actual_population'],False)
    def test_exact_sleep_program(self):
        self.assertEqual(lookup('PROGRAM_1BED_V1')['sleep_roles'],['double'])
        self.assertEqual(lookup('PROGRAM_2BED_V1')['sleep_roles'],['double','twin'])
    def test_unapproved_three_never_fallback(self):
        p=lookup('PROGRAM_3BED_V1')
        self.assertEqual(p['approval']['status'],'UNAPPROVED_CAPACITY_PROFILE')
        self.assertFalse(p['search_policy']['approved_search_eligible'])
        self.assertIsNone(p['approval']['source'])
        self.assertEqual(p['execution_readiness']['status'],'BLOCKED_UNAPPROVED_PROFILE')
    def test_immutable_independent_lookup(self):
        p=lookup('PROGRAM_2BED_V1');p['sleep_roles'].append('fake')
        p['approval']['source']['section']='MUTATED'
        self.assertEqual(lookup('PROGRAM_2BED_V1')['sleep_roles'],['double','twin'])
        self.assertEqual(lookup('PROGRAM_2BED_V1')['approval']['source']['section'],'A9')
        a=list_profiles();a[0]['source_inventory']['living_items'].clear()
        self.assertEqual(len(list_profiles()[0]['source_inventory']['living_items']),4)
    def test_typed_ids(self):
        for x in (1,True,None,{},[],1.0):
            with self.assertRaisesRegex(ValueError,'PROGRAM_ID_STRING_REQUIRED'):lookup(x)
    def test_unknown_no_hidden_fallback(self):
        for x in ('PROGRAM_0BED_V1','PROGRAM_4BED_V1','program_1bed_v1',' PROGRAM_1BED_V1'):
            with self.assertRaisesRegex(ValueError,'UNKNOWN_PROGRAM_PROFILE_NO_FALLBACK'):lookup(x)
    def test_no_authority(self):
        for p in list_profiles():
            for k in ('accepted','qualified','display_allowed','delivery_allowed'):self.assertIs(p[k],False)
            self.assertFalse(p['execution_readiness']['public_execution_supported'])
            self.assertEqual(p['execution_readiness']['quality_status'],'PROFILE_NOT_READY')
            self.assertFalse(p['execution_readiness']['source_branch_existence_is_readiness'])
    def test_single_source_not_adapter_ready(self):
        p=lookup('PROGRAM_1BED_V1')
        self.assertTrue(p['execution_readiness']['constructible_source_branch_exists'])
        self.assertEqual(p['execution_readiness']['status'],'ONE_BED_ADAPTER_NOT_AUDITED')
        self.assertEqual(p['source_inventory']['dining_distinct_instances'],4)
        self.assertEqual(p['source_inventory']['excess_four_place_bundle_for_one_bedroom'],'SOURCE_PRESENT_NOT_AUTOMATICALLY_OPTIMAL')
    def test_actual_twin_names_and_sizes(self):
        p=lookup('PROGRAM_2BED_V1')['source_inventory']
        self.assertEqual([x['source_id'] for x in p['twin_fixtures']],['bed1.bedA','bed1.bedB'])
        self.assertEqual([x['size_m'] for x in p['twin_fixtures']],[['1.9','.9']]*2)
    def test_same_group_is_not_equal_item_counts(self):
        p=lookup('PROGRAM_1BED_V1')
        self.assertEqual(p['design_persons_per_unit'],2)
        self.assertEqual(p['source_inventory']['dining_distinct_instances'],4)
        self.assertIn('Counts of chairs and beds need not be equal',p['relation_semantics']['qualified_adequacy_for_same_design_group'])
        self.assertEqual(p['relation_semantics']['verification_status'],'NOT_VERIFIED')
    def test_bundle_and_missing_quality(self):
        for p in approved_profiles():
            self.assertEqual(set(p['required_bundle']),{'sleep','living_seating','dining','clothes_storage','activities','access'})
            self.assertIn('CALIBRATED_ROOM_AND_UNIT_QUALITY_FLOORS',p['execution_readiness']['missing'])
            self.assertFalse(p['search_policy']['automatic_fallback'])
            self.assertFalse(p['search_policy']['budget_is_infeasibility'])
            self.assertFalse(p['search_policy']['maximize_bedrooms'])
if __name__=='__main__':unittest.main()
