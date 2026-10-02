# Source One Atlas — Step 4C Results

**Delivery:** intake/search **0.3.0**, local candidate, 1 October 2026, Asia/Manila. **Baseline:** records **0.2.1**, engine **0.1.1**, dictionary **A1 / 0.1.0-local-candidate**. The inherited records version and engine/dictionary identifiers intentionally remain distinct from this workflow release.

Working persistent intake/review and deterministic explicit-criteria search are delivered. **126 tests pass: 84 inherited + 42 new; zero failures/errors. All 44 original known-answer results remain unchanged.** This is bounded local SQLite evidence, not completion of every AT-01–24 workflow, cloud deployment, shared editing or recovery.

## Baseline and implementation boundary

The current-baseline marker, complete four-document Step 3 specification, Step 4B results/repair notes/relationships, engine and Store interfaces, schema, dictionary, source reports and preserved fixtures governed the implementation. Historical instructions were source material only. No Step 1/2 redesign or workbook re-extraction was needed.

The current Step 4B package was copied into this workspace before executing any generator. Its original 84 tests and 44 known answers were reproduced before editing (`reference/Step-4C-Baseline-Reproduction.txt`). The source package remains unchanged: all 70 original manifested files still match (`reference/Step-4C-source-integrity.json`). No writes targeted Final Output.

`atlas/search.py`, `atlas/intake.py`, `atlas/phrases.py` and `atlas/workflow_cli.py` extend the existing implementation. The only Store edits add four immutable workflow record contracts and permit an absent description code on an intake preview. The executed SQLite schema, existing Store change/retrieval operations, batch loader, engine, original tests and dictionary are unchanged. Fourteen inherited files are independently pinned and checked by the new runner. No replacement record architecture, opaque product identifier, external AI dependency or cloud service was introduced.

## Implemented behavior

- Capture preserves source/precise location, original wording, units, literal formulas, cached values, uncertainty, attachments/references and source-versus-illustrative attribution. Client requirements remain separate from supplier claims.
- Persisted previews expose interpreted facts, complete codes/readable characteristics, exact equality, matching candidates, contradictions and full candidate differences. Preview creates no resolved specification/product/version/association.
- Reviewed decisions support existing/new descriptions, separately identified offerings, added source information, continued triage, supported triage resolution, requests, H01 clarification, H06 correction and H02 physical change. Actor, reason, evidence, original source and result links survive reopening. Failed commits roll back; repeated identical reviewed submissions return the original IDs.
- A broad match cannot silently assign a more specific candidate to an incompletely described offering. Such selection requires a complete explicitly supported description and evidence; conflicting known facts fail. Exact complete descriptions reuse the existing immutable specification. Equal codes never merge products.
- Search applies selected structured criteria to decoded facts and typed relationships. Per-criterion explanations distinguish matches, gaps and contradictions. Unknown, explicit negative, not-applicable, source-conflict and unsupported states remain visible. Known contradictions dominate unrelated missing facts.
- Quantity role, exact dictionary unit conversion, supplied qualifier/basis/condition, tolerance and interval containment are respected. Whole product intervals must be contained in requested intervals. Approximate values do not satisfy exact requests. Named dimensions do not imply fitment or confirmed compatibility.
- Named scopes stay separate; one layer must jointly support grouped layer criteria. Complete recorded stacks, order and repeats remain inspectable. Broad laminate and kit/component discovery is supported; no combined kit Spec ID or inferred separate sale.
- Capabilities remain custom-build possibilities. One manufacturing alternative must jointly contain the requested target/range and satisfy the other criteria; unrelated alternatives are not combined. Legacy free-form alternatives and unresolved feasibility conditions remain potential rather than invented products.
- Quotation, photos, sampling, approval type and current kit-membership filters operate on the supplier's exact version/association, resolved business context, customization, packing and selected sample or kit revision. No cross-supplier/context/iteration evidence union. Rejected/withdrawn decisions do not count as current positive approvals. Kit approval never comes from component approval.
- Current offering results follow supported associations and physical versions. Historical search labels older contexts; inherited historical retrieval retains original quotes/approvals and separately labelled corrections/provenance. The three Step 4B repair suites pass unchanged.
- Phrase proposals preserve the original text and unsupported/ambiguous spans. Editable structured criteria require an explicit persisted confirmation before execution. Core search works directly without phrases or AI. Bare ounces are never assigned a volume standard.

