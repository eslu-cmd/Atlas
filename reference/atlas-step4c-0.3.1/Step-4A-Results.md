# Source One Atlas — Step 4A Results

**Date:** 1 October 2026. **Implementation:** 0.1.1. **Dictionary:** A1 / 0.1.0-local-candidate. **Status:** local candidate for review; not published or deployed.

The bounded local dictionary/identifier implementation is delivered. The current test run passes 47 test methods, with no failures or errors. Independent known answers, round trips, negative cases, source mapping assertions and isolated dictionary-only decoding are included. This is not validation of the later Atlas application or all 24 acceptance workflows.

The selected workbook batch is fully accounted for: **12 records; 10 encoded descriptions; 2 unresolved triage records**. Codes retain the supported distinguishing facts and explicitly unresolved specification statements. An encoded incomplete description is not a resolved supplier-product association, verified performance claim or approval.

## Targeted repair 0.1.1

This working package supersedes the unpatched 0.1.0 Step 4A implementation. Two reproduced defects were repaired: dictionary compatibility omitted numeric restrictions and other field rules; repeated named-scope merging could discard unsupported child properties. The original 38 tests plus nine new regression methods pass (47 total, zero failures/errors). All 44 original known-answer vectors, dictionary bytes and fixture files are unchanged. See `Repair-Notes.md` for before/after evidence and scope. The original delivered package under Final Output was not modified.

## Baseline and authority

Implemented Documents 1–4 of `closing up/Step three results.md`, especially I01–I14 and D3-001–D3-006, under the user's Step 4A instructions. An unchanged reference copy is included. The source package was treated as read-only. No original script was run against it. The workbook extraction hash matches the final check; copied Step 3 and registry CSVs match their originals. Inspection details and source hashes appear in `Source-Ledger.md` and `source-ledger.json`.

The namespace is exactly `A1!`. Supplier SKU, kit references, prices, packing, approvals, printing and evidence are excluded from base facts. No alternative identifier scheme, application interface, cloud service, database, importer, migration or recovery work was built.

## Delivered implementation

- `atlas/engine.py` and the CLI implement core blocks, typed fields, nested scopes and optional layers, exact quantities, intervals, qualifiers, supplied tolerances, named dimensions, escaping, canonicalization, validation, complete decoding and comparison.
- `dictionary/atlas-A1-0.1.0.json` exports the vocabulary, rules, units, scopes, types, ordering, entry metadata and per-row legacy disposition. `dictionary/REFERENCE.md` is its readable companion.
- `fixtures/verified-batch.json` contains original source cells, formulas/cache distinctions, merged supplier context, structured facts, mapping decisions, independently specified expected IDs, exclusions and uncertainties. `fixtures/verified-results.json` contains actual results and complete dictionary decodes.
- `Encoding-Report.md` presents every selected record. `tests/test_engine.py` contains labelled illustrative W01–W08 cases and independent negative/positive tests. `Test-Results.md` and `test-results.json` record the executed run and expected versus actual codes.
- `README.md` provides copyable encode, decode and test commands. The engine and test suite use only the Python standard library. Source workbook inspection used the bundled openpyxl environment; it is not a runtime dependency.

## Reuse and substantive changes

Retained Proposal 4's field-scoped material families/grades, treatment, articles, non-kit roles, shape, construction and compatible features. Every original CSV entry has an explicit retained, amended, excluded or reference-only disposition. The copied `registries.py` supplied data for the release; the historical encoder and tests were inspected but not adopted as proof.

Replaced the historical fixed-width and implied-scale mechanics with direct A1 quantities and rational arithmetic. No class-default ounce unit, bare-mm rim inference, six-percent capacity matching, float rounding, uppercasing of free text or future-suffix truncation remains. In particular, historical `M05000` and `R09800` must not be read using old scale rules in A1; legacy strings without `A1!` are rejected. No automatic legacy migration is provided.

Historical TH used microns. A1 TH uses canonical mm: 30 microns becomes `TH:0_03`, not `TH:30`. PRINTED is excluded from CL; PF/UNTESTED is excluded as evidence-only. PN/PC/PS/PM/IC and SK are rejected from base fields. LS is superseded by structured layer groups. C/K roles and CY/M remain reference vocabulary and cannot issue combined kit identifiers.

FR separates known function from saleability; LP supports a known closure whose role is X/P. Role B/L/A makes the matching FR redundant. Additional compatible features sort into the core and FX. Bag no-handle can coexist with a window but cannot coexist with a handle. Repeated named scopes merge compatible local facts, including partial material blocks and complementary dimensions, without inheriting parent facts.

