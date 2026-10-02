# Source One Atlas — Step 3 Results

**Completed:** 1 October 2026  
**Status:** Consolidated Step 3 documentation, ready for implementation and testing.  
**Saving authorization:** The user reviewed the final eight-point summary and explicitly requested that the complete Step 3 output be saved in the project's `closing up` folder.  
**Validation boundary:** Implementation, migration, deployment, and production testing have not been performed or validated by this work.

This file contains all four final Step 3 documents. It replaces the earlier Step 3 drafts and detached amendments. The current conversation's approved decisions take precedence over conflicting Step 2 or Step 1 rules. Step 1 and Step 2 source files remain unchanged.

## Final review summary

1. **Spec IDs and vendors:** objective specifications, separate vendor offerings and histories.
2. **Kits:** separate kit references linking individually identified components.
3. **Printing:** linked customizations, leaving the base Spec ID unchanged; no required printability field.
4. **Code structure:** meaningful dictionary parts, compact measurements, optional variable-length layers.
5. **Adding and finding information:** source preservation, duplicate checks, explicit search criteria, and visible uncertainty.
6. **History:** revisions, corrections, quotations, sampling, and approvals retain their proper context.
7. **Acceptance checks:** all 24 Step 2 case identifiers retained and updated for the later approved changes.
8. **Implementation handoff:** bounded implementation, testing, and recovery checks before migration or deployment.

## Contents

