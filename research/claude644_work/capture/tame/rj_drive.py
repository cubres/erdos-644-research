import sys, subprocess, itertools, time
k=int(sys.argv[1]); t=int(sys.argv[2]); p=int(sys.argv[3]); Nlo=int(sys.argv[4]); Nhi=int(sys.argv[5]); j=sys.argv[6]; kmin=sys.argv[7] if len(sys.argv)>7 else '1'
for N in range(Nlo,Nhi+1):
    for n in itertools.combinations_with_replacement(range(1,N+1),p):
        if sum(n)!=N: continue
        t0=time.time()
        out=subprocess.run(['python3','cegar_rj.py',str(k),str(t),','.join(map(str,n)),j,kmin,'20000'],capture_output=True,text=True).stdout.strip().splitlines()
        print(f"N={N} n={n}: {out[-1] if out else 'NO OUTPUT'} [{time.time()-t0:.0f}s]",flush=True)
