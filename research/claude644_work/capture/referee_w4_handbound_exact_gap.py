# Referee: rerun w4_handbound_e2e_gap.py (Lemma 7.27) and w4_handbound_e2e_l50.py (Lemma 7.41 branch)
# but replace the random FINAL responses by an EXACT check: points are grouped by signature
# (membership in each fixed edge, membership in each final request); a pair of signatures is a potential
# 2-transversal iff every fixed edge contains one of them, and it is killed iff some final request contains both.
import sys, random; sys.path.insert(0,'.')
import w4_handbound_e2e as base
import w4_handbound_e2e_gap as GAP, w4_handbound_e2e_l50 as L50
from collections import Counter
REC=[]
def rec_respond(s,D):
    D=set(D); assert len(D)<=s.T,('request too big',len(D),s.T); REC.append(D); return set(s.fresh(s.r))
base.Game.respond=rec_respond
def exact(nfixed):
    def chk(fin):
        fixed=fin[:nfixed]; reqs=REC[-(len(fin)-nfixed):]
        assert len(fin)<=7
        sig=Counter()
        for p in set().union(*fixed):
            sig[(tuple(p in e for e in fixed),tuple(p in D for D in reqs))]+=1
        keys=list(sig)
        for i,s1 in enumerate(keys):
            for s2 in keys[i:]:
                if s1==s2 and sig[s1]<2:
                    # single point: transversal alone?
                    if all(s1[0]) and not any(s1[1]): return ('single',s1)
                    continue
                if all(a or b for a,b in zip(s1[0],s2[0])) and not any(a and b for a,b in zip(s1[1],s2[1])):
                    return (s1,s2)
        return None
    return chk
GAP.two_transversal=exact(4); L50.two_transversal=exact(5)
seed=int(sys.argv[1]); n=int(sys.argv[2])
rng=random.Random(seed); st=Counter()
for it in range(n):
    r=rng.choice([1000,1001,1003,1200,1500,2000]); st['gap '+GAP.L27(r,rng)]+=1
rng=random.Random(seed); 
for it in range(n):
    r=rng.choice([60,100,101,300,1000]); st['l50 '+L50.run(r,rng)]+=1
print('PASS (exact final responses)',dict(st))
