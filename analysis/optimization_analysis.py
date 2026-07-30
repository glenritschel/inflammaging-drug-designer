"""
Reproducible optimization for the senotherapeutic placeholder design model
(inflammaging). Exhaustively searches every therapeutic-target subset x
cell-selectivity localization, scoring predicted anti-inflammaging efficacy vs
adverse-effect penalty, and reports the optimum per delivery route.

Illustrative heuristic weights (see notes) — the STRUCTURE of the result is the
finding, not the exact numbers. Model is kept identical to the interactive tool
(index.html) so the two agree.
"""
import json, itertools

SEVW = {"serious": 25, "moderate": 10, "low": 3}

# therapeutic targets: mode ('l' senolytic / 'm' senomorphic), efficacy weight,
# adverse effects [(label, tissue, severity)]
THER = {
 "BCLxL": ("l", 35, [("Thrombocytopenia","platelets","serious"),("Loss of beneficial senescence","senescent","moderate")]),
 "BCL2":  ("l", 18, [("Neutropenia","marrow","moderate")]),
 "SRC":   ("l", 25, [("Bleeding","platelets","serious"),("Fluid retention / edema","vasc","moderate")]),
 "NaK":   ("l", 24, [("Cardiac arrhythmia","cardiac","serious")]),
 "HSP90": ("l", 24, [("Hepatotoxicity","liver","moderate"),("GI upset","gi","low")]),
 "FOXO4": ("l", 24, [("Cytopenia","marrow","moderate"),("Loss of beneficial senescence","senescent","moderate")]),
 "GLS1":  ("l", 18, [("GI upset","gi","low")]),
 "PI3K":  ("l", 20, [("Hyperglycemia","metabolic","moderate"),("Immunosuppression","immune","moderate")]),
 "NFkB":  ("m", 30, [("Immunosuppression / infection","immune","serious")]),
 "JAK":   ("m", 28, [("Immunosuppression / infection","immune","serious"),("Anemia / cytopenia","marrow","moderate")]),
 "mTOR":  ("m", 28, [("Immunosuppression","immune","moderate"),("Mucositis / mouth ulcers","gi","moderate"),("Hyperglycemia / dyslipidemia","metabolic","moderate")]),
 "p38":   ("m", 24, [("Hepatotoxicity","liver","moderate"),("GI upset","gi","low")]),
 "NLRP3": ("m", 24, [("Infection risk","immune","moderate")]),
 "STING": ("m", 22, [("Impaired antiviral immunity","immune","moderate")]),
 "IL6R":  ("m", 18, [("Infection","immune","moderate"),("Neutropenia","marrow","low")]),
}
LABEL = {
 "BCLxL":"BCL-xL","BCL2":"BCL-2","SRC":"SRC-family","NaK":"Na/K-ATPase","HSP90":"HSP90",
 "FOXO4":"FOXO4-p53","GLS1":"GLS1","PI3K":"PI3K/AKT","NFkB":"NF-kB (IKK)","JAK":"JAK1/2",
 "mTOR":"mTOR","p38":"p38 MAPK","NLRP3":"NLRP3","STING":"cGAS-STING","IL6R":"IL-6/IL-6R",
}
ALL_TISSUES = ["senescent","platelets","marrow","immune","cardiac","liver","gi","vasc","metabolic"]
LOC = {
 "systemic": ALL_TISSUES,
 "protac":   [t for t in ALL_TISSUES if t != "platelets"],   # PROTAC degrader spares platelets (no cereblon)
 "senescent":["senescent"],                                    # SA-b-gal / galacto-prodrug: acts only in senescent cells
}
REV_THRESHOLD = 40

def evaluate(hit, loc):
    reach = set(LOC[loc])
    eff = min(100, sum(THER[t][1] for t in hit))
    active = {}
    for t in hit:
        for label, tissue, sev in THER[t][2]:
            if tissue in reach:
                if label not in active or SEVW[sev] > SEVW[active[label][0]]:
                    active[label] = (sev, tissue)
    penalty = sum(SEVW[s] for s, _ in active.values())
    score = max(0, eff - penalty)
    n_serious = sum(1 for s, _ in active.values() if s == "serious")
    return dict(eff=eff, reversal=eff >= REV_THRESHOLD,
                aes={k: v[0] for k, v in active.items()},
                n_aes=len(active), n_serious=n_serious, penalty=penalty, score=score)

targets = list(THER)
results = []
for r in range(1, len(targets)+1):
    for hit in itertools.combinations(targets, r):
        for loc in LOC:
            results.append(dict(hit=list(hit), loc=loc, **evaluate(hit, loc)))

def best(pred, key):
    c = [x for x in results if pred(x)]
    return max(c, key=key) if c else None

def names(hit): return " + ".join(LABEL[t] for t in hit)

print(f"Evaluated {len(results)} designs "
      f"({2**len(targets)-1} target subsets x {len(LOC)} routes).\n")

print("Global best design score:")
g = best(lambda x: True, lambda x: (x["score"], -len(x["hit"])))
print(f"  {names(g['hit'])} | {g['loc']} | eff {g['eff']} | AEs {g['n_aes']} | score {g['score']}\n")

print("Best per delivery route (max score among reversal-achieving designs):")
route_best = {}
for loc in LOC:
    b = best(lambda x: x["loc"] == loc and x["reversal"],
             lambda x: (x["score"], -x["n_aes"], -len(x["hit"])))
    route_best[loc] = b
    print(f"  {loc:9s}: {names(b['hit']):40s} eff {b['eff']:3d}  "
          f"AEs {b['n_aes']} ({b['n_serious']} serious)  score {b['score']}")

print("\nZero-AE reachability by route (max efficacy with no active adverse effect):")
for loc in LOC:
    z = best(lambda x: x["loc"] == loc and x["n_aes"] == 0,
             lambda x: (x["eff"], -len(x["hit"])))
    print(f"  {loc:9s}: " + (f"eff {z['eff']} via {names(z['hit'])}" if z
                             else "no zero-AE design exists"))

summary = {loc: {"hit": b["hit"], "eff": b["eff"], "n_aes": b["n_aes"],
                 "n_serious": b["n_serious"], "score": b["score"],
                 "adverse_effects": b["aes"]} for loc, b in route_best.items()}
with open("results/optimization_results.json", "w") as f:
    json.dump({"global_best": {"hit": g["hit"], "loc": g["loc"], "score": g["score"]},
               "route_optima": summary, "n_designs_evaluated": len(results)}, f, indent=2)
print(f"\nSaved optimization_results.json")
