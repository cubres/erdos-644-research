"""Referee w9 [nonint#2] -- case-level test of the Prop C proof. For every small (k,s,c,d) (conditions NOT assumed)
and every class pattern (j,a,b), a>=b, decide exactly by SAT (w9_ref_nonint2_sat.decide restricted to that pattern)
whether a bad tuple with that pattern exists; the proof claims:
   a=b=0:        bad => 4s>=3k
   a>=1, b=0:    bad => NOT[(c-a d>s and (5-a)s<2k+c-a d) or ((6-a)s<k+2(c-a d))]   (needs X nonempty: (a-1)d<k)
   a,b>=1, j>=1: bad => 4(c-a d)(c-b d) <= j s^2                                     (needs c-a d>=0, c-b d>=0)
   j=0:          never bad when 5d<k.
Any violation = error in the case analysis. Usage: python3 w9_ref_nonint2_cases.py kmin kmax"""
import sys
from w9_ref_nonint2_sat import decide

def claim_allows_bad(k, s, c, d, j, a, b):
    """True if the proof's per-pattern necessary condition for badness holds (so badness is allowed)."""
    if j == 0:
        return not (5*d < k)
    if a == 0 and b == 0:
        return 4*s >= 3*k
    if b == 0 or a == 0:
        aa = max(a, b)
        if (aa-1)*d >= k: return True  # X may be empty: proof silent
        x = c - aa*d
        cond = (x > s and (5-aa)*s < 2*k + x) or ((6-aa)*s < k + 2*x)
        return not cond
    if c - a*d < 0 or c - b*d < 0: return True  # proof silent (degenerate)
    return 4*(c-a*d)*(c-b*d) <= j*s*s

kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
viol = 0; tested = 0; badcount = 0
for k in range(kmin, kmax+1):
    for s in range(0, k):
        for c in range(0, (k+s)//2+1):
            if c > k: continue
            for d in range(0, k//2+1):
                for (j, a, b) in [(j, a, b) for j in range(8) for a in range(8) for b in range(8) if j+a+b == 7 and a >= b]:
                    if (a > 0 or b > 0) and False: pass
                    ok, res = decide(k, s, c, d, classes=[(j, a, b)])
                    tested += 1
                    if not ok:
                        badcount += 1
                        if not claim_allows_bad(k, s, c, d, j, a, b):
                            viol += 1; print('VIOLATION', (k, s, c, d), (j, a, b), flush=True)
    print(f'k={k} done: patterns tested {tested}, bad {badcount}, violations {viol}', flush=True)
