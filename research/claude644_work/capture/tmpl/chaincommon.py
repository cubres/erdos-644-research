exec(open('chainmin.py').read().split("L_,A_,B_,C_=2,3,4,5")[0])
import itertools
A_,B_=3,4
cands=[(k,s,t) for k in [1,2,9,10,21,22,39,40] for s,t in [(A_,B_),(B_,A_)]]
cases=[(False,False),(True,False),(False,True),(True,True)]
doms=[domain(c) for c in cases]
for r in range(2,5):
    found=[]
    for ch in itertools.permutations(cands,r):
        if all(valid(W,S,list(ch)) for W,S in doms): found.append(ch)
    print(r,len(found),found[:10],flush=True)
    if found: break