## Source data and illustrative data

`fixtures/verified-batch.json`, `fixtures/verified-results.json`, the original reports and reviewed example database remain inherited source evidence. The preserved batch still comprises **12 source/triage records**, **10 descriptions referencing nine distinct specifications**, **two unresolved descriptions**, and **12 unresolved supplier-product associations**. No automatic supplier-product promotion occurs.

V962/V963 retain one shared base specification and separate original printing/commercial statements. V18's `=P18/H18` and absent cached result remain literal. V1000's supplied 0.01 and 10.37 are not reconciled. V993 retains material alternatives/conflict and source boundaries; only its already-reviewed bag/no-handle facts are searchable. V1143 remains the source-labelled Example with shape/measurement uncertainty. “Verified” means transcription accuracy, not product truth, availability, performance, fit or approval.

`tests/test_step4c.py`, the inherited `atlas/demo.py`, and `examples/step4c-demo/` are explicitly illustrative, except new test 30 uses the preserved batch in an isolated fresh database. The demonstration calls actual CLI processes and retains each JSON input/output, review decision and database. Its offering and approval statements do not claim workbook support.

## Actual execution evidence

| Evidence | Result |
|---|---|
| Baseline reproduced before editing | 84 passed; 44 original known answers unchanged |
| Final inherited engine tests | 47 passed |
| Final inherited record tests | 25 passed |
| Final unchanged repair regressions | 12 passed |
| New persistent intake/search scenarios | 42 passed |
| Total | 126; zero failures/errors |
| Known-answer stability | All 44 original input/expected/actual results unchanged |
| Inherited integrity | All 14 pinned files unchanged |
| Original source-package manifest | All 70 files match |
| Actual CLI demonstration | Capture → preview → exact reuse/commit → retry → broad/narrow search → phrase review/confirmation/execution → historical retrieval |
| Runtime | Python 3.9.6; SQLite 3.43.2; on-disk stores and process-boundary CLI operations |

Run `python3 run_step4c_tests.py`. `step4c-test-results.json` records versions, runtime, timestamp, individual scenarios and actual outcomes; `Step-4C-Test-Run.txt` and `Step-4C-Inherited-Test-Run.txt` preserve execution logs. Tests assert independent expected classifications, IDs, immutable history and prohibited outcomes, not just encoding round trips. The new scenarios are in `tests/test_step4c.py`. Reports generated by inherited runners remain baseline-specific historical evidence.

The first new-suite run exposed a nullable preview-code check rejecting source-only intake. It was corrected without weakening specification validation. Additional adversarial checks explicitly cover sample V1/V2 evidence separation, membership without a quotation, unsupported/conflicting source review and unchanged original triage. No demonstrated defect required changing the inherited engine, dictionary or existing Store revision operations.

## AT-01–24 coverage

Numbers below refer to the new `test_01`–`test_42`. “Exercised” means the named local portions only; this is not a claim that all 24 whole workflows passed.

