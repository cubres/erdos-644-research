import time
from adaptive import evaluate2
t=6/7
for d,lab in [([0.453,0.25,0.15,0.001,0.001,0.002],'nearcore-like'),([0.457,0.25,0.15,0,0,0],'nc-pure')]:
    t0=time.time()
    print(lab,'nogap',evaluate2(0.5,0.25,0.15,d,t),flush=True)
    print(lab,'gap',evaluate2(0.5,0.25,0.15,d,t,lo=3/7,hi=10/21),'%.0fs'%(time.time()-t0),flush=True)
