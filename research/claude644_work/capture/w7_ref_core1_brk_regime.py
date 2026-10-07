# Referee w7 / core#1 BREAK-IT: boundary of "tau_f <= 6k/S_min < 8 in the counterexample regime".
# For every k and every integer t with 3k/4 < t <= ceil(7k/8): is 6k/stated < 8 ?  (exact Fractions)
from fractions import Fraction as Fr
bad_stated=[]; bad_sharp=[]
for k in range(1,401):
    for t in range(1,-(-7*k//8)+1):
        if 4*t<=3*k: continue
        st=min(t,(3*(2*t-k-2))//2+1); sh=min(t,-((-3*(2*t-k-1))//2))
        if st<=0 or Fr(6*k,st)>=8: bad_stated.append((k,t,st,Fr(6*k,st) if st>0 else None))
        if sh<=0 or Fr(6*k,sh)>=8: bad_sharp.append((k,t,sh))
print('t>3k/4 but 6k/stated >= 8 (or stated<=0):',len(bad_stated),'cases; first:',[(k,t,s,str(r)) for k,t,s,r in bad_stated[:8]])
print('  residues k mod 4 of failures:',sorted(set(k%4 for k,*_ in bad_stated)),' all have 4t=3k+2:',all(4*t==3*k+2 for k,t,*_ in bad_stated))
print('with sharpened ceil(3(2t-k-1)/2): failures',len(bad_sharp),bad_sharp[:8])
