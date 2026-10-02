# Source One Atlas

Shared sourcing knowledge registry — specifications, supplier products, source evidence, requests, comparisons, samples, approvals, history.

## Current baseline

Workflow **0.3.1** / Records **0.2.1** / Engine **0.1.1** / Dictionary **A1 / 0.1.0-local-candidate**.

- Preserved behavioral reference: `reference/atlas-step4c-0.3.1/` (DO NOT MODIFY — verified against SHA-256 `4bd81d33e98e8ebf8e260f9b815d175ffc001f4ba8c477e5d1cfd0dea7a77894`).
- Full test suite (146 tests, 0 failures, 44 known answers unchanged) must stay green on every change.

Run baseline from the repo:

```sh
python3 scripts/run_reference_baseline.py
```

Verify preserved reference hasn't drifted:

```sh
cd reference/atlas-step4c-0.3.1 && python3 verify_package.py
```

## Layout

```
Atlas/
├── reference/atlas-step4c-0.3.1/   # Preserved behavioral reference (read-only)
├── service/                         # Production Python service wrapping the engine
├── api/                             # Vercel Python serverless functions
├── web/                             # Static frontend (M1 proof)
├── scripts/                         # Dev / CI helpers
└── tests/                           # Service-layer tests (reference suite runs separately)
```

## Hosting

- **Compute:** Python 3.12 serverless functions on Vercel (`api/*.py`)
- **Frontend:** Static HTML+JS at `web/` for M1 proof; dedicated UI stack follows the Claude Design brief
- **Database:** Supabase Postgres via transaction pooler (port 6543), accessed server-side only through a trusted Python service
- **Storage:** Supabase Storage for attachments (not yet wired)

## Core invariants (specialists MUST read source rules in `reference/atlas-step4c-0.3.1/Step-3.md` AND `reference/atlas-step4c-0.3.1/Workflow-Reference.md`)

- Spec ID encodes distinguishing characteristics via the A1 dictionary. Never substitute an opaque catalogue number, hash, or short label + lookup.
- `specification` ≠ `supplier product` ≠ `physical version`. Matching specs do NOT establish shared identity, compatibility, or approval.
- Printing/customization and supplier kits live OUTSIDE the base Spec ID (D3-001, D3-002).
- Source capture ≠ review ≠ commit. All three are separate operations.
- Unknown is neither yes nor no (A05). Supplier claims never become verified product claims.
- Source attribution, not universal verification badges (A06). Approvals retain explicit scope.
- Immutable history (A17 H01–H10). Associations change through recorded events.
- Phrase interpretation is bounded, editable, confirmed (D2-014). No mandatory LLM in basic operations.
- Preserved batch has **12 unresolved supplier-product associations** — do NOT resolve by assumption.
- The included `reference/atlas-step4c-0.3.1/schema/postgres-candidate.sql` is UNEXECUTED and does NOT by itself enforce the Python application contracts.

## M1 proof scope (in progress)

- Minimal frontend calling the deployed Python service, reproducing representative known-answer results
- Python 3.12 (pinned via `.python-version`); baseline rerun on the pinned runtime
- Authenticated, transactional Supabase write + read through the trusted service: rollback, retry safety, unauthorized-write rejection
- Durable records + dictionary allocations in Supabase (never function memory or local files)
