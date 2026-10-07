"""Resumable driver.  usage: python3 drive2.py MODE k t p Nlo Nhi LOG [j]   MODE = tc (cegar_tc, (7,2)) or rj (cegar_rj, R_j-free)
Shapes: all compositions n1<=...<=np of N.  Skips shapes already in LOG."""
import sys, subprocess, itertools, time, os, re
mode=sys.argv[1]; k,t,p,Nlo,Nhi=map(int,sys.argv[2:7]); log=sys.argv[7]; j=sys.argv[8] if len(sys.argv)>8 else '7'
done=set()
if os.path.exists(log):
    for line in open(log):
        m=re.match(r"N=\d+ n=(\([\d, ]+\)):",line)
        if m: done.add(m.group(1))
f=open(log,'a')
for N in range(Nlo,Nhi+1):
    for n in itertools.combinations_with_replacement(range(1,N+1),p):
        if sum(n)!=N or str(n) in done: continue
        t0=time.time()
        cmd=['python3','cegar_tc.py',str(k),str(t),','.join(map(str,n)),'1','20000'] if mode=='tc' else \
            ['python3','cegar_rj.py',str(k),str(t),','.join(map(str,n)),j,'1','20000']
        out=subprocess.run(cmd,capture_output=True,text=True).stdout.strip().splitlines()
        print(f"N={N} n={n}: {out[-1] if out else 'NO OUTPUT'} [{time.time()-t0:.0f}s]",file=f,flush=True)
print("ALL DONE",file=f,flush=True)
