# Step 4B reproducible test execution

84 tests: 47 baseline + 37 persistent-record tests. 0 failures; 0 errors.

Python 3.9.6; SQLite 3.43.2. 2026-10-01T16:42:16.461073+00:00.

Record-layer evidence, not completion of all 24 acceptance workflows, shared editing, deployment or recovery.

44 known answers unchanged: True. Baseline file hashes unchanged: True.

Run `python3 run_all_tests.py`. Full expected/actual assertions are in `tests/test_records.py` and `tests/test_repairs_021.py`; machine-readable execution is in `record-test-results.json`. Baseline known answers remain in `test-results.json`.

| Persistent test | Result |
|---|---|
| test_01_shared_spec_separate_histories_and_cross_links_rejected | pass |
| test_02_clarification_preserves_original_quote_and_other_vendor | pass |
| test_03_physical_artwork_and_sample_changes_are_distinct | pass |
| test_04_kit_revisions_retain_membership_and_unknown_quantity | pass |
| test_05_packing_and_commercial_revisions_preserve_supplied_values | pass |
| test_06_proof_internal_acceptance_client_approval_and_context | pass |
| test_07_misplaced_evidence_corrected_or_unresolved_with_trail | pass |
| test_08_historical_retrieval_survives_reopen | pass |
| test_09_atomic_rollback_references_and_immutable_storage | pass |
| test_10_disproved_claim_correction_removes_current_indication | pass |
| test_11_pair_specific_compatibility_never_transfers | pass |
| test_12_source_batch_preserved_without_product_invention | pass |
| test_13_findings_uncertainty_attachments_and_sampling_notes | pass |
| test_14_request_job_handoff_and_capability_scope | pass |
| test_15_identity_resolution_requires_evidence_and_keeps_references | pass |
| test_16_dictionary_release_preserved_and_duplicate_meaning_rejected | pass |
| test_17_failed_correction_leaves_no_partial_replacement | pass |
| test_18_cli_persistence_and_atomic_apply | pass |
| test_19_revision_lineage_rejects_cross_product_and_cross_version | pass |
| test_20_sku_and_sample_labels_are_locally_scoped | pass |
| test_21_sampling_retrieval_exposes_photos_requests_and_decisions | pass |
| test_22_later_dictionary_cannot_reinterpret_issued_meaning | pass |
| test_23_failed_kit_revision_rolls_back_new_component | pass |
| test_24_history_follows_multiple_corrections_without_rewriting_original | pass |
| test_25_retrospective_quote_still_shows_prior_correction_to_its_context | pass |
| test_R1_approval_evidence_is_not_replaced_by_correction_note | pass |
| test_R1_failed_reassociation_preserves_evidence_and_active_state | pass |
| test_R1_replacement_retrieval_exposes_incoming_correction_provenance | pass |
| test_R1_successive_corrections_and_handoff_provenance_survive_reopen | pass |
| test_R2_exact_product_and_business_distinctions_are_not_erased | pass |
| test_R2_explicit_inherited_contradictions_remain_rejected | pass |
| test_R2_handoff_accepts_equivalent_quote_and_approval_context | pass |
| test_R2_sample_approval_accepts_redundant_resolved_scope | pass |
| test_R3_changed_composition_does_not_inherit_approval | pass |
| test_R3_kit_samples_notes_acceptance_and_client_approval_persist | pass |
| test_R3_sequence_has_exactly_one_permanent_owner | pass |
| test_R3_wrong_kit_client_customization_and_sequence_labels | pass |
