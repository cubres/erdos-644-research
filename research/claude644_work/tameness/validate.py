# cross-check C lib (test_lib) against capture/lib72.py brute force on random small families + known examples
import random, subprocess, sys, itertools
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
import lib72 as L
def m(s): return sum(1<<int(c) for c in s)
cases=[]
lemma74=[m(s) for s in "0135 0146 0234 0236 0256 1234 1245 1256 3456".split()]
cases.append((7,lemma74))
sh=[x if x!=m("1245") else m("0245") for x in lemma74]
cases.append((7,sh))
cases.append((9,L.complete(9,5))); cases.append((7,L.complete(7,4))); cases.append((6,L.complete(6,4)))
random.seed(1)
for t in range(300):
    n=random.randint(5,9); k=random.randint(2,min(5,n-1))
    allk=L.complete(n,k); q=random.random()
    H=[e for e in allk if random.random()<q] or allk[:1]
    cases.append((n,H))
inp="".join(f"{n} {len(H)} "+" ".join(map(str,H))+"\n" for n,H in cases)
out=subprocess.run(['./test_lib'],input=inp,capture_output=True,text=True).stdout.split("\n")
bad=0
for (n,H),line in zip(cases,out):
    a,t,nc=map(int,line.split())
    b=int(L.is_72(H,n)); tt=L.tau(H,n)
    # twins brute
    S=set(H); cls=0; seen=[False]*n
    for v in range(n):
        if seen[v]: continue
        cls+=1
        for w in range(v,n):
            sw=lambda E:E if ((E>>v)&1)==((E>>w)&1) else E^(1<<v)^(1<<w)
            if not seen[w] and all(sw(E) in S for E in S): seen[w]=True
    if (a,t,nc)!=(b,tt,cls): bad+=1; print("MISMATCH",n,H,(a,t,nc),(b,tt,cls))
print("cases",len(cases),"mismatches",bad)
print("lemma7.4 family: is72,tau,twins =",out[0]); print("shifted:",out[1]); print("K95:",out[2],"K74:",out[3],"K64:",out[4])
