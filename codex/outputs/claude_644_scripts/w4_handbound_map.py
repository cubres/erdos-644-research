import sys, collections
import w4_handbound_chain as C
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3]); names=sys.argv[4].split(',')
def which(x,y,z,g1,g2):
    ok=[]
    for n in names:
        v,_=C.bestg(x,y,z,g1,g2,beta,[n],False)
        if v<=beta+1e-12: ok.append(n)
    return ok
lo=2-beta-2*h
print('STEP1 lo',lo)
uniq=collections.Counter(); 
for i in range(N+1):
    m=lo+(h-lo)*i/N
    w=min(m,1-(beta+m)/2)
    row=collections.Counter()
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            ok=which(m,y,z,m,h)
            if len(ok)==1: row[ok[0]]+=1
            if not ok: row['NONE']+=1
    print(round(m,3),dict(row))
print('STEP2')
for i in range(N+1):
    q=h+(0.5-h)*i/N
    w=min(lo,1-(beta+q)/2)
    row=collections.Counter()
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            ok=which(q,y,z,lo,h)
            if len(ok)==1: row[ok[0]]+=1
            if not ok: row['NONE']+=1
    print(round(q,3),dict(row))
