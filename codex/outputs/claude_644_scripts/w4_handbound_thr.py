import sys
import w4_handbound_chain as C
names=sys.argv[1].split(','); N=int(sys.argv[2])
def ok(beta,h):
    lo,b1=C.step1(beta,h,N,names,False)
    if b1: return False,('s1',b1[:3])
    b2=C.step2(beta,h,lo,N,names,False)
    return (not b2),('s2',b2[:3])
for beta in [float(b) for b in sys.argv[3].split(',')]:
    for h in [0.44,0.45,0.46,0.47,0.48]:
        r,info=ok(beta,h)
        print(beta,h,r, '' if r else info)
