"""normalized (k=1) closing conditions of known lemmas: return minimal budget over orientations."""
import itertools
def perms(a,b,c): return set(itertools.permutations((a,b,c)))
def split(x,y,z):
    S=x+y+z; return min(max((1+S)/2, 1-a+abs(b-c), 1/3+a) for a,b,c in perms(x,y,z))
def asym1(x,y,z):
    S=x+y+z; return min(max(S,0.5+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3) for a,b,c in perms(x,y,z))
def asym2(x,y,z):
    S=x+y+z; return min(max(S,1/3+a,1-a+c,(1+2*a+3*b+c)/3) for a,b,c in perms(x,y,z))
def four(x,y,z):
    S=x+y+z; return min(max(a+b,0.5+a,0.5+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4) for a,b,c in perms(x,y,z))
def sym(x,y,z):
    S=x+y+z; m,yy,zz=sorted((x,y,z),reverse=True)
    return max(1+m-yy-zz,(1+m)/2,(2+m+yy-zz)/3,(3+S)/5)
def s0(x,y,z):
    best=9
    for a,b,c in perms(x,y,z):
        v=max(a,a+b,a+c,b+c,(1+2*c)/2,(1+2*b)/2,(1+3*a)/3,(2+b+c)/3,(2+2*a+c)/4,(2+2*a+b)/4,(3+a)/4)
        best=min(best,v)
    return best
ALL={'split':split,'asym1':asym1,'asym2':asym2,'four':four,'sym':sym,'s0':s0}

EPS=1e-9
# ---- gap lemmas: G(lo,hi) means traces <=EPS+ hi imply <=EPS+ lo ----
def g0(x,y,z,lo,hi):
    best=9
    for a,b,c in perms(x,y,z):
        S=a+b+c; p=max(0,1-a-b-hi); q=max(0,1-a-c-hi)
        best=min(best,max(S+p+q,(1+3*a+p+q)/3,b+c+2*lo))
    return best
def g1(x,y,z,lo,hi,t):
    # gapsurvive: conditions depend on t through Q=(S-t)+ ; return True/False
    for a,b,c in perms(x,y,z):
        S=a+b+c; Q=max(0,S-t)
        if a+b<=EPS+t and 1-a-b<=EPS+hi and 1-a-c+Q<=EPS+hi and 2*a+2*Q+1-b-c<=EPS+2*t and b+c+2*lo<=EPS+t and 2+a-b+lo+Q<=EPS+3*t:
            return True
    return False
def g2(x,y,z,lo,hi,t):
    for a,b,c in perms(x,y,z):
        S=a+b+c; g=max(0,1-b-hi)
        if g<=EPS+min(a,c) and b+2*g<=EPS+t and a+lo<=EPS+t and c+lo<=EPS+t and 1+2*b<=EPS+2*t and 3<=EPS+4*t and 3+S<=EPS+5*t:
            return True
    return False
def nc(x,y,z,m,t):
    """nearcore with dichotomy <=EPS+m or >1/2"""
    for a,b,c in perms(x,y,z):
        S=a+b+c; D=max(0,S-t)
        base = b+c<=EPS+t and m+c<=EPS+t and 1+b-c<=EPS+t and 2+a-2*c<=EPS+2*t and 2+a+m-c<=EPS+3*t and a+m<=EPS+t
        if not base: continue
        if S<=EPS+t and 1-a+b<=EPS+t and 2-2*a+c<=EPS+2*t: return True
        if 1-a+b+D<=EPS+t and 2-2*a+c+D<=EPS+2*t and 2-c+D<=EPS+2*t and 3-a-b+D<=EPS+3*t: return True
    return False
