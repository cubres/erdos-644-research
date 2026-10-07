"""Learn a region of invalid requests using an exact affine response witness.

A numerical LP selects a basis only. Rational matrix inversion and symbolic
substitution verify the resulting response on every point of its region.
"""
from fractions import Fraction as F
from math import gcd
import numpy as np
from scipy.optimize import linprog
import sympy as sp
import z3


def linear(expr,index):
    n=len(index)
    if z3.is_rational_value(expr):return [F(0)]*n+[F(expr.numerator_as_long(),expr.denominator_as_long())]
    if z3.is_const(expr) and expr.decl().name() in index:
        out=[F(0)]*(n+1);out[index[expr.decl().name()]]=1;return out
    kind=expr.decl().kind();children=expr.children()
    if kind==z3.Z3_OP_TO_REAL:return linear(children[0],index)
    if kind==z3.Z3_OP_UMINUS:return [-v for v in linear(children[0],index)]
    if kind in (z3.Z3_OP_ADD,z3.Z3_OP_SUB):
        rows=[linear(c,index) for c in children]
        if kind==z3.Z3_OP_SUB:rows=[rows[0]]+[[-v for v in r] for r in rows[1:]]
        return [sum(v) for v in zip(*rows)]
    if kind==z3.Z3_OP_MUL:
        scalar=F(1);nonconstant=[]
        for c in children:
            r=linear(c,index)
            if any(r[:-1]):nonconstant.append(r)
            else:scalar*=r[-1]
        assert len(nonconstant)<=1
        return [scalar*v for v in nonconstant[0]] if nonconstant else [F(0)]*n+[scalar]
    if kind==z3.Z3_OP_DIV:
        a,b=map(lambda c:linear(c,index),children);assert not any(b[:-1])
        return [v/b[-1] for v in a]
    raise ValueError(('nonlinear expression',str(expr)))


def inequalities(expr,index):
    out=[]
    def visit(e,neg=False):
        if z3.is_true(e):assert not neg;return
        if z3.is_false(e):assert neg;return
        if z3.is_not(e):visit(e.arg(0),not neg);return
        if z3.is_and(e):
            assert not neg
            for child in e.children():visit(child)
            return
        kind=e.decl().kind();assert kind in (z3.Z3_OP_LE,z3.Z3_OP_GE,z3.Z3_OP_LT,z3.Z3_OP_GT)
        a,b=[linear(c,index) for c in e.children()];row=[v-w for v,w in zip(a,b)]
        strict=kind in (z3.Z3_OP_LT,z3.Z3_OP_GT)
        if kind in (z3.Z3_OP_GE,z3.Z3_OP_GT):row=[-v for v in row]
        if neg:row=[-v for v in row];strict=not strict
        den=1
        for c in row:den=den*c.denominator//gcd(den,c.denominator)
        nums=[int(c*den) for c in row];div=0
        for c in nums:div=gcd(div,abs(c))
        out.append((tuple(F(c,div or 1) for c in nums),strict))
    visit(expr)
    unique={}
    for row,strict in out:
        if not any(row[:-1]):
            assert row[-1]<0 if strict else row[-1]<=0
            continue
        den=1
        for c in row[:-1]:den=den*c.denominator//gcd(den,c.denominator)
        divisor=0
        for c in row[:-1]:divisor=gcd(divisor,abs(int(c*den)))
        factor=F(den,divisor);canonical=tuple(c*factor for c in row);key=canonical[:-1]
        previous=unique.get(key)
        if previous is None or canonical[-1]>previous[0]:unique[key]=(canonical[-1],strict)
        elif canonical[-1]==previous[0]:unique[key]=(canonical[-1],strict or previous[1])
    return sorted((key+(constant,),strict) for key,(constant,strict) in unique.items())


def learn(poly,h,d,request):
    n=len(h);index={v.decl().name():i for i,v in enumerate(list(h)+list(d))}
    rows=inequalities(poly,index);A=[];B=[]
    # A*(h,margin) <= B(d); all strict rows have a common positive margin.
    for row,strict in rows:
        A.append(list(row[:n])+[F(int(strict))])
        B.append([-v for v in row[n:2*n]]+[-row[-1]])
    A += [[F(0)]*n+[F(-1)],[F(0)]*n+[F(1)]]
    B += [[F(0)]*(n+1),[F(0)]*n+[F(1)]]
    rhs=[sum(a*b for a,b in zip(row[:-1],request))+row[-1] for row in B]
    result=linprog([0]*n+[-1],A_ub=np.array(A,dtype=float),b_ub=list(map(float,rhs)),bounds=(None,None),method='highs')
    assert result.status==0 and result.x[-1]>0
    tight=[i for i,s in enumerate(result.ineqlin.residual) if abs(s)<1e-7]
    basis=[];echelon={}
    for i in tight:
        r=A[i][:]
        for pivot,old in sorted(echelon.items()):
            factor=r[pivot]
            if factor:r=[v-factor*w for v,w in zip(r,old)]
        pivot=next((j for j,v in enumerate(r) if v),None)
        if pivot is None:continue
        factor=r[pivot];echelon[pivot]=[v/factor for v in r];basis.append(i)
        if len(basis)==n+1:break
    assert len(basis)==n+1
    raw=sp.Matrix([A[i] for i in basis]).inv()*sp.Matrix([B[i] for i in basis])
    witness=[[F(int(v.p),int(v.q)) for v in row] for row in raw.tolist()]
    # Conditions on d under which this affine response solves every row.
    conditions=[]
    for a,b in zip(A,B):
        conditions.append([sum(v*witness[j][k] for j,v in enumerate(a))-b[k] for k in range(n+1)])
    value=lambda row:sum(v*w for v,w in zip(row[:-1],request))+row[-1]
    assert all(value(row)<=0 for row in conditions) and value(witness[-1])>0
    def af(row):return z3.Sum(*[z3.RealVal(str(v))*q for v,q in zip(row[:-1],d) if v],z3.RealVal(str(row[-1])))
    region=z3.And(*[af(row)<=0 for row in conditions],af(witness[-1])>0)
    certificate={'basis':basis,'A':[list(map(str,row)) for row in A],
                 'B':[list(map(str,row)) for row in B],
                 'affine_response':[list(map(str,row)) for row in witness],
                 'region':[list(map(str,row)) for row in conditions],
                 'parameters':list(map(str,request)),'rows_before_projection':len(rows)}
    return z3.simplify(region),certificate
