# Referee w9, claim randomside#2 (Theorem 1*), LINE-BY-LINE lens.
# Independent high-precision (mpmath, dps 60) check of the EXACT inequalities of Lemma F and Lemma P, with the claim's
# own parameter choices (m = ceil(2e^2 k^2/N)+1, D = floor(N/k) resp. D = T, T = ceil(3k/4)), for k up to 1e16.
# ln C(N,k) is computed with loggamma at high precision (no float cancellation).
# Lemma F needs:  (i) 15m <= 0.4k ; (ii) heavy fraction  C(k,m+1)C(N',k-m-1)/C(N',k) <= 0.034 with N'=N-15m ;
#                 (iii) X := rho' * C(N-15m,k)/2 * (1-6*0.034)*2 ... we use the claim's Good >= C(N-15m,k)/2 and need
#                 rho' * C(N-15m,k)/2 >= 6 ln C(N,k) + ln 7 + k   (=> 7 C^6 e^{-X} <= e^{-k}).
# Lemma P needs:  J := mu/(2(1+3a2+1.5a1)) >= k/400.
# Also checks the claim's simplified sufficient condition 0.375 s - 0.06 >= ln(77.2 s) + ln ln(ek) at s = ln k.
import sys
from mpmath import mp, mpf, loggamma, log, exp, ceil, floor, e
mp.dps = 60
def lC(n, r):
    n = mpf(n); r = mpf(r)
    return loggamma(n+1) - loggamma(r+1) - loggamma(n-r+1)
def logL(N, k, T, Ds):
    return max(log(D) + lC(N, k) - lC(N-T+D, k) for D in Ds)
def lemmaF(N, k):
    T = int(ceil(mpf(3)*k/4)); s = mpf(k)**2/N
    m = int(ceil(2*e**2*s)) + 1
    ok1 = 15*m <= 0.4*k
    Np = N - 15*m
    heavy = lC(k, m+1) + lC(Np, k-m-1) - lC(Np, k)
    ok2 = heavy <= log(mpf('0.034'))
    D = int(floor(mpf(N)/k)); D = max(1, min(D, T))
    lL = logL(N, k, T, [D])
    lrho = lL - log(2) - lC(N, k)                 # ln rho'
    lX = lrho + lC(N-15*m, k) - log(2)             # ln (rho' C(N-15m,k)/2)
    need = 6*lC(N, k) + log(7) + k
    return ok1, ok2, float(lX - log(need)), m, float(heavy)
def lemmaP(N, k):
    T = int(ceil(mpf(3)*k/4))
    D1 = max(1, min(int(floor(mpf(N)/k)), T))
    lL = logL(N, k, T, sorted(set([D1, T])))       # the claim uses D=floor(N/k) if N<=Tk else D=T; max is >= both
    lM = lL - log(2)
    r1 = lC(N-k, k) - lC(N, k); r2 = lC(N-2*k, k) - lC(N, k)
    lmu = 3*lM + r1 + r2 - log(6)
    a2 = exp(lM + r2); a1 = exp(2*lM + r1 + r2)
    J = exp(lmu) / (2*(1 + 3*a2 + mpf('1.5')*a1))
    return float(log(J) - log(mpf(k)/400))
def simplified(k):
    s = log(k)
    return float(mpf('0.375')*s - mpf('0.06') - log(mpf('77.2')*s) - log(log(e*k)))
if __name__ == "__main__":
    ks = [int(float(a)) for a in sys.argv[1].split(',')]
    for k in ks:
        lk = log(k)
        print(f"k={k:.3e} ln k={float(lk):.2f} simplified-cond margin at s=ln k: {simplified(k):+.3f}")
        # Lemma F range N in [600k, k^2/ln k]
        Nlo = 600*k; Nhi = int(mpf(k)**2/lk)
        worstF = None; badF = []
        if Nhi >= Nlo:
            N = Nlo
            while True:
                r = lemmaF(N, k)
                if worstF is None or r[2] < worstF[1]: worstF = (N, r[2], r[3], r[4])
                if not (r[0] and r[1] and r[2] >= 0): badF.append((N, r))
                if N >= Nhi: break
                N = min(Nhi, int(N*1.5))
        print(f"   F on [600k,k^2/lnk]: worst margin {worstF[1] if worstF else None:+.3f} at N={worstF[0] if worstF else 0:.3e} m={worstF[2] if worstF else 0} heavy={worstF[3] if worstF else 0:.2f}; failures: {len(badF)}"
              + (f" first {badF[0][0]:.3e} {badF[0][1]}" if badF else ""))
        # Lemma P range N in [k^2/ln k, 1e8 k^2]
        N = Nhi; worstP = None
        while N <= 10**8*k*k:
            p = lemmaP(N, k)
            if worstP is None or p < worstP[1]: worstP = (N, p)
            N = int(N*2.5)
        print(f"   P on [k^2/lnk, 1e8 k^2]: worst margin ln(J/(k/400)) = {worstP[1]:+.3f} at N={worstP[0]:.3e}")
