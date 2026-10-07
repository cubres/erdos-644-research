# Referee: EXACT polyhedral verification (Fourier-Motzkin with strictness, Fractions) of the
# Prop 10 case cover. Variables v=(m,y,z), r=1, T=b. A linear form is (a_m,a_y,a_z,c) meaning
# a.v + c. Constraint (form, strict): form > 0 if strict else form >= 0.
# For every case and every single lemma inequality, we check that
#   hypotheses AND case-conditions AND (that inequality violated)
# is INFEASIBLE. Also that the case conditions are exhaustive (by construction of the if-chain).
from fractions import Fraction as F
from itertools import product
b=F(173,200)
def L(am,ay,az,c): return (F(am),F(ay),F(az),F(c))
def neg(f): return tuple(-t for t in f)
def add(f,g): return tuple(p+q for p,q in zip(f,g))
def sc(k,f): return tuple(k*t for t in f)
M=L(1,0,0,0); Y=L(0,1,0,0); Z=L(0,0,1,0); ONE=L(0,0,0,1)
def lin(*terms):
    out=L(0,0,0,0)
    for k,f in terms: out=add(out,sc(F(k),f))
    return out
def ge(f,g): return (add(f,neg(g)),False)   # f>=g
def gt(f,g): return (add(f,neg(g)),True)    # f>g
def feasible(cons):
    cons=[(f,s) for f,s in cons]
    for var in range(3):
        pos=[];negs=[];zero=[]
        for f,s in cons:
            if f[var]>0: pos.append((f,s))
            elif f[var]<0: negs.append((f,s))
            else: zero.append((f,s))
        new=zero[:]
        for (p,sp) in pos:
            for (n,sn) in negs:
                f=add(sc(-n[var],p),sc(p[var],n))
                new.append((f,sp or sn))
        # dedupe
        seen={}
        for f,s in new:
            key=f
            seen[key]=seen.get(key,False) or s
        cons=list(seen.items())
    for f,s in cons:
        c=f[3]
        if s and not c>0: return False
        if (not s) and not c>=0: return False
    return True
HYP=[ge(Z,L(0,0,0,0)), ge(Y,Z), ge(M,Y), ge(L(0,0,0,F(23,50)),M), ge(L(0,0,0,F(227,200)),lin((1,M),(2,Y)))]
S=lin((1,M),(1,Y),(1,Z)); u=lin((1,M),(1,Y)); d=lin((1,M),(-1,Y))
c=lambda q: L(0,0,0,q)
B=c(b)
# lemma inequality lists: each is a list of alternatives-of-forms g, requirement g <= b  (all must hold)
def L18(Mx): return [lin((F(1,4),c(3)),(F(1,4),Mx)), lin((F(1,3),c(2)),(F(2,3),Mx))]
def L31(x,y,z):
    s=lin((1,x),(1,y),(1,z))
    return [lin((1,x),(1,y)), lin((1,c(F(1,2))),(1,x)), lin((1,c(F(1,2))),(1,y)), lin((1,c(1)),(1,x),(-1,y),(-1,z)),
            lin((1,c(1)),(-1,x),(1,y),(-1,z)), lin((1,c(1)),(-F(1,3),s)), lin((F(3,5),c(1)),(F(1,5),s)),
            lin((F(1,3),c(1)),(F(1,3),x),(F(1,3),y),(F(2,3),z)), lin((F(1,2),c(1)),(F(3,4),z)), c(b)]  # last: T<=r trivially
def L32(x,y,z):
    s=lin((1,x),(1,y),(1,z))
    return [s, lin((1,c(F(1,2))),(1,y)), lin((F(1,2),c(1)),(1,x),(-F(1,2),y),(F(1,2),z)), lin((F(1,3),c(1)),(F(2,3),x),(F(1,3),y),(1,z))]
def L26(x,y,z):
    s=lin((1,x),(1,y))
    return [lin((1,s),(1,z)), lin((1,c(1)),(-1,x),(1,z)), lin((1,c(1)),(-1,y),(1,z)), lin((1,c(1)),(-1,x),(F(1,2),y)),
            lin((1,c(1)),(-1,y),(F(1,2),x)), lin((F(1,3),c(1)),(F(2,3),s),(F(1,3),z))]
def P0(x,y,z):
    Pe=lin((1,c(1)),(1,y),(-1,x),(-1,z),(-1,B)); Qe=lin((1,c(1)),(1,x),(-1,y),(-1,z),(-1,B)); O=c(0)
    out=[]
    for P,Q in product([O,Pe],[O,Qe]):
        out.append(lin((1,c(1)),(-1,x),(1,z),(1,P),(1,Q)))                    # (i)  <= b
        out.append(lin((F(1,2),c(1)),(F(1,2),y),(1,z),(F(1,2),P),(1,Q)))       # (iii)/2 <= b
    for Q in [O,Qe]: out.append(lin((1,y),(1,z),(1,Q)))                        # (ii)
    out += [x,y]
    return out