## Local implementation choices and vocabulary limits

These choices make underspecified mechanics explicit without changing the approved base identity rules:

1. Structured descriptions use dictionary block/field names. Exact numeric strings and unit objects avoid binary float ambiguity. No general natural-language encoder is claimed. Arrays represent intervals, lists, statements and qualifier/tolerance rows as documented in the README.
2. Existing list domains serialize as comma-separated tokens. OT/UT entries sort by target and exact text; free text preserves case and UTF-8 bytes. Only registered aliases/unit spellings are supported; arbitrary synonym guessing is excluded.
3. Applicability and contradiction rules are concrete in the export and engine: field-local dependencies, closure/article constraints, bleaching/feedstock conflicts, feature exclusions, explicit construction/material compatibility and quantity domains. Unstated facts are not inferred. These candidate rules are local implementation rules, not a new claim of exhaustive materials science validation.
4. Historical GA has no identified gauge convention and EC labels “ECT” without its full unit standard. They are excluded as bare numeric fields; `UT:GA=...` and `UT:EC=...` preserve the supplied statement pending a specific standard. This is an explicit vocabulary limit, not silent data loss. A future exact standard requires additive dictionary support.
5. FF was called a registered non-circular fitment key, but the supplied registry does not define bounded expansions for any such keys. The FF type is retained with an empty registration table and rejects arbitrary strings; use named dimensions and targeted UT until a real bounded definition is added. No opaque key was fabricated.
6. No new material/variant token was necessary for the selected batch. “Half Dome” and “SOS” remain targeted unresolved wording rather than forced into a potentially different existing meaning. A future reviewed term can be added without redefining the old ID.
7. Resource guards are 100,000 encoded characters and depth 32. Exceeding them fails explicitly and does not truncate. These limits are engineering guards, not approved universal business length limits.
8. Dictionary compatibility checks preserve existing meanings, types, units and semantic rules, permit supported additive vocabulary, and retain retired entries for decode. Multi-user atomic allocation is not implemented in this local milestone.

No business-decision question was needed to implement the supported grammar. Source ambiguity stayed local to the affected records. The GA/EC/FF limits are explicit; they should not be represented as fully resolved numeric/registered vocabulary.

## Verified workbook coverage

The batch is Main Table rows **4, 7, 18, 961, 962, 963, 993–997, 1000, 1088, 1141, 1142, 1143**. Rows 993–997 are one unresolved record/alternative group with continuation information; no unsupported split into products was made.

There are 1,100 nonempty rows after the three header rows, with 1,072 nonempty description cells and a formatted extent of 1,860 rows. The batch covers 16 physical rows, 13 nonempty rows and 12 description cells. **1,087 nonempty rows and 1,060 description cells remain outside the mapped batch.** These are auditable worksheet counts, not a complete product or quotation census.

- Rows 4/7 preserve dome versus unresolved half-dome, PS, optical clarity, unit mass and nominal designation. Unlabelled dimensions are not promoted to fitment.
- Row 18 preserves the Mylar pouch description and its price formula/cache separately.
- Row 961 converts explicitly named inch dimensions exactly.
- Rows 962/963 produce the same complete base code while printing and different prices remain outside it.
- Rows 993–997 are triaged for unresolved virgin/recycled alternatives and record boundaries.
- Row 1000 preserves recycled white kraft, inside treatment and printing request separately; it does not invent a post-consumer percentage or article type.
- Row 1088 preserves white colour without inferring bleaching, named dimensions and unresolved SOS/trade size.
- Rows 1141/1142 retain paper plus repeated PE layers with unknown order, unresolved PE quantity units, unresolved ounces and cold-use wording. Top diameter is not treated as confirmed fitment.
- Row 1143 is explicitly labelled “Example” in the source and contains rectangular/Dia tension plus ambiguous bare weight. It stays in triage and is not promoted to verified supplier-product evidence.

“Verified” is used only for the user's completed transcription work. No original document-extraction exercise was repeated.

## Acceptance traceability

“Partial” below means only the indicated local engine/source boundary was exercised; it is not a pass for the full acceptance case. All test method names are in `Test-Results.md`; input, expected and actual known answers are in `test-results.json`.

