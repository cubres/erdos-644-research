"""Referee w9, nonint#3: exact integer arithmetic of Lemma H / Prop B / Cor H2 / N' special case.
b(n,c) = ceil((n-c)/3) + 2*ceil(c/4) is the proof's largest block. One anchor with trace c' forces
tau(H[U]) <= b(n,c') (else s' >= b and the tuple is bad).  Two anchors: x1+x2 <= n (x_i=|U_i n U|),
c'_i = max(0, x_i - delta_i).  Worst case T(n,d1,d2) = max_{x1+x2<=n} min_i b(n,c'_i)."""
from fractions import Fraction as Fr
def cdiv(a,b): return -(-a//b)
def b(n,c): return cdiv(n-c,3) + 2*cdiv(c,4)
_cache={}
def Tw(n,d1,d2):
    """max_{x1+x2<=n} min(b(n,max(0,x1-d1)), b(n,max(0,x2-d2))) via prefix maxima (exact)."""
    if n not in _cache:
        B=[b(n,c) for c in range(n+1)]; M=[]; m=-1
        for v in B: m=max(m,v); M.append(m)
        _cache[n]=(B,M)
    B,M=_cache[n]
    return max(min(B[max(0,x1-d1)], M[max(0,n-x1-d2)]) for x1 in range(n+1))
viol=0; worst=None; checked=0; viol_nohyp=[]
for n in range(0,161):
    B = [b(n,c) for c in range(n+1)]
    for d1 in range(0,40):
        for d2 in range(d1,40):
            T = Tw(n,d1,d2)
            rhs = Fr(5*n-d1-d2+38,12)
            if n >= d1+d2:
                checked += 1
                if T > rhs: viol += 1; print('VIOL', n,d1,d2,T,rhs)
                slack = rhs - T
                if worst is None or slack < worst[0]: worst=(slack,n,d1,d2,T)
            elif T > rhs and len(viol_nohyp)<5: viol_nohyp.append((n,d1,d2,T,rhs))
print('Lemma H arithmetic: cases', checked, 'violations', viol, 'min slack', worst)
print('without |U|>=d1+d2 the derivation fails, e.g.', viol_nohyp[:3])
# best additive constant: max over cases of 12*T - 5n + d1 + d2
best = max(12*Tw(n,d1,d2) - 5*n + d1 + d2
           for n in range(0,121) for d1 in range(0,12) for d2 in range(0,12) if n>=d1+d2)
print('sharpest constant K with 12 tau <= 5n - d1 - d2 + K (n<=120,d<12):', best, '(claim uses 38)')
# Prop B: C(U,k) in H, |U|=k+s => tau(H[U]) >= s+1; so s+1 <= T(k+s,d1,d2).  Claim 7s <= 5k - d1 - d2 + 25.
# (both clusters present => 5 d_i < k by the a=6,b=1 tuple, so d1+d2 < 2k/5 automatically)
pv=0; pb=-10**9
for k in range(1,121):
    for d1 in range(0,cdiv(k,5)):
        for d2 in range(d1,cdiv(k,5)):
            if 5*d1>=k or 5*d2>=k: continue
            for s in range(0,2*k):
                n=k+s
                T = Tw(n,d1,d2)
                if s+1 <= T:   # not excluded by the argument
                    pb = max(pb, 7*s-5*k+d1+d2)
                    if 7*s > 5*k-d1-d2+25: pv+=1; print('PropB VIOL',k,s,d1,d2)
print('Prop B: violations', pv, ' max over admissible of 7s-5k+d1+d2 =', pb, '(claim <=25, notes say 24)')
# Cor H2 and N'
print('Cor H2: 5*(7k/4)/12 = ', Fr(5*7,4*12), 'k ; 3/4 - 35/48 =', Fr(3,4)-Fr(35,48))
for k in range(4,400):
    for N in range(0, 2*k):
        if 5*N+38 < 9*k: pass
        if N < Fr(9*k,5)-8: assert Fr(5*N+38,12) < Fr(3*k,4), (k,N)
print("N' special case: |V| < 9k/5-8 => (5|V|+38)/12 < 3k/4 : OK for k<400")
