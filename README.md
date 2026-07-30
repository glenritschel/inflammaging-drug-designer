# Senotherapeutic Placeholder Drug Designer (Inflammaging)

An interactive, browser-based tool for reasoning about **why senolytic and
senomorphic drugs cause the side effects they do — and which of those are
actually fixable.**

It encodes a small causal map:

```
drug  →  senescence node  →  cell / tissue  →  outcome (efficacy or adverse effect)
```

and lets you design a hypothetical ("placeholder") senotherapeutic **forward** —
pick the nodes it engages and how it's delivered, and see the predicted efficacy
and adverse effects — or **backward** — state the outcome you want and let the
tool find a node set + delivery route that achieves it.

> **The one idea.** Some adverse effects are *off-target* (the drug hits a
> protein it shouldn't) and vanish when you make the molecule more selective. But
> the worst ones are *on-target in the wrong cell* — the same node that clears a
> senescent cell harms elsewhere (BCL-xL inhibition killing senescent cells, but
> causing thrombocytopenia in platelets; NF-κB/JAK inhibition silencing the SASP,
> but immunosuppressing host-defense immune cells). A third class is *intrinsic
> to senolysis itself* (loss of beneficial transient senescence, inside the
> senescent cell). **Target selectivity cannot remove the on-target/off-cell
> harms. Cell-selective delivery can.**

## Try it

Open [`index.html`](index.html) in any modern browser — it's a single
self-contained file, no build step, no dependencies. Also live at
`glenritschel.github.io/inflammaging-drug-designer`.

- **Forward mode** — check the senolytic and/or senomorphic nodes to engage,
  choose a delivery localization (systemic, PROTAC degrader, or
  senescent-cell-targeted), and read off predicted efficacy, an inflammaging-
  reduction verdict, the active adverse effects, and a design score. Every
  adverse effect is labelled *on-target / wrong cell* (removable by
  localization) or *intrinsic to senolysis* (removable only by dropping the
  node).
- **Backward mode** — set a goal ("achieve reduction, avoid all serious effects,
  avoid thrombocytopenia") and the tool searches the design space and loads the
  best placeholder that satisfies it.
- **Optimized presets** — one-click optima, including the senescent-cell-targeted
  profile that reaches maximal efficacy with zero predicted adverse effects.

## What's in the model

Node universe (illustrative): **senolytic** — BCL-xL, BCL-2, SRC-family,
Na/K-ATPase, HSP90, FOXO4–p53, GLS1, PI3K/AKT; **senomorphic** — NF-κB/IKK,
JAK1/2, mTOR, p38 MAPK, NLRP3, cGAS–STING, IL-6/IL-6R. Delivery routes: systemic,
PROTAC degrader (platelet-sparing), senescent-cell-targeted (SA-β-gal /
galacto-prodrug). See [`docs/concept.md`](docs/concept.md) for the biology and
design logic.

## Reproducible analysis

[`analysis/`](analysis/) holds the non-interactive analysis behind the companion
preprint and the US provisional patent specification (US Application 64/121,903):
an exhaustive target-set × delivery-route optimization (98,301 designs), a
developability screen (RDKit) over twelve PubChem-sourced candidate structures,
figure generation, and a REINVENT4 generative-design scoring specification for a
galacto-caged senolytic. See [`analysis/README.md`](analysis/README.md) to
reproduce.

## ⚠️ Important — what this is and isn't

This is a **conceptual / educational instrument.** The efficacy weights and
severities are **illustrative design heuristics, not measured pharmacology.** The
*structure* of the conclusions (that only senescent-cell targeting reaches zero
adverse effects; that the clean optimum must drop the senolysis-intrinsic nodes)
is robust; the specific numbers are not. Do **not** use it to rank real compounds
or predict real safety margins. Swap in measured selectivity and potency data
before drawing any program decision. Not medical advice.

## License

MIT — see [`LICENSE`](LICENSE).

Built by Glen Ritschel (Ritschel Research), in collaboration with Claude (Anthropic), 2026.

Repo: https://github.com/glenritschel/inflammaging-drug-designer
