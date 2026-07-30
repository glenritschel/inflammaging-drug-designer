# analysis — reproducibility code and data

Code and data behind the preprint *"Localization, not selectivity: a causal
node–cell–outcome framework for designing senescent-cell-directed
senotherapeutics, with an application to inflammaging"* and its companion US
provisional patent specification (US Application 64/121,903, filed 29 July 2026).

The interactive tool (`../index.html`) lives in the repository root. This folder
is the non-interactive analysis.

## Contents

| File | What it does |
|---|---|
| `optimization_analysis.py` | Exhaustive node-set × delivery-route optimization (98,301 designs). Writes `results/optimization_results.json`. |
| `validate_and_screen.py` | Parses the 12 candidate SMILES, cross-checks RDKit formula/MW against the literature reference for each drug, then runs the developability screen. Writes `results/developability_results.csv`. |
| `make_figure.py` | Renders `results/optimization_figure.png`. |
| `make_structures_grid.py` | Renders `results/candidate_structures.png`. |
| `candidates.csv` | The 12 candidate agents with PubChem-sourced SMILES + CIDs + node. |
| `reinvent4_senotherapeutic_scoring.toml` | REINVENT4 scoring specification for a galacto-caged (senescent-cell-activated) de-novo molecule. |
| `results/` | Generated outputs (JSON, CSV, figures). |

## Reproduce

```bash
pip install -r requirements.txt
python optimization_analysis.py      # route optima over 98,301 designs
python validate_and_screen.py        # SMILES validation + developability table
python make_figure.py                # optimization figure
python make_structures_grid.py       # structures grid
```

## Notes

The per-node efficacy weights and severities are **illustrative heuristics** for
exploring trade-offs, not measured pharmacology. The *structure* of the
conclusions (only senescent-cell targeting reaches zero adverse effects; the
clean optimum must drop the senolysis-intrinsic nodes BCL-xL and FOXO4–p53) is
robust; the specific numbers are not. Candidate SMILES were retrieved from
PubChem and parsed in RDKit; formula and molecular weight were cross-checked
against the literature reference for each named drug (matching for eleven of
twelve; the twelfth, the PROTAC DT2216, parsed cleanly to its expected large
composition). No wet-laboratory data is included.
