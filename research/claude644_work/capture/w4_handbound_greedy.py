import sys
import w4_handbound_chain as C
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3]); names=sys.argv[4].split(',')
order=sys.argv[5].split(',') if len(sys.argv)>5 else names
def ok(ns):
    lo,b1=C.step1(beta,h,N,ns,False)
    if b1: return False
    return not C.step2(beta,h,lo,N,ns,False)
cur=list(names)
assert ok(cur)
for n in order:
    t=[m for m in cur if m!=n]
    if ok(t): cur=t; print('drop',n)
    else: print('keep',n)
print(cur)
