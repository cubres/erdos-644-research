"""Exact strictness extension for the already proved pencil lemma.

Every revealed type belongs to the closed admissible set C. In a counterexample
each such type is strictly super-heavy somewhere. In a fixed weak pattern P,
the other coordinates are light, so sum_{i in P}(t_i-2*x_i/3)>0. A limiting
MIN/RMIN type satisfies this too: if it were light everywhere, it would itself
contradict the pencil lemma. This file changes only strict LP certificate
systems, never requests or their validity requirements.
"""
from fractions import Fraction as F
import b4core as bc

def strict_forms(ineqs, n):
    forms=[({bc.TAU:F(1)},F(3,4))]
    for k in range((n-bc.TOFF)//3):
        heavy=[]
        for i in range(3):
            sig=({bc.T(k,i):F(-1),bc.G(i):F(1)},F(0))
            light=({bc.T(k,i):F(1),bc.X(i):F(-2,3)},F(0))
            if sig in ineqs: heavy.append(i)
            elif light not in ineqs: raise ValueError('type without a full weak pattern')
        if not heavy: raise ValueError('type without a heavy part')
        d={}
        for i in heavy:
            d[bc.T(k,i)]=F(1)
            d[bc.X(i)]=F(-2,3)
        forms.append((d,F(0)))
    return forms

def strict_system(ineqs, eqs, d, h, n):
    A=list(ineqs)
    for form, rhs in [(d,h)]+strict_forms(ineqs,n):
        row={j:-v for j,v in form.items()};row[n]=F(1)
        A.append((row,-rhs))
    return A,list(eqs),{n:F(1)},F(0)

def install():
    bc.strict_system=strict_system
