# Step 4A test execution

47 test methods; 0 failures; 0 errors.

Local identifier/dictionary only. No application, history, concurrency, approval, recovery or production validation.

Fresh run: `python3 run_tests.py`. Full inputs and expected versus actual codes: `test-results.json`.

| Test | Result |
|---|---|
| test_all_legacy_rows_have_disposition | pass |
| test_construction_and_feedstock | pass |
| test_dictionary_rule_changes_rejected | pass |
| test_json_duplicate_cli_fails | pass |
| test_no_silent_empty_or_extra_input | pass |
| test_numeric_unknown_standards_fail_explicitly | pass |
| test_percentage_tolerance_bounds | pass |
| test_repeated_scope_intervals | pass |
| test_retained_core_vocabulary_execution | pass |
| test_scope_complementary_facts | pass |
| test_W01_independent_diameters | pass |
| test_W02_W03_printing_context_separate | pass |
| test_W04_scopes_and_layers | pass |
| test_W05_clarification_descriptions_differ | pass |
| test_W06_additive_dictionary_and_old_meanings | pass |
| test_W07_separate_components | pass |
| test_W08_unresolved_ounces | pass |
| test_canonical_and_complete_extensions | pass |
| test_consistency_and_applicability | pass |
| test_dictionary_only_subprocess | pass |
| test_dimensions_and_targets | pass |
| test_exact_numbers | pass |
| test_exact_units_and_thickness | pass |
| test_intervals_fraction_count | pass |
| test_layer_repeats_reverse | pass |
| test_lid_function_without_saleability | pass |
| test_malformed_unsupported_duplicates | pass |
| test_measurement_comparison | pass |
| test_multiple_features | pass |
| test_nested_no_inheritance_and_merge | pass |
| test_resource_refusal | pass |
| test_retired_entry_still_decodes | pass |
| test_tolerance_qualification | pass |
| test_unknown_na_other | pass |
| test_unresolved_units_fail | pass |
| test_utf8_structural_escaping | pass |
| test_workbook_expected_codes | pass |
| test_workbook_mapping_independent | pass |
| test_new_reference_only_role_cannot_disable_existing_code | pass |
| test_numeric_minimum_and_new_bound_are_incompatible | pass |
| test_other_field_semantic_properties_are_preserved | pass |
| test_raw_scope_container_types_rejected_before_merge | pass |
| test_repeated_scope_unsupported_child_rejected_both_orders | pass |
| test_restrictive_numeric_maximum_is_incompatible | pass |
| test_standalone_unsupported_child_rejected | pass |
| test_supported_field_additions_and_retirement_remain_compatible | pass |
| test_valid_scope_merge_still_allowed_both_orders | pass |

## Independent code answers

