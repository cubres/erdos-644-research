"""Small discovery test: thin a two-part core and retain two fixed anchors."""
import argparse,json,time
from p644_patterns import Pattern,check_72

def run(q,epsilon,time_limit):
    forbidden=[(1-2*q/3,q/2),(1-4*q/7,4*q/7),(1-q/2,2*q/3)]
    intervals=[];left=1-q
    for lo,hi in sorted(forbidden):
        if lo>hi:continue
        lo-=epsilon;hi+=epsilon
        if left<lo:intervals.append((left,lo))
        left=max(left,hi)
    if left<q:intervals.append((left,q))
    boxes=[([lo,1-hi,0,0],[hi,1-lo,0,0])for lo,hi in intervals]
    for v in [[q,0,1-q,0],[0,q,0,1-q]]:boxes.append((v,v))
    pat=Pattern([q,q,1-q,1-q],1,boxes=boxes,name='thinned core plus two anchors')
    start=time.time();status,info=check_72(pat,time_limit=time_limit,want_solution=True,intersecting=False)
    traces=[]
    if status=='FAILS':
        for j in range(7):traces.append([sum(m[i]for cell,m in info['cells']if j in cell)for i in range(4)])
    return {'q':q,'epsilon':epsilon,'core_intervals':intervals,
            'status':status,'elapsed_seconds':time.time()-start,'row_traces_rounded':traces,'info':info}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--q',type=float,default=.9)
    p.add_argument('--epsilon',type=float,default=.001);p.add_argument('--time-limit',type=float,default=60)
    a=p.parse_args();print(json.dumps(run(a.q,a.epsilon,a.time_limit),indent=2))
