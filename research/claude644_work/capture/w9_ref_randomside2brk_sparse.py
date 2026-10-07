# [randomside#2] BREAK-IT referee: exact (mpmath, 300 digits) evaluation of the STATED constants of Lemma F and
# Lemma P of Theorem 1*, at astronomically large k (the regime where the hand proof lives; the attacker's
# sparse_regimes.py used different m and a weaker target).
#  L = max_D D C(N,k)/C(N-T+D,k) (D in {floor(N/k) capped at T, T}),  T = ceil(3k/4),  rho' C(N,k) = L/2.
#  LEMMA F (claim): m = ceil(2e^2 k^2/N)+1, need 15m <= 0.4k, h:=(e k^2/((m+1)(N-15m-k)))^{m+1} <= 0.034,
#     X := ln(rho' C(N-15m,k)/2) >= ln(6 lnC(N,k) + k + ln 7)      [=> Pr <= e^{-k}]
#  LEMMA P (claim): M'=L/2, q_i = C(N-ik,k)/C(N,k), mu = M'^3 q1 q2/6;
#     J := min(mu, M'^2 q1/6, M'/6)/11 >= k/400                       [=> Pr <= e^{-k/400}]
#     also exact Janson exponent Jex = mu/(2(1+3a2+1.5a1)) >= J (check).
#  Also: the claim's reduction 'suffices 0.375 s - 0.06 >= ln(77.2 s) + ln ln(ek)' is tested for SUFFICIENCY.
import sys
from mpmath import mp, mpf, loggamma, log, exp, ceil, floor, e
mp.dps=300
def lC(a,k): return loggamma(a+1)-loggamma(k+1)-loggamma(a-k+1)
def lnL(N,k,T):
    best=None
    for D in set([min(T,floor(N/k)), T, mpf(1)]):
        if D<1 or N-T+D<k: continue
        v=log(D)+lC(N,k)-lC(N-T+D,k)
        best=v if best is None or v>best else best
    return best
def F_check(N,k,T):
    s=k*k/N; m=ceil(2*e**2*s)+1
    ok15 = 15*m<=mpf('0.4')*k
    h=(e*k*k/((m+1)*(N-15*m-k)))**(m+1)
    X=lnL(N,k,T)-log(4)+lC(N-15*m,k)-lC(N,k)
    need=log(6*lC(N,k)+k+log(7))
    return ok15, h<=mpf('0.034'), X-need, m, h
def P_check(N,k,T):
    lM=lnL(N,k,T)-log(2); M=exp(lM)
    q1=exp(lC(N-k,k)-lC(N,k)); q2=exp(lC(N-2*k,k)-lC(N,k))
    mu=M**3*q1*q2/6; a2=M*q2; a1=M*M*q1*q2
    J=min(mu, M*M*q1/6, M/6)/11
    Jex=mu/(2*(1+3*a2+mpf('1.5')*a1))
    assert Jex>=J*(1-mpf(10)**-50)
    return log(J)-log(k/400), log(Jex)-log(k/400)
def suff(s,k): return mpf('0.375')*s-mpf('0.06') - (log(mpf('77.2')*s)+log(log(e*k)))
if __name__=="__main__":
    lks=[float(a) for a in sys.argv[1].split(',')]
    for lk in lks:
        k=floor(exp(mpf(lk))); T=ceil(3*k/4)
        print(f"== ln k = {lk}  (k ~ {float(k):.3e})",flush=True)
        # regime (b): N in [600k, k^2/ln k]
        lo=600*k; hi=k*k/log(k); worstF=None; failsF=[]
        steps=60
        for i in range(steps+1):
            N=floor(lo*(hi/lo)**(mpf(i)/steps))
            ok15,okh,mF,m,h=F_check(N,k,T)
            s=k*k/N
            if not(ok15 and okh and mF>=0): failsF.append((float(s),ok15,okh,float(mF)))
            if suff(s,k)>=0 and not(ok15 and okh and mF>=0):
                print("   !! stated sufficient condition holds but F fails at s=",float(s))
            if worstF is None or mF<worstF[0]: worstF=(mF,float(s),int(m),float(h))
        print(f"  F on [600k,k^2/lnk]: worst margin {float(worstF[0]):.3f} at s={worstF[1]:.3g} (m={worstF[2]}, h={worstF[3]:.2e});"
              f" failures {len(failsF)}" + (f" first {failsF[:3]}" if failsF else ""),flush=True)
        print(f"  stated sufficient cond at s=ln k: {float(suff(log(k),k)):+.3f}")
        # regime (c): N in [k^2/ln k, 1e12 k^2] plus N=1e40 k^2
        worstP=None; failsP=[]
        lo=k*k/log(k); hi=mpf(10)**12*k*k
        pts=[floor(lo*(hi/lo)**(mpf(i)/80)) for i in range(81)]+[floor(mpf(10)**40*k*k), floor(0.75*k*k), floor(3*k*k/4+k)]
        for N in pts:
            mP,mPex=P_check(N,k,T)
            if mP<0: failsP.append((float(N/(k*k)),float(mP)))
            if worstP is None or mP<worstP[0]: worstP=(mP,float(N/(k*k)),mPex)
        print(f"  P on [k^2/lnk,1e40k^2]: worst ln(J/(k/400)) {float(worstP[0]):.3f} at N/k^2={worstP[1]:.3g}"
              f" (exact Janson margin {float(worstP[2]):.3f}); failures {len(failsP)}"+(f" {failsP[:3]}" if failsP else ""),flush=True)
