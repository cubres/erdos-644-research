"""For the 2-part (7,2) families with excess 1 at k=12, N=22: for each missing profile class j, is a single k-set
of that class addable? is the whole class addable?  (NUMERICAL, MILP)"""
from add_one import can_add
from tc_gen import is72_gen
k=12
fams=[((10,12),[1,3,5,7,9]),((10,12),[0,1,3,5,7,9]),((11,11),[1,3,5,7,9,11]),((12,10),[3,5,7,9,11]),((12,10),[3,5,7,9,11,12])]
for n,J in fams:
    T=[(j,k-j) for j in J]
    miss=[j for j in range(k+1) if j<=n[0] and k-j<=n[1] and j not in J]
    out=[]
    for j in miss:
        single=can_add(list(n),T,(j,k-j))
        whole=None
        if single: whole=is72_gen(list(n),T+[(j,k-j)])[0]
        out.append((j,single,whole))
    print(n,J,"missing j -> (single addable, whole class addable):",out,flush=True)
