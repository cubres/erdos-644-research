"""Decide (7,2) for a type-closed family (parts n, types T) in parallel over all 715 supports.
usage: python3 decide_tc.py k n1,n2,... 'j-list or profile list' timelimit tag"""
import sys, json, time
from multiprocessing import Pool
from tc_gen import gen_ilp
from tc_lib import SUPPORTS, order_supports
k=int(sys.argv[1]); n=[int(x) for x in sys.argv[2].split(',')]
T=json.loads(sys.argv[3]); TL=float(sys.argv[4]); tag=sys.argv[5]
if isinstance(T[0],int): T=[(j,k-j) for j in T]
T=[tuple(t) for t in T]
def work(idx):
    t0=time.time(); r=gen_ilp(n,T,SUPPORTS[idx],time_limit=TL); return idx,r,time.time()-t0
if __name__=='__main__':
    order=order_supports(); res={}
    with Pool(8) as pool:
        for idx,r,dt in pool.imap_unordered(work, order):
            res[idx]=r
            if r is not False: print(f"support {idx}: {r} ({dt:.0f}s)",flush=True)
            if r is True: print("BAD TUPLE FOUND -> not (7,2)",flush=True); pool.terminate(); break
    und=[i for i,r in res.items() if r is None]
    print(f"done {tag}: checked {len(res)} supports; undecided {und}; feasible {[i for i,r in res.items() if r]}",flush=True)
