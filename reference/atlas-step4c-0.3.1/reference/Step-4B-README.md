# Atlas Step 4B — persistent records 0.2.1

Runnable local relationship layer around the unchanged **0.1.1 engine** and **A1 / 0.1.0-local-candidate dictionary**. The complete Spec ID remains the meaningful identifier; storage UUIDs only identify records. No deployment or live service is involved. This patch supersedes records 0.2.0; the original delivery is preserved. See `Repair-0.2.1-Notes.md` for reproduced defects and before/after evidence.

## Run

Use Python with the standard-library `sqlite3` module and SQLite JSON support. No package installation is needed. The delivered run used Python 3.9.6 / SQLite 3.43.2; Python 3.10+ remains the baseline's recommended runtime. Open a terminal in this package directory.

```sh
python3 run_all_tests.py
python3 -m atlas.records_cli --db local.sqlite init
python3 -m atlas.records_cli --db local.sqlite import-reviewed
python3 -m atlas.records_cli --db local.sqlite list triage
```

`run_all_tests.py` reruns all 47 original tests, compares all 44 known answers and baseline file hashes, and runs the 25 original on-disk relationship tests plus 12 repair regressions (84 tests total). It rewrites only test reports inside this package. Exit status is nonzero on failures. For tests without report writes:

```sh
python3 -m unittest discover -s tests -v
```

Keep illustrative scenarios in a separate database:

```sh
python3 -m atlas.records_cli --db demo.sqlite demo
python3 -m atlas.records_cli --db demo.sqlite apply fixtures/create-offering.json
```

The first command returns IDs for two illustrative suppliers and their independent products, samples, quotations and approvals. `apply` accepts an explicit JSON operation plan and rolls the whole plan back on failure. The supplied plan labels every invented record as illustrative. `$name` references an earlier result in that plan. Supported operations are `add`, `register_dictionary`, `issue`, `change_association`, `revise`, `correct_approval` and `resolve_identity`; their arguments match `Store` below. There is no prose interpretation or automatic product creation.

Use an ID from the output with these retrieval commands:

```sh
python3 -m atlas.records_cli --db demo.sqlite history RECORD_ID
python3 -m atlas.records_cli --db demo.sqlite product-history PRODUCT_ID
python3 -m atlas.records_cli --db demo.sqlite sampling-history SEQUENCE_ID
python3 -m atlas.records_cli --db demo.sqlite memberships VERSION_ID
python3 -m atlas.records_cli --db demo.sqlite current-association VERSION_ID
```

`get ID` retrieves one record; `list KIND` retrieves a record type. `history` returns the immutable original graph, separately labelled `later_corrections` and `later_revisions`, and the root's active/withdrawn indication. `correction_provenance` separately exposes incoming H07 events, predecessor approval contexts, original approval documents and correction notes, with explicit per-approval active/withdrawn status. It is available from a replacement approval and from a handoff referencing it. It does not substitute today's association into an earlier quote. Sampling retrieval includes notes, photo references, revision requests and scoped decisions. Kit history expands its component associations and complete codes. `memberships` provides the reverse lookup, including historical revisions.

Two ready-to-inspect stores are included: `examples/reviewed-batch.sqlite` and `examples/illustrative.sqlite`. Their record IDs are in the adjacent JSON files. The illustrative store includes a clarification and a withdrawn approval to demonstrate historical retrieval. These databases are examples; tests use isolated temporary stores. Run import/demo once per fresh database; repeated imports are not a general deduplicating intake workflow.

## Python operations

```python
from atlas.records import Store
from atlas.demo import illustrative

with Store('my-demo.sqlite') as store:
    ids = illustrative(store)  # explicitly synthetic
    meta = dict(actor='Local reviewer', reason='Illustrative clarification',
                provenance='illustrative')
    precise = store.issue('A1!APTX.CUB.XXX.M500.R98_125',
                          ids['dictionary'], **meta)
    change = store.change_association(
        ids['A']['association'], precise, event_type='H01',
        evidence=[ids['evidence']], **meta)
    old_quote = store.history(ids['A']['quote'])
    assert ids['A']['association'] in old_quote['original_context']
    assert change['record'] not in old_quote['original_context']
```

`Store.add(kind, data, links, actor=..., reason=..., provenance=..., effective_at=None)` is the typed construction API. See the compact `CONTRACTS` declarations in `atlas/records.py` for all required and optional fields, edge types and cardinalities. Links use existing record IDs, as one ID or a list; an empty list omits an optional link. Unknown fields, missing required edges, invalid targets and inconsistent contexts are rejected. Unknown business facts belong in explicit assertion states, not guessed values. `data` holds supplied literal content; use typed links for relationships.

Use `with store.transaction():` around dependent multi-record writes. `revise(old, new_data, evidence=[...], links={...}, **meta)` supplies a **complete replacement payload**, creates the linked immutable revision and records its H02/H03/H04/H05/H09/H10 event in one transaction. For a physical change, create its version and association inside one outer transaction. Sample V2 uses `revise` on a sample, never on a physical version or kit revision. A sampling sequence requires exactly one `product` or `kit` link. Each sample context pins the applicable physical version/association or exact kit revision; kit samples use the existing notes, evidence, acceptance and approval operations. A changed kit revision gets a new context and new quote; commercial revisions cannot move a quote to another product/version or kit revision.

`correct_approval(old, evidence=[...], destination=context_id, sample=sample_id, **meta)` withdraws a wrong association and creates the supported replacement atomically. The replacement retains the actual approval evidence; the H07 event holds the correction evidence. Successive corrections retain a retrievable chain without making former associations valid again. Omit destination to retain an unresolved destination without guessing. `resolve_identity` appends an explanation referencing explicitly classified identity evidence; it never destructively merges identities or moves evidence. `same_context` compares exact version/kit revision, association, customization and packing links plus client/request/job scope resolved through the job/request. Redundant explicit links are equivalent; missing-versus-known or genuinely different scope is not. `referring(id, role=None, kind=None)` retrieves reverse links, including SKU history and source findings. `compatibility(left_version, right_version)` returns claims and confirmations for exactly that pair.

The original encoding CLI remains unchanged:

```sh
python3 -m atlas --dictionary dictionary/atlas-A1-0.1.0.json encode fixtures/cup.json
```

Its full usage is preserved in `reference/Step-4A-README.md`.

## Storage and next stage

`schema/sqlite.sql` is the executed local schema. `Relationships.md` explains the typed records, ownership, revisions, historical retrieval and intended Postgres mapping. `schema/postgres-candidate.sql` is an **unexecuted translation**, not an installed Supabase migration. The planned Supabase/Postgres, Vercel and GitHub direction is unchanged. A trusted write service and eventual database-backed workflow checks must carry these contracts forward before exposing writes to shared clients.

Read `Step-4B-Results.md` for exact results, acceptance boundaries and the next-stage handoff. `manifest.json` covers every delivered file except itself; `verify_package.py` verifies its hashes. Regenerating reports or modifying the example databases intentionally changes those hashes. The retained Step 4A reports are historical engine evidence, not current descriptions of Step 4B scope.
