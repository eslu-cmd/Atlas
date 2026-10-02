# Step 4C 0.3.1 workflow and query reference

## Source capture and review

`Intake.capture(document, actor=..., reason=..., provenance=...)` creates immutable source, location, attachment-reference, assertion and triage records. `document` accepts:

- `label`, `kind` (`supplier_statement` or `client_requirement`).
- `source`: existing source payload shape: title, URI, optional SHA-256 and metadata.
- `locator`: precise worksheet/cells, page/paragraph, image region or message reference, preserved literally.
- `statements`: original `statement`, `uncertainty`, optional `supplied`, `interpretation`, `evidence_kind`, and per-statement `locator`.
- `attachments`: URI/media-type and optional hash/caption. Attachment bytes are not imported.
- Optional engine `facts`, `uncertainty_facts`, and supplied `context` snapshot.

Use `supplied` for original units, formulas, cached values, references and discrepancies. These are retained without arithmetic or inferred normalization. Unsupported descriptions can be captured with no interpreted `facts`.

Uncertainty facts are objects such as `{"field":"MA_GRADE","scope":[],"state":"conflicting","wording":"virgin or recycled"}`. States retain the inherited seven distinctions: not_supplied, explicitly_unknown, not_applicable, ambiguous, conflicting, unsupported, stated. A stated assertion is not a verification badge.

`preview(intake, facts=None, uncertainty_facts=None, ...)` defaults to the captured interpretation. Explicit alternatives create another immutable preview; they do not edit the source. Default review also carries unresolved assertion-level wording and the two unencoded batch cases' original uncertainty. Preview persists a review snapshot and may register the inherited dictionary. It creates no specification, supplier product, version or association.

The preview checks all existing specifications using selected supported facts, exposes exact complete-description equality, and displays all full codes/readable descriptions. Contradicted candidates remain distinguishable. `differences` includes the full interpreted and candidate facts plus per-criterion explanations; additional characteristics are visible even when the broad criteria match. Complete equality also includes features, groups, qualifiers and unresolved wording, through canonical A1 content.

`commit(preview, decision, actor=..., reason=..., provenance=...)` requires `confirmed: true` and a nonempty list of assertion IDs in `evidence`. The actor, reason, evidence, entire decision and result IDs are immutable. Each preview has one decision. Identical retries return the same decision/records after reopening; changed retry payloads fail. A terminal resolution also prevents a different preview from resolving the same intake twice. A triage decision may be followed by a new preview and resolution. All dependent writes share one transaction; failures roll back every new record.

| Action | Decision fields and effect |
|---|---|
| `triage` | Preserve unresolved record and append review evidence/reason. No resolved business record. |
| `specification` | Issue/reuse supported complete description. New descriptions require `distinguishing_reason`; exact descriptions reuse automatically. No invented offering. |
| `offering` | Same specification check, plus explicit existing `supplier`, `reference`, optional `sku` and `version_label`; creates a separate product/version/association. No merge by description. |
| `clarification` | Existing current `association`; H01 keeps product and version, changes description with evidence. |
| `correction` | Existing current `association`; H06 withdraws misleading current association, preserving original evidence/history. |
| `physical_change` | Existing current `association` and supplied `version_label`; H02 creates linked physical version and its association. |
| `add_information` | Existing `subject` product/version/association/kit/revision; appends sourced assertions without changing physical identity. |
| `request` | Only client-requirement intake; optional client ID. Preserves requirements/source separately from supplier statements. |

All description decisions accept optional `selected_specification`. A broad match alone is rejected. To affirm a more complete existing candidate, the reviewer must explicitly supply its complete `supported_code` and supporting evidence. Known facts must agree, including known OTHER slots and their exact OT explanations. Dropping or changing an OTHER characteristic, changing scoped/layer constructions, or changing unresolved statements requires a new, fully supported preview. Preview comparisons expose the OTHER difference, and commit rechecks it. Filling unknowns while retaining the same OTHER explanation remains supported. The action is a recorded human assessment, not machine verification of source truth. Conflict/ambiguity/unsupported markers must be addressed in an explicitly amended preview before a resolved description/association commit.

Ordinary facts do not trigger a clarification-versus-change question. Only review of changed existing offering information selects H01, H06 or H02. Printing/artwork, quotes, packing and sampling continue through their established Store operations; this milestone does not duplicate those workflows.

