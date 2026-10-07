exec(open('chainmin.py').read().split("L_,A_,B_,C_=2,3,4,5")[0])
import itertools
A_,B_=3,4
cands=[(k,s,t) for k in [1,2,9,10,21,22,39,40,41,42,3,4,5,6] for s,t in [(A_,B_),(B_,A_)]]
for case in [(False,False),(True,False),(False,True),(True,True)]:
    W,S=domain(case)
    sols=[]
    for r in range(1,5):
        for ch in itertools.permutations(cands,r):
            if valid(W,S,list(ch)): sols.append(ch)
        if sols: break
    print(case, 'shortest len',r, sols[:12], 'count',len(sols), flush=True)