| Test | Expected | Actual |
|---|---|
| test_W01_independent_diameters | `A1!APTX.CUB.XXX.M500.R98` | `A1!APTX.CUB.XXX.M500.R98` |
| test_W01_independent_diameters | `A1!APTX.CUB.XXX.M500.R98_125` | `A1!APTX.CUB.XXX.M500.R98_125` |
| test_W02_W03_printing_context_separate | `A1!APPX.CUB.XXX.M500.X` | `A1!APPX.CUB.XXX.M500.X` |
| test_W04_scopes_and_layers | `A1!BKRX.BGX.XXT.X.X~S(INSIDE){CL:BROWN.MA:BKRX}` | `A1!BKRX.BGX.XXT.X.X~S(INSIDE){CL:BROWN.MA:BKRX}` |
| test_W04_scopes_and_layers | `A1!BKRX.BGX.XXT.X.X~S(INSIDE){CL:WHITE.MA:BKRX}` | `A1!BKRX.BGX.XXT.X.X~S(INSIDE){CL:WHITE.MA:BKRX}` |
| test_W04_scopes_and_layers | `A1!BKRX.BGX.XLX.X.X~L(O){MA:BKRX;MA:APTX}` | `A1!BKRX.BGX.XLX.X.X~L(O){MA:BKRX;MA:APTX}` |
| test_W04_scopes_and_layers | `A1!BKRX.BGX.XLX.X.X~L(X){MA:APTX;MA:BKRX}` | `A1!BKRX.BGX.XLX.X.X~L(X){MA:APTX;MA:BKRX}` |
| test_W05_clarification_descriptions_differ | `A1!BKWX.CUB.XXX.M500.X` | `A1!BKWX.CUB.XXX.M500.X` |
| test_W05_clarification_descriptions_differ | `A1!BKWP.CUB.XXX.M500.X` | `A1!BKWP.CUB.XXX.M500.X` |
| test_W07_separate_components | `A1!ACPX.CYX.XXS.X.X` | `A1!ACPX.CYX.XXS.X.X` |
| test_W07_separate_components | `A1!ACPX.CYX.XXF.X.X` | `A1!ACPX.CYX.XXF.X.X` |
| test_W07_separate_components | `A1!ACPX.CYX.XXN.X.X` | `A1!ACPX.CYX.XXN.X.X` |
| test_W07_separate_components | `A1!BTSX.NPX.XXX.X.X` | `A1!BTSX.NPX.XXX.X.X` |
| test_W08_unresolved_ounces | `A1!XXXX.CUX.XXX.X.X+UT:CA=16%20oz` | `A1!XXXX.CUX.XXX.X.X+UT:CA=16%20oz` |
| test_dimensions_and_targets | `A1!XXXX.BGX.XXX.X.X+DM:HEIGHT=50_8,WIDTH=20.TO:[DM_HEIGHT,1,2]` | `A1!XXXX.BGX.XXX.X.X+DM:HEIGHT=50_8,WIDTH=20.TO:[DM_HEIGHT,1,2]` |
| test_exact_units_and_thickness | `A1!APTX.XXX.XXX.X.R76_2+GW:10.TH:0_03` | `A1!APTX.XXX.XXX.X.R76_2+GW:10.TH:0_03` |
| test_exact_units_and_thickness | `A1!XXXX.CUX.XXX.M29_5735295625.X` | `A1!XXXX.CUX.XXX.M29_5735295625.X` |
| test_exact_units_and_thickness | `A1!XXXX.CUX.XXX.M28_4130625.X` | `A1!XXXX.CUX.XXX.M28_4130625.X` |
| test_exact_units_and_thickness | `A1!XXXX.BGX.XXX.G1000.X` | `A1!XXXX.BGX.XXX.G1000.X` |
| test_intervals_fraction_count | `A1!XXXX.CUX.XXX.M1/3.R98-99` | `A1!XXXX.CUX.XXX.M1/3.R98-99` |
| test_intervals_fraction_count | `A1!XXXX.BGX.XXX.N2.X` | `A1!XXXX.BGX.XXX.N2.X` |
| test_layer_repeats_reverse | `A1!BKRX.BGX.XXX.X.X~L(X){MA:APEX;MA:APEX;MA:BKRX}` | `A1!BKRX.BGX.XXX.X.X~L(X){MA:APEX;MA:APEX;MA:BKRX}` |
| test_layer_repeats_reverse | `A1!BKRX.BGX.XXX.X.X~L(O){MA:BKRX;MA:APEX}` | `A1!BKRX.BGX.XXX.X.X~L(O){MA:BKRX;MA:APEX}` |
| test_lid_function_without_saleability | `A1!XXXX.CUX.XXX.X.X+AP:STRAW_HOLE.FR:CLOSURE.LP:D` | `A1!XXXX.CUX.XXX.X.X+AP:STRAW_HOLE.FR:CLOSURE.LP:D` |
| test_lid_function_without_saleability | `A1!XXXX.CUL.XXD.X.X` | `A1!XXXX.CUL.XXD.X.X` |
| test_multiple_features | `A1!XXXX.BGX.XXT.X.X+FX:W,Z` | `A1!XXXX.BGX.XXT.X.X+FX:W,Z` |
| test_multiple_features | `A1!XXXX.BGX.XXN.X.X+FX:W` | `A1!XXXX.BGX.XXN.X.X+FX:W` |
| test_nested_no_inheritance_and_merge | `A1!BKRX.BGX.XXX.X.X~S(INSIDE){CL:WHITE.OP:OPAQUE}` | `A1!BKRX.BGX.XXX.X.X~S(INSIDE){CL:WHITE.OP:OPAQUE}` |
| test_nested_no_inheritance_and_merge | `A1!APTX.XXX.XXX.X.X~S(BODY){-~S(OUTSIDE){CL:RED}}` | `A1!APTX.XXX.XXX.X.X~S(BODY){-~S(OUTSIDE){CL:RED}}` |
| test_tolerance_qualification | `A1!XXXX.CUX.XXX.M500.X+QC:[CA,TARGET,FILL,20%20%C2%B0C].TO:[CA,5,10]` | `A1!XXXX.CUX.XXX.M500.X+QC:[CA,TARGET,FILL,20%20%C2%B0C].TO:[CA,5,10]` |
| test_tolerance_qualification | `A1!XXXX.CUX.XXX.M500.X` | `A1!XXXX.CUX.XXX.M500.X` |
| test_unknown_na_other | `A1!XXXX.BGX.XXX.0.0` | `A1!XXXX.BGX.XXX.0.0` |
| test_unknown_na_other | `A1!A99X.XXX.XXX.X.X+OT:MA_GRADE=novel%20polymer` | `A1!A99X.XXX.XXX.X.X+OT:MA_GRADE=novel%20polymer` |
| test_utf8_structural_escaping | `A1!XXXX.BGX.XXX.X.X+UT:DM=%C3%A9%20%2E%2C%3A%3B%7B%7D%5B%5D%28%29%25%2B%7E%7C%2F%3D%E4%B8%AD%E6%96%87` | `A1!XXXX.BGX.XXX.X.X+UT:DM=%C3%A9%20%2E%2C%3A%3B%7B%7D%5B%5D%28%29%25%2B%7E%7C%2F%3D%E4%B8%AD%E6%96%87` |
| test_workbook_expected_codes | `A1!APSX.BWX.XXX.X.X+FR:CLOSURE.GW:3_3.LP:D.NC:6oz.OP:CLEAR.UT:DM=90%20mm%3B%20dimension%20role%20unspecified` | `A1!APSX.BWX.XXX.X.X+FR:CLOSURE.GW:3_3.LP:D.NC:6oz.OP:CLEAR.UT:DM=90%20mm%3B%20dimension%20role%20unspecified` |
| test_workbook_expected_codes | `A1!APSX.BWX.XXX.X.X+FR:CLOSURE.GW:3_3.NC:6oz.OP:CLEAR.UT:DM=90%20mm%3B%20dimension%20role%20unspecified,LP=Half%20Dome` | `A1!APSX.BWX.XXX.X.X+FR:CLOSURE.GW:3_3.NC:6oz.OP:CLEAR.UT:DM=90%20mm%3B%20dimension%20role%20unspecified,LP=Half%20Dome` |
| test_workbook_expected_codes | `A1!JMPX.POX.XXS.X.X+NC:20%20Serve.UT:DM=216%20x%20278%20x%2076mm%3B%20dimension%20roles%20unspecified` | `A1!JMPX.POX.XXS.X.X+NC:20%20Serve.UT:DM=216%20x%20278%20x%2076mm%3B%20dimension%20roles%20unspecified` |
| test_workbook_expected_codes | `A1!BKWX.BGX.XXX.X.X+DM:GUSSET=34_925,HEIGHT=190_5,WIDTH=146_05.GS:30` | `A1!BKWX.BGX.XXX.X.X+DM:GUSSET=34_925,HEIGHT=190_5,WIDTH=146_05.GS:30` |
| test_workbook_expected_codes | `A1!BWXX.WRX.XXX.X.X+GS:60.UT:DM=12x12%20mm%3B%20dimension%20roles%20unspecified` | `A1!BWXX.WRX.XXX.X.X+GS:60.UT:DM=12x12%20mm%3B%20dimension%20roles%20unspecified` |
| test_workbook_expected_codes | `A1!BWXX.WRX.XXX.X.X+GS:60.UT:DM=12x12%20mm%3B%20dimension%20roles%20unspecified` | `A1!BWXX.WRX.XXX.X.X+GS:60.UT:DM=12x12%20mm%3B%20dimension%20roles%20unspecified` |
| test_workbook_expected_codes | `A1!BKCX.XXX.XXX.X.X+CL:WHITE.FS:RECYCLED.GS:60.UT:DM=4%2E25%20x%202%2E5%20x%203%2E75%20inches%3B%20dimension%20roles%20unspecified,FS=100%25%20recycled%3B%20post-consumer%20share%20unspecified~S(INSIDE){MA:XXXG}` | `A1!BKCX.XXX.XXX.X.X+CL:WHITE.FS:RECYCLED.GS:60.UT:DM=4%2E25%20x%202%2E5%20x%203%2E75%20inches%3B%20dimension%20roles%20unspecified,FS=100%25%20recycled%3B%20post-consumer%20share%20unspecified~S(INSIDE){MA:XXXG}` |
| test_workbook_expected_codes | `A1!BKRX.BGX.XXX.X.X+CL:WHITE.DM:DEPTH=120_65,HEIGHT=406_4,WIDTH=196_85.GS:80.NC:16LB.UT:CF=SOS` | `A1!BKRX.BGX.XXX.X.X+CL:WHITE.DM:DEPTH=120_65,HEIGHT=406_4,WIDTH=196_85.GS:80.NC:16LB.UT:CF=SOS` |
| test_workbook_expected_codes | `A1!BKRX.CUX.XSX.X.X+CL:WHITE.DM:HEIGHT=152,TOP_DIA=90.UT:CA=20oz,MA_TREATMENT=18PE%20%2B18PE%3B%20side%2Forder%20and%20quantity%20units%20unspecified,TR=cold%20beverage%20use~L(X){GS:260.MA:BKRX;MA:APEX;MA:APEX}` | `A1!BKRX.CUX.XSX.X.X+CL:WHITE.DM:HEIGHT=152,TOP_DIA=90.UT:CA=20oz,MA_TREATMENT=18PE%20%2B18PE%3B%20side%2Forder%20and%20quantity%20units%20unspecified,TR=cold%20beverage%20use~L(X){GS:260.MA:BKRX;MA:APEX;MA:APEX}` |
| test_workbook_expected_codes | `A1!BKRX.CUX.XSX.X.X+CL:WHITE.DM:HEIGHT=178,TOP_DIA=105.UT:CA=32oz,MA_TREATMENT=18PE%20%2B18PE%3B%20side%2Forder%20and%20quantity%20units%20unspecified,TR=cold%20beverage%20use~L(X){GS:280.MA:BKRX;MA:APEX;MA:APEX}` | `A1!BKRX.CUX.XSX.X.X+CL:WHITE.DM:HEIGHT=178,TOP_DIA=105.UT:CA=32oz,MA_TREATMENT=18PE%20%2B18PE%3B%20side%2Forder%20and%20quantity%20units%20unspecified,TR=cold%20beverage%20use~L(X){GS:280.MA:BKRX;MA:APEX;MA:APEX}` |
