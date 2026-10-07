import sys
from explore import *
from game import enum_requests
names=['A','B','C']; cells={0b011:4,0b101:1,0b110:1,0b001:2,0b010:2,0b100:5}
print('state', show(names,cells))
# all size-6 requests, count open classes (maxdrop=1)
res=[]
for d in enum_requests(3,cells):
    req={''.join(names[i] for i in range(3) if m>>i&1):k for m,k in d.items()}
    out=responses(names,cells,req,'D',maxdrop=0,quiet=True)
    nopen=sum(1 for h,n2,c2,v in out if not v)
    res.append((nopen,len(out),req))
res.sort(key=lambda t:(t[0],t[1]))
for nopen,ncl,req in res[:40]:
    print(nopen,'open of',ncl,'classes  req',req)
