import time, sys
from p644_restricted import has_72, tau_restricted
t0=time.time()
print("independent check: FKW parity family m=3: |S|=22, |X|=12, r=12, odd intersection", flush=True)
print("tau =", tau_restricted(22,12,12,{1,3,5,7,9,11}), flush=True)
ok, wit = has_72(22,12,12,{1,3,5,7,9,11})
print("has (7,2):", ok, "| edges:", len(wit) if ok else "bad 7-tuple:", None if ok else wit, f"[{time.time()-t0:.0f}s]", flush=True)
