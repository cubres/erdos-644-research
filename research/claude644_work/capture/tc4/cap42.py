"""42 audited two-type capacity functions (both orientations) from the note's templates.json via the note's
exact checker (w4_cells/p644_continuous_type_cells_check.audited_shapes).  Returns list of facet lists
[(u,v)] meaning  u*s + v*t <= cap  (s = first-type load, t = second-type load)."""
import sys, os
from fractions import Fraction as F
from pathlib import Path
W=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','w4_cells')
sys.path.insert(0,W)
def load():
    from p644_continuous_type_cells_check import audited_shapes
    sh=audited_shapes(Path(W)/'logs/astra_two_part_gap_central/templates.json')
    out=[]
    for s in sh: out.append([(F(u,d),F(v,d)) for u,v,d in s])
    return out
if __name__=='__main__':
    c=load(); print(len(c)); print(c[:3])
