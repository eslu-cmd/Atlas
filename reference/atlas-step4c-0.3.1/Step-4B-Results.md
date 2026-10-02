# Source One Atlas — Step 4B Results

**Delivery:** persistent records **0.2.1**, local candidate, 1 October 2026 (Asia/Manila). **Inherited engine:** 0.1.1. **Dictionary:** A1 / 0.1.0-local-candidate. These versions intentionally differ.

Step 4B now has runnable persistence, typed relationships, revision/correction operations and historical retrieval. The complete A1 Spec ID remains dictionary-decodable and separate from supplier identity. **84 tests pass: 47 unchanged engine tests + 25 unchanged original record tests + 12 repair regressions; zero failures/errors. All 44 original known answers are unchanged.** Records patch 0.2.1 supersedes 0.2.0. The engine, dictionary and original source fixtures require no repair and remain unchanged. The original Final Output delivery is preserved.

## Bounded 0.2.1 repair

The working implementation matched all 62 files in the deposited 0.2.0 package before work. Its original 72-test suite was reproduced successfully. Twelve regressions were added before fixes: **1 failure, 8 errors, 3 passes** on 0.2.0; **12 passes** after repair. `Repair-0.2.1-Notes.md` explains each reproduction and the recorded execution files.

1. **Approval provenance resolved:** replacement approvals retain actual approval evidence. Correction notes remain on H07 events. Replacement/handoff retrieval exposes the incoming correction chain, original documents and explicitly withdrawn predecessor associations, including successive corrections after reopen.
2. **Equivalent context resolved:** comparison uses resolved client/request/job scope plus exact physical-version or kit-revision, specification-association, customization and packing links. Redundant explicit links pass; genuinely different, missing-versus-known and contradictory contexts do not.
3. **Kit sampling resolved:** sequences own exactly one permanent supplier product or kit. Kit sample contexts pin exact composition revisions and applicable business/customization scope. Notes, acceptance, client approval and V1/V2 work without automatic revision/specification creation or component-approval inheritance.

No storage table migration, dictionary change, workbook extraction, new architecture, intake/search, UI or infrastructure work was added. There is no remaining blocker for these three repairs. These are record-layer results, not whole-application or production certification.

## Baseline and implementation boundary

The current baseline marker and all four consolidated Step 3 documents controlled this work. The repaired current `atlas-step4a/` package was copied into a separate workspace; its 47 tests were reproduced before implementation. The superseded archive was not used. Engine contracts, dictionary, tests, source ledger, encoding report and mapped fixtures were inspected. Step 1/2 proposals were not reopened. Historical document instructions were treated as source material, not execution authorization.

The source folder was treated as read-only. No scripts ran inside it. `reference/baseline-integrity.json` freezes hashes of the unchanged engine entry points, engine tests, dictionary and two source fixtures. The earlier manifest is preserved in `reference/Step-4A-manifest.json`. The original engine test runner remains unchanged; the new runner combines its results with persistence tests. No cloud credentials, subscriptions or live infrastructure were accessed.

The selected implementation is standard-library Python with on-disk SQLite and a JSON CLI. The supplied tree had no detected Supabase/Vercel project setup to reuse. The approved Supabase/Postgres, Vercel and GitHub direction remains the target; `schema/postgres-candidate.sql` is an unexecuted translation. **Only SQLite behavior was exercised.** No claim of Supabase, Postgres, Vercel, shared editing or production validation is made.

## Delivered behavior

- Immutable complete specifications retain the issuing dictionary document. Permanent supplier products/SKUs, physical versions and changing specification associations have separate identities.
- Sources, precise locations, assertions, distinct uncertainty states, findings and attachment references remain retrievable.
- Printing/artwork revisions stay outside base Spec IDs. No printability field was added.
- Supplier kits have component memberships and supplied quantity states per revision; components keep their own supplier/version/specification associations. Unknown quantity stays null, with no default one or separate-sale inference.
- Quotations preserve supplied commercial values and exact context, including packing and customization. Old quotation values, formulas and discrepancies are never recalculated or silently repaired.
- Supplier-product or supplier-kit sampling sequences have local V1/V2 labels, comments, photo references, revision requests and decisions. V2 creates neither a specification, physical version nor kit revision automatically.
- Proof agreement, Source One sample acceptance and client approval remain distinct. Known client/job, sample, customization and version contexts are checked. Compatibility is an exact version pair, with claims distinct from human confirmation.
- Requests, clients, jobs, capability alternatives and immutable operations handoffs retain their proper references. Capabilities cannot masquerade as products.
- H01–H10 operations preserve historical references. Wrong approvals can be withdrawn and explicitly reassociated, or left unresolved without a guessed destination. Identity resolution requires explicit identity evidence and retains old references; there is no destructive identity merge.
- Historical retrieval expands the original graph and separately labels later corrections and revisions. Product/sampling histories and reverse kit memberships are available through executable operations.
- Foreign keys, identity uniqueness, immutable-row triggers and transaction savepoints prevent dangling references, overwrites and partial failed operations through the supported Store API.

