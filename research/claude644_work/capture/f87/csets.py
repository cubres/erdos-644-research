"""EXACT enumeration, complement-set formulation (independent of exhaustive.py and of all LP/SAT code).
A bad 7-tuple A_1..A_7 of 8-sets on the 15-set S  <->  sets c_v = {i : v notin A_i} (v in S) with
 (i)   c_u cap c_v != empty for all u, v (u = v allowed)          [no 2-transversal]
 (ii)  every i in [7] lies in exactly 7 of the c_v                  [|A_i| = 8]
 (iii) |c_v| >= 3                                                    [FKW Claim 1: degree <= 4]
For the parity family with |X| = 7:  |A_i cap X| odd for all i  <=>  XOR_{v in X} chi(c_v) = 0.
New family additionally: a in Y = S\X, b in X, c_a u c_b = [7]   [{a,b} in no A_i].
Step 1: enumerate all multisets M of 15 sets satisfying (i)-(iii) (canonical order, no S7 reduction).
Step 2: for each M, test all ways to choose the X-sub-multiset (7 sets, XOR 0) and a in Y, b in X with c_a|c_b=127."""
import itertools, time, sys
from collections import Counter
FULL=127
SETS=[s for s in range(128) if bin(s).count('1')>=3]
SETS.sort(key=lambda s:(bin(s).count('1'),s))
pc=lambda s: bin(s).count('1')
def enum():
    res=[]; cov=[0]*7; cur=[]
    def rec(start, remaining, total_size):
        if remaining==0:
            if all(c==7 for c in cov): res.append(list(cur))
            return
        # size bound: remaining sets have size >=3 and total must be 49
        need=49-total_size
        if need<3*remaining: return
        for idx in range(start,len(SETS)):
            s=SETS[idx]
            if pc(s)>need-3*(remaining-1): continue
            if any((s&u)==0 for u in cur): continue
            ok=True
            for i in range(7):
                if s>>i&1 and cov[i]>=7: ok=False; break
            if not ok: continue
            for i in range(7):
                if s>>i&1: cov[i]+=1
            cur.append(s)
            rec(idx, remaining-1, total_size+pc(s))
            cur.pop()
            for i in range(7):
                if s>>i&1: cov[i]-=1
    rec(0,15,0)
    return res
def splits(M, need_ab):
    """return list of (X multiset, Y multiset) splits with XOR_X = 0 (|X|=7), and (if need_ab) a in Y, b in X, c_a|c_b=FULL"""
    out=[]
    idxs=range(15)
    seen=set()
    for Xi in itertools.combinations(idxs,7):
        Xs=tuple(sorted(M[i] for i in Xi))
        if Xs in seen: continue
        seen.add(Xs)
        x=0
        for s in Xs: x^=s
        if x!=0: continue
        Ys=list(M); 
        for s in Xs: Ys.remove(s)
        if need_ab:
            if not any((ca|cb)==FULL for ca in Ys for cb in Xs): continue
        out.append((Xs,tuple(sorted(Ys))))
    return out
if __name__=='__main__':
    t0=time.time(); Ms=enum()
    print(f'step 1: {len(Ms)} multisets satisfying (i)-(iii) ({time.time()-t0:.0f}s)',flush=True)
    fkw=0; new=0
    for M in Ms:
        s1=splits(M,False)
        if s1: fkw+=1
        s2=splits(M,True)
        if s2:
            new+=1; print('NEW-FAMILY BAD TUPLE:',[format(s,'07b') for s in M], s2[0])
    print(f'step 2: multisets admitting an FKW-parity split (FKW rank-8 family not (7,2)): {fkw};  '
          f'admitting a split with the (a,b) condition (new family not (7,2)): {new}  ({time.time()-t0:.0f}s)')
