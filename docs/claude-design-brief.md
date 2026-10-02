# Source One Atlas — Claude Design brief

For the interface wolt / Claude Design.
Owner: flexi (lead builder). Last updated: 2026-10-02.

## 0. Read these first (not paraphrases — the authoritative sources)

Everything below is operational framing. Any design decision that affects
behavior must trace back to these sources, in this order of precedence:

1. `reference/atlas-step4c-0.3.1/reference/Step-3.md` — the four approved
   Step 3 documents. **Document 1 (A01–A22)** is the specification;
   **Document 2 (I01–I14)** is the identifier grammar and dictionary;
   **Document 3** is the acceptance set AT-01–24; **Document 4** carries the
   approved D3-001–006 review decisions and R02 change ledger.
2. `reference/atlas-step4c-0.3.1/Workflow-Reference.md` — the exact supported
   capture/review/commit, search criteria, phrase vocabulary, and evidence
   filters as currently implemented.
3. `reference/atlas-step4c-0.3.1/Step-4C-Results.md` §"AT-01–24 coverage" —
   what each acceptance case covers locally today versus what remains for the
   whole workflow.
4. `reference/atlas-step4c-0.3.1/README.md` for the CLI demonstration flow
   you'll be reinterpreting as a UI.

**Do not propose features that redesign Atlas.** Do not introduce AI
interpretation into basic search, duplicate detection, or data entry. Do not
collapse the three identities (specification / supplier product / physical
version). Do not add "verification badge" chrome where source attribution is
the rule.

## 1. The product in one paragraph

Atlas is the shared sourcing knowledge registry Source One uses to understand
client requests, retrieve candidate supplier offerings, assemble bounded
comparisons, record samples and approvals, and hand agreed work to operations.
Its identifiers (A1 Spec IDs) encode distinguishing product characteristics
through a published dictionary — not opaque catalogue numbers. The interface
exists to make source capture, review, commit, and retrieval visibly correct
and auditable; polish follows behavior, not the other way around.

## 2. Users and primary responsibilities

Three responsibilities, not three permission roles (D2-018):

- **Contributor** — captures source material from a quotation, catalogue,
  message, or verbal input. Preserves original wording, units, and the
  uncertainty they came in with. Does not fabricate missing facts.
- **Reviewer** — inspects a captured intake, decides whether an existing
  specification applies, a new one is needed, triage continues, a prior
  association needs clarification/correction, or a physical change creates
  a linked version. Writes the actor, reason, and evidence into the commit.
- **Pricing / operations consumer** — searches explicitly, inspects
  candidates against criteria with gaps and contradictions visible, and
  (eventually) hands an agreed supplier product + specification + evidence
  bundle to operations without pricing calculations inside Atlas.

A single person can hold any mix of these responsibilities; the UI should
avoid implying a privilege hierarchy.

## 3. Non-goals for this UI (keep out of scope)

- Pricing calculations, quantity-break math, currency conversions
- Any "approve" button that bypasses the sample / client / customization scope
- Universal verification badges, star ratings, confidence scores
- Automatic merging of nearby measurements, free-text similarity suggestions
- AI prose interpretation of search inputs (phrases are bounded; see §7)
- NetSuite / ERP connectivity, inventory, production execution
- Any mandatory LLM in basic data entry, search, or review

## 4. Chosen frontend stack

**Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS 4 + shadcn/ui.**
Deployed in the same Vercel project as the Python API (coexists with `api/*.py`).

Rationale:
- Industry-standard vocabulary Claude Design can draw against.
- Server components keep most data fetching close to the API routes.
- Tailwind + shadcn/ui gives a consistent token system without wrestling a bespoke design language — Claude Design can override tokens later.
- Deploys as a sidecar of the existing Python functions on Vercel.

Interim: the current M1 proof uses vanilla HTML/CSS/JS at the repo root
(`index.html`, `style.css`, `app.js`). This is a deployment smoke test, not a
visual prototype — ignore it as design input.

**No visual polish round yet.** Deliver component wireframes, interaction
specs, and a token system first. Hand off clickable prototypes that we wire to
the live API.

