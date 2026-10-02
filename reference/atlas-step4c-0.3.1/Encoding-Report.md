# Verified workbook — selected Step 4A encoding batch

The user confirmed transcription accuracy. This report does not independently verify supplier claims, performance, fit or approvals. The source workbook remains unchanged.

Selected: 12 records across 16 physical rows, of which 13 contain values. Ten descriptions encoded; two records retained in triage with no resolved association. All selected continuation rows are accounted for.

Main Table has 1100 nonempty rows after headers, 1072 nonempty description cells and a formatted extent of 1860 rows. Outside this batch, 1087 nonempty rows and 1060 nonempty description cells remain for mapping/boundary review. These are row counts, not asserted product counts. No full migration is claimed.

Rows 1–3 are grouped headers. D2 says Category and E2 says Material, but early selected rows put material in D and product type in E. Mapping uses contents. Supplier values are taken only from an explicit cell or the merged range containing that row; no fill-down across unrelated sections.

Formula text and workbook cached results are preserved separately; caches were not recalculated or certified. All supplied original cells are in fixtures/verified-batch.json.

| Record | Source rows | Outcome |
|---|---|
| V4 | 4–4 | Encoded incomplete supported description |
| V7 | 7–7 | Encoded incomplete supported description |
| V18 | 18–18 | Encoded incomplete supported description |
| V961 | 961–961 | Encoded incomplete supported description |
| V962 | 962–962 | Encoded incomplete supported description |
| V963 | 963–963 | Encoded incomplete supported description |
| V993 | 993–997 | Triage; no resolved ID |
| V1000 | 1000–1000 | Encoded incomplete supported description |
| V1088 | 1088–1088 | Encoded incomplete supported description |
| V1141 | 1141–1141 | Encoded incomplete supported description |
| V1142 | 1142–1142 | Encoded incomplete supported description |
| V1143 | 1143–1143 | Triage; no resolved ID |

## V4 — Main Table rows 4–4

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A4 | Sowinpak | supplied |
| B4 | CN | supplied |
| C4 | 6oz Clear PS Dome Lids | supplied |
| D4 | Plastic - PS | supplied |
| E4 | Bowl Lid | supplied |
| F4 | 90 | supplied |
| G4 | 3.3g | supplied |
| H4 | 1000 | supplied |
| I4 | 50 | supplied |
| J4 | 20 | supplied |
| K4 | 4 | supplied |
| L4 | 490 | supplied |
| M4 | 205 | supplied |
| N4 | 485 | supplied |
| O4 | 0.01281 | supplied |
| P4 | 12.81 | supplied |
| Q4 | 92232 | supplied |
| R4 | 3500 | supplied |
| S4 | 20 | supplied |
| T4 | 14 days | supplied |
| U4 | 30 days | supplied |

