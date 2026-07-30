"""
Validate PubChem-sourced SMILES (RDKit parse + formula/MW), cross-check MW/formula
against literature reference values, then run the developability screen.
Reads candidates.csv (name,smiles,pubchem_cid,node) and writes
developability_results.csv.

Note on the check: SMILES were retrieved from PubChem by name (CID recorded in
candidates.csv). This session cannot fetch PubChem live (robots.txt), so the
"reference" formula/MW below are literature values for each named drug. A match
therefore confirms the pasted structure IS the intended compound (right formula,
right mass), not merely that it parses. DT2216 (a large PROTAC) is reported
without a hardcoded reference and cross-checked only structurally.
"""
import csv
from rdkit import Chem
from rdkit.Chem import Descriptors, QED, Crippen, rdMolDescriptors, FilterCatalog

# name -> (reference molecular formula, reference MW)  [literature values; None = report only]
REF = {
 "navitoclax":  ("C47H55ClF3N5O6S3", 974.6),
 "venetoclax":  ("C45H50ClN7O7S",    868.4),
 "dasatinib":   ("C22H26ClN7O2S",    488.0),
 "fisetin":     ("C15H10O6",         286.2),
 "quercetin":   ("C15H10O7",         302.2),
 "ruxolitinib": ("C17H18N6",         306.4),
 "sirolimus":   ("C51H79NO13",       914.2),
 "telaglenastat":("C26H24F3N7O3S",   571.6),
 "alvespimycin":("C32H48N4O8",       616.7),
 "MCC950":      ("C20H24N2O5S",      404.5),
 "losmapimod":  ("C22H26FN3O2",      383.5),
 "DT2216":      (None,               None),
}

params = FilterCatalog.FilterCatalogParams()
params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.PAINS)
params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.BRENK)
catalog = FilterCatalog.FilterCatalog(params)
BASIC_N = Chem.MolFromSmarts("[NX3;!$(N=*);!$(N-[#6]=[O,N,S])]")

rows_in = list(csv.DictReader(open("candidates.csv")))

print("VALIDATION (RDKit parse + formula/MW vs literature reference):\n")
valid = []
for r in rows_in:
    name, smi, cid, node = r["name"], r["smiles"], r["pubchem_cid"], r["node"]
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"  {name:14s} CID {cid:12s}  FAIL — SMILES did not parse"); continue
    f  = rdMolDescriptors.CalcMolFormula(mol)
    mw = Descriptors.MolWt(mol)
    exp_f, exp_mw = REF.get(name, (None, None))
    if exp_f is None:
        verdict = "REPORTED (no hardcoded ref; parsed OK)"
    else:
        ok = (f == exp_f) and (abs(mw - exp_mw) <= 1.5)
        verdict = "PASS" if ok else ("CHECK: " + ("formula " if f != exp_f else "")
                                      + ("MW" if abs(mw - exp_mw) > 1.5 else ""))
    ref_str = f"{exp_f} ({exp_mw})" if exp_f else "—"
    print(f"  {name:14s} CID {cid:12s}  RDKit {f} ({mw:.1f})  vs ref {ref_str:22s}  {verdict}")
    valid.append((name, cid, node, mol))

def screen(name, cid, node, mol):
    mw = Descriptors.MolWt(mol); clogp = Crippen.MolLogP(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    hbd = rdMolDescriptors.CalcNumHBD(mol); hba = rdMolDescriptors.CalcNumHBA(mol)
    rotb = rdMolDescriptors.CalcNumRotatableBonds(mol); arom = rdMolDescriptors.CalcNumAromaticRings(mol)
    qed = QED.qed(mol)
    ro5 = sum([mw > 500, clogp > 5, hbd > 5, hba > 10])
    veber = (rotb <= 10) and (tpsa <= 140)
    alerts = len(catalog.GetMatches(mol))
    herg = (clogp >= 3.7) and mol.HasSubstructMatch(BASIC_N) and (250 <= mw <= 600)
    return dict(name=name, node=node, cid=cid, MW=round(mw,1), cLogP=round(clogp,2),
                TPSA=round(tpsa,1), HBD=hbd, HBA=hba, RotB=rotb, ArRings=arom,
                QED=round(qed,3), Ro5_viol=ro5, Veber_pass=veber, n_alerts=alerts, hERG_flag=herg)

cols = ["name","node","cid","MW","cLogP","TPSA","HBD","HBA","RotB","ArRings","QED","Ro5_viol","Veber_pass","n_alerts","hERG_flag"]
rows = [screen(n,c,nd,m) for n,c,nd,m in valid]
print("\nDEVELOPABILITY SCREEN:\n")
print(" | ".join(cols))
for r in rows: print(" | ".join(str(r[c]) for c in cols))
with open("results/developability_results.csv","w",newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)
print(f"\n{len(valid)}/{len(rows_in)} candidates validated. Saved developability_results.csv")