## 5. Core screens (M1 → M2 scope)

Each screen below maps to the current `atlas/workflow_cli.py` operations and
`atlas/search.py` query shape. If a UI element has no corresponding supported
operation, mark it as "future" or exclude it.

### 5.1 Intake capture (contributor view)

Supports `Intake.capture(document, actor, reason, provenance)`. Document fields
map directly: `label`, `kind` (supplier_statement | client_requirement),
`source` (title/URI/SHA/metadata), `locator` (worksheet+cells / page+paragraph
/ image region / message reference), `statements` (original wording +
uncertainty + optional supplied + interpretation + evidence_kind + per-statement
locator), `attachments` (URI + media type + hash + caption), optional engine
`facts`, `uncertainty_facts`, supplied `context`.

Must preserve:
- Original units/formulas/cached values literally (no silent arithmetic).
- Per-field uncertainty states: `not_supplied`, `explicitly_unknown`,
  `not_applicable`, `ambiguous`, `conflicting`, `unsupported`, `stated`.
- Attachments as references (URIs/hashes); no byte import at this stage.

Visible before the reviewer sees it: who captured it, when, from what source,
what was supplied vs. what the contributor interpreted.

### 5.2 Review preview (reviewer view)

Supports `Intake.preview(intake, facts?, uncertainty_facts?, ...)`. Must show:
- Full canonical A1 code for the interpreted facts.
- Readable characteristic descriptions.
- **Exact-equality candidates** (highlighted) vs. **matching candidates**
  (same supported facts, different additional facts).
- **Known contradictions** flagged distinctly from gaps.
- Per-criterion differences for every candidate (which fact agrees, which
  is a gap, which contradicts).
- Full before/candidate facts including OTHER slots (`OT:` explanations),
  scoped layers, unresolved wording (`UT:`), qualifiers (`QC`, `TO`).
- An editable alternative preview path: changing facts creates another
  immutable preview rather than mutating the original.

Must NOT:
- Imply a candidate is a match merely because measurements are close.
- Transfer a candidate's samples/approvals to the proposed offering.
- Hide incompatibility of a known OTHER explanation.

### 5.3 Commit decision (reviewer view)

Supports `Intake.commit(preview, decision, actor, reason, provenance)`.
`confirmed: true` is required and the commit is immutable. Decision actions:
`triage`, `specification`, `offering`, `clarification`, `correction`,
`physical_change`, `add_information`, `request`. The UI must distinguish
these clearly — each has distinct downstream history semantics (A17 H01–H10)
and distinct required fields (see Workflow-Reference §"Reviewed decisions").

Required visible fields regardless of action: actor, reason, evidence (one
or more assertion IDs from the intake), optional `selected_specification`
with its full `supported_code`. A broad match alone is explicitly rejected
by the backend — the UI must either present a complete explicitly-supported
candidate or route to a new preview.

Retry safety: submitting the same decision + evidence + preview returns the
same decision IDs (no duplicate). Changed payload for the same preview
fails. Design feedback for both cases.

### 5.4 Search (consumer view)

Supports `Search(store).search(query)`. The query shape is fully specified in
Workflow-Reference §"Structured query"; mirror it exactly. Key constraints:

- Only selected criteria restrict results. The UI must never silently add
  criteria the user did not pick.
- Each criterion needs a satisfies / gap / contradiction explanation per
  candidate. Contradictions dominate gaps.
- Result types shown separately: `specification`, `offering`, `kit`,
  `capability`, `triage`. No fuzzy score; no proximity sort.
- Evidence filters (quotation, photos, sampling, approval, kit_membership)
  apply to supplier-specific context and never fabricate transferred
  evidence across suppliers.
- `historical: true` returns older associations/versions, explicitly labelled
  `current: false`.
- An empty result set is distinguishable from an error or an unsupported
  query. Status codes: `ok`, `unsupported`, `error`.

Design implications: show criteria as discrete chips, each with a
"required / optional / excluded" state. Explanations attach to the row, not
only to the header. Capabilities visually distinct from existing products.

