# Source One Atlas — Step 4C 0.3.1

Persistent intake, review and explicit-criteria search, extending records **0.2.1**, engine **0.1.1**, and dictionary **A1 / 0.1.0-local-candidate**. Standard-library Python and local SQLite; no installation, AI or network required. Executed on Python 3.9.6 / SQLite 3.43.2.

## Verify and run

Open a terminal in this extracted package. Verify before running generators, which refresh reports:

```sh
python3 verify_package.py
python3 run_step4c_tests.py
```

The combined runner executes **146 tests: 84 inherited + 42 original Step 4C + 20 repair regressions**, checks all **44 unchanged known answers**, and verifies 14 pinned inherited files plus the repair-specific protected files. See `Repair-0.3.1-Notes.md` for the four reproduced defects and before/after evidence. Original commands remain available; `python3 run_all_tests.py` intentionally runs only the inherited 84. `python3 -m unittest discover -s tests -v` runs all tests without generating reports.

## End-to-end CLI demonstration

This creates a new, explicitly illustrative database and calls the real CLI in separate processes for capture, preview, commit, retry, search, phrase review, confirmation, execution and historical retrieval:

```sh
python3 tools/step4c_demo.py --out work/my-first-demo
```

Use a fresh directory each time. Existing directories are preserved. Every JSON input and actual output is saved for inspection. Expected: exact existing description reused; one new illustrative offering; retry creates no duplicate; approval narrowing returns two matches and one offering needing evidence. The new offering has no fabricated quote, sample or approval.

A completed run is bundled in `examples/step4c-demo/`. Inspect its preview before submitting the already-reviewed decision again:

```sh
python3 -m json.tool examples/step4c-demo/02-preview-output.json
python3 -m atlas.workflow_cli --db examples/step4c-demo/atlas.sqlite commit examples/step4c-demo/03-commit-input.json
python3 -m atlas.workflow_cli --db examples/step4c-demo/atlas.sqlite search examples/step4c-demo/05-browse-input.json
python3 -m atlas.workflow_cli --db examples/step4c-demo/atlas.sqlite search examples/step4c-demo/06-narrow-input.json
```

The repeated commit returns `repeated: true` and its original record IDs. Demonstration decisions are synthetic; they are not source-backed product claims.

For a new review, copy and edit the demo's `01-capture-input.json`, then run:

```sh
python3 -m atlas.workflow_cli --db work/my-first-demo/atlas.sqlite capture work/my-first-demo/01-capture-input.json
```

Use the returned intake ID in a preview input of the form `{"intake":"ID","actor":"Reviewer","reason":"Review supplied evidence"}`. `preview` returns complete codes, readable characteristics, equality indicators, per-criterion comparisons and complete before/candidate facts. Copy its preview ID and the intake's assertion IDs into a commit input. `Workflow-Reference.md` defines every supported decision. A commit requires `confirmed: true`; printing a preview never commits a specification or offering.

The bundled demo's IDs are in `examples/step4c-demo/summary.json`. Retrieval commands accept those IDs:

```sh
python3 -m atlas.workflow_cli --db examples/step4c-demo/atlas.sqlite intake-history INTAKE_ID
python3 -m atlas.workflow_cli --db examples/step4c-demo/atlas.sqlite execute-phrase CONFIRMATION_ID
python3 -m atlas.workflow_cli --db examples/step4c-demo/atlas.sqlite inspect RECORD_ID
```

## Preserved source batch

The untouched example contains 12 source/triage records, ten encoded descriptions referencing nine specifications, two unresolved descriptions, and **zero resolved supplier products**:

```sh
python3 -m atlas.records_cli --db examples/reviewed-batch.sqlite list triage
python3 -m atlas.workflow_cli --db examples/reviewed-batch.sqlite search fixtures/search-bags.json
python3 -m atlas.workflow_cli --db examples/reviewed-batch.sqlite search fixtures/search-laminates.json
```

To import the preserved batch into a fresh database, run `python3 -m atlas.records_cli --db work/source.sqlite import-reviewed`. That inherited batch loader is deliberately not a general deduplicating importer; run it once per fresh database. Reviewed **intake commits** have retry protection.

“Verified” means accurately transcribed from its quotation source. Source statements do not establish truth, availability, performance, fit or approval. Formula/cached-value separation, discrepancies, V962/V963 shared base, and V993/V1143 unresolved cases remain intact.

## Interfaces and scope

- `Intake(store).capture`, `.preview`, `.commit`, `.history`: persistent source/review operations.
- `Search(store).search(query)`: structured query, returning `ok`, `unsupported`, or `error`; results classify as `match`, `potential`, or `contradiction`.
- `Phrases(store).propose`, `.confirm`, `.execute`: bounded reviewed phrase interpretation.
- Existing `Store` APIs and `atlas.records_cli` retain their record/revision/history contracts. See `reference/Step-4B-README.md` and `Relationships.md`.

Read `Workflow-Reference.md` for supported criteria and decisions, `Step-4C-Results.md` for actual coverage and limitations, and `Next-Stage-Handoff.md` before extending the package. No deployment, shared editing, recovery trial or all-24-workflow certification is claimed.