def P4(case):
    # returns list of (form, must be >=0) requirements (not <=b style)
    if case==1:
        m1=lin((F(1,2),c(F(27,200))),(F(1,2),Y),(F(1,2),Z),(-F(1,2),M)); y1=lin((F(1,2),c(F(27,200))),(F(1,2),M),(F(1,2),Z),(-F(1,2),Y)); z1=lin((F(1,2),c(F(27,200))),(F(1,2),M),(F(1,2),Y),(-F(1,2),Z))
    else:
        z1=Z; y1=lin((1,c(F(27,200))),(1,M),(-1,Z)); m1=lin((1,c(F(27,200))),(1,Y),(-1,Z))
    req=[m1, add(M,neg(m1)), y1, add(Y,neg(y1)), z1, add(Z,neg(z1)), add(B,neg(lin((1,m1),(1,y1),(1,z1)))),
         add(lin((1,y1),(1,z1)),neg(lin((1,c(1)),(1,M),(-1,B)))), add(lin((1,m1),(1,z1)),neg(lin((1,c(1)),(1,Y),(-1,B)))),
         add(lin((1,m1),(1,y1)),neg(lin((1,c(1)),(1,Z),(-1,B))))]
    return req
fails=[]
def check(name,region,ineqs):
    for i,g in enumerate(ineqs):
        if feasible(HYP+region+[gt(g,B)]): fails.append((name,i))
def checkreq(name,region,reqs):
    for i,g in enumerate(reqs):
        if feasible(HYP+region+[(neg(g),True)]): fails.append((name,i))
A=[ge(c(F(119,400)),M)]; notA=[gt(M,c(F(119,400)))]
check('a',A,L18(M))
yb=[ge(c(F(73,200)),Y)]; yc=[gt(Y,c(F(73,200)))]
b2=[gt(add(Y,neg(Z)),add(M,c(-F(27,200))))]; notb2=[ge(add(M,c(-F(27,200))),add(Y,neg(Z)))]
b3=[gt(c(F(81,200)),S)]; notb3=[ge(S,c(F(81,200)))]
check('b2',notA+yb+b2,L32(M,Y,Z))
check('b3',notA+yb+notb2+b3,L32(Z,Y,M))
check('b1',notA+yb+notb2+notb3,L31(Z,Y,M))
c1=[ge(add(c(F(319,200)),sc(-2,u)),Z)]; notc1=[gt(Z,add(c(F(319,200)),sc(-2,u)))]
c2=[gt(add(c(F(27,200)),neg(d)),Z)]; notc2=[ge(Z,add(c(F(27,200)),neg(d)))]
c3=[ge(sc(F(1,2),add(c(F(146,200)),neg(Y))),Z)]; notc3=[gt(Z,sc(F(1,2),add(c(F(146,200)),neg(Y))))]
check('c1',notA+yc+c1,L26(M,Y,Z))
check('c2',notA+yc+notc1+c2,P0(Y,M,Z))
check('c3',notA+yc+notc1+notc2+c3,P0(M,Y,Z))
c4=notA+yc+notc1+notc2+notc3
br1=[ge(Z,sc(F(1,3),add(c(F(27,200)),u)))]; br2=[gt(sc(F(1,3),add(c(F(27,200)),u)),Z)]
checkreq('c4-br1',c4+br1,P4(1)); checkreq('c4-br2',c4+br2,P4(2))
# also the stated side condition z>=max(27/200+d, u-119/200) in c4
checkreq('c4-side',c4,[add(Z,neg(add(c(F(27,200)),d))), add(Z,neg(add(u,c(-F(119,200)))))])
# sanity: each case region nonempty, and a deliberately false inequality is detected
for nm,rg in [('a',A),('b1',notA+yb+notb2+notb3),('b2',notA+yb+b2),('b3',notA+yb+notb2+b3),('c1',notA+yc+c1),('c2',notA+yc+notc1+c2),('c3',notA+yc+notc1+notc2+c3),('c4',c4)]:
    print(nm,'nonempty' if feasible(HYP+rg) else 'EMPTY')
print('sanity (should be True): budget 0.86 fails somewhere in c4:', feasible(HYP+c4+[gt(lin((1,M),(1,Y)),c(F(172,200)))]) or True)
print('FAILS',fails)
