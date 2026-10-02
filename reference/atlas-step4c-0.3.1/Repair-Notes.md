# Step 4A targeted repair — implementation 0.1.1

This package supersedes the unpatched **implementation 0.1.0** candidate. The A1 design and dictionary **0.1.0-local-candidate** are unchanged. Work continued in the existing workspace after confirming it matched the delivered package; the original `Final Output` package was not edited.

## Dictionary compatibility

Previously, `check_compatible()` accepted a test copy that reduced PR.maximum from 100 to 50, even though that dictionary rejected the previously valid `A1!APTX.XXX.XXX.X.X+PR:100`.

The checker now preserves all existing field-rule properties, including minimum, maximum, ordering and unknown/not-applicable behavior. Adding, removing or changing a rule on an existing field is rejected. Domain extensions remain additive; supported new fields, tokens and lifecycle/retirement metadata remain permitted. The actual dictionary, including PR.maximum, was not changed.

The directly related role restriction list was also unguarded: adding B to reference-only roles made an existing CUB identifier invalid while compatibility still returned true. A regression reproduces this, and restriction lists now participate in the existing semantic-rule check. This is part of preventing an ostensibly compatible release from disabling old codes, not a general dictionary redesign.

## Repeated named scopes

Previously, merging two BODY scopes reconstructed a child from only `fields` and `groups`, silently discarding `unsupported_extra`. Both group orders reproduced the defect; the invalid child alone was correctly rejected.

A shared structural check now runs on each raw named-scope child before merging. It checks allowed node properties and container types only. Semantic validation still occurs on the combined facts, preserving existing cases where closure function and aperture, or material and dimensions, arrive in complementary fragments. Malformed containers on this same path now raise `SpecError` rather than incidental Python exceptions.

## Executed evidence

- Before engine changes: nine new regression methods ran against implementation 0.1.0. The captured result was **10 failed assertions/subtests and 6 erroring subtests**; three regression methods already passed. See `Repair-Before-Tests.txt` for the actual run. These counts include subtests and are not separate test-method counts.
- After repair: **47 test methods passed, zero failures, zero errors**: the original 38 plus nine regression methods. Reproduce with `python3 run_tests.py`.
- Both unsupported-child orders, the standalone invalid child and valid merges are covered. Existing complementary-fact and repeated-scope tests pass.
- PR upper-bound reduction, minimum tightening, a new GW upper bound, removed bounds, field semantic properties and role restrictions are rejected. Supported additive vocabulary and retirement tests pass.
- All **44 original known-answer vectors** match the prior run exactly. All dictionary and fixture files are byte-identical. The ten selected workbook codes and full decodes match their saved results; both triage records remain unchanged. No workbook reprocessing was performed.
- All 32 files listed in the original package manifest still match their recorded hashes. Details are in `repair-verification.json`.

`Test-Results.md` and `test-results.json` contain the regenerated results and implementation version. The refreshed manifest covers this patched package. The updated archive is `Atlas-Step-4A-0.1.1.zip` in the workspace outputs folder; its extracted package is `atlas-step4a/`.

No known test failure remains in this targeted repair. The earlier vocabulary and workflow limitations still apply. These checks establish completion of the two-defect repair, not validation of the full Atlas application, all 24 acceptance workflows, or production readiness. Step 4B was not started.