### 5.5 Phrase review (consumer view)

Supports `Phrases.propose → confirm → execute`. The bounded vocabulary is
listed in Workflow-Reference §"Reviewed phrases" — reproduce that list verbatim
in a `?` panel. The UI must:

- Show the original phrase character spans.
- Highlight unsupported/ambiguous spans in-place; the reviewer can
  acknowledge them without pretending they were interpreted.
- Make the editable proposed criteria obviously an interpretation, not fact.
- Require a persisted confirmation before execute.
- Never silently drop punctuation or guess units.

### 5.6 Record detail (any view)

Pulling together `Store.history` returns the original graph, every preview,
every decision. Show a timeline that labels each entry with its event type
(H01 clarification, H02 physical change, H03 printing/artwork, H04 packing,
H05 commercial, H06 error/disproved, H07 misplaced approval, H08
merge/separation, H09 sampling iteration, H10 kit composition change).

Earlier quotes/approvals must display in their original context with any
subsequent correction visibly labelled rather than silently rewritten (A17).

## 6. Visible invariants (design must enforce these)

- The three identities are visibly distinct: `specification` icons/surfaces
  never substitute for `supplier product` or `physical version`.
- Spec IDs are always displayed as **copyable, complete codes**. Previews
  may show a shortened form **labelled as a preview**; copy must return the
  full string (A22).
- Unknown is first-class — never collapsed to blank or interpreted as "no".
- Source attribution shows alongside every assertion (A06). No universal
  verification badge. If a UI element reads "verified", it means
  "transcription verified from the source document", not "product truth".
- Printing / customization UI lives beneath an offering, not on the base
  spec card. Supplier kits show components with their own Spec IDs; no
  combined kit Spec ID (D3-001).
- "12 unresolved supplier-product associations in the preserved batch" is
  surfaced in the search results for that batch — do not hide them.

## 7. Data flow and API

- Backend: Python 3.12 serverless functions at `/api/*`. See `api/*.py` in the
  repo for current M1 endpoints; the production endpoints will mirror
  `atlas/workflow_cli.py` sub-commands under paths like `/api/intake/capture`,
  `/api/intake/preview`, `/api/intake/commit`, `/api/search`, `/api/phrases/*`,
  `/api/records/*`. Contracts are strict JSON shapes defined by the
  preserved `atlas/*.py` modules.
- Database: Supabase Postgres via trusted service only. The browser must
  never write directly to Atlas tables — RLS rejects anon writes. The
  frontend obtains the public Supabase URL + anon key only for read-only
  reflection (not required for most views).
- Attachments: Supabase Storage, write via trusted service. URIs returned to
  the browser; the browser renders previews.

## 8. Deliverables requested (first round)

1. **Component inventory** mapped to the operations in §5 — one component
   per supported action, no speculative widgets.
2. **Interaction specs** for intake capture → preview → commit (the single
   most important flow). Include empty, loading, error, retry, and conflict
   states.
3. **Search result row** spec showing match / gap / contradiction
   per-criterion explanations without taking visual priority over the
   candidate itself.
4. **History timeline** component covering H01–H10 events.
5. **Design token system** (color, type, spacing, elevation). Tailwind
   theme or CSS variables.
6. **Three screens** fully specified as clickable prototypes:
   intake capture, review preview, search results. Hand off as linkable
   artifacts (Figma / Claude Design / HTML).

## 9. Not requested yet

- Marketing site, landing, dashboards, analytics, admin, permissions UI.
- Visual branding, logo, iconography beyond functional icons.
- Mobile-specific layouts (desktop-first; responsive later).
- Dark mode (deferred).
- Animations beyond state transitions needed for feedback.

## 10. How to work with flexi

- Open questions and conflicts → file them against the Workflow-Reference /
  Step-3 citations so the discussion stays grounded.
- When a design element has no backend contract, flag it and we define the
  contract before the UI assumes it exists.
- Avoid redesigning Atlas semantics in the UI; propose them to flexi who
  owns integration decisions and surfacing to the product owner.