The logical schema is the typed `CONTRACTS` registry. The executed SQL uses immutable record snapshots plus ordered foreign-key links and uniqueness keys. Business scope validation belongs to the Python Store; bare SQL is not a supported application write interface. `Relationships.md` documents this boundary and the Postgres migration requirements.

## Source facts versus illustrative fixtures

`fixtures/verified-batch.json` and `fixtures/verified-results.json` remain byte-identical to Step 4A. No workbook re-extraction was necessary; mapped cells, headers, merged/continuation context, formulas, cached results, original statements and uncertainty were sufficient.

The persistent reviewed store contains **12 source/triage records, 10 encoded descriptions referencing nine distinct complete specifications, and two records without a resolved description**. V962/V963 share a base specification while their different printing/price statements remain in their original source snapshots. V993 retains its alternatives/record-boundary uncertainty; V1143 remains the source-labelled Example with conflicting shape/dimension context. V18 retains `=P18/H18` and its absent cached result; V1000 retains both 0.01 and 10.37 without arithmetic correction.

All 12 supplier-product associations remain unresolved. The importer creates **no supplier products, physical versions, resolved quotations, approvals, kits, clients or artwork** from this batch. Encoded descriptions are not permission to invent offering identity. “Verified” describes accurate transcription only.

`atlas/demo.py`, `tests/test_records.py`, `tests/test_repairs_021.py` and `fixtures/create-offering.json` contain labelled illustrative scenarios. The illustrative database is separate from the reviewed source database. Its fictional names, evidence and attachment URIs do not claim workbook support. The nine requested relationship behaviors are tested with these fixtures where the workbook does not establish the relevant facts.

## Execution evidence

Run `python3 run_all_tests.py` from the package. The delivered execution used Python **3.9.6**, SQLite **3.43.2**, on-disk temporary databases, process-boundary CLI reads, close/reopen checks and explicit failed transactions.

| Evidence | Actual result |
|---|---|
| Original engine suite | 47 tests, 0 failures, 0 errors |
| Original known-answer vectors | 44/44 unchanged, including input/expected/actual content |
| Original persistent record suite | 25 tests, 0 failures, 0 errors |
| Repair regression suite | 12 tests, 0 failures, 0 errors |
| Combined | 84 tests, 0 failures, 0 errors |
| Baseline implementation/dictionary/fixture hashes | All seven pinned files unchanged |
| Invalid reference/cross-scope/lineage attempts | Rejected in negative scenarios |
| Failed multi-record operations | No partial version, approval, component or CLI-plan changes |
| Reopened storage | Original graph and separately labelled corrections unchanged |

`record-test-results.json` records versions, runtime, timestamp, individual expected/actual outcomes and integrity checks. `Record-Test-Results.md` is the compact execution list. `tests/test_records.py` and `tests/test_repairs_021.py` contain the executable actions and exact assertions, including prohibited outcomes. Baseline known-answer details remain in `test-results.json` and `Test-Results.md`.

### Requested scenarios

| Requested behavior | Persistent tests |
|---|---|
| 1. Shared Spec ID, separate supplier histories, invalid links rejected | 01, 06, 19 |
| 2. Clarification retains product/version and earlier quote context | 02 |
| 3. Physical, customization and sample changes remain distinct | 03, 20 |
| 4. Kit composition history, unknown quantities, no sale inference | 04, 23 |
| 5. Packing/commercial snapshots and supplied arithmetic retained | 05, 12 |
| 6. Distinct approval forms; no scope inheritance | 01, 06, 11, 14 |
| 7. Misplaced evidence correction, unresolved destination, no equality merge | 07, 15, 17 |
| 8. Historical retrieval with later corrections | 02, 04, 05, 08, 10, 13, 21, 24, 25 |
| 9. Reopen, invalid references and transaction rollback | 08, 09, 17, 18, 23 |

## Step 3 acceptance coverage

Every entry below describes **partial record-layer or inherited engine coverage**, not a whole-workflow pass. Test numbers refer to `test_01`–`test_25` in the persistence suite. All 24 cases have not been completed.