`Intake.history` returns the original graph, every preview and every decision. Search retains the original triage, labels its resolved/unresolved status and includes its decisions/links. Resolved triage still displays its original supplied interpretation; the linked current offering/specification is a separate result. Source assertions added with `add_information` remain retrievable through reverse `subject` links and the intake decision. They do not automatically redefine structural specifications.

## Structured query

```json
{
  "criteria": [
    {"field":"AR_CLASS","value":"CU"},
    {"field":"CA","value":{"value":"0.5","unit":"L"}},
    {"field":"MA_TREATMENT","value":"G","scope":["INSIDE"]}
  ],
  "types": ["specification","offering","capability","triage"],
  "evidence": {"quotation":true,"approval":"client_approval"},
  "scope": {"client":"EXISTING_CLIENT_ID"},
  "historical": false
}
```

All options are optional. Only selected criteria/evidence/scope constrain classification. By default all five result types are browsed. Every result remains visible in its category; no fuzzy score, ID substring matching or hidden similarity threshold is used. A successful query may have no matches while still explaining contradictory records. An empty store returns `status: ok, results: []`. Unsupported fields/options return `status: unsupported`; malformed data, broken references or storage failure return `status: error`. CLI exits: 0 success, 3 unsupported search, 2 error.

Result types: immutable `specification` descriptions; supplier `offering` version/association; separate `kit` revision; `capability` manufacturing alternatives; original `triage` source. A description/capability never implies an available product. Current offering results use current physical versions and their supported current associations. All descriptions remain browseable. `historical: true` also returns older offering associations/versions and kit revisions, explicitly labelled `current: false`. Use `inspect`/Store.history for original quotes/approvals and separately labelled later corrections.

### Supported fields

- Core slots: MA_FAMILY, MA_GRADE, MA_TREATMENT, AR_CLASS, AR_ROLE, CF_SHAPE, CF_CONSTRUCTION. Values are dictionary tokens. MA_GRADE includes its family (`APT`, `APP`, `BKR`) to preserve meaning.
- `CF_FEATURE`: `{"article":"BG","closure":false,"token":"N"}` selects the article feature dictionary, including no-handle/plain negatives and additional features. `closure: true` selects the lid-profile dictionary: core/FX when the encoded role is L, otherwise LP when FR establishes closure. `closure: false` reads article-scoped core/FX only for roles other than L, including a role-X closure with separate LP. FR alone never reinterprets article tokens as lid tokens. A missing compatible optional feature is a gap; explicit negatives, non-applicability and dictionary-defined mutually exclusive features are contradictions.
- `CA` and `FI`: encoded quantity (`M500`, `M480-520`, `R98`, `0`) or `{value,unit}`. Capacity volume, mass/load and count roles remain distinct.
- `DM_HEIGHT`, DM_WIDTH, DM_LENGTH, DM_DEPTH, DM_GUSSET, DM_DIAMETER, DM_TOP_DIA and DM_BOTTOM_DIA: named dimensions. No inference from TOP_DIA to FI.
- Dictionary numeric/integer fields including GW, GS, TH, EL, PY, CM, PR; dictionary enum/list fields including colour, optics, bleaching, feedstock, treatment-related characteristics, aperture and explicit yes/no/none values. A list criterion selects one recorded member.
- Dictionary string fields (e.g. NC, SZ, HL, WN, TT, SG, RS where registered) use **exact stated values**, not general prose interpretation. FF remains restricted to registered fitments; LP uses lid profiles. Unsupported fields and values are reported.
- Convenience `kind`: cup, lid, bag, kit. `cup` needs a recorded body function; use `AR_CLASS: CU` to broadly find cup-family records with unresolved function. `laminate: true` discovers recorded laminate family, construction or layer stacks; absence of a recorded stack is an information gap.

No printing/price/source/approval field becomes an intrinsic characteristic. OT/UT, raw MA/AR/CF blocks and arbitrary prose are not query operators; use specific slots and inspect retained statements. Unsupported syntax is rejected as a whole query.

### Scope, layers and kits

`scope` on a criterion is a path of named intrinsic scopes, e.g. `["INSIDE"]`. No parent inheritance or inside/outside substitution. Missing child facts are gaps.

`{"layer":[{"field":"MA_GRADE","value":"APT"},{"field":"CL","value":"WHITE"}]}` requires both facts within **one recorded layer**. Its explanation shows each layer's independent comparisons. A partial construction without a satisfying recorded layer remains potential, never a fictional combined layer. Separate layer clauses intentionally mean separate existential requirements. Specialized layer-thickness and nested layer/component filters are deferred and rejected explicitly. Complete ordered/unknown-order construction is always returned for inspection, retaining repeated layers.

