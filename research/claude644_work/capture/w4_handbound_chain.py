import sys, itertools
from w4_handbound_explore import perms, L18,L29,L33,L20,L23,L25,L31,L32,GT
from w4_handbound_static import triple
def L26g(x,y,z,g1,g2):
    out=9
    for a,b,c in perms(x,y,z):
        S=a+b+c
        base=[S,1-a+c,1-b+c,1-a+b/2,1-b+a/2]
        v=max(base+[(1+2*(a+b)+c)/3])
        if g2>=0.5: v=min(v,max(base+[g1+max(a,b)]))
        out=min(out,v)
    return out
def L35g(x,y,z,g1,g2):
    out=9; h=g2; l=g1
    for a,b,c in perms(x,y,z):
        S=a+b+c
        out=min(out,max(S,(1-h)+b,(1-h)+c,2-2*h-a,1/3+a,((2-h)+2*a-b)/3,((2-h)+2*a-c)/3,((3-2*h)+a-b-c)/3,2*l+b+c))
    return out
def L37g(x,y,z,g1,g2,beta):
    out=9; h=g2; l=g1
    for a,b,c in perms(x,y,z):
        S=a+b+c
        if S<beta: continue
        v=max(a+b,(1-h)+b,(1-h)+c,.25+a+(b+c)/4,2*l+b+c,.5+a/2+(c+l)/4)
        # also need (1-beta)+z<=h and (1-beta)+y<=h used in proof
        if (1-beta)+c>h or (1-beta)+b>h: continue
        out=min(out,v)
    return out
def L15g(x,y,z,g1,g2):
    out=9; m=g1
    for a,b,c in perms(x,y,z):
        if 1-a-b>g2 or 1-a-c>g2: continue
        q=max(b+c,b+m,c+m,(1+b+c+2*m)/4)
        out=min(out,a+q)
    return out
UNC={'L18':L18,'L29':L29,'L33':L33,'L20':L20,'L23':L23,'L25':L25,'L31':L31,'L32':L32,'GT':GT}
def bestg(x,y,z,g1,g2,beta,names,use_static=True):
    v=9;arg=None
    for n in names:
        if n in UNC: b=UNC[n](x,y,z)
        elif n=='L26': b=L26g(x,y,z,g1,g2)
        elif n=='L35': b=L35g(x,y,z,g1,g2)
        elif n=='L37': b=L37g(x,y,z,g1,g2,beta)
        elif n=='L15': b=L15g(x,y,z,g1,g2)
        if b<v: v,arg=b,n
    if v>beta and use_static:
        s,_=triple(x,y,z)
        if s<v: v,arg=s,'static'
    return v,arg
ALL='L18,L29,L33,L26,L20,L23,L25,L31,L32,GT,L35,L15,L37'.split(',')
def step1(beta,h,N,names=ALL,use_static=True):
    lo=2-beta-2*h
    bad=[]
    for i in range(N+1):
        m=lo+(h-lo)*i/N
        w=min(m,1-(beta+m)/2)
        for j in range(N+1):
            for k in range(j+1):
                y=w*j/N; z=w*k/N
                v,a=bestg(m,y,z,m,h,beta,names,use_static)
                if v>beta: bad.append((round(m,4),round(y,4),round(z,4),round(v,4),a))
    return lo,bad
def step2(beta,h,l,N,names=ALL,use_static=True):
    bad=[]
    for i in range(N+1):
        q=h+(0.5-h)*i/N
        w=min(l,1-(beta+q)/2)
        for j in range(N+1):
            for k in range(j+1):
                y=w*j/N; z=w*k/N
                v,a=bestg(q,y,z,l,h,beta,names,use_static)
                if v>beta: bad.append((round(q,4),round(y,4),round(z,4),round(v,4),a))
    return bad
if __name__=="__main__":
    beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3])
    lo,bad=step1(beta,h,N)
    print('step1 lo',lo,'bad',len(bad)); [print(b) for b in bad[:20]]
    bad2=step2(beta,h,lo,N)
    print('step2 bad',len(bad2)); [print(b) for b in bad2[:20]]

# ---- fixed static patterns (cells X=AB,Y=AC,Z=BC; requests 0..3)
from w4_handbound_pat import pat_budget
PATS={
 'P4':{'X':[(0,2),(0,1,3)],'Y':[(1,2),(0,1,3)],'Z':[(2,3),(0,1,3)],'PA':[(3,)],'PB':[(1,)],'PC':[(0,)]},
 'P0':{'X':[(0,1),(0,3)],'Y':[(1,2,3)],'Z':[(1,3)],'PA':[(1,)],'PB':[(1,),(2,)],'PC':[(0,),(1,3)]},
 'P5':{'X':[(0,1),(0,2,3)],'Y':[(1,2)],'Z':[(1,3)],'PA':[(3,)],'PB':[(2,)],'PC':[(0,),(1,2),(1,3)]},
}
def patval(name,x,y,z):
    return min(pat_budget(PATS[name],a,b,c) for a,b,c in perms(x,y,z))
_old_bestg=bestg
def bestg(x,y,z,g1,g2,beta,names,use_static=True):
    v,arg=_old_bestg(x,y,z,g1,g2,beta,[n for n in names if n not in PATS],False)
    for n in names:
        if n in PATS and v>beta:
            b=patval(n,x,y,z)
            if b<v: v,arg=b,n
    if v>beta and use_static:
        from w4_handbound_static import triple
        s,_=triple(x,y,z)
        if s<v: v,arg=s,'static'
    return v,arg
