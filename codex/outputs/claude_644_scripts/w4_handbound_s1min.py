import sys
import w4_handbound_chain as C
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3]); names=sys.argv[4].split(','); order=sys.argv[5].split(',')
st=len(sys.argv)>6 and sys.argv[6]=='1'
def ok(ns):
    lo,b=C.step1(beta,h,N,ns,st); return not b, b[:5]
cur=list(names); r,b=ok(cur); print('full',r,b)
for n in order:
    t=[m for m in cur if m!=n]
    r,b=ok(t)
    if r: cur=t; print('drop',n)
    else: print('keep',n,b[:2])
print(cur)