- [Document 1 — Atlas Specification](#document-1--atlas-specification)
- [Document 2 — Identifier and Atlas Dictionary](#document-2--identifier-and-atlas-dictionary)
- [Document 3 — Acceptance and Traceability](#document-3--acceptance-and-traceability)
- [Document 4 — Step 3 Results and Step 4 Handoff](#document-4--step-3-results-and-step-4-handoff)

---

# Document 1 — Atlas Specification

**Status: consolidated Step 3 specification, ready for implementation.**  
This document and Documents 2–4 below replace the earlier Step 3 drafts and amendments. Implementation has not been performed or validated.

## A01. Authority and purpose

Apply the current conversation's approved decisions first, then Step 2 Results, then Step 1 Results where not superseded.

Atlas is a shared sourcing knowledge registry. It supports requests, specification browsing, supplier offerings, quotations, customization, sampling history, client approvals, and information handoff to operations.

The Spec ID describes product characteristics. It is the directory through which supplier offerings are found. It does not itself own vendor sampling history, commercial offers, or client approval.

## A02. Scope

Initial coverage includes cups, lids, bags, supplier kits, and broad laminate browsing.

Retain the agreed exclusions: pricing calculations, working estimates, production execution, NetSuite, full catalogue migration, full offline browsing, elaborate permissions, automatic similarity scoring, exhaustive material coverage, and specialized layer-thickness filtering.

Core browsing and search require no AI.

## A03. Records and relationships

| Record | Meaning |
|---|---|
| Specification | An immutable description of base-product characteristics, identified by its complete Spec ID. |
| Supplier product | A permanent reference to a particular supplier's offering. |
| Physical product version | An actual changed version of that supplier product. |
| Specification association | The link between a supplier-product version and its applicable description, with history. |
| Customization revision | Printing requirements and details, colour count where known, artwork/proof references, and relevant job/client context. |
| Supplier kit and kit revision | A separate kit reference and its component membership at a particular revision. |
| Source and assertion | Original information, its location, attribution, interpretation, and subsequent findings. |
| Sampling history | Vendor-product-specific sample iterations, photos, comments, revision requests, and acceptance evidence. |
| Approval | Explicit evidence for a particular client, supplier product/version, and relevant customization or sample iteration. |
| Compatibility relationship | A scoped supplier claim or human confirmation concerning a particular pair. |
| Packing option | Packing facts associated with the relevant supplier offering. |
| Quotation | Supplied commercial facts and the product, kit, customization, specification, and packing context concerned. |
| Capability | A supplier's stated manufacturing possibilities, separate from an existing product. |
| Request and handoff | Incoming requirements and the agreed information passed to operations. |

Several supplier products may share a specification without sharing evidence or identity.

A supplier SKU belongs to the supplier-product record. A kit reference belongs to a supplier kit. Neither substitutes for a descriptive Spec ID.

## A04. Source capture

Retain the original document and precise location: page, image, worksheet/cells, relevant headers, or message reference.

Preserve distinctions between supplied values, spreadsheet formulas, displayed results, and continuation rows. Do not silently move misplaced values, infer missing units, fix commercial arithmetic, or split an options list into invented products.

A normalized fact remains linked to its original source. Additional decimal places do not, by themselves, establish a genuinely different intended specification.

## A05. Uncertainty

Keep not supplied, explicitly unknown, not applicable, ambiguous, conflicting, and unsupported information distinguishable in the record.

Unknown is neither yes nor no. Negative statements such as uncoated require supporting information.

An unresolved conflict must not be presented as a resolved characteristic. Preserve the competing statements and their sources.

## A06. Evidence

Retain attribution and subsequent findings. Neither supplier origin nor Source One origin guarantees truth.

Do not introduce a universal verification badge.

Approval and compatibility evidence retain their explicit scope. Finding two offerings under the same Spec ID does not transfer either form of evidence.

## A07. Intake and duplicate prevention

Incoming information can:

1. Add information to an existing specification or supplier-product context.
2. Support a distinct specification and its relevant supplier association.

Before creating a new Spec ID, show existing specifications matching the entered characteristics. The user may select an existing description or identify the characteristic that distinguishes the proposed one.

For an existing supplier product, inspect the source and context of changed information. Distinguish a clarification, correction, or actual physical change using A17. Do not ask this question for every ordinary field entry.

Do not merge specifications solely because measurements are close. Do not require a numerical proximity threshold or similarity score.

If interpretation remains unresolved, retain a searchable triage record. Do not fabricate a resolved specification merely to complete an upload.

## A08. Requests

Retain supplied requirements, usage, distribution information, attachments, and the request or its source link.

Separate client requirements from supplier statements.

For a typed phrase, show interpreted search criteria before execution. Unsupported wording remains visible rather than becoming an invented criterion.

## A09. Search

Only selected criteria restrict results.

Distinguish:

- Recorded characteristics that meet the criteria.
- Potentially relevant records needing information.
- Records with known contradictions.

Contradictions are not matches. Unknown values do not satisfy a required characteristic.

Quotes, photos, sampling, approvals, and kit membership filter results only when selected. These filters operate on the relevant supplier records and evidence—not as universal properties of the shared specification.

Capabilities appear separately from existing products. A failed search is distinguishable from an empty result set.

## A10. Comparison

- Compare the complete specification, including relevant extensions, scope, qualifiers, and unresolved statements.
- Convert equivalent units exactly when quantity role, basis, and conditions are compatible.
- A broad request can match a more specific description.
- A specific request against an incomplete description produces an information gap.
- Different intended characteristics remain distinct.
- Apply only supplied tolerances, in their stated scope.
- Overlapping tolerance ranges do not establish equality or interchangeability.
- If a request specifies an acceptable interval, an explicitly supplied candidate interval must be wholly contained within it to satisfy that criterion.
- Matching diameters or rim descriptions do not establish confirmed fit.

Atlas does not need a dedicated sample-measurement workflow. If a document happens to contain an observation, retain the source without automatically converting it into an intended product characteristic.

## A11. Capabilities

Retain manufacturing ranges, alternatives, and conditions when supplied.

Do not combine characteristics from separate capability alternatives unless joint feasibility is established.

A capability is a sourcing starting point. It does not create an existing product, quotation, sample, approval, or stock claim.

Do not add a required “can this supplier print?” field or an unknown-printability badge. Existing customization records and proofs remain available without inferring an unrestricted printing capability.

## A12. Compatibility

Identify the particular products/versions, claim or confirmation, conditions, source, and person/date where known.

Keep supplier-claimed pairing separate from explicit human confirmation.

A shared specification, diameter, or rim style does not transfer confirmation to another vendor's offering or a changed product.

## A13. Kits and layers

### Supplier kits

Each component has its own specification and supplier-product context.

A separate kit reference links the component records and quantities where known. Opening a kit exposes its components; opening a component exposes its supplier-kit memberships.

Kit membership does not lengthen or change an otherwise unchanged component Spec ID.

A composition change creates a linked kit revision. Earlier quotations and approvals retain the kit revision they concerned.

Do not infer separate sale or a quantity of one.

### Layers within one product

Use the optional layer representation in Document 2. Include only the known layers. Preserve known order; represent unknown order explicitly.

Do not infer adhesives, intermediate layers, thicknesses, or an exhaustive composition from a partial description.

## A14. Sampling and approvals

Sampling is an interaction with a particular vendor about its product.

Retain a simple sequence such as:

- Sample V1 received.
- Photos and comments added.
- Revision requested, with the reason.
- Sample V2 received.
- Acceptance or approval recorded, with its actor and evidence.

Where several sampling efforts concern the same supplier product, distinguish their request, job, or client context when known. A “V2” label is local to its sampling sequence.

A sample iteration is not automatically a physical product version or a new specification.

Vendor proof agreement, Source One sample acceptance, and client approval remain distinct. Approval concerns the relevant vendor product/version, customization, sample iteration, and client. Atlas does not automate production authorization.

## A15. Printing and customization

The base specification represents the underlying product characteristics independently of printing.

Printing, colour count, method, sides, coverage, artwork, proofs, and relevant approvals belong to linked customization records. Printing alone does not create another base Spec ID.

No required print-status or printability field belongs in the base specification.

A supplier's printed quotation may supply customization information without an identified client or final artwork. Preserve those omissions rather than inventing a job.

Separating a base description from customization does not prove that a blank item is separately available for purchase.

A genuine change to the underlying material, dimensions, or construction still follows A17's physical-change rules.

**This rule supersedes the earlier Step 2 requirement that printing alone distinguish base Spec IDs.**

## A16. Commercial facts

Retain supplied prices, currencies, price bases, quantity breaks, validity, tooling, dates, Incoterms, packing, and other terms.

Unknown values remain unknown. Inconsistent unit and carton prices remain preserved and flagged, not recalculated into agreement.

Quotes identify the supplier product/version or kit revision, the applicable specification association, customization where relevant, and packing context.

A price or packing change does not automatically change the product specification.

## A17. History

Definitions and historical snapshots are immutable. Associations change through recorded events.

Record the actor/source, recorded time, reason, affected references, and previous/new associations. Record an effective date only when known.

| Event | Stable identity and current change | Earlier records |
|---|---|---|
| **H01 — Clarification** | Keep supplier product and physical version. Associate the more precise description. | Retain original wording and association; show the clarification without transferring it to other suppliers. |
| **H02 — Physical change** | Keep permanent supplier-product reference; create a linked physical version and applicable specification. | Quotes and approvals remain on their original version. |
| **H03 — Printing/artwork change** | Keep the unchanged base specification; create a customization revision. | Earlier proofs and approvals retain their original customization context. |
| **H04 — Packing change** | Add a packing option or revision beneath the offering. | Earlier quotes retain their packing. |
| **H05 — Commercial change** | Add the new quote or commercial revision. | Do not overwrite earlier terms. |
| **H06 — Error/disproved claim** | Correct the current association and link the supporting correction. | Preserve the earlier claim and specification meaning; remove misleading current indications. |
| **H07 — Misplaced approval** | Withdraw the wrong association and establish a supported correct one. | Retain the document and correction trail. Hold ambiguous destinations for review. |
| **H08 — Merge/separation** | Resolve individual associations using identity evidence. | Preserve old references and explain their current resolution. Equal descriptions alone do not justify merging. |
| **H09 — Sampling iteration** | Add vendor-specific photos, comments, revision requests, and acceptance evidence. | Retain previous iterations. Do not automatically change intended specifications. |
| **H10 — Kit composition change** | Keep kit identity; create a linked kit revision with its component membership. | Earlier quotes and approvals retain the previous composition. |

Opening an old quote or approval retrieves its original context plus clearly labelled later corrections. Related history must not appear as new approval.

## A18. Handoff

Retain the agreed supplier product/version or kit revision, specification, customization/artwork, client approval, packing, quotations, and unresolved qualifications.

Preserve what was handed over. Later corrections are additions to its history, not silent rewrites.

## A19. Responsibilities

Use the direct-factory supplier model.

Contributors identify sources; pricing interprets commercial information; knowledgeable product reviewers resolve classification and conflicts. These are responsibilities, not a new permission hierarchy.

Supplier/location counts do not certify manufacturing independence.

## A20. Shared updates

Detect conflicting edits before they silently overwrite one another. Preserve the competing changes and their resolution.

Dictionary allocation must prevent one token being concurrently assigned different meanings.

## A21. Recovery

Use the existing Supabase, Vercel, and GitHub starting point.

Verify subscription capabilities and cost. Restore records and corresponding attachments together in a separate trial environment.

Measure recoverable data age and restoration duration separately. The accepted one-hour potential data-loss window remains conditional on simplicity and cost; it is not a restoration-time guarantee.

## A22. Display

Show readable descriptions, supplier context, relevant gaps, and history.

A shortened code preview is labelled as a preview. Copying or exporting the Spec ID returns its complete value.

No shared specification page may imply that every listed vendor has another vendor's samples or approval.

---

# Document 2 — Identifier and Atlas Dictionary

**Status: consolidated Step 3 identifier specification.**  
This replaces the earlier padded measurement format, print extensions, and combined-kit examples. It specifies the implementation target; it is not a claim that the existing encoder supports it.

## I01. Contract

The full Spec ID expresses base-product characteristics through dictionary-defined parts.

It must decode without an arbitrary whole-product lookup. A hash, catalogue number, kit reference, supplier SKU, or database key cannot substitute for its distinguishing characteristics.

Printing customizations and supplier kits follow A13/A15 and remain outside the base Spec ID.

## I02. Description equality

A specification is an immutable canonical description.

Compare the complete description, including extensions, scope, qualifiers, and unresolved specification statements. A hash may accelerate lookup but cannot establish equality without comparing the complete content.

Equal descriptions do not establish equal supplier products, compatibility, or approval.

## I03. Grammar

`A1` names this grammar and meaning namespace.

```text
id       = "A1!" node

node     = core [ "+" fields ] [ "~" groups ]

core     = material "." article "." configuration "." capacity "." fitment

material = family grade treatment
article  = class role
configuration = shape construction feature

capacity = "X" | "0" | ("M" | "G" | "N") amount
fitment  = "X" | "0" | "R" amount

amount   = scalar | scalar "-" scalar
scalar   = integer | decimal | fraction
decimal  = integer "_" digits
fraction = integer "/" positive-integer

fields   = field *( "." field )
field    = key ":" typed-value
key      = two uppercase ASCII letters

groups   = group *( "|" group )
group    = "S(" scope "){" fragment "}"
         | "L(" direction "){" fragment *( ";" fragment ) "}"

fragment = fields [ "~" groups ]
         | "-" [ "~" groups ]

direction = "O" | "X"
```

Rules:

- Material has four characters: family 1, grade 2, treatment 1.
- Article has three: class 2, role 1.
- Configuration has three: shape 1, construction 1, feature 1.
- Measurements have variable length.
- `.` separates fields/blocks; `_` marks a decimal.
- `S` identifies a named surface or intrinsic part of one product.
- `L(O)` is outside-to-inside layer order.
- `L(X)` means layer order is unknown.
- A fragment with no known local fields uses `-`.
- Parsing respects nested brackets, parentheses, and braces.
- Supplier kits have **no component-aggregation grammar inside a Spec ID**.

The full identifier includes every encoded extension and group. Dropping them produces an incomplete preview, not an equivalent Spec ID.

## I04. Core dictionary

Retain the existing Proposal 4 material, article, shape, construction, and feature registries, subject to this document's explicit amendments and applicability checks.

Examples of existing entries:

| Field | Token | Meaning |
|---|---|---|
| Family | `A` | Polymer |
| Family | `B` | Paper/paperboard |
| Family | `C` | Molded fibre/agricultural residue |
| Polymer grade | `PT` | PET |
| Polymer grade | `PP` | Polypropylene |
| Polymer grade | `CP` | CPLA |
| Paper grade | `KR` | Kraft; bleaching unspecified |
| Paper grade | `KB` | Brown/natural unbleached kraft |
| Paper grade | `KW` | White bleached kraft |
| Paper grade | `TS` | Tissue paper |
| Treatment | `N` | No coating/barrier treatment |
| Treatment | `P` | One-sided PE coating |
| Treatment | `Q` | Two-sided PE coating |
| Treatment | `E` | PET coating/lining |
| Treatment | `C` | CPET coating |
| Class | `CU` | Cup |
| Class | `BG` | Bag |
| Class | `CY` | Cutlery |
| Class | `NP` | Napkin/tissue |
| Role | `B` | Body sold separately |
| Role | `L` | Closure sold separately |
| Role | `P` | Component not independently saleable |
| Construction | `L` | Laminated multilayer |
| Bag feature | `T` | Twisted paper handle |
| Bag feature | `W` | Window |
| Bag feature | `Z` | Tin tie |
| Cutlery feature | `F` | Fork |
| Cutlery feature | `N` | Knife |
| Cutlery feature | `S` | Spoon |

Tokens are interpreted within their field and article/role scope.

Do not infer bleaching from colour. Do not infer uncoated from a material name.

Do not infer separate sale from a component record. When saleability is unknown, use role `X`.

Where needed, `FR:BODY`, `FR:CLOSURE`, or `FR:ACCESSORY` records known function without asserting saleability. Omit it when the core role already establishes the same function.

`LP` holds an existing lid-profile token when closure function is known but the core role is not `L`. With role `L`, the profile belongs in the existing core feature position instead.

Historical kit/combination role entries remain reference vocabulary, but they are not used to publish combined supplier-kit Spec IDs under this design.

## I05. Unknown, other, and not applicable

Within registered core slots:

- `X`/`XX` means unknown.
- `9`/`99` means a known other value that requires an `OT` explanation.
- `0`/`00` means explicitly not applicable only where the slot's dictionary allows it.

For capacity and fitment, the whole token is `X` for unknown or `0` for explicitly not applicable.

Unknown is not zero, uncoated, or absent. A numeric value of zero must not be silently converted to non-applicability.

Not supplied and explicitly unknown may share an unknown code value while remaining distinct in the source records.

Conflicting assertions must not be silently resolved during encoding. Preserve them in the source/triage record and withhold a new resolved association until the relevant conflict is addressed.

## I06. Compact exact measurements

### Units

| Prefix | Meaning |
|---|---|
| `M` | Capacity in millilitres |
| `G` | Mass-based capacity/load in grams, when that is the stated quantity role |
| `N` | Count capacity |
| `R` | Circular rim/opening diameter in millimetres |

The number is the actual value in that unit. It is **not** an integer requiring an implied scale factor.

```text
R98       = 98 mm
R98_125   = 98.125 mm
R98_5     = 98.5 mm
M500      = 500 mL
```

Do not pad with zeros. Do not introduce parentheses merely because a value has more decimal places.

`R98-99` describes an explicitly stated closed interval from 98 to 99 mm. It is not a similarity group and does not imply that products in that interval are interchangeable.

### Exact normalization

Normalize supported equivalent units exactly:

- Length → mm.
- Mass → g.
- Volume → mL.
- Areal mass → g/m².
- Count → integer.

Use dictionary-defined exact conversion factors. For example, 1 inch = 25.4 mm; 1 litre = 1,000 mL.

Canonical numbers have no exponent, leading plus, redundant leading/trailing zeros, or negative zero. A terminating result uses decimal notation. A nonterminating exact result may use a reduced fraction.

Count values and count-interval endpoints must be integers. Capacity and diameter scalar values must be positive. Intervals must be ordered and valid for the quantity; a singleton interval becomes its scalar.

Bare ounces, an unidentified fluid-ounce standard, and unspecified gauge are not converted by assumption. Preserve unresolved wording.

Original units and numerical spelling remain in the source record. Decimal places alone do not establish a tolerance or prove a different product.

### Qualifications

`QC` preserves mode, basis, and conditions:

```text
QC:[target,mode,basis,condition;target,mode,basis,condition]
```

- Target: `CA`, `FI`, another numeric facet, or a named dimension such as `DM_HEIGHT`.
- Mode: `REPORTED`, `TARGET`, `GUARANTEED`, or `APPROXIMATE`.
- Basis: `UNKNOWN`, `FILL`, `BRIM`, or `NA`, where applicable.
- Condition: escaped exact text, or `-` when absent.

Absent qualification means reported value, unknown basis, and no supplied condition. It does not establish target, brimful, or guaranteed status.

Sort entries by target. Permit one qualification entry per target. An approximate value cannot establish an exact requirement.

`TO` preserves a supplied tolerance around a scalar:

```text
TO:[target,minus,plus;target,minus,plus]
```

The tolerance uses the target's canonical unit, with nonnegative offsets. It does not apply to other measurements or independently establish guaranteed production performance.

Do not redundantly encode the same tolerance both as an interval and as `TO`.

## I07. Intrinsic fields

Retain applicable existing fields for base-product characteristics, including:

- `CL`, `OP`, `BL`: base colour, optical class, bleaching.
- `GW`, `GS`, `TH`: unit mass, basis weight, thickness.
- `AP`, `RS`, `TF`, `FF`: aperture and interface characteristics.
- `FS`, `PR`: feedstock and recycled content.
- `HL`, `WN`, `TT`, `SG`, `WP`: handle, window, tin tie, gusset, wrapping.
- Relevant stated performance or compliance characteristics.

Each dictionary entry specifies its type, units, domain, and applicability. A statement encoded here is not an independent verification badge.

Do not carry evidence-only values such as “untested” as if they were a physical material state. Preserve the testing/evidence context separately.

### Printing exclusions

`PN`, `PC`, `PS`, `PM`, and `IC` are not base-specification fields.

Print state, colour count, sides, method, coverage, artwork, and printing proofs belong to customization records. “Printed” is not a substitute value for base colour.

Supplier SKU, price, packing, source identity, and approval are also excluded.

### Multiple features

`FX` carries additional compatible feature tokens in the same article/role scope.

Choose the lexically first known compatible feature for the core and sort the remaining tokens in `FX`. Do not combine a negative/plain feature with contradictory positive features.

### Named dimensions

`DM` uses named dimensions in canonical millimetres:

```text
DM:HEIGHT=155,TOP_DIA=98
```

Initial names: `LENGTH`, `WIDTH`, `HEIGHT`, `DEPTH`, `GUSSET`, `DIAMETER`, `TOP_DIA`, and `BOTTOM_DIA`.

Sort names. Do not infer measurement roles from an unexplained tuple. A stated top diameter does not automatically become fitment.

## I08. Optional scopes and layers

A fragment may contain:

- `MA`: material block.
- `AR`: article block.
- `CF`: configuration block.
- `CA`: capacity.
- `FI`: fitment.
- Other registered intrinsic fields.

These five block fields are prohibited as duplicate root fields because the root already contains them.

Missing child fields are unknown. There is no automatic inheritance of material or other characteristics from the parent.

Initial named scopes include `INSIDE`, `OUTSIDE`, `WINDOW`, `HANDLE`, `BODY`, and `LINER`. They describe parts or aspects of a single product, not supplier-kit membership.

For layers:

- Include only layers supported by the description.
- Normalize known order outside to inside.
- Reverse an explicitly inside-to-outside list during normalization.
- With unknown order, use `L(X)` and sort fragments as a multiset, retaining repeated layers.
- Do not manufacture layers to make a stack appear complete.
- Do not include a layer section when there are no layer facts to represent.

Only one layer stack is permitted at a given node. Conflicting stacks require source review.

## I09. Text, other values, and unresolved statements

Encode free text as UTF-8 percent escapes with uppercase hexadecimal digits. ASCII letters, digits, hyphen, and underscore remain literal. Escape spaces and structural punctuation.

```text
16 oz → 16%20oz
```

`OT` explains an unregistered value in a known slot:

```text
OT:MA_GRADE=exact%20description
```

Each `9`/`99` slot requires a corresponding explanation.

`UT` preserves the smallest relevant unresolved specification statement:

```text
UT:CA=16%20oz
```

Targets identify a core slot, registered field, or a scoped unresolved characteristic. Multiple entries are sorted by target and text and separated by commas; punctuation inside the text is escaped.

Do not put an entire product record or an arbitrary lookup reference into `UT`.

Unresolved wording remains unresolved after decoding. It cannot establish a structured match merely because it appears inside a code.

## I10. Canonicalization

1. Separate base-product facts from customization, supplier identity, commercial facts, kit membership, and evidence.
2. Establish each supported characteristic's field and scope.
3. Preserve unresolved distinguishing wording rather than guessing.
4. Normalize only registered aliases and exact unit equivalences.
5. Preserve quantity role, basis, mode, conditions, and supplied tolerance.
6. Format numbers under I06.
7. Sort fields by key and entries by their dictionary-defined order.
8. Reject duplicate resolved fields at one scope.
9. Canonicalize nested fragments.
10. Normalize layer direction and ordering under I08.
11. Sort independent groups by complete canonical encoding.
12. Merge repeated named scopes only when their facts are consistent; otherwise retain the source conflict for review.
13. Omit redundant unknown fragment fields and default qualifiers.
14. Validate cross-field consistency.
15. Compare complete canonical descriptions before reusing a specification.

Source repetition is not evidence of additional physical layers, parts, or quantities.

The initial unknown-only root is not sufficient for a meaningful specification unless a field or group supplies an actual characteristic or unresolved specification statement.

## I11. Dictionary and decoding

Every dictionary entry must define:

- Token, immutable meaning, and scope.
- Human-readable wording.
- Type, units, scale if any, and permitted values.
- Applicability and unknown/not-applicable behavior.
- Dependencies and contradictions.
- Canonical ordering and normalization.
- Introduction release and retirement/replacement information.

The initial export uses the retained Proposal 4 registries with these amendments applied. The export must contain all grammar, unit, scope, and token dependencies needed by its codes.

A decoder must recognize the namespace, load a supporting dictionary, parse the complete code, validate it, render every encoded characteristic, and verify canonical form by re-encoding.

Unsupported tokens produce an explicit unsupported result. Never discard an unfamiliar suffix or silently interpret a partial decode as the full specification.

Malformed, inconsistent, or resource-exceeding input is retained for review, not truncated.

Registered size or characteristic combinations remain permitted if their entries expand into explicit bounded characteristics. They cannot conceal arbitrary whole-product records.

## I12. Stable meanings

Allocate tokens atomically within their scope. Never reuse a published token for a different meaning.

Retired entries remain decodable. Compatible additions may extend the dictionary; changing an existing meaning or grammar requires a new namespace.

Record the dictionary release used to issue a specification and preserve its dependencies.

Do not automatically rewrite old identifiers when new vocabulary appears. A later clarification or correction changes the supplier association through A17.

These changes replace unapproved draft formats. They are not a migration of an existing deployed Source One code system.

## I13. Complete worked examples

The examples are illustrative. They do not claim that a workbook supplies every illustrated characteristic.

### W01 — Different stated rim diameters

Separately sold PET cup bodies, 500 mL, with coating and configuration unspecified:

```text
A1!APTX.CUB.XXX.M500.R98
A1!APTX.CUB.XXX.M500.R98_125
```

- `A/PT/X`: polymer, PET, unknown treatment.
- `CU/B`: separately sold cup body.
- `XXX`: configuration unspecified.
- `M500`: 500 mL.
- `R98` / `R98_125`: different stated rim diameters.

The codes are **24 and 28 characters**.

The spelling represents established descriptions; it does not decide whether an incoming measurement is a new product, a correction, or unsupported information.

### W02 — Base product and printing

Illustrative separately sold 500 mL PP cup:

```text
A1!APPX.CUB.XXX.M500.X
```

The base code is **22 characters**.

An unprinted offer, a one-colour printing option, and a two-colour printing option can refer to this same base specification. Printing details and their quotes belong to linked customization/offer records.

No print-status extension is added. No client, artwork, or blank-product availability is invented from an incomplete source.

### W03 — Different client logos

Two clients use different logos on the base cup in W02.

The base Spec ID stays the same. Customization revisions, artwork, proofs, and approvals remain separately scoped to the relevant client and vendor product.

### W04 — Bag interior and layer distinctions

Illustrative kraft bag with twisted paper handles, bleaching unspecified, and a stated brown or white kraft interior:

```text
A1!BKRX.BGX.XXT.X.X~S(INSIDE){CL:BROWN.MA:BKRX}
A1!BKRX.BGX.XXT.X.X~S(INSIDE){CL:WHITE.MA:BKRX}
```

Each is **47 characters**. `KR` does not claim bleaching. The interior colour/material does not automatically describe the outside.

Illustrative kraft/PET laminate with known outside-to-inside order:

```text
A1!BKRX.BGX.XLX.X.X~L(O){MA:BKRX;MA:APTX}
```

Unknown order:

```text
A1!BKRX.BGX.XLX.X.X~L(X){MA:APTX;MA:BKRX}
```

Each is **41 characters**. The unknown-order example is sorted for consistency, but the dictionary explicitly says that its displayed order is not a physical layer order.

### W05 — Clarification without physical change

Illustrative white bleached kraft cup, separately sold, 500 mL; existing coating later established as one-sided PE:

```text
Before:
A1!BKWX.CUB.XXX.M500.X

After:
A1!BKWP.CUB.XXX.M500.X
```

Each is **22 characters**.

Keep the supplier product and physical version. Record the more precise specification association. Earlier quotes retain their original description with the clarification visible.

### W06 — Dictionary continuity

A dictionary release defines `R98` as a 98 mm rim and issues W01.

A later release adds another material grade. W01 retains its original meaning and spelling.

An older dictionary cannot guess the new grade; it reports unsupported vocabulary. This is a release-behavior example, not evidence that a production dictionary has already been published.

### W07 — Four-component supplier kit

Illustrative components, with separate sale unspecified:

| Component | Its Spec ID |
|---|---|
| CPLA spoon | `A1!ACPX.CYX.XXS.X.X` |
| CPLA fork | `A1!ACPX.CYX.XXF.X.X` |
| CPLA knife | `A1!ACPX.CYX.XXN.X.X` |
| Paper tissue | `A1!BTSX.NPX.XXX.X.X` |

Each component code is **19 characters**.

An illustrative kit reference such as `KIT-001` links the supplier's four component records and stated quantities. The kit reference is not a Spec ID, and that spelling is not a required kit naming format.

Changing kit membership creates a kit revision, not a combined descriptive code. No component is assumed to be separately saleable.

### W08 — Incomplete description

Illustrative “16 oz cup,” without a resolved ounce standard, material, or saleability:

```text
A1!XXXX.CUX.XXX.X.X+UT:CA=16%20oz
```

The code is **33 characters**. It decodes an unresolved capacity statement without inventing millilitres or a fluid-ounce standard.

## I14. Human use

Atlas presents ordinary fields and readable descriptions and generates the code.

Copy/export returns the full identifier. Previews are labelled as shortened.

The remaining length of an individual multilayer product follows its actual encoded characteristics. Supplier kits and printing no longer inflate the base code.

No universal maximum business length has been approved; implementation must never solve a length limit by silently dropping distinguishing information.

---

# Document 3 — Acceptance and Traceability

**Status: consolidated acceptance specification.**  
All 24 Step 2 case identifiers are retained. Later approved changes are applied explicitly. These are requirements for implementation testing, not reported test passes.

## T01. Source fixtures

| Fixture | Inspected source | Constraint |
|---|---|---|
| S1 | UGS, Main Sheet, A3:D3 and associated row fields/headers | The 20 oz PET cup wording does not establish all measurement roles, treatment, or construction. |
| S2 | COQ, PET Cups + Lids, C49:H49 | Opening options do not establish separate SKUs. |
| S3 | COQ, Paper Bag, D20:I21 | Preserve interior differences and dimension context. Do not infer bleaching from white colour. |
| S4 | UGS, Main Sheet, A279:D279 and associated row fields/headers | Preserve component-specific materials and the supplier's kit relationship. Do not distribute one material or dimension across every component. |
| S5 | COQ, PP Cups + Lids, C37:T37, C46:T46, C52:T52 | Preserve base-product facts, printing options, supplied tolerance, packing, and inconsistent commercial arithmetic. |
| S6 | COQ, OGR + Bags w Tin Tie, C10:T10 | Preserve supplied kraft/PET construction and uncertain or misplaced source fields. |

COQ is *SOG Compilation of Quotations*. UGS is *Updated God Sheet*.

These are recorded source descriptions, not independently verified products or transactions. Document 2's examples are explicitly illustrative.

## T02. Acceptance cases

| Case | UC / Step 2 basis | Rule home | Required and prohibited outcomes |
|---|---|---|---|
| **AT-01 — Incomplete RFQ** | UC-001; D2-010, 018 | A05, A08; I05, I09 | Preserve supplied context; do not invent unstated requirements. |
| **AT-02 — Broad search and narrowing** | UC-002, 003; D2-005, 010 | A07, A09–A10; I01–I02 | Apply only selected criteria. Before new-spec creation, show matching existing descriptions. Do not collapse distinct specs or supplier products. |
| **AT-03 — Phrase interpretation** | UC-001, 002; D2-014 | A08–A09 | Show interpreted criteria for correction before search; do not invent unsupported facts. |
| **AT-04 — Missing/conflicting information** | UC-002, 008; D2-009, 010 | A05, A07, A09–A10; I05 | Distinguish matches, gaps, and contradictions. Unresolved conflicts do not become resolved characteristics. |
| **AT-05 — Lid options and compatibility** | UC-003, 007; D2-008, 010 | A04, A12; I04, I07 | Preserve options and pair-specific evidence; do not invent SKUs, separate sale, or confirmed fit. |
| **AT-06 — Bag distinctions** | UC-003, 005; D2-005, 009 | A04, A13; I06–I09; W04 | Retain interior material/colour and dimension context. Do not infer bleaching or units. |
| **AT-07 — Supplier kit** | UC-005; D2-001, 016; D3-001 | A03, A13, H10; W07 | Each component has its own Spec ID and supplier record. Kit reference/revision links them and known quantities. Do not create a combined kit Spec ID or infer separate sale. |
| **AT-08 — Printing and commercial variants** | UC-003, 006, 009; D2-003, 004, 017, amended by D3-002 | A15–A16; I07; W02–W03 | Otherwise identical base descriptions share a Spec ID. Printing details stay in linked customization/offer records; quotes retain supplied values. No base print-status or printability field. |
| **AT-09 — Laminate browsing** | UC-002, 005; D2-013; D3-003 | A09, A13; I08; W04 | Find laminate records and expose supplied layers and order. No reserved empty layer slots or invented properties. |
| **AT-10 — Units, tolerance, and observations** | UC-003; D2-009; D3-004, 005 | A04, A07, A10; I06 | Convert exactly; preserve supplied tolerances and context. Extra precision alone does not establish a new product. An observation in a source must not silently overwrite intended specifications. No dedicated sample-measurement feature is required. |
| **AT-11 — Unpriced catalogue** | UC-004; D2-008, 010, 018 | A03–A07, A09 | Preserve searchable source/product information without fabricated quotes, sampling, or approval. |
| **AT-12 — Manufacturing capability** | UC-002, 004; D2-010, 011 | A09, A11, A19 | Return a capability as a sourcing starting point. Do not invent products or mix incompatible alternatives. |
| **AT-13 — Clarification** | UC-003, 008, 009; D2-001, 016 | H01; I02; W05 | Keep supplier identity and physical version while refining its association. Preserve old context; do not transfer clarification to other suppliers. |
| **AT-14 — Disproved claim** | UC-004, 008, 009; D2-007, 008 | A06, H06; I12 | Correct current association and retain the claim/finding trail. Do not redefine old meanings or retain a misleading current match. |
| **AT-15 — Proof, sampling, approval** | UC-007; D2-003, 008, 016; D3-002, 005 | A14–A15, H09 | Retrieve vendor-product-specific iterations, photos, comments, and approvals. Distinguish proof agreement, Source One acceptance, and client approval. Another vendor or client inherits none. |
| **AT-16 — Physical and customization changes** | UC-003, 007, 009; D2-002, 003, 016; D3-002, 005 | H02–H03, H09 | Actual base-product change creates applicable physical/spec versions. Printing/artwork creates customization revisions. Sample V2 alone does neither automatically. |
| **AT-17 — Packing and quote alternatives** | UC-006; D2-004, 017 | A16, H04–H05 | Preserve supplied commercial and packing context. Do not recalculate source quotes or alter base specs for packing/price alone. |
| **AT-18 — Correction, merge, separation** | UC-009; D2-001, 016; D3-006 | A07, H07–H08 | Correct associations with history retained. Do not merge on numerical closeness or shared descriptions, or guess where approval belongs. |
| **AT-19 — Evidence filters** | UC-010; D2-010, 011 | A09, A14, A19 | Apply selected evidence filters to the proper supplier context. Do not imply universal approval or unsupported manufacturing independence. |
| **AT-20 — Unfamiliar information** | UC-004, 012; D2-012, 018 | A07; I05, I09, I11 | Keep original wording and known facts searchable pending classification. Do not force an interpretation or lose information. |
| **AT-21 — Operations handoff** | UC-011; D2-017 | A18 | Retrieve the agreed supplier product/version or kit revision and its supporting context. No production execution or NetSuite integration. |
| **AT-22 — Dictionary continuity** | UC-003, 009, 011, 012; D2-005, 006, 020; D3-004 | I01–I12; W06 | Decode complete old meanings with supporting dictionaries. Do not guess newer tokens, truncate extensions, or reinterpret old scales. |
| **AT-23 — Shared corrections** | UC-009, 011; D2-019 | A17, A20; I12 | Detect conflicting updates and retain their resolution. Prevent duplicate allocation of dictionary meanings. |
| **AT-24 — Recovery** | UC-011; D2-015, 019 | A21 | Restore records and attachments together. Measure data age and restoration duration against the verified arrangement; do not claim an untested guarantee. |

D3 references are defined in Document 4. D2 references retain historical traceability; the later D3 decision controls where an explicit supersession is recorded.

## T03. Execution record

Each test execution records:

- Specification, dictionary, and implementation version.
- Exact fixture or labelled illustrative input.
- Actions performed.
- Expected and actual result.
- Evidence that the prohibited behavior was prevented.
- Pass, fail, or blocked status and explanation.

Execute against the eventual implementation. Historical test totals do not certify this specification.

## T04. Whole-workflow checks

Within the existing cases, verify:

1. Two vendors sharing one Spec ID retain different sampling and approval histories.
2. A second sample iteration does not automatically change the base specification.
3. Printing and different client logos use linked customization records without duplicating the base specification.
4. A supplier kit exposes separate component codes and retains past composition through kit revisions.
5. A changed measurement passes through source/context review and duplicate checking without automatic proximity merging.
6. Layer order and unknown order survive decoding.
7. Old quotes and approvals reopen in their original context after correction.
8. Complete codes decode with the dictionary alone, while commercial/evidence records remain outside them.
9. Conflicting edits and unsupported dictionary entries fail visibly rather than silently losing information.
10. Restored attachments open through restored records.

## T05. Checks completed during documentation

The drafting checks included source inspection, comparison with prior decisions, paper walkthroughs, example-length counting, structural checks on the displayed example strings, and coverage bookkeeping.

The displayed examples were checked for five core blocks, expected fixed widths in the first three blocks, compact measurement shapes, balanced delimiters, and absence of rejected print/combined-kit extensions.

Coverage bookkeeping found all **24 acceptance cases** and all **20 Step 2 decisions** represented, with later supersessions explicit.

These checks are not a completed encoder/decoder implementation, semantic test suite, search test, concurrency test, or recovery trial.

---

# Document 4 — Step 3 Results and Step 4 Handoff

**Status: Step 3 documentation complete and ready for implementation.**

Documents 1–4 in this file are the current specification. They replace the earlier drafts and separate amendments. Implementation and testing remain Step 4 work.

## R01. Approved review decisions

| Decision | Current rule |
|---|---|
| **D3-001 — Separate kit reference** | Each component has its own Spec ID and supplier-product context. A supplier kit links them through a separate reference and composition revisions. No combined kit Spec ID. |
| **D3-002 — Printing as customization** | Keep the base Spec ID unchanged for printing. Store printing details, artwork, proofs, and approvals in linked customization records. Do not add a required printability field. This supersedes the earlier D2-003 printed/unprinted base-spec distinction. |
| **D3-003 — Optional layers** | Add a variable-length layer section only when there are layer facts. Preserve known order and explicitly unknown order. Do not reserve empty layer slots. |
| **D3-004 — Compact measurements** | Encode direct values without padding or special parentheses for additional precision. Use a consistent decimal marker and dictionary-defined units. |
| **D3-005 — Vendor sampling history** | Keep sample iterations, photos, comments, revision requests, and acceptance evidence on the vendor's product. No dedicated sample-measurement workflow. Shared specifications do not share sampling history. |
| **D3-006 — Duplicate check** | Before creating another Spec ID, show matching existing specifications. Reuse the applicable description or establish its distinguishing difference. Do not automatically merge numerically nearby measurements. |

All other Step 1/Step 2 decisions remain in force where not superseded.

## R02. Change ledger

| Existing mechanism or rule | Treatment | Reason and practical effect |
|---|---|---|
| Proposal 4 characteristic blocks and scoped registries | Retain | Preserve accumulated useful encoding machinery. |
| Optional tail treated as separate from the everyday identifier | Repair | The full Spec ID must retain distinguishing extensions. |
| Registered sizes and bounded characteristic combinations | Retain | Legitimate dictionary entries are not arbitrary product lookups. |
| Supplier kit serialized as one long description | Remove | D3-001 requires separate component codes and a kit relationship. |
| Printed/unprinted base-spec distinction and proposed print fields | Supersede | D3-002 places printing in customization records. |
| Proposal 1 scope/layer principles | Adapt | Preserve location and order within a product without adopting an opaque payload. |
| Fixed empty layer positions | Do not introduce | D3-003 requires optional, extensible layer information. |
| Padded, implied-scale measurement fields and precision escape syntax | Replace | D3-004 uses direct compact values consistently. |
| Assumed units, approximate matching, or silent rounding | Remove | Exact quantities and explicit uncertainty remain authoritative. |
| Unlabelled dimension tuple | Repair | Named dimensions prevent invented measurement roles. |
| Colour assumed to prove bleaching | Reject inference | Existing `KR` supports unspecified bleaching; colour stays separate. |
| Role assumed to establish separate sale | Repair interpretation | Preserve known function without inventing saleability. |
| One feature slot losing additional bag features | Repair | Additional compatible features remain encoded. |
| Vendor SKU inside specification | Remove from spec | Keep it on the supplier-product record. |
| Specification equality treated as supplier-product identity | Repair | Several vendor offerings can share one objective description. |
| Global verification/approval interpretation | Apply Step 2 rules | Attribution, findings, and approvals stay scoped. |
| Dedicated sample-measurement workflow | Remove | D3-005 uses simple vendor sampling history. |
| New measurement automatically creating or merging specifications | Prevent | Source/context review and the approved duplicate check govern classification. |
| Old records losing their original associations | Repair | A17 defines stable references, revisions, and original-context retrieval. |
| Future code segments silently ignored | Reject | Unsupported meaning remains explicit; full decoding is required. |
| Historical lid-option splits | Reject unsupported splits | Source wording alone does not establish separate SKUs. |
| Historical CPET “missing token” example | Correct | The inspected registry already contains CPET treatment `C`. |
| Wider migration, pricing, permissions, and production work | Keep excluded/deferred | Preserve the agreed scope. |

## R03. Completion assessment

| Requirement | Documentation result |
|---|---|
| Settled business rules carried forward | Consolidated in Document 1. |
| Later approved changes integrated | Applied throughout all four documents, not left as detached amendments. |
| Meaningful coding requirement | Defined by the grammar, dictionaries, and complete examples in Document 2. |
| Kit correction | Component codes and separate kit references replace combined encoding. |
| Printing correction | Customization replaces base print fields and print-specific base IDs. |
| Sampling correction | Vendor-product history replaces the measurement workflow. |
| Measurement examples | Regenerated in the approved compact format. |
| Historical behavior | Defined for clarification, change, customization, commercial events, correction, sampling, and kits. |
| Acceptance coverage | All 24 cases retained and updated; all 20 D2 decisions accounted for. |
| Whole-design consistency | Checked across specification identity, vendor context, customization, kits, history, and duplicate prevention. |
| Implementation validation | Not performed or claimed. |

The examples now include a **24-character cup**, a **28-character more precise diameter example**, **19-character component codes**, and **41-character layer examples**.

These lengths describe the displayed illustrative cases, not universal maximums.

## R04. Source coverage

**Read fully during the Step 3 work:** Step 1 Results, Step 2 Results, original project brief, synthesis, reconciliation, evidence document, root/proposals README files, Proposal 4 specification and open questions, historical test battery, and UI design.

**Inspected selectively:** Proposal 1's fact model, parts/layers, canonicalization, evidence, matching, and history; relevant reasoning in Proposals 2 and 3; Proposal 4's registries/book, encoder/decoder, search, schema, evolution logic, and selected tests/reports.

**Workbook coverage:** Fixtures S1–S6 and relevant surrounding fields and headers. This was not an exhaustive review of both workbooks.

No complete historical implementation audit, production validation, or subscribed recovery inspection is claimed.

## R05. Step 4 implementation order

1. **Freeze the implementation baseline.** Use these four consolidated documents and export the initial versioned dictionary with their amendments applied.
2. **Build the revised encoder/decoder.** Test exact units, compact values, scopes, layers, unknowns, qualifiers, canonicalization, and unsupported entries.
3. **Implement the record relationships.** Separate objective specifications, supplier products, physical versions, customizations, kits, sources, sampling history, approvals, packing, and quotes.
4. **Implement intake and search.** Include existing-specification checking, explicit criteria, uncertainty, and separate capability results.
5. **Implement history and concurrent-change handling.** Reopen old quotes and approvals after each supported change.
6. **Run all 24 acceptance cases.** Use the inspected fixtures and clearly labelled illustrative cases. Record actual results.
7. **Verify recovery capability and cost, then restore a trial copy.** Include attachments and measure both data age and restoration duration.
8. **Review the results before migration or deployment.**

The implementation may expose defects in a proposed mechanism. Resolve them against the agreed behavior and record substantive changes. Do not silently weaken requirements or reopen settled business decisions without a demonstrated conflict.

## R06. Remaining validation gates

These do not represent missing business decisions or unfinished document consolidation:

- Encoder/decoder correctness.
- Search and comparison behavior.
- Correct preservation of historical context.
- Concurrent edits and dictionary allocation.
- The subscribed recovery arrangement and restore trial.
- Usability of the implemented forms and code displays.

The numeric-versus-alphanumeric comparison remains parked; it is not a prerequisite for implementing this baseline.

No implementation, migration, or deployment was performed in Step 3.

## R07. Delivery and next discussion

The user explicitly requested that all four final documents be collected into this Markdown file in the source package's `closing up` folder. This saving request authorizes the new file; it does not authorize rewriting Step 1, Step 2, the workbooks, or the reference implementation.

A separate workspace instruction file was saved earlier only because the user explicitly requested standing working preferences: evaluate changes against the whole design, and keep review moving with a focused question or the next substantive point.

**Step 3 is complete at the documentation level. The next phase is implementation and testing against this consolidated specification.**
