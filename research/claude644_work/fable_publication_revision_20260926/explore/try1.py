import time
from adaptive import evaluate
t = 6/7
def show(x,y,z,d,label):
    t0=time.time(); v,h = evaluate(x,y,z,d,t,nrand=40,climb=25)
    print(label,(x,y,z),'d=',[round(a,3) for a in d],'worst=%.4f'%v,'h=',[round(a,3) for a in h],'%.0fs'%(time.time()-t0),flush=True)
x,y,z=0.5,0.25,0.15
show(x,y,z,[x,y,t-x-y,0,0,0],'avoid X,Y,partZ')
show(x,y,z,[x,t-x-z,z,0,0,0],'avoid X,Z,partY')
show(x,y,z,[t-y-z,y,z,0,0,0],'avoid Y,Z,partX')
