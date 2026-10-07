# Referee w10, tameness#2: exact finite-k evaluation of Prop S's failure-probability bound.
# log10 of  p^N (N+1)^p (e mu/a)^{a/omega},  a = 6/7 (eta -> 1/7), mu = rho C(m,k), rho = 2N ln2/C(u0,k).
from mpmath import mp, mpf, log, exp, binomial, floor, e
mp.dps=50
def bound(k,beta,p,s,refined):
    N=7*k//4-1; u0=int(floor((1+mpf(beta))*k)); m=int(floor((1+mpf(beta)/2)*k))
    rho=2*N*log(2)/binomial(u0,k); mu=rho*binomial(m,k); a=mpf(6)/7
    om = (1-mpf(k)/(m+p*s))**s if refined else exp(-mpf(s)*k/N)
    if e*mu/a>=1: return None
    lg = N*log(p)+p*log(N+1)+(a/om)*log(e*mu/a)
    return lg/log(10), rho
for (beta,p,s,ref) in [(0.1,2,5,False),(0.1,7,6,False),(0.1,64,8,False),(0.1,10**6,10,False),
                       (0.1,2,1,True),(0.1,64,2,True),(0.1,10**6,3,True),(0.02,10**6,3,True),(0.02,10**6,12,False)]:
    row=[]
    for k in (40,100,400,1000,4000,20000):
        r=bound(k,beta,p,s,ref); row.append('n/a' if r is None else mp.nstr(r[0],4))
    print(f"beta={beta} p={p} s={s} {'refined' if ref else 'crude  '}: log10 P(bad) bound at k=40,100,400,1e3,4e3,2e4:",row)
