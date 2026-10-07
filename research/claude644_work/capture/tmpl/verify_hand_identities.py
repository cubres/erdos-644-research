# Exact symbolic verification of every linear identity used in the hand proofs of
# (1) the Gap-Pair Lemma, (2) Theorem TT (two types, p parts), (3) the V-support construction.
import sympy as sp
x,y,a,b=sp.symbols('x y a b')
def chk(lhs,rhs,msg):
    d=sp.expand(lhs-rhs); assert d==0,(msg,d); print('ok',msg)
# ---- Gap-Pair: hyps H1: 7(1-a)-4y>0, H2: 7b-4x>0, G: x+y-7/4-(b-a)>0, a>=0, b<=1, b-a>=0
H1=7*(1-a)-4*y; H2=7*b-4*x; G=x+y-sp.Rational(7,4)-(b-a)
# P1: x-(b+3a/4) = G + H1/4 ;  P2: y-(7/4-a-3b/4) = G + H2/4
chk(x-(b+3*a/4), G+H1/4, 'P1'); chk(y-(sp.Rational(7,4)-a-3*b/4), G+H2/4, 'P2')
# Qb facets: (b+3a/4)-(a+3b/4) = (b-a)/4 ; (7/4-a-3b/4)-3(1-b)/2 = 1/4+3b/4-a >= (1-b)/4 + (b-a)
chk((b+3*a/4)-(a+3*b/4),(b-a)/4,'Qb1'); chk((sp.Rational(7,4)-a-3*b/4)-sp.Rational(3,2)*(1-b),(1-b)/4+(b-a),'Qb2')
# Qa facets: (b+3a/4)-3a/2 = (b-a)+a/4 ; (7/4-a-3b/4)-((1-b)+3(1-a)/4) = (b-a)/4
chk((b+3*a/4)-sp.Rational(3,2)*a,(b-a)+a/4,'Qa1'); chk((sp.Rational(7,4)-a-3*b/4)-((1-b)+sp.Rational(3,4)*(1-a)),(b-a)/4,'Qa2')
R1=sp.Rational(3,2)*b-x; R2=sp.Rational(3,2)*(1-a)-y
chk(x-(a+b), 2*G+R1+2*R2+(1-b)/2,'V1'); chk(y-(2-a-b), 2*G+2*R1+R2+a/2,'V2')
chk(x-(sp.Rational(5,4)*a+b/2), G+R2+(sp.Rational(1,4)+b/2-sp.Rational(3,4)*a) - 0, 'V3a')
chk(sp.Rational(1,4)+b/2-sp.Rational(3,4)*a, (1-b)/4+sp.Rational(3,4)*(b-a),'V3b')
chk(y-(sp.Rational(7,4)-sp.Rational(5,4)*a-b/2), G+R1+a/4,'V4')
# ---- Theorem TT: per-part checks (symbols for the relevant parts)
xi,ai,bi,xK,bK,xL,aL,aK=sp.symbols('xi ai bi xK bK xL aL aK')
K2iK=(xi-ai)+(xK-bK)-sp.Rational(3,4)       # >=0
RK=sp.Rational(3,2)*bK-xK                   # >0 (Qb failure at K)
RL=sp.Rational(3,2)*aL-xL                   # >0
K2LK=(xL-aL)+(xK-bK)-sp.Rational(3,4)       # >=0
# a_L+b_K>3/2:  (aL+bK-3/2)/2 = K2LK + RK + RL ... check: 
chk((aL+bK-sp.Rational(3,2))/2, K2LK+RK+RL,'aL+bK>3/2')
# i!=K, a_i>0, with slack s_b=1-bK-bi>=0, a_i<=1:
sb=1-bK-bi
chk(xi-ai-bi, K2iK+RK+sb+(bK/2-sp.Rational(1,4)),'TT V1 at i')   # bK>1/2
chk(xi-sp.Rational(5,4)*ai-bi/2, K2iK+RK+sb/2+(1-ai)/4,'TT V2 at i')
# i=K, a_K>0, sa=1-aL-aK>=0:
sa=1-aL-aK
K2LKx=(xL-aL)+(xK-bK)-sp.Rational(3,4)
chk(xK-aK-bK, K2LKx+RL+sa+(aL/2-sp.Rational(1,4)),'TT V1 at K')
chk(xK-sp.Rational(5,4)*aK-bK/2, K2LKx+RL+sp.Rational(5,4)*sa+(sp.Rational(3,4)*aL+bK/2-sp.Rational(1,2)),'TT V2 at K')
# Qb facet a_i+3b_i/4<=x_i for a_i>b_i>0, i!=J, with 4x_J<7b_J and b_i+b_J<=1:
xJ,bJ=sp.symbols('xJ bJ')
K2iJ=(xi-ai)+(xJ-bJ)-sp.Rational(3,4); RJ=sp.Rational(7,4)*bJ-xJ
chk(xi-ai-sp.Rational(3,4)*bi, K2iJ+RJ+sp.Rational(3,4)*(1-bJ-bi) - 0 ,'TT Qb facet (a>b case)')
print('ALL IDENTITIES VERIFIED')
