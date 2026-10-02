# Atlas Step 4A — local implementation candidate 0.1.1

This patch supersedes implementation 0.1.0. The A1 dictionary remains `0.1.0-local-candidate`, unchanged. See `Repair-Notes.md` for the two fixes and 47-test result.

Python 3.10+; standard library only. No installation, network, database or product catalogue is needed. Open a terminal in this folder.

```sh
python3 -m atlas --dictionary dictionary/atlas-A1-0.1.0.json encode fixtures/cup.json
python3 -m atlas --dictionary dictionary/atlas-A1-0.1.0.json decode 'A1!APTX.CUB.XXX.M500.R98_125'
python3 run_tests.py
```

The first command returns `A1!APTX.CUB.XXX.M500.R98_125`. Decode returns complete structured facts and readable statements. The test command regenerates `Test-Results.md` and `test-results.json`; failures produce a nonzero exit status. To run without writing reports:

```sh
python3 -m unittest discover -s tests -v
```

Read `Step-4A-Results.md` for scope and acceptance coverage, `Encoding-Report.md` for all 12 selected source records, and `dictionary/REFERENCE.md` for vocabulary. `dictionary/atlas-A1-0.1.0.json` is the self-contained dictionary release. `reference/` contains unchanged reference copies, not executable instructions. `fixtures/verified-batch.json` preserves cells, formulas, cached values, supplier merge context, mapping decisions and independently specified expected codes. Worked W01–W08 inputs and known answers are in `tests/test_engine.py`; they are illustrative, not workbook transcriptions.

## Interface

```python
from atlas import Engine, SpecError
engine = Engine("dictionary/atlas-A1-0.1.0.json")
code = engine.encode({"fields": {"MA": "APTX", "AR": "CUX",
                              "CA": {"value": "0.5", "unit": "L"}}})
facts = engine.decode(code)
readable = engine.describe(code)
comparison = engine.compare(code, code)
```

Each node has `fields` and optional `groups`. Root block fields are `MA`, `AR`, `CF`, `CA`, `FI`; unspecified root blocks become unknown. Child nodes have the same fields but inherit nothing. Child block values that only repeat unknown are omitted. The root's blocks are serialized before `+`; duplicating them after `+` is invalid.

- A named scope is `{"scope":"INSIDE","node":{"fields":{"CL":"WHITE"}}}`.
- A layer stack is `{"direction":"X","layers":[{"fields":{"MA":"BKRX"}},{"fields":{"MA":"APTX"}}]}`. `O` means outside to inside; structured input also accepts `I` and reverses it. `X` sorts a multiset and retains repeats.
- Exact measurements accept integers or strings, never floats. A `{value,unit}` object performs an exact conversion. A bare numeric intrinsic field is already in its dictionary canonical unit; explicit unit objects are preferable for source mapping. Core CA/FI accept encoded blocks or explicit unit objects, never bare quantities with guessed roles.
- A two-element value list is a closed interval. `DM` is a map of registered names to exact measurements.
- `QC` is a list of `[target,mode,basis,condition]`; `TO` is a list of `[target,minus,plus]`. A tolerance offset can also be an explicit unit object. Conditions are exact Unicode text; `-` means absent.
- `OT` and `UT` are lists of `[target,exact text]`. Do not insert an entire record, SKU or commercial context into unresolved text. Such classification is an intake responsibility.
- Enum tokens are exact dictionary tokens; no unregistered synonym inference. List and FX values are arrays. Free text preserves case and Unicode spelling; structural punctuation is escaped.
- `X`/`XX` means unknown. `0`/`00` is accepted only where registered. Python `None` is not an implicit NA instruction. Numeric zero never becomes NA.

`canonicalize` accepts a supported structured description or noncanonical A1 string and returns the canonical complete code. `decode`/`validate` require already canonical spelling and reject unsupported suffixes. `compare` compares complete canonical descriptions. `compare_measurement(request,candidate,target)` compares compatible local numeric contexts, reports gaps, and uses interval containment; it does not establish fit or interchangeability. Scope-specific measurement comparison can be made by supplying the explicitly selected local fields as nodes; no automatic parent inheritance.

The CLI also exposes `validate`, `canonicalize` and `compare`. Every CLI operation requires `--dictionary`; no silent newest-release selection. Issue records should retain the dictionary release returned by decode/validation. IDs themselves have the approved A1 namespace, not an invented release segment.

`check_compatible(old_dictionary,new_dictionary)` checks old definitions and rules before compatible additions. This is a local compatibility check, not an atomic multi-user allocation service. Retired tokens remain decodable. Semantic rule changes are rejected for namespace review.

Misplaced fields, conflicts and unsupported input raise `SpecError`; CLI errors return status 2 and `complete:false`. The caller retains its original input. Limits are 100,000 characters and 32 nested groups; excess fails explicitly. No shortened ID is accepted as the complete original. This is a resource guard, not an approved maximum business length.
