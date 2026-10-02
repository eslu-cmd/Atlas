# Step 4C bounded repairs — workflow 0.3.1

**Status:** all four independently reported defects repaired. Records baseline 0.2.1, engine 0.1.1 and dictionary A1 / 0.1.0-local-candidate remain unchanged. This patch performs no redesign, deployment or next-stage work.

## Actual before/after evidence

The deposited 0.3.0 package's 112 manifested files were verified before local work. Its full **126-test suite passed** before editing; that reproduction is saved in `reference/Step-4C-0.3.0-Reproduced-Tests.txt`. The superseded manifest/results are retained under `reference/`.

`tests/test_repairs_031.py` was added and executed against unchanged 0.3.0 code before fixes: **20 tests, 12 failures, zero errors, eight passes**. Failures reproduce every reported issue and related scope variants; the eight passing tests establish retained safeguards. `Repair-0.3.1-Before-Tests.txt` contains actual assertions/traces; `Repair-0.3.1-Before-Results.json` lists the failing cases.

After repair: **20/20 regressions pass** (`Repair-0.3.1-After-Tests.txt`). The full suite passes **146 tests: 47 engine + 25 records + 12 record repairs + 42 original Step 4C + 20 new repairs**, with **zero failures/errors**. All **44 original known-answer results** are unchanged. `step4c-test-results.json`, `Step-4C-Test-Run.txt` and `Step-4C-Inherited-Test-Run.txt` record the current combined execution. Run `python3 run_step4c_tests.py` to reproduce.

## R1 — Known OTHER retained in candidate review: fixed

Reproduction: an intake describes `A99X` with `OT:MA_GRADE=Experimental Resin Q`. The former guard omitted the OTHER slot from selected criteria and preserved UT/groups but not OT. Selecting the existing PET description with its `supported_code` succeeded without amending the source interpretation.

The new root OTHER comparison preserves each target plus exact explanation. Preview explicitly distinguishes incompatible known values from missing information. Commit rechecks the same comparison, rejecting loss/substitution even when a supported candidate code is supplied. Existing group protection retains scoped/layer content. Evidence-backed reinterpretation requires a new explicit preview; it does not overwrite the old one or source.

R1 tests cover rejected substitution and transaction rollback, original source/preview after reopen, candidate contradiction display, explicit amended preview and decision chain, exact OTHER description reuse, filling an unknown rim while preserving OTHER, and rejection of a different OTHER explanation.

## R2 — Feature dictionary scope and uncertainty: fixed

Reproduction: core `CU ... S` with role X, FR:CLOSURE and LP:F was treated as lid token S (sipper), although core S means stackable lip. LP:D with an otherwise unknown core was overlooked. A twisted handle was also treated as contradicting an unrecorded compatible window.

Search now chooses the encoding location and dictionary explicitly. Closure queries read core/FX only for encoded role L; otherwise they read LP when FR establishes closure. Article-feature queries read core/FX for non-L roles, including role-X closures. FR does not move core/FX tokens into the lid dictionary. Intake criteria now use the encoded role for core/FX scope, preventing review from regenerating the same error.

A present feature satisfies its criterion. A missing compatible optional feature is an information gap. Dictionary-defined mutually exclusive features, explicit negative/plain states and non-applicability remain contradictions. The dictionary itself is unchanged.

R2 tests cover all three reproductions, flat-versus-sipper, explicit dome, core role-L profiles, missing LP, article-scoped stackable lip on a closure, no-handle versus handle, no-handle versus missing window, valid handle/window/tin-tie FX combinations, mutually exclusive handles, explicit plain/NA, article mismatch and exact intake preview consistency.

## R3 — Ordinary numeric zero: fixed

Reproduction: PR:0 compared with required PR=0 entered the CA/FI applicability branch and contradicted itself.

The sentinel branch is restricted to CA/FI. PR zero now follows the ordinary exact numeric/interval path. R3 tests cover zero equality, zero inside an acceptable interval, different numeric values, nonzero-versus-zero, and unchanged CA/FI explicit-not-applicable behavior. No engine or dictionary change was necessary.

## R4 — Approval iteration scope: fixed

Reproduction: V1 rejection and V2 approval in one exact business/product context were pooled by a broad approval-only filter, causing V1 to invalidate V2. Adding a sampling filter avoided the defect because it selected iteration-specific evaluation.

Approval evaluation always partitions decisions by exact sample ID within an equivalent exact context, whether or not sampling is selected. A sample ID preserves its sequence ownership; repeated V1 labels across independent sampling efforts are not equal scopes. Unsampled decisions are a distinct group. Selected photo/sampling evidence still requires one actual iteration. Active rejections/conflicting decisions block only their own group; withdrawn approvals never count as positive.

R4 tests cover broad approval success with rejected V1/approved V2, explicit V1/V2 results, sampling-filter consistency, reopen, independent efforts reusing V1, same-iteration conflict, withdrawn approval, unsampled approval separation/conflict, and supplier/client/customization/physical-version/kit-revision isolation. The unchanged original suites also retain their cross-context and historical correction checks.

## Compatibility and limits

There is no storage migration and no rewrite of historical approvals, intakes or reviews. Existing rejected/approved evidence remains immutable. Rejected candidate commits create no partial offering records. Only intake/search behavior and workflow packaging/documentation changed; original tests, Store, engine, dictionary and source fixtures remain unchanged and hash-checked.

Historical 0.3.0 demo snapshots remain labelled illustrative; they are preserved rather than rewritten. The corrected implementation and new persistent regressions are the current behavior evidence. The archive/checksum, refreshed manifest and current wrapper verification identify 0.3.1. Fresh-extraction tests run outside the deposit so report generators do not alter the installed package.

None of the four reported defects has a remaining blocker. All prior local-candidate limitations remain: trusted SQLite service, bounded phrases and dictionary vocabulary, no shared-concurrency/cloud-production validation, no records-plus-attachments restore trial, no all-24-complete-workflow claim. Supporting evidence still requires human interpretation; an OTHER explanation is not automatically mapped to a registered material.
