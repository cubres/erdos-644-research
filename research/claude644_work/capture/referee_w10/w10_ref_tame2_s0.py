# Referee w10, tameness#2: s0 tables, crude (claim) vs refined weight bound; quantifier check.
from mpmath import mp, mpf, log, exp
mp.dps=40
def psi(x): x=mpf(x); return x*log(x)-(x-1)*log(x-1)
def Delta(b): b=mpf(b); return psi(1+b)-psi(1+b/2)
def s0(b,p,refined):
    s=0
    while True:
        base = (2+mpf(b))/mpf(b) if refined else exp(mpf(4)/7)
        if mpf(6)/7*base**s*Delta(b) > mpf(7)/4*log(p): return s
        s+=1
print("Delta monotone check:", all(Delta(i/1000.)<Delta((i+1)/1000.) for i in range(1,500)))
for b in ('0.001','0.01','0.02','0.05','0.1','0.2','0.4','0.4999'):
    print("beta",b," crude s0(p=2,7,64,1e6) =",[s0(b,p,False) for p in (2,7,64,10**6)],
          " refined =",[s0(b,p,True) for p in (2,7,64,10**6)])
# crude bound with FIXED s: smallest beta covered, beta0(s,p): (6/7)e^{4s/7}Delta(beta0)=(7/4)ln p
def beta0(s,p):
    lo,hi=mpf('1e-40'),mpf('0.5')
    tgt=mpf(7)/4*log(p)/(mpf(6)/7*exp(mpf(4*s)/7))
    if Delta(hi)<=tgt: return None
    for _ in range(300):
        mid=(lo+hi)/2
        if Delta(mid)>tgt: hi=mid
        else: lo=mid
    return hi
for s in (3,5,13,63):
    print("crude, fixed s=%d: beta0(p=2,7,1e6) ="%s,[mp.nstr(beta0(s,p),4) if beta0(s,p) else 'none' for p in (2,7,10**6)])
# refined: worst beta in (0,1/2) for fixed s -- min over beta of (6/7)((2+b)/b)^s Delta(b)
for s in (1,2,3,5,13):
    vals=[(mpf(6)/7*((2+mpf(b))/mpf(b))**s*Delta(b),b) for b in [mpf(i)/2000 for i in range(1,1000)]]
    mn=min(vals)
    pmax=exp(mn[0]/(mpf(7)/4))
    print("refined, s=%d: min_beta LHS = %s at beta=%s  => every beta in (0,1/2) works for p < %s"%(s,mp.nstr(mn[0],5),mp.nstr(mn[1],4),mp.nstr(pmax,5)))
# s=63, crude: claimed "every p < exp(1e14)" (notes) at beta>=0.02
print("crude s=63 beta=0.02: ln p bound =", mp.nstr(mpf(6)/7*exp(mpf(4*63)/7)*Delta('0.02')/(mpf(7)/4),6))
