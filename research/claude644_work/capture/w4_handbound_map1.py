import sys, collections
import w4_handbound_chain as C
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3]); names=sys.argv[4].split(',')
lo=2-beta-2*h
for i in range(N+1):
    m=lo+(h-lo)*i/N
    w=min(m,1-(beta+m)/2)
    row=collections.Counter()
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            ok=[n for n in names if C.bestg(m,y,z,m,h,beta,[n],False)[0]<=beta+1e-12]
            if len(ok)==1: row[ok[0]]+=1
            elif not ok: row['NONE']+=1
            else: row['multi']+=1
    print(round(m,3),round(w,3),dict(row))