| Case | Step 4C exercised portions | Remaining boundary |
|---|---|---|
| AT-01 Incomplete RFQ | 06, 27–28: separate requirements, retained original phrase/unknown units | Full RFQ/business handoff usability |
| AT-02 Broad/narrow search | 01–05, 08, 40, 42: equality vs matching, reviewed selection, differences, narrowing, rollback/retry | Shared multiuser review |
| AT-03 Phrase interpretation | 27–28, CLI demo: proposal, editing, unsupported spans, confirmation/reopen | Broader language intentionally unsupported |
| AT-04 Missing/conflicting | 07, 09, 35, 37, 42: unknown/negative/NA/conflict/unsupported and contradictions | Human conflict-resolution quality |
| AT-05 Lid options/fit | 10, 39; inherited engine/relationships: no diameter-to-fit inference, lid function/profile | Complete source-option review/fit-confirmation UI |
| AT-06 Bag distinctions | 14, 30, 36: inside/outside, no handle, named dimensions; preserved source facts | Broader catalogue coverage |
| AT-07 Supplier kits | 22–23, 34: component browsing, membership, revision evidence, unknown quantities | Full kit intake/forms; inherited construction API remains |
| AT-08 Printing/commercial variants | 30 and inherited tests: V962/V963 unchanged, no product promotion | Dedicated commercial/customization intake UX |
| AT-09 Laminate browsing | 15: discovery, complete stack inspection, no fictional combined layer | Specialized layer-thickness intentionally deferred |
| AT-10 Units/tolerances | 10–13: exact conversion, roles, basis/conditions, approximation, tolerance, interval containment | Wider unit/observation source coverage |
| AT-11 Unpriced catalogue | 01, 21, 34: unpriced offering still searchable; no invented evidence | General catalogue import excluded |
| AT-12 Capability | 16–17, 41: separate possibilities, containing range, joint alternatives, legacy gaps | Richer reviewed feasibility-condition vocabulary |
| AT-13 Clarification | 24: same identity/version, updated current search, original quote retained | Shared correction UX |
| AT-14 Disproved claim | 25, 38: correction/current withdrawal, original claims retrievable | Broader source-finding workflow |
| AT-15 Proof/sample/approval | 19–21, 33: types, client/customization/sample scope, rejected/withdrawn results | Complete user interface; attachment bytes |
| AT-16 Physical/customization changes | 19, 25; inherited suite: physical change vs sample V2 | Integrated customization authoring flow |
| AT-17 Packing/quote alternatives | 18, 21, 32 plus unchanged inherited tests: scoped quote evidence and preserved supplied context | Pricing calculations excluded; commercial entry UX |
| AT-18 Correction/identity | 02–05, 24–25, 38, 40; inherited H07 tests: no implicit identity merge, preserved corrections | Comprehensive human merge/separation tools |
| AT-19 Evidence filters | 18–23, 32–34: exact supplier/client/version/customization/sample/kit boundaries | Shared-service validation |
| AT-20 Unfamiliar info/triage | 07, 26, 30, 35, 37: searchable source, retained unresolved originals, append-only supported resolution | Arbitrary vocabulary intentionally not guessed |
| AT-21 Operations handoff | No new handoff workflow; unchanged inherited retrieval/repair tests pass | Full handoff UI/whole workflow |
| AT-22 Dictionary continuity | 44 known answers and 14 pinned-file checks; inherited dictionary tests | Shared dictionary publication/allocation |
| AT-23 Shared corrections | Local transaction/retry protection only; 04–05 | Shared concurrency/conflict resolution not tested |
| AT-24 Recovery | Reopen/rollback tests only | Subscription/cost verification and records-plus-attachments restoration not performed |

## Limitations and remaining work

This is a trusted local Python/SQLite CLI and callable API. Search scans the small local store; indexing, pagination, permission infrastructure and shared concurrency are not supplied. The SQL schema still relies on the Python service for typed business validation. The unexecuted Postgres candidate remains a future migration aid, not a validated Supabase deployment.

Phrase vocabulary is deliberately small and documented. It requires explicit handling of every unsupported span; users may confirm a supported subset while retaining the exclusions. Nested layer/component filtering, specialized layer-thickness filtering, arbitrary prose matching and general workbook importing are not supported. GA/EC/FF dictionary limitations remain unchanged.

Targeted unresolved wording and general capability feasibility conditions are classified conservatively as gaps. Complete construction/evidence alternatives remain visible so a reviewer can resolve them. A no-match layer search cannot prove absence of an unrecorded layer in a partial construction. Supplemental source assertions are inspectable; they do not silently rewrite structural specifications. Human reviewers remain responsible for whether cited evidence actually supports a decision.

No supplier count establishes manufacturing independence. No kit membership proves separate sale. No customization establishes unrestricted printing capability. No copied attachment URI proves availability of its bytes. No local test certifies product truth or production authorization.

The approved Supabase/Postgres, Vercel and GitHub direction remains unchanged. No cloud provisioning, deployment, remote publishing, pricing calculations, production execution, general identity merging, permissions system or recovery work was added. `Next-Stage-Handoff.md` gives the bounded continuation. The self-contained versioned ZIP, refreshed per-file manifest, SHA-256 checksum and package-verification output accompany this delivery.
