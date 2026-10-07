# Check the explicit sufficient conditions of the SPARSE part of Theorem 1* (all N) for given k, tau.
# Size lemma: tau(H)>=T => |H| >= L := max_D D*C(N,k)/C(N-T+D,k).  rho' = L/(2 C(N,k)).
# (F) Fano-direct: m minimal with 6*C(k,m+1)*prod_{i=0..m}(k-i)/(N'-k+1+i) <= 1/2, N'=N-15m;
#     need rho'*C(N-15m,k)/2 >= 6 ln C(N,k) + k/100 + ln 7  => Pr[(7,2)&tau>=T] <= 2(e^{-k/100} + e^{-L/2}).
# (P) 3PD Janson: J = mu/(2(1+3a2+1.5a1)) ; need J >= k/100  => Pr <= 2e^{-k/100}.
# All binomial RATIOS computed as sums of log1p (stable for huge N).  NUMERICAL CHECK of explicit inequalities.
import math, sys, numpy as np
def lratio(N,Np,k):   # ln C(N,k)/C(Np,k), N>=Np>=k
    i=np.arange(k,dtype=np.float64); return float(np.sum(np.log1p((N-Np)/(Np-i))))
def lC(N,k):
    i=np.arange(k,dtype=np.float64); return float(np.sum(np.log((N-i)/(k-i))))
def logL(N,k,T):
    Ds=sorted(set([1,2,3]+[int(round(1.2**i)) for i in range(1,200) if 1.2**i<=T]+[T]))
    return max(math.log(D)+lratio(N,N-T+D,k) for D in Ds)
def fano_margin(N,k,T,lL):
    lrho_rel=lL-math.log(2)          # ln(rho' C(N,k))
    for m in range(1,k):
        Np=N-15*m
        if Np-k<1 or 15*m>=T: return None
        lr=math.log(6)+math.lgamma(k+1)-math.lgamma(m+2)-math.lgamma(k-m)+sum(math.log((k-i)/(Np-k+1+i)) for i in range(m+1))
        if lr<=math.log(0.5): break
    lhs=lrho_rel-lratio(N,N-15*m,k)-math.log(2)       # ln(rho' * C(N-15m,k)/2)
    need=6*lC(N,k)+k/100+math.log(7)
    return lhs-math.log(need), m
def pd_margin(N,k,T,lL):
    lMp=lL-math.log(2)                # ln M' = ln(rho' C(N,k))
    r1=-lratio(N,N-k,k); r2=-lratio(N,N-2*k,k)   # ln C(N-k,k)/C(N,k), ln C(N-2k,k)/C(N,k)
    lmu=3*lMp+r1+r2-math.log(6)
    la2=lMp+r2; la1=2*lMp+r1+r2
    terms=[0.0, math.log(3)+la2, math.log(1.5)+la1]; mx=max(terms)
    lden=math.log(2)+mx+math.log(sum(math.exp(t-mx) for t in terms))
    return (lmu-lden)-math.log(k/100)
if __name__=="__main__":
    tau=float(sys.argv[2]) if len(sys.argv)>2 else 0.75
    for k in [int(a) for a in sys.argv[1].split(',')]:
        T=math.ceil(tau*k); print(f"k={k} T={T}")
        N=int(600*k); unc=[]; firstF=lastF=firstP=None
        while N<=10**6*k**2:
            lL=logL(N,k,T); f=fano_margin(N,k,T,lL); p=pd_margin(N,k,T,lL)
            okF= f is not None and f[0]>=0; okP=p>=0
            if not(okF or okP): unc.append(N)
            print(f"  N={N:.3e} c=N lnk/k^2={N*math.log(k)/k**2:9.3f} lnL={lL:9.1f} F:{'OK ' if okF else 'no '}{(f[0] if f else float('nan')):8.2f} m={f[1] if f else '-'}  P:{'OK ' if okP else 'no '}{p:9.2f}")
            N=int(N*1.8)
        print("  UNCOVERED:",[f"{g:.2e}" for g in unc])