| Case | Evidence in this delivery | Remaining workflow boundary |
|---|---|---|
| AT-01 | 14: requirements/source/context preservation | RFQ intake and requirement review |
| AT-02 | Existing engine description equality; 01 prevents identity collapse | Search, narrowing and pre-creation duplicate workflow |
| AT-03 | No new coverage | Phrase interpretation/criteria confirmation |
| AT-04 | 12/13: source uncertainty, competing statements and triage | Search matches/gaps/contradictions and resolution UI |
| AT-05 | 11: exact-pair claim/confirmation; inherited lid fixtures | Options intake and compatibility review workflow |
| AT-06 | Inherited bag encoding; 12 persists its mapping | Application comparison/browsing |
| AT-07 | 04/23: kits, memberships, quantities and history | Kit intake/editor interface |
| AT-08 | 03/05/12: customizations and quote/source context | Commercial/customization intake UI |
| AT-09 | Inherited layer decode; 12 persists source mapping | Laminate browsing/search |
| AT-10 | Inherited exact measurement tests; source assertions stay separate | Context review and duplicate check before classification |
| AT-11 | Source records can persist with no invented quotes | Catalogue intake/search |
| AT-12 | 14: capability alternatives separate from products | Capability search/results workflow |
| AT-13 | 02: stable identity/version, changed association, old quotes | Shared correction/intake workflow |
| AT-14 | 10/13: corrected current association and finding trail | Search and reviewer presentation of disputed facts |
| AT-15 | 01/06/07/20/21: scoped sampling and three approval forms | Evidence review/interface and broader workflow validation |
| AT-16 | 03/19: physical/customization/sample distinction | Guided change classification |
| AT-17 | 05/12: packing, supplied terms, immutable old quotes | Commercial intake/alternatives interface |
| AT-18 | 07/15/17: withdrawal, supported reassociation, identity evidence | Human identity resolution UI and comprehensive merge/separation workflows |
| AT-19 | 01/06/11: evidence remains supplier/client/version scoped | Selected evidence search filters |
| AT-20 | 12/13: original unfamiliar wording and uncertainties persist | Searchable triage/classification workflow |
| AT-21 | 08/14: immutable handoff and retained corrections | Operations handoff interface and full workflow test |
| AT-22 | 16/22 plus inherited engine tests: issuing release and old meanings | Shared dictionary publication/allocation |
| AT-23 | Uniqueness/rollback checks only | Concurrent editing, conflict retention/resolution, atomic dictionary allocation |
| AT-24 | Local reopen/rollback only; no recovery claim | Subscription/cost verification and records-plus-attachments restore trial |

The new R1 regressions extend AT-15/18/21 and T04.7 evidence; R2 extends AT-15/21 scope comparisons; R3 extends AT-07/15/16 and T04.2/4. These do not complete their remaining UI or shared-workflow boundaries.

T04.1–4 and T04.7–8 have corresponding record/engine evidence above. T04.5's source/context review and duplicate workflow remains partial. T04.6 layer behavior remains the inherited tested engine behavior. Unsupported dictionary entries fail visibly, but T04.9's shared conflicting-edit workflow remains deferred. T04.10 attachment restoration was not executed.

## Limitations and precise next-stage handoff

**Complete in this milestone:** the bounded local record substrate, typed reference checks, immutable context/revision history, minimal correction operations, selected source persistence, usable CLI/Python retrieval, baseline stability and the listed executable relationship scenarios.

**Next stage:** implement intake and explicit-criteria search around these contracts. Add existing-description checking before creation, triage resolution with identity evidence, matches/gaps/contradictions, separate capability results and scoped evidence filters. Preserve full IDs and expose both original context and labelled subsequent corrections. Do not turn the source batch into inferred supplier products during that work.

Then port the transaction service to the intended Postgres/Supabase environment and run these scenarios there; implement/test shared corrections and dictionary allocation before shared writes. The SQL candidate is a starting artifact, not an operational migration. Complete the remaining Step 3 acceptance workflows, user interfaces and concurrency checks before claiming all 24 cases passed.

Attachment URIs and hashes are references only. The package does not copy the full original workbook or retrieve real photo/artwork bytes. The selected source snapshot makes the local tests self-contained; recovery still requires the original records and corresponding attachment objects. Verify subscribed capability/cost, conduct a separate restore trial, and measure recoverable data age and restoration duration independently.

The current local API assumes trusted explicit record construction; it does not validate the truth of evidence or interpret commercial prose. Some structured supplied-value payloads intentionally remain flexible. Identity resolution is append-only explanation, not a completed general-purpose merge/separation tool. Subsequent resolution of an already withdrawn unresolved approval is a later workflow operation; the current record and correction trail remain accessible. No new UI, AI interpretation, pricing calculator, permissions system, full catalogue migration or dedicated sample-measurement subsystem was introduced. GA/EC/FF dictionary limits remain unchanged.

No deployment, paid service, production data change or external repository operation was performed. The versioned archive includes implementation, schema, preserved references/fixtures, example databases, reproducible tests and a SHA-256 file manifest. Review `README.md` first for operation and setup.
