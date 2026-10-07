import sys
from w4_handbound_chain import *
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3]); names=sys.argv[4].split(','); st=sys.argv[5]=='1'
lo,bad=step1(beta,h,N,names,st)
print('step1',len(bad)); [print(b) for b in bad[:15]]
bad2=step2(beta,h,lo,N,names,st)
print('step2',len(bad2)); [print(b) for b in bad2[:15]]
