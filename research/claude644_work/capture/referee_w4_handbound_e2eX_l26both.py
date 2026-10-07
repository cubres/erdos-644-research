# Referee: exhaustive adversary restricted to the rarely-hit "both responses large" branch of L26 (Lemma 2),
# r up to argv[1]; later responses = complements (worst case).  Also an independent badness check.
import sys
import w4_handbound_e2e_lemmas as L
from referee_w4_handbound_e2eX_adaptive import ExGame, _H
from w4_handbound_e2e import two_transversal
def nobad2(edges):
    V=sorted(set().union(*edges))
    for i,u in enumerate(V):
        for v in V[i:]:
            if all(u in e or v in e for e in edges): return (u,v)
    return None
rmax=int(sys.argv[1]); n=0; trip=0; fails=0
for r in range(4,rmax+1):
    for x in range(r+1):
        for y in range(r+1-x):
            for z in range(r+1-max(x,y)):
                if x+z>r or y+z>r: continue
                T=L.T_L26(r,x,y,z)
                if T>r: continue
                PEn,PFn,PGn=r-x-y,r-x-z,r-y-z
                if not (T-y<PFn and T-x<PGn and (T-y+1)+(T-x+1)<=r): continue
                trip+=1
                for a in range(max(0,T-y+1),PFn+1):
                    for b in range(max(0,T-x+1),PGn+1):
                        for c in range(0,min(PEn,r-a-b)+1):
                            g=ExGame(r,T,lambda g,D,a=a,b=b,c=c:_H(g,D,x,y,z,[('PF',a),('PG',b),('PE',c)]))
                            ed=L.run_L26(g,x,y,z); n+=1
                            t1=two_transversal(ed); t2=nobad2(ed)
                            if t1 is not None or t2 is not None:
                                fails+=1; print('FAIL',r,x,y,z,T,a,b,c,t1,t2)
    print('r',r,'triples',trip,'games',n,'fails',fails,flush=True)