`{"component":[...]}` on kit results requires the selected facts jointly within one component's specification. Components remain individually identified with their original membership association, quantities and saleability state. Component evidence does not approve the assembled kit. Kits have no combined Spec ID.

### Classification and exact quantities

Each selected criterion has an explanation: satisfies, gap, or contradiction. Any known contradiction dominates gaps within that evaluated description/alternative. Unknown never satisfies a required fact. Explicit negative/not-applicable values contradict incompatible positives. Source conflicts stay unresolved; a conflict is not arbitrarily resolved to one competing value. Targeted UT wording is conservatively treated as a gap for that target and remains inspectable.

Exact conversions use the inherited dictionary and rational arithmetic. Canonical-unit numbers are allowed in structured criteria; noncanonical units require `{value,unit}`. Bare `oz` is unsupported. The not-applicable `0` sentinel applies only to CA/FI; ordinary numeric facets such as PR retain numeric zero and compare it numerically. Numeric `qualifier` is `[mode,basis,condition]`, default `["REPORTED","UNKNOWN","-"]`. Mode, basis and condition must agree; unknown/incompatible qualifications never become matches. Approximate values do not automatically satisfy exact requirements.

`tolerance: [minus,plus]` applies only to that scalar criterion, in its canonical units or explicit unit objects. Recorded TO tolerances also expand only their named quantity. A product's full stated interval must be wholly inside the requested acceptable interval. Overlap is insufficient. Equality still compares the full canonical description, not containment.

Capabilities deliberately reverse the containment direction: a manufacturing range must contain the requested target/interval. One alternative must jointly support all selected criteria. Independent alternatives are never combined. Capability `alternatives` accept engine nodes or `{facts: node}`; older free-form alternatives stay visible as potential, pending review. Supplied general feasibility `conditions` remain visible and require review instead of pretending conditional manufacturing is an unconditional match.

### Supplier evidence filters

Select any of quotation, photos, sampling, kit_membership (`true`) and approval (`proof_agreement`, `source_one_acceptance`, `client_approval`). Scope may select existing client/request/job/version/association/customization/packing/sample/kit_revision IDs.

Quotation, sample and approval filters must jointly hold in one exact supplier context; resolved equivalent redundant client/request links are accepted. Distinct/missing business scope is not combined. Approval decisions are always partitioned by exact sample ID within the exact context, even without a selected sampling filter; sample IDs retain sequence ownership, so labels reused across efforts do not combine decisions. Unsampled approvals form a separate group. A V1 rejection cannot veto V2 approval. A rejection/conflict in the same group still prevents that group from supplying positive approval. When photos/sampling or an explicit sample are selected, all sample-dependent evidence must concern that iteration; unsampled approval cannot supply its approval. Quotation records remain pinned to their original context. Rejected, withdrawn or conflicting approval decisions do not count as current positive evidence. Missing evidence is a gap, not proof that evidence cannot exist.

Kit membership works without a quote/context and uses a current kit revision's exact component association. Photos require a photo note with attachment references. Context alternatives are returned separately; no supplier-wide or shared-specification evidence union occurs. Evidence filters on specification/capability/triage results are gaps rather than borrowed supplier evidence.

## Reviewed phrases

The parser is deterministic and bounded. It retains the original phrase, character spans of unsupported/ambiguous wording and editable proposed criteria. It never executes a proposal.

Supported words: cup(s), lid(s), bag(s), kit(s), laminate(s), PET, PP, PS, kraft, paper, clear, white, uncoated, quoted, sampled, photos. Supported quantities: `500 ml`, `0.5 L`, `1 litre`/`liter`; `rim 98 mm`, `height 2 in`, `width 10 cm`, `depth 40 mm`. Letter case is ignored. Units, field roles and decimal spelling must fit this vocabulary. Singular/plural litre/liter are recognized.

No guess is made for oz, unlabelled dimensions, arbitrary adjectives, negation, conjunctions, approval type/client, printing capability, or comparative prose. They remain unsupported spans. Conflicting repeated field proposals are flagged for editing. Punctuation is not silently discarded.

`Phrases.propose(phrase, ...)` saves a review. `confirm(review, query, confirmed=True, acknowledged=review.unsupported, ...)` records the explicitly accepted edited query and every acknowledged unsupported span. The reviewer may intentionally search only a supported subset; the original exclusions remain visible. `execute(confirmation)` requires the saved confirmation ID and returns original phrase, confirmation and search. A proposal ID cannot execute search. Core structured search needs no phrase interpretation.
