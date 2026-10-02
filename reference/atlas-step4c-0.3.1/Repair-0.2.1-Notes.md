# Step 4B bounded repair — records 0.2.1

This package supersedes records **0.2.0**. Engine **0.1.1** and dictionary **A1 / 0.1.0-local-candidate** are unchanged. The original Final Output delivery is preserved, read-only. No business-design changes, workbook extraction, deployment or production validation were performed.

## Baseline and actual before/after evidence

All 62 files in the existing workspace matched the deposited package before work. The original suite was reproduced: **72 tests passed**, comprising 47 engine and 25 record tests, with **44 known answers unchanged**. That run is retained in `reference/Step-4B-0.2.0-Reproduced-Tests.json`; the prior file manifest is in `reference/Step-4B-0.2.0-manifest.json`.

The 12 tests in `tests/test_repairs_021.py` were added before changing the implementation. Running them against 0.2.0 produced **1 failed test, 8 erroring tests and 3 passing tests**, captured in `Repair-0.2.1-Before-Tests.txt`. The passing tests checked pre-existing rejection/rollback safeguards. The errors exposed missing provenance retrieval, false context mismatch and unsupported kit ownership; they are not claimed as assertion failures.

After the bounded changes, **all 12 repair tests pass**. The combined execution passes **84 tests: 47 engine + 25 original records + 12 regressions**, with **0 failures and 0 errors**. All 44 original known-answer vectors remain unchanged. `Repair-0.2.1-After-Tests.txt`, `Repair-0.2.1-Full-Test-Run.txt`, `record-test-results.json` and `Record-Test-Results.md` retain execution evidence. The original test files are unchanged. Run `python3 run_all_tests.py` to reproduce all tests.

## 1. Approval evidence and correction provenance — resolved

**Reproduction:** an approval references its own signed-document source, location, attachment and assertion. A different source/document/assertion explains its misfiling. In 0.2.0, `correct_approval` assigned that correction assertion as the replacement's approval evidence. Opening the replacement omitted the original approval and incoming H07 event.

**Change:** the replacement keeps the prior approval's evidence links and immutable decision/approver/date. Only the H07 event references the correction evidence. `history` walks incoming H07 events for approvals in the opened record's graph, follows predecessor approval chains, and returns a separate `correction_provenance` structure. It expands the documents, sources, assertions and contexts and labels every approval association's active/withdrawn state. Incorrect prior contexts do not become part of the replacement's current `original_context` or another offering's approval list.

**Tests:** distinct signed and correction documents; preservation of the original record; separately retrieved evidence types; incoming event and predecessor retrieval; successive explicit corrections; handoff retrieval; close/reopen equality; unrelated approval isolation; rollback on invalid reassociation. Original approvals remain withdrawn, not erased or silently reapproved.

No historical 0.2.0 records are rewritten. The reverse H07 traversal can expose predecessor evidence already retained in an older store. This patch does not perform a migration that replaces the evidence links of previously created 0.2.0 replacement records; their immutable links remain historical facts, with the chain now retrievable.

## 2. Resolved business-context comparison — resolved

**Reproduction:** C1 inherits client/request through a job; C2 supplies the same client/request redundantly. Both validate, but 0.2.0 compares the raw link dictionaries and rejects an approval using C2 with a sample using C1. Handoffs suffer the same mismatch.

**Change:** `same_context` compares exact non-business links and the existing `_business_scope` result. Physical version or kit revision, specification association, customization and packing remain exact references. Job/request/client must match after resolution. Missing-versus-known is unequal; missing values are not wildcards. Explicit/inherited contradictions are still rejected by existing validation.

**Tests:** redundant client/request links in sample/approval and quote/approval/handoff comparisons, symmetry and reopen; differing client/request/job; missing versus known context; different physical version, association, customization or packing; contradictory explicit versus inherited scope. The existing 72 tests also continue to pass.

## 3. Supplier-kit sampling — resolved

**Reproduction:** the sequence contract requires a product; kit ownership is unsupported. The sample validator requires a physical version, so valid kit contexts cannot be sampled or accepted.

**Change:** a sequence has exactly one product or kit link. Product sampling retains its original validation. Kit sampling validates that the sample context's exact kit revision belongs to the sequence's permanent kit. Existing resolved business-scope checks, local sample labels, iteration lineage, notes and scoped approval checks apply to both. No SQL table change, product surrogate for kits or combined kit Spec ID is introduced.

**Tests:** kit V1/V2, photos/comments/revision requests/evidence, Source One acceptance, client approval, close/reopen retrieval, unchanged identity/revision/specification counts after sample V2, separate sequences reusing V1, and explicit sample context on a later composition. Wrong kit, wrong owner type, dual/missing owner, conflicting client, mismatched customization, duplicate label and cross-sequence predecessor are rejected. Earlier samples/approvals keep original component membership after composition changes, including after reopen. Component approval cannot support assembled-kit handoff, and an old kit sample/approval cannot authorize a new revision.

## Compatibility and limits

The record schema stays at version 1. Existing product-sequence records remain valid. The CLI reports 0.2.1; the logical contract, relationship documentation and reports are updated. Original engine, dictionary, source fixtures and original engine/record tests remain byte-identical. Existing example databases remain unchanged; their saved historical retrieval example is refreshed for the additional provenance field.

Only temporary local SQLite databases were used for repair tests. Supabase/Postgres, full intake/search, UI, concurrent editing, recovery and production behavior were not exercised. None of these three repairs has a remaining blocker. The broader limitations in `Step-4B-Results.md` still apply.
