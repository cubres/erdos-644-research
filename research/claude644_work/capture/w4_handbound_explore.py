import itertools, sys
# normalized r=1; each lemma returns sufficient budget B (closes if beta >= B), given good triple sizes
def perms(x,y,z):
    return set(itertools.permutations((x,y,z)))
def L18(x,y,z,m=None):
    M=max(x,y,z); 
    if M>0.5: return 9
    return max((3+M)/4,(2+2*M)/3)
def L29(x,y,z,m=None):
    S=x+y+z; return min(max((1+S)/2,1-a+abs(b-c),1/3+a) for a,b,c in perms(x,y,z))
def L33(x,y,z,m=None):
    S=x+y+z; return min(max(S,1/3+a,1-a+c,(1+2*a+3*b+c)/3) for a,b,c in perms(x,y,z))
def L26(x,y,z,m=None):
    out=9
    for a,b,c in perms(x,y,z):
        S=a+b+c
        base=[S,1-a+c,1-b+c,1-a+b/2,1-b+a/2]
        v=max(base+[(1+2*(a+b)+c)/3])
        if m is not None: v=min(v,max(base+[m+max(a,b)]))
        out=min(out,v)
    return out
def L20(x,y,z,m=None):
    out=9
    for a,b,c in perms(x,y,z):
        s=a+b; M=max(a,b)
        out=min(out,max(2*M+c,(1+2*s+3*c)/3,(2+2*s+2*M+3*c)/5))
    return out
def L23(x,y,z,m=None):
    out=9
    for a,b,c in perms(x,y,z):
        s=a+b
        out=min(out,max(s+c,(1+3*a+b+2*c)/3,(1+a+3*b+2*c)/3,(2+3*s+3*c)/5,(1+2*s+3*c)/3))
    return out
def L25(x,y,z,m=None):
    S=x+y+z
    lo=max((1+2*S)/3,S); hi=1.0
    f=lambda B: S+sum(max(0,1-2*B+2*w) for w in (x,y,z))<=B
    if not f(hi): return 9
    for _ in range(50):
        mid=(lo+hi)/2
        if f(mid): hi=mid
        else: lo=mid
    return hi
def L31(x,y,z,m=None):
    out=9
    for a,b,c in perms(x,y,z):
        S=a+b+c
        out=min(out,max(a+b,.5+a,.5+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4))
    return out
def L32(x,y,z,m=None):
    out=9
    for a,b,c in perms(x,y,z):
        S=a+b+c
        out=min(out,max(S,.5+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3))
    return out
def GT(x,y,z,m=None):
    return (3-x-y-z)/2
def L35(x,y,z,m):
    # gap: no intersection in (m,1/2]; l=m, h=1/2
    out=9; h=.5; l=m
    for a,b,c in perms(x,y,z):
        S=a+b+c
        out=min(out,max(S,(1-h)+b,(1-h)+c,2-2*h-a,1/3+a,((2-h)+2*a-b)/3,((2-h)+2*a-c)/3,((3-2*h)+a-b-c)/3,2*l+b+c))
    return out
def L37(x,y,z,m,beta):
    out=9; h=.5; l=m
    for a,b,c in perms(x,y,z):
        S=a+b+c
        if S<beta: continue
        out=min(out,max(a+b,(1-h)+b,(1-h)+c,.25+a+(b+c)/4,2*l+b+c,.5+a/2+(c+l)/4))
    return out
def L15(x,y,z,m):
    # x_ = cell whose two edges have private parts <=1/2 : need 1-a-b<=1/2 and 1-a-c<=1/2
    out=9
    for a,b,c in perms(x,y,z):
        if 1-a-b>0.5 or 1-a-c>0.5: continue
        # q=T-a >= b+c, b+m, c+m ; 1<=4q-b-c-2m
        q=max(b+c,b+m,c+m,(1+b+c+2*m)/4)
        out=min(out,a+q)
    return out
LEM={'L18':L18,'L29':L29,'L33':L33,'L26':L26,'L20':L20,'L23':L23,'L25':L25,'L31':L31,'L32':L32,'GT':GT,'L35':L35,'L15':L15}
def best(x,y,z,m,beta,names):
    v=9;arg=None
    for n in names:
        if n=='L37': b=L37(x,y,z,m,beta)
        elif n in ('L35','L15','L26'): b=LEM[n](x,y,z,m)
        else: b=LEM[n](x,y,z)
        if b<v: v,arg=b,n
    return v,arg
def scan(beta,names,N=60):
    worst=(0,None)
    lo=(3*beta-2)/2
    for i in range(N+1):
        m=lo+(0.5-lo)*i/N
        w=min(m,1-(beta+m)/2)
        for j in range(N+1):
            for k in range(j+1):
                y=w*j/N; z=w*k/N
                v,a=best(m,y,z,m,beta,names)
                if v>worst[0]: worst=(v,(m,y,z,a))
    return worst
if __name__=="__main__":
    beta=float(sys.argv[1]); names=sys.argv[2].split(',')
    print(scan(beta,names))
