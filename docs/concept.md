# The concept: on-target ≠ off-cell

Senotherapeutic programs keep running into the same wall: a drug that
convincingly clears senescent cells or silences their inflammatory secretome
also does something harmful elsewhere. The reflex is to make the molecule *more
selective*. This tool exists to show, concretely, when that helps and when it
can't.

## Three kinds of adverse effect

Model the biology as a directed map:

```
drug → senescence node → cell / tissue → outcome
```

Every adverse effect then falls into one of three classes:

**Off-target.** The drug binds a protein with no part in the therapeutic
mechanism. These harms are *removable by selectivity* — a cleaner molecule that
spares those proteins simply loses those effects, at no cost to efficacy.

**On-target, wrong cell.** The harm comes from the *therapeutic* node doing its
job in a cell where you didn't want it. BCL-xL inhibition is a legitimate
senolytic mechanism in the senescent cell — but the identical inhibition in
platelets causes thrombocytopenia. NF-κB and JAK inhibition silence the SASP, but
the same pathway blockade in host-defense immune cells causes immunosuppression.
**No amount of target selectivity removes these**, because there is no wrong
target to remove — only a wrong location.

**Intrinsic to senolysis.** Some harm arises *inside* the senescent cell itself:
aggressive clearance also removes the beneficial, transient senescence that
supports wound healing and tumor suppression. This can't be localized away
either — it can only be avoided by not engaging the nodes that cause it
(BCL-xL, FOXO4–p53).

## The lever is localization, not selectivity

If the on-target/off-cell class is a dominant safety problem — and for the
BCL-xL- and NF-κB/JAK-class agents here it is — then the design axis that matters
is *where the drug is allowed to act*, not *what it binds*. Restrict exposure to
the senescent cell — via an SA-β-galactosidase–activated galacto-prodrug (the
payload uncaged only where β-gal is high), a platelet-sparing PROTAC degrader, or
a senescent-cell surface-antigen conjugate — and the on-target/off-cell harms go
inactive while efficacy at the diseased cell is preserved.

Exhaustive optimization over the node universe confirms the structural result:
**only the senescent-cell-targeted route reaches zero predicted adverse
effects.** No systemic design does, and neither does a platelet-sparing PROTAC
route on its own. And the clean optimum necessarily excludes BCL-xL and
FOXO4–p53 — the two nodes whose harm is intrinsic to senolysis. That is the whole
thesis in one sentence: this is a localization problem, not a selectivity
problem.

*Illustrative model — heuristic weights, not validated pharmacology. Not medical advice.*
