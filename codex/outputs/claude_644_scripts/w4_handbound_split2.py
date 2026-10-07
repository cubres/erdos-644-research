import sys, itertools, collections
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3])
def L32o(a,b,c): S=a+b+c; return max(S,.5+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3)
def L31o(a,b,c): S=a+b+c; return max(a+b,.5+a,.5+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4)
def L18(a,b,c): M=max(a,b,c); return max((3+M)/4,(2+2*M)/3)
lo=2-beta-2*h
cnt=collections.Counter(); bad=[]
for i in range(N+1):
    m=lo+(h-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            # orientations: roles given as positions of cells (m=X_EG, y, z) 
            opts=[]
            if L18(m,y,z)<=beta: opts.append('L18')
            for name,f in (('L32',L32o),('L31',L31o)):
                for perm in itertools.permutations(range(3)):
                    v=(m,y,z); p=tuple(v[t] for t in perm)
                    if f(*p)<=beta+1e-12: opts.append((name,perm))
            if not opts: bad.append((round(m,3),round(y,3),round(z,3)))
            else: cnt[opts[0] if len(opts)==1 else 'multi']+=1
            if len(opts)==1: pass
print(len(bad),bad[:8]); print(cnt)
