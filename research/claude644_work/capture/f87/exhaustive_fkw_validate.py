"""EXACT EXHAUSTIVE proof (pure integer DFS, no LP/SAT) that
   H = { 8-subsets E of S : |E cap X| odd, {a,b} not subset E },  S = {a} u X u D,  |X| = 7 (b in X, C = X\{b}), |D| = 7,
has property (7,2).
A 7-tuple A_1..A_7 is encoded by vertex types sig(v) = {i : v in A_i} subset [7].  No 2-transversal  <=>
sig(x) u sig(y) != [7] for all x, y (x = y allowed).
Claim 1 (FKW): in a bad tuple every vertex has degree <= 4 (if deg v >= 5 the other <= 2 edges share a point since
8+8 > 15, giving a 2-transversal).  So types have size <= 4.
Rows: |A_i| = 8, |A_i cap X| odd, not both a, b in A_i  (i.e. sig(a) cap sig(b) = empty).
Symmetry: rows relabelled so sig(a) = {0..da-1}; C- and D-vertices are interchangeable within their part
(multisets: non-decreasing type index).  (No other symmetry is used.)
Exhaustive DFS; prints the number of bad tuples found (0 => (7,2))."""
import itertools, sys, time
FULL=127
TYPES=[s for s in range(128) if bin(s).count('1')<=4]
TYPES.sort()
deg=lambda s: bin(s).count('1')
def run(check_family='new'):
    found=[]; nodes=[0]
    order=['a','b']+['C']*6+['D']*7
    cnt=[0]*7; cntX=[0]*7
    used=[]
    def rec(pos, last_idx, total):
        nodes[0]+=1
        rem=15-pos
        if total+4*rem<56: return
        for i in range(7):
            if cnt[i]+rem<8: return
        if pos==15:
            if total!=56: return
            if all(cnt[i]==8 and cntX[i]%2==1 for i in range(7)):
                found.append(list(used))
            return
        part=order[pos]
        if part=='a': cands=[(1<<da)-1 for da in range(5)]
        else: cands=TYPES
        start = last_idx if (pos>2 and order[pos-1]==part) else 0
        for ti in range(start if part!='a' else 0, len(cands)):
            s=cands[ti]
            pass          # {a,b} in no edge
            if any((s|u)==FULL for u in used): continue
            if (s|s)==FULL: continue
            ok=True
            for i in range(7):
                if s>>i&1 and cnt[i]>=8: ok=False; break
            if not ok: continue
            inX = part in ('b','C')
            for i in range(7):
                if s>>i&1: cnt[i]+=1; cntX[i]+=inX
            used.append(s)
            rec(pos+1, ti, total+deg(s))
            used.pop()
            for i in range(7):
                if s>>i&1: cnt[i]-=1; cntX[i]-=inX
    rec(0,0,0)
    return found, nodes[0]
if __name__=='__main__':
    t0=time.time()
    found,nodes=run()
    print(f'bad tuples found: {len(found)}; DFS nodes {nodes}; {time.time()-t0:.0f}s')
    for f in found[:5]: print([format(s,'07b') for s in f])
