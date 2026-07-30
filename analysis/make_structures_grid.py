"""Render a grid of the verified candidate structures from candidates.csv."""
import csv
from rdkit import Chem
from rdkit.Chem import Draw

mols, legends = [], []
with open("candidates.csv") as f:
    for r in csv.DictReader(f):
        m = Chem.MolFromSmiles(r["smiles"])
        if m:
            mols.append(m)
            legends.append(f'{r["name"]} — {r["node"]} (CID {r["pubchem_cid"]})')

img = Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(360, 280), legends=legends)
img.save("results/candidate_structures.png")
print(f"rendered {len(mols)} structures -> candidate_structures.png")
