# NUMERICAL: max over probability mu on edges of P_{iid}(E∩F∩G = ∅) ("good-triple Lagrangian")
# for complete families K_n^k, both (7,2) and non-(7,2). Multi-start projected ascent (replicator dynamics).
import itertools, numpy as np, sys
def run(n,k,starts=40,iters=3000,seed=0):
    E=[frozenset(c) for c in itertools.combinations(range(n),k)]
    m=len(E); M=np.array([[ [1.0 if not (E[a]&E[b]&E[c]) else 0.0 for c in range(m)] for b in range(m)] for a in range(m)]) if m<=80 else None
    rng=np.random.default_rng(seed); best=0;bx=None
    for s in range(starts):
        x=rng.dirichlet(np.ones(m)*0.3)
        for it in range(iters):
            g=np.einsum('abc,b,c->a',M,x,x)  # gradient/3
            val=x@g
            if val<=0: break
            x=x*g/val   # replicator (Baum-Eagon) increases the cubic form
        val=np.einsum('abc,a,b,c->',M,x,x,x)
        if val>best: best=val;bx=x
    supp=[(tuple(sorted(E[i])),round(bx[i],3)) for i in np.argsort(-bx)[:10] if bx[i]>1e-3]
    return best,supp
for n,k in [(5,3),(6,3),(7,3),(6,4),(7,4),(8,4)]:
    b,s=run(n,k); print(n,k,"max P(good)=%.4f"%b, s[:8]); sys.stdout.flush()