Supplier context: {"A": {"source": "A4", "value": "Sowinpak", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B4", "value": "CN", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- D identifies PS, E and C identify bowl closure; role X does not assert separate sale.
- Clear becomes optical class. G explicitly supplies grams. F header supplies mm but no dimension role; not promoted to rim.
- 6oz is a lid trade designation, not lid capacity. Half Dome remains unresolved rather than equated to Dome.

### Structured facts and result

```json
{
  "fields": {
    "MA": "APSX",
    "AR": "BWX",
    "FR": "CLOSURE",
    "OP": "CLEAR",
    "GW": {
      "value": "3.3",
      "unit": "g"
    },
    "NC": "6oz",
    "UT": [
      [
        "DM",
        "90 mm; dimension role unspecified"
      ]
    ],
    "LP": "D"
  }
}
```

Complete generated Spec ID:

```text
A1!APSX.BWX.XXX.X.X+FR:CLOSURE.GW:3_3.LP:D.NC:6oz.OP:CLEAR.UT:DM=90%20mm%3B%20dimension%20role%20unspecified
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Polymer; PS (polystyrene, general purpose); UNKNOWN treatment
- product: article = Bowl; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Functional role = "CLOSURE"
- product: Unit weight = "3_3" g
- product: Lid profile = dome lid
- product: Nominal capacity as quoted = "6oz"
- product: Optical class = "CLEAR"
- product: Unresolved specification statements = [["DM", "90 mm; dimension role unspecified"]]

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H4",
    "I4",
    "J4",
    "K4",
    "L4",
    "M4",
    "N4",
    "O4",
    "P4",
    "Q4",
    "R4",
    "S4",
    "T4",
    "U4"
  ],
  "supplier": {
    "A": {
      "source": "A4",
      "value": "Sowinpak",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B4",
      "value": "CN",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Saleability, treatment, measurement role and ounce standard not supplied.

## V7 — Main Table rows 7–7

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| C7 | 6oz Clear PS Half Dome Lids | supplied |
| D7 | Plastic - PS | supplied |
| E7 | Bowl Lid | supplied |
| F7 | 90 | supplied |
| G7 | 3.3g | supplied |
| H7 | 1000 | supplied |
| I7 | 50 | supplied |
| J7 | 20 | supplied |
| K7 | 4 | supplied |
| L7 | 490 | supplied |
| M7 | 205 | supplied |
| N7 | 485 | supplied |
| O7 | 0.01281 | supplied |
| P7 | 12.81 | supplied |
| Q7 | 92232 | supplied |
| R7 | 3500 | supplied |
| S7 | 20 | supplied |
| T7 | 14 days | supplied |
| U7 | 30 days | supplied |

Supplier context: {"A": {"source": "A4", "value": "Sowinpak", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B4", "value": "CN", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- D identifies PS, E and C identify bowl closure; role X does not assert separate sale.
- Clear becomes optical class. G explicitly supplies grams. F header supplies mm but no dimension role; not promoted to rim.
- 6oz is a lid trade designation, not lid capacity. Half Dome remains unresolved rather than equated to Dome.

### Structured facts and result

```json
{
  "fields": {
    "MA": "APSX",
    "AR": "BWX",
    "FR": "CLOSURE",
    "OP": "CLEAR",
    "GW": {
      "value": "3.3",
      "unit": "g"
    },
    "NC": "6oz",
    "UT": [
      [
        "DM",
        "90 mm; dimension role unspecified"
      ],
      [
        "LP",
        "Half Dome"
      ]
    ]
  }
}
```

Complete generated Spec ID:

```text
A1!APSX.BWX.XXX.X.X+FR:CLOSURE.GW:3_3.NC:6oz.OP:CLEAR.UT:DM=90%20mm%3B%20dimension%20role%20unspecified,LP=Half%20Dome
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Polymer; PS (polystyrene, general purpose); UNKNOWN treatment
- product: article = Bowl; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Functional role = "CLOSURE"
- product: Unit weight = "3_3" g
- product: Nominal capacity as quoted = "6oz"
- product: Optical class = "CLEAR"
- product: Unresolved specification statements = [["DM", "90 mm; dimension role unspecified"], ["LP", "Half Dome"]]

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H7",
    "I7",
    "J7",
    "K7",
    "L7",
    "M7",
    "N7",
    "O7",
    "P7",
    "Q7",
    "R7",
    "S7",
    "T7",
    "U7"
  ],
  "supplier": {
    "A": {
      "source": "A4",
      "value": "Sowinpak",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B4",
      "value": "CN",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Saleability, treatment, measurement role and ounce standard not supplied.

## V18 — Main Table rows 18–18

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A18 | Paharpur 3P | supplied |
| B18 | India | supplied |
| C18 | 20 Serve Mylar Bags | supplied |
| D18 | Stand up Pouch | supplied |
| E18 | / | supplied |
| F18 | 216 x 278 x 76mm | supplied |
| G18 | / | supplied |
| H18 | 1000 | supplied |
| I18 | 5800 | supplied |
| J18 | / | supplied |
| K18 | / | supplied |
| L18 | 450 | supplied |
| M18 | 330 | supplied |
| N18 | 220 | supplied |
| O18 | =P18/H18 | formula / cached None |
| P18 | 76.15 | supplied |
| Q18 | / | supplied |
| R18 | / | supplied |
| S18 | / | supplied |
| T18 | / | supplied |
| U18 | / | supplied |

Supplier context: {"A": {"source": "A18", "value": "Paharpur 3P", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B18", "value": "India", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- Mylar maps to retained J/MP; Stand up Pouch supplies PO and stand-up gusset S.
- 20 Serve stays a trade designation; no count-capacity inference.
- O18 formula and cached result retained separately; no recalculation or quote correction.

### Structured facts and result

```json
{
  "fields": {
    "MA": "JMPX",
    "AR": "POX",
    "CF": "XXS",
    "NC": "20 Serve",
    "UT": [
      [
        "DM",
        "216 x 278 x 76mm; dimension roles unspecified"
      ]
    ]
  }
}
```

Complete generated Spec ID:

```text
A1!JMPX.POX.XXS.X.X+NC:20%20Serve.UT:DM=216%20x%20278%20x%2076mm%3B%20dimension%20roles%20unspecified
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Multi-Material Laminate; Metallized polyester laminate (mylar); UNKNOWN treatment
- product: article = Pouch; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; stand-up gusset
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Nominal capacity as quoted = "20 Serve"
- product: Unresolved specification statements = [["DM", "216 x 278 x 76mm; dimension roles unspecified"]]

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H18",
    "I18",
    "J18",
    "K18",
    "L18",
    "M18",
    "N18",
    "O18",
    "P18",
    "Q18",
    "R18",
    "S18",
    "T18",
    "U18"
  ],
  "supplier": {
    "A": {
      "source": "A18",
      "value": "Paharpur 3P",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B18",
      "value": "India",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- No exhaustive layers, order or named dimension roles supplied.

## V961 — Main Table rows 961–961

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A961 | MPC Paper | supplied |
| B961 | Canada | supplied |
| C961 | Large Cookie Bag | supplied |
| D961 | Paper Container | supplied |
| E961 | Bleached / White Kraft | supplied |
| F961 | 7.5 (H) x 5.75 (W) x 1.375 (G) inches | supplied |
| G961 | 30gsm | supplied |
| H961 | 1500 | supplied |
| L961 | 9 | supplied |
| M961 | 5.5 | supplied |
| N961 | 12 | supplied |
| P961 | 72 | supplied |

Supplier context: {"A": {"source": "A961", "value": "MPC Paper", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B961", "value": "Canada", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- C identifies bag despite generic D category. E explicitly states Bleached / White Kraft, supporting KW.
- F explicitly labels H/W/G and inches: exact conversion; G supplies basis weight.

### Structured facts and result

```json
{
  "fields": {
    "MA": "BKWX",
    "AR": "BGX",
    "DM": {
      "HEIGHT": {
        "value": "7.5",
        "unit": "in"
      },
      "WIDTH": {
        "value": "5.75",
        "unit": "in"
      },
      "GUSSET": {
        "value": "1.375",
        "unit": "in"
      }
    },
    "GS": {
      "value": "30",
      "unit": "gsm"
    }
  }
}
```

Complete generated Spec ID:

```text
A1!BKWX.BGX.XXX.X.X+DM:GUSSET=34_925,HEIGHT=190_5,WIDTH=146_05.GS:30
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Paper and Paperboard; White bleached kraft; UNKNOWN treatment
- product: article = Bag; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Named dimensions = {"GUSSET": "34_925", "HEIGHT": "190_5", "WIDTH": "146_05"} mm
- product: Basis weight = "30" g/m2

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H961",
    "L961",
    "M961",
    "N961",
    "P961"
  ],
  "supplier": {
    "A": {
      "source": "A961",
      "value": "MPC Paper",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B961",
      "value": "Canada",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Treatment, construction and saleability unspecified.

## V962 — Main Table rows 962–962

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| C962 | Wax Paper Wrap Non Printed | supplied |
| D962 | Paper Wrap | supplied |
| E962 | Wax Paper | supplied |
| F962 | 12x12 | supplied |
| G962 | 60gsm | supplied |
| H962 | 5000 | supplied |
| L962 | 12.5 | supplied |
| M962 | 12.5 | supplied |
| N962 | 9 | supplied |
| P962 | 46.63 | supplied |

Supplier context: {"A": {"source": "A961", "value": "MPC Paper", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B961", "value": "Canada", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- Wax Paper uses retained B/WX grade; coating mechanism not inferred from grade.
- F2 explicitly labels dimension mm. Tuple roles remain unknown even though plausible inches are not assumed.
- Printing separated; base descriptions must compare equal.

### Structured facts and result

```json
{
  "fields": {
    "MA": "BWXX",
    "AR": "WRX",
    "GS": "60",
    "UT": [
      [
        "DM",
        "12x12 mm; dimension roles unspecified"
      ]
    ]
  }
}
```

Complete generated Spec ID:

```text
A1!BWXX.WRX.XXX.X.X+GS:60.UT:DM=12x12%20mm%3B%20dimension%20roles%20unspecified
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Paper and Paperboard; Wax-base paper; UNKNOWN treatment
- product: article = Wrap or sheet; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Basis weight = "60" g/m2
- product: Unresolved specification statements = [["DM", "12x12 mm; dimension roles unspecified"]]

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H962",
    "L962",
    "M962",
    "N962",
    "P962"
  ],
  "supplier": {
    "A": {
      "source": "A961",
      "value": "MPC Paper",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B961",
      "value": "Canada",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification",
  "customization": {
    "source": "C962",
    "print_state": "non-printed"
  }
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Dimension roles unknown; header/cell plausibility is not permission to change units.

## V963 — Main Table rows 963–963

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| C963 | Wax Paper Wrap Printed | supplied |
| D963 | Paper Wrap | supplied |
| E963 | Wax Paper | supplied |
| F963 | 12x12 | supplied |
| G963 | 60gsm | supplied |
| H963 | 5000 | supplied |
| L963 | 12.5 | supplied |
| M963 | 12.5 | supplied |
| N963 | 9 | supplied |
| P963 | 60.31 | supplied |

Supplier context: {"A": {"source": "A961", "value": "MPC Paper", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B961", "value": "Canada", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- Wax Paper uses retained B/WX grade; coating mechanism not inferred from grade.
- F2 explicitly labels dimension mm. Tuple roles remain unknown even though plausible inches are not assumed.
- Printing separated; base descriptions must compare equal.

### Structured facts and result

```json
{
  "fields": {
    "MA": "BWXX",
    "AR": "WRX",
    "GS": "60",
    "UT": [
      [
        "DM",
        "12x12 mm; dimension roles unspecified"
      ]
    ]
  }
}
```

Complete generated Spec ID:

```text
A1!BWXX.WRX.XXX.X.X+GS:60.UT:DM=12x12%20mm%3B%20dimension%20roles%20unspecified
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Paper and Paperboard; Wax-base paper; UNKNOWN treatment
- product: article = Wrap or sheet; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Basis weight = "60" g/m2
- product: Unresolved specification statements = [["DM", "12x12 mm; dimension roles unspecified"]]

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H963",
    "L963",
    "M963",
    "N963",
    "P963"
  ],
  "supplier": {
    "A": {
      "source": "A961",
      "value": "MPC Paper",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B961",
      "value": "Canada",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification",
  "customization": {
    "source": "C963",
    "print_state": "printed"
  }
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Dimension roles unknown; header/cell plausibility is not permission to change units.

## V993 — Main Table rows 993–997

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A993 | PAK2ECO PACKAGING LIMITED | supplied |
| B993 | TH | supplied |
| C993 | BAG PAPER BROWN 6# | supplied |
| D993 | Paper - Virgin Kraft  | supplied |
| E993 | Bag - Without Handle<br> | supplied |
| F993 | 150X280X90 | supplied |
| H993 | 500 | supplied |
| K993 | 5.9 | supplied |
| L993 | 300 | supplied |
| M993 | 170 | supplied |
| N993 | 420 | supplied |
| D996 | Paper - Recyced Kraft | supplied |

Supplier context: {"A": {"source": "A993", "value": "PAK2ECO PACKAGING LIMITED", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B993", "value": "TH", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- C993:C996 and shared dimensions/packing span continuation rows; D993:D995 says virgin kraft and D996 says recycled kraft.
- All cells in rows 993–997 retained, including empty continuation rows and overlapping merged structures.
- It is unresolved whether these are alternatives or a conflict. No resolved Spec ID or invented SKU split.

### Structured facts and result

No resolved Spec ID. Known statements remain in the source/triage fixture:

```json
{
  "article": "bag",
  "handle": "without handle",
  "original_material_statements": [
    "Paper - Virgin Kraft  ",
    "Paper - Recyced Kraft"
  ]
}
```

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H993",
    "K993",
    "L993",
    "M993",
    "N993"
  ],
  "supplier": {
    "A": {
      "source": "A993",
      "value": "PAK2ECO PACKAGING LIMITED",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B993",
      "value": "TH",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Resolve record/alternative boundary and material statements before association.

## V1000 — Main Table rows 1000–1000

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A1000 | Redstar | supplied |
| B1000 | Vietnam | supplied |
| C1000 | 100% Recycled White Kraft Paper 60 gsm With Greaseproof coating inside 4.25 x 2.5 x 3.75 inches Note: Kindly quote us with 2 color print | supplied |
| D1000 | Others (Specified in Item Name) | supplied |
| E1000 | Paper - Greaseproof | supplied |
| F1000 | 4.25 x 2.5 x 3.75 inches | supplied |
| G1000 | 60 | supplied |
| H1000 | 1000 | supplied |
| I1000 | 200 | supplied |
| J1000 | 5 | supplied |
| K1000 | 3.7 | supplied |
| L1000 | 235 | supplied |
| M1000 | 210 | supplied |
| N1000 | 230 | supplied |
| O1000 | 0.01 | supplied |
| P1000 | 10.37 | supplied |

Supplier context: {"A": {"source": "A1000", "value": "Redstar", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B1000", "value": "Vietnam", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- C explicitly supplies recycled white kraft and 60 gsm. KC and FS RECYCLED retain recycled material; no PR=100 because post-consumer basis unspecified.
- Inside greaseproof coating is local treatment; no parent-to-child material inheritance.
- No article type inferred from packing/dimensions. Printing request moved to customization.

### Structured facts and result

```json
{
  "fields": {
    "MA": "BKCX",
    "CL": "WHITE",
    "FS": "RECYCLED",
    "GS": "60",
    "UT": [
      [
        "DM",
        "4.25 x 2.5 x 3.75 inches; dimension roles unspecified"
      ],
      [
        "FS",
        "100% recycled; post-consumer share unspecified"
      ]
    ]
  },
  "groups": [
    {
      "scope": "INSIDE",
      "node": {
        "fields": {
          "MA": "XXXG"
        }
      }
    }
  ]
}
```

Complete generated Spec ID:

```text
A1!BKCX.XXX.XXX.X.X+CL:WHITE.FS:RECYCLED.GS:60.UT:DM=4%2E25%20x%202%2E5%20x%203%2E75%20inches%3B%20dimension%20roles%20unspecified,FS=100%25%20recycled%3B%20post-consumer%20share%20unspecified~S(INSIDE){MA:XXXG}
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Paper and Paperboard; Recycled kraft; UNKNOWN treatment
- product: article = UNKNOWN article class; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Base colour = "WHITE"
- product: Feedstock = "RECYCLED"
- product: Basis weight = "60" g/m2
- product: Unresolved specification statements = [["DM", "4.25 x 2.5 x 3.75 inches; dimension roles unspecified"], ["FS", "100% recycled; post-consumer share unspecified"]]
- product/INSIDE: material = UNKNOWN material family; UNKNOWN; greaseproof treated

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H1000",
    "I1000",
    "J1000",
    "K1000",
    "L1000",
    "M1000",
    "N1000",
    "O1000",
    "P1000"
  ],
  "supplier": {
    "A": {
      "source": "A1000",
      "value": "Redstar",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B1000",
      "value": "Vietnam",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification",
  "customization": {
    "source": "C1000",
    "request": "Kindly quote us with 2 color print"
  }
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Bleaching, article and dimension roles unknown; no independent coating verification.

## V1088 — Main Table rows 1088–1088

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| B1088 | India | supplied |
| C1088 | Bag, Paper 16LB White SOS (80GSM Kraft) | supplied |
| D1088 | Bag | supplied |
| E1088 | White Kraft Paper, 80gsm | supplied |
| F1088 | 7.75 W x 4.75 D x 16 H inches | supplied |
| G1088 | 80gsm | supplied |
| H1088 | 500 | supplied |
| L1088 | 41 | supplied |
| M1088 | 41 | supplied |
| N1088 | 38 | supplied |
| O1088 | 0.06 | supplied |
| P1088 | 28.14 | supplied |
| U1088 | 30–40 days after order confirmation | supplied |

Supplier context: {"A": {"source": "A1086", "value": "ProPac Solution", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B1088", "value": "India", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- White Kraft does not establish bleaching: KR plus WHITE.
- Explicit W/D/H inches normalized exactly. 16LB retained as trade designation rather than load.
- SOS remains targeted unresolved construction.

### Structured facts and result

```json
{
  "fields": {
    "MA": "BKRX",
    "AR": "BGX",
    "CL": "WHITE",
    "GS": "80",
    "NC": "16LB",
    "UT": [
      [
        "CF",
        "SOS"
      ]
    ],
    "DM": {
      "WIDTH": {
        "value": "7.75",
        "unit": "in"
      },
      "DEPTH": {
        "value": "4.75",
        "unit": "in"
      },
      "HEIGHT": {
        "value": "16",
        "unit": "in"
      }
    }
  }
}
```

Complete generated Spec ID:

```text
A1!BKRX.BGX.XXX.X.X+CL:WHITE.DM:DEPTH=120_65,HEIGHT=406_4,WIDTH=196_85.GS:80.NC:16LB.UT:CF=SOS
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Paper and Paperboard; Kraft paper, bleach state unspecified; UNKNOWN treatment
- product: article = Bag; UNKNOWN role
- product: configuration = UNKNOWN shape; UNKNOWN construction; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Base colour = "WHITE"
- product: Named dimensions = {"DEPTH": "120_65", "HEIGHT": "406_4", "WIDTH": "196_85"} mm
- product: Basis weight = "80" g/m2
- product: Nominal capacity as quoted = "16LB"
- product: Unresolved specification statements = [["CF", "SOS"]]

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H1088",
    "L1088",
    "M1088",
    "N1088",
    "O1088",
    "P1088",
    "U1088"
  ],
  "supplier": {
    "A": {
      "source": "A1086",
      "value": "ProPac Solution",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B1088",
      "value": "India",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Bleaching, treatment, saleability and interpretation of SOS unspecified.

## V1141 — Main Table rows 1141–1141

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A1141 | TBH Industries | supplied |
| B1141 | Malaysia | supplied |
| C1141 | 20oz SINGLE WALL PAPER COLD CUP | supplied |
| D1141 | Cup (Single-Wall) | supplied |
| E1141 | Paper - White Kraft | supplied |
| F1141 | (T) 90 MM X (H)152MM (260gsm +18PE +18PE) | supplied |
| H1141 | 1000PCS | supplied |
| I1141 | 50 | supplied |
| J1141 | 20 | supplied |
| O1141 | 0.035 | supplied |
| T1141 | 10 | supplied |
| U1141 | 14 | supplied |

Supplier context: {"A": {"source": "A1141", "value": "TBH Industries", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B1141", "value": "Malaysia", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- Single wall is explicit; White Kraft does not establish bleaching. T/H are top diameter/height in cup context and explicit mm. Top diameter is not fitment.
- Parenthetical gsm + PE + PE supplies paper basis weight and two PE occurrences; no PE weight/unit or layer order inferred.
- Unknown-order multiset retains both PE layers. Ounces unresolved.

### Structured facts and result

```json
{
  "fields": {
    "MA": "BKRX",
    "AR": "CUX",
    "CF": "XSX",
    "CL": "WHITE",
    "DM": {
      "TOP_DIA": "90",
      "HEIGHT": "152"
    },
    "UT": [
      [
        "CA",
        "20oz"
      ],
      [
        "TR",
        "cold beverage use"
      ],
      [
        "MA_TREATMENT",
        "18PE +18PE; side/order and quantity units unspecified"
      ]
    ]
  },
  "groups": [
    {
      "direction": "X",
      "layers": [
        {
          "fields": {
            "MA": "BKRX",
            "GS": "260"
          }
        },
        {
          "fields": {
            "MA": "APEX"
          }
        },
        {
          "fields": {
            "MA": "APEX"
          }
        }
      ]
    }
  ]
}
```

Complete generated Spec ID:

```text
A1!BKRX.CUX.XSX.X.X+CL:WHITE.DM:HEIGHT=152,TOP_DIA=90.UT:CA=20oz,MA_TREATMENT=18PE%20%2B18PE%3B%20side%2Forder%20and%20quantity%20units%20unspecified,TR=cold%20beverage%20use~L(X){GS:260.MA:BKRX;MA:APEX;MA:APEX}
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Paper and Paperboard; Kraft paper, bleach state unspecified; UNKNOWN treatment
- product: article = Cup; UNKNOWN role
- product: configuration = UNKNOWN shape; single wall; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Base colour = "WHITE"
- product: Named dimensions = {"HEIGHT": "152", "TOP_DIA": "90"} mm
- product: Unresolved specification statements = [["CA", "20oz"], ["MA_TREATMENT", "18PE +18PE; side/order and quantity units unspecified"], ["TR", "cold beverage use"]]
- product: layers unknown order (display sorted; repeats retained)
- product/layer[1]: material = Paper and Paperboard; Kraft paper, bleach state unspecified; UNKNOWN treatment
- product/layer[1]: Basis weight = "260" g/m2
- product/layer[2]: material = Polymer; PE (polyethylene, grade unspecified); UNKNOWN treatment
- product/layer[3]: material = Polymer; PE (polyethylene, grade unspecified); UNKNOWN treatment

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H1141",
    "I1141",
    "J1141",
    "O1141",
    "T1141",
    "U1141"
  ],
  "supplier": {
    "A": {
      "source": "A1141",
      "value": "TBH Industries",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B1141",
      "value": "Malaysia",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- PE quantity units, side/order, bleaching, capacity standard and saleability unresolved.

## V1142 — Main Table rows 1142–1142

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A1142 | TBH Industries | supplied |
| B1142 | Malaysia | supplied |
| C1142 | 32oz SINGLE WALL PAPER COLD CUP | supplied |
| D1142 | Cup (Single-Wall) | supplied |
| E1142 | Paper - White Kraft | supplied |
| F1142 | (T) 105 MM X (H)178MM (280gsm +18PE +18PE) | supplied |
| H1142 | 500pcs | supplied |
| I1142 | 25 | supplied |
| J1142 | 20 | supplied |
| O1142 | 0.055 | supplied |
| T1142 | 10 | supplied |
| U1142 | 14 | supplied |

Supplier context: {"A": {"source": "A1142", "value": "TBH Industries", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B1142", "value": "Malaysia", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- Single wall is explicit; White Kraft does not establish bleaching. T/H are top diameter/height in cup context and explicit mm. Top diameter is not fitment.
- Parenthetical gsm + PE + PE supplies paper basis weight and two PE occurrences; no PE weight/unit or layer order inferred.
- Unknown-order multiset retains both PE layers. Ounces unresolved.

### Structured facts and result

```json
{
  "fields": {
    "MA": "BKRX",
    "AR": "CUX",
    "CF": "XSX",
    "CL": "WHITE",
    "DM": {
      "TOP_DIA": "105",
      "HEIGHT": "178"
    },
    "UT": [
      [
        "CA",
        "32oz"
      ],
      [
        "TR",
        "cold beverage use"
      ],
      [
        "MA_TREATMENT",
        "18PE +18PE; side/order and quantity units unspecified"
      ]
    ]
  },
  "groups": [
    {
      "direction": "X",
      "layers": [
        {
          "fields": {
            "MA": "BKRX",
            "GS": "280"
          }
        },
        {
          "fields": {
            "MA": "APEX"
          }
        },
        {
          "fields": {
            "MA": "APEX"
          }
        }
      ]
    }
  ]
}
```

Complete generated Spec ID:

```text
A1!BKRX.CUX.XSX.X.X+CL:WHITE.DM:HEIGHT=178,TOP_DIA=105.UT:CA=32oz,MA_TREATMENT=18PE%20%2B18PE%3B%20side%2Forder%20and%20quantity%20units%20unspecified,TR=cold%20beverage%20use~L(X){GS:280.MA:BKRX;MA:APEX;MA:APEX}
```

Independent expected code matches: True.

Dictionary decode:

- product: material = Paper and Paperboard; Kraft paper, bleach state unspecified; UNKNOWN treatment
- product: article = Cup; UNKNOWN role
- product: configuration = UNKNOWN shape; single wall; UNKNOWN feature
- product: Local capacity = unknown
- product: Local fitment = unknown
- product: Base colour = "WHITE"
- product: Named dimensions = {"HEIGHT": "178", "TOP_DIA": "105"} mm
- product: Unresolved specification statements = [["CA", "32oz"], ["MA_TREATMENT", "18PE +18PE; side/order and quantity units unspecified"], ["TR", "cold beverage use"]]
- product: layers unknown order (display sorted; repeats retained)
- product/layer[1]: material = Paper and Paperboard; Kraft paper, bleach state unspecified; UNKNOWN treatment
- product/layer[1]: Basis weight = "280" g/m2
- product/layer[2]: material = Polymer; PE (polyethylene, grade unspecified); UNKNOWN treatment
- product/layer[3]: material = Polymer; PE (polyethylene, grade unspecified); UNKNOWN treatment

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H1142",
    "I1142",
    "J1142",
    "O1142",
    "T1142",
    "U1142"
  ],
  "supplier": {
    "A": {
      "source": "A1142",
      "value": "TBH Industries",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B1142",
      "value": "Malaysia",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- PE quantity units, side/order, bleaching, capacity standard and saleability unresolved.

## V1143 — Main Table rows 1143–1143

### Original cells and context

| Cell | Original value | Kind / cached result |
|---|---|
| A1143 | TBH Industries | supplied |
| B1143 | Malaysia | supplied |
| C1143 | Example: 32 oz Bleached Rectangular Bagasse Container | supplied |
| D1143 | Container | supplied |
| E1143 | Bagasse | supplied |
| F1143 | 204 Dia x 59.6 | supplied |
| G1143 | 12.5 | supplied |
| H1143 | 500 | supplied |

Supplier context: {"A": {"source": "A1143", "value": "TBH Industries", "basis": "explicit cell or containing merged range only"}, "B": {"source": "B1143", "value": "Malaysia", "basis": "explicit cell or containing merged range only"}}

### Mapping decisions

- Source labels this Example; it is not independently established supplier-product evidence.
- C says rectangular while F supplies Dia. Preserve both and withhold resolved association.
- G bare 12.5 sits under a mixed weight/thickness header; do not infer unit or role.

### Structured facts and result

No resolved Spec ID. Known statements remain in the source/triage fixture:

```json
{
  "material": "bagasse",
  "bleaching_statement": "Bleached",
  "capacity_unresolved": "32 oz"
}
```

### Outside the code

{
  "commercial_packing_evidence_cells": [
    "H1143"
  ],
  "supplier": {
    "A": {
      "source": "A1143",
      "value": "TBH Industries",
      "basis": "explicit cell or containing merged range only"
    },
    "B": {
      "source": "B1143",
      "value": "Malaysia",
      "basis": "explicit cell or containing merged range only"
    }
  },
  "transcription": "User-confirmed accurate transcription; no independent certification"
}

Every original cell remains in the source snapshot; commercial cells do not define equality. No component quantity, saleability or approval is inferred.

### Remaining uncertainty

- Shape/dimension conflict and ambiguous measurement role.
