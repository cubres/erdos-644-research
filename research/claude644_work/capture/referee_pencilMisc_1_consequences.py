#!/usr/bin/env python3
"""Referee check 4: what the method actually yields at a critical host (U = E cup B, |B| = t-1,
F = E, g = 0), using the EXACT optimum Q* of the anchored labelling (same model as
referee_pencilMisc_1_labeling.py).  Deficit lower bound delivered: d >= t - Q*.

Compares with the claimed consequence d >= 2(t - 3e/4) - O(1) and with the corrected
d >= min(t - 2ceil(e/4), 2t - 6ceil(e/4) - 1).
Also checks the trivial-U observation for the 'relaxed principal target'.
"""
def cdiv(a, b):
    return -(-a // b)

def comps(n, k):
    if k == 1:
        yield (n,); return
    for i in range(n + 1):
        for r in comps(n - i, k - 1):
            yield (i,) + r

def qstar(f, g, N, t):
    best = None
    for (xb, xb2, xc, xc2) in comps(f + g, 4):
        Pa = max(xb + xc, xb2 + xc2); Pa2 = max(xb2 + xc, xb + xc2)
        if max(Pa, Pa2) > t - 1:
            continue
        pen = max(cdiv(f, 2), f - (xb + xb2), f - (xc + xc2))
        w = max(0, N - f - (t - 1 - Pa) - (t - 1 - Pa2))
        v = w + pen
        best = v if best is None or v < best else best
    return best

worst_gap = None
for e in range(4, 49):
    for t in range(cdiv(e, 2) + 2, 2 * e):
        qs = qstar(e, 0, e + t - 1, t)
        if qs is None:
            continue
        dmin = t - qs
        corrected = min(t - 2 * cdiv(e, 4), 2 * t - 6 * cdiv(e, 4) - 1)
        assert dmin >= corrected, (e, t, dmin, corrected)
        claimed = 2 * t - 1.5 * e
        gap = claimed - dmin
        if worst_gap is None or gap > worst_gap[0]:
            worst_gap = (gap, e, t, dmin, claimed)
print('corrected deficit bound min(t-2ceil(e/4), 2t-6ceil(e/4)-1) is delivered for all e<=48')
print('largest shortfall of the method vs claimed 2t-3e/2 :', worst_gap, '(grows linearly with t-e)')
for (e, t) in [(40, 48), (40, 60), (44, 60)]:
    qs = qstar(e, 0, e + t - 1, t)
    print(f'  e={e}, t={t}: method gives d >= {t-qs}; claimed 2t-3e/2 = {2*t-1.5*e}; t-e/2 = {t-e/2}')

# relaxed principal target with U = E: LHS = (t - 1) + (e - e - t) = -1 regardless.
for (e, t) in [(40, 31), (80, 61), (100, 76)]:
    print(f'  U=E, e={e}, t={t}: LHS=-1, 2(t-3e/4)={2*t-1.5*e}; anchored bound q <= {qstar(e,0,e,t)} (no contradiction since q=1)')
