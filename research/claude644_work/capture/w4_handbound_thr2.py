import sys
import w4_handbound_chain as C
names=sys.argv[1].split(','); N=int(sys.argv[2]); beta=float(sys.argv[3]); h=float(sys.argv[4])
lo,b1=C.step1(beta,h,N,names,False)
print('step1',len(b1),b1[:8])
b2=C.step2(beta,h,lo,N,names,False)
print('step2',len(b2),b2[:8])
