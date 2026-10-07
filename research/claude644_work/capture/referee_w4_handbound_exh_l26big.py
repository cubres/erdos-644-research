# Referee: exhaustive-H check of L26 at minimal T for r in [lo,hi], restricted to triples where the
# 'both big' branch is arithmetically reachable (needs r>=22); counts branches.
import sys; sys.path.insert(0,'.')
import referee_w4_handbound_exh as X, w4_handbound_e2e_lemmas as L
from collections import Counter
br=Counter(); fails=[]
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for r in range(lo,hi+1):
    for x in range(r+1):
        for y in range(r+1-x):
            for z in range(r+1-max(x,y)):
                T=L.T_L26(r,x,y,z)
                if T>r: continue
                if not (T<=r-x+y-z-1 and T<=r-y+x-z-1 and 2*T<=r+x+y-2): continue
                cap={}
                def probe(g,D): cap['s']=[len(p) for p in X.regions(g,D)]; return set(g.fresh(g.r))
                L.run_L26(X.ExGame(r,T,Hspec=probe),x,y,z)
                for vec in X.vecs(cap['s'],r):
                    for rep in range(2):
                        g=X.ExGame(r,T,Hspec=X.make_spec(vec,rep,0))
                        L.run_L26(g,x,y,z)
                        H=g.H; E,F,G=g.edges; a=len(F&H); b=len(G&H)
                        br['b<=T-x' if b<=T-x else ('a<=T-y' if a<=T-y else 'both big')]+=1
                        bad=X.covered([E,F,G,H],g.reqs)
                        if bad: fails.append((r,x,y,z,T,vec,bad))
    print(r,dict(br),'fails',len(fails),flush=True)
