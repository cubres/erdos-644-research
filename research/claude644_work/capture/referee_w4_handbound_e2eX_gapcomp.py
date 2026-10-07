# Referee: rerun the Lemma 9 (note 7.27) and Lemma 7/8 (7.41 in 7.50) e2e games with the FINAL
# responses replaced by the complement of the request (maximal edges = worst case for badness).
import sys, random
import w4_handbound_e2e as B
def comp(s,D):
    D=set(D); assert len(D)<=s.T,('request too big',len(D),s.T)
    return set(range(s.nxt))-D
B.Game.respond=comp
which=sys.argv[1]; seed=int(sys.argv[2]); n=int(sys.argv[3])
if which=='gap':
    import w4_handbound_e2e_gap as M
    rng=random.Random(seed); st={}
    for it in range(n):
        r=rng.choice([1000,1001,1003,1200,1500,2000]); c=M.L27(r,rng); st[c]=st.get(c,0)+1
else:
    import w4_handbound_e2e_l50 as M
    rng=random.Random(seed); st={}
    for it in range(n):
        r=rng.choice([60,100,101,300,1000]); c=M.run(r,rng); st[c]=st.get(c,0)+1
print('PASS',which,st)