| Case | Step 4A coverage | Still outside this execution |
|---|---|---|
| AT-01 | Partial: W08, unknown/NA, unresolved units, original source context | RFQ intake UI/workflow |
| AT-02 | Partial: complete description equality and distinct-code tests | Search, narrowing and pre-creation duplicate UI |
| AT-03 | Not executed | Phrase interpretation and confirmation UI |
| AT-04 | Partial: duplicates, local contradictions, triage records and numeric gaps | Multi-record search classification and conflict resolution workflow |
| AT-05 | Partial: lid profile/function, no saleability/fit inference, rows 4/7 | Options workflow and pair-specific compatibility evidence |
| AT-06 | Partial: W04, named dimensions, white versus bleaching, rows 961/1088 | Application browsing/comparison |
| AT-07 | Partial: W07 component codes; combined kit codes rejected | Supplier kit record/revision persistence and historical membership |
| AT-08 | Partial: W02/W03 boundary; rows 962/963 equal base codes, excluded printing fields | Linked customization and quotation application workflows |
| AT-09 | Partial: W04, ordered/unordered repeated layers and complete decode | Laminate search/browsing UI |
| AT-10 | Partial: exact units/fractions, intervals, scoped QC/TO, containment | Measurement review and observation-to-association workflow |
| AT-11 | Partial: base facts can encode without a quote; no invented approvals | Unpriced catalogue intake and search |
| AT-12 | Not executed | Capability alternatives and sourcing workflow |
| AT-13 | Partial: W05 produces distinct descriptions without rewriting either | Stable supplier/physical-version associations and historical quote views |
| AT-14 | Partial: stable meanings, explicit evidence-field exclusion | Disproved-claim correction trail and current search state |
| AT-15 | Partial: approval/sampling fields rejected from base input | Vendor/client-specific proof, sample and approval histories |
| AT-16 | Partial: printing excluded, base changes distinguish codes | Physical/customization revisions and sample-iteration workflow |
| AT-17 | Partial: source price/packing preserved outside IDs; formulas not rewritten | Quote/packing alternatives and historical persistence |
| AT-18 | Partial: exact description comparison; no proximity equality or conflict guessing | Association correction, merges and separations |
| AT-19 | Not executed | Supplier-scoped evidence filters |
| AT-20 | Partial: targeted UT/OT, unsupported vocabulary errors, triage preservation | Searchable intake queue and classification workflow |
| AT-21 | Not executed | Operations handoff records and historical retrieval |
| AT-22 | Local dictionary/engine portions executed: W06, retired meanings, unknown-token refusal, isolated decode, complete extensions | Old quotation/approval application retrieval |
| AT-23 | Partial: local dictionary compatibility checks | Atomic allocation, concurrent edits and shared correction resolution |
| AT-24 | Not executed | Recovery subscription/cost verification and restoration trial |

W01–W08 have independent expected code/fact assertions where applicable. W02/W03, W05 and W07 test identifier behavior and exclusion boundaries; their relationship/history narratives require the later record system and are not simulated as completed workflows. W06 uses an explicitly test-only added grade to prove refusal by an older dictionary; no token was published.

## Validation evidence and limitations

`python3 run_tests.py` executes the suite and regenerates expected-versus-actual records. It also tests a temporary directory containing only `atlas/` and the exported dictionary; a nested layer code decodes completely there. No source workbook, historical registry module, database, internet or product lookup is present in that subprocess.

A vocabulary sweep covers over 200 material-grade and article-feature combinations in addition to hand-specified known answers. Every copied CSV row is checked against its exported disposition. These checks supplement semantic tests; they do not establish physical truth or exhaustive correctness for all future combinations.

There are no known failing tests in the delivered suite. The remaining limitations are the stated vocabulary restrictions, finite guards, manually reviewed small source batch and later workflows. The code cannot decide whether arbitrary UT prose improperly embeds a whole product record; intake must enforce that semantic boundary. The fixture builder did not create a production importer, and no general automated workbook mapping is claimed. Dictionary release publication/allocation remains unimplemented.

## Precise Step 4B handoff

Use this A1 candidate and its independent fixtures as the starting point for review; preserve complete identifiers and the issuing dictionary release. Do not replace them with shortened keys or reinterpret legacy scales.

Step 4B should implement the record relationships: immutable specifications; permanent supplier products and physical versions; historical specification associations; sources/assertions; separate customization revisions; separate kits and kit revisions; packing and quotations; vendor-specific sample sequences and scoped approvals. Keep original statements, formulas and uncertainties linked to their worksheet cells. Equal descriptions must never merge supplier identity, fit or approval automatically.

Resolve the two triage records only against their original statements and context; keep them available without inventing a resolved product. GA/EC need specified standards and FF needs actual bounded definitions before those values can become resolved dictionary entries. Add vocabulary without reinterpreting issued candidate codes.

Intake/search, duplicate checks, history, concurrency and recovery remain later validation gates in the approved order. No migration or deployment decision is implied by this local result.
