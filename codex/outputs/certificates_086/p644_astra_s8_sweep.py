"""Reproduce the bounded S8 parameter audit, saving rational survivors."""
from pathlib import Path
import json
import time
from p644_explore8 import script8
from p644_strategy_lp import solve


def main():
    results=[]
    for a in (5,6,7):
        start=time.monotonic();count=0;wins=[];unknown=[]
        for b0 in range(14-a):
            for b1 in range(2,17-b0):
                script=script8(a,2,2,b0,b1,'A')
                if script is None:continue
                count+=1;answer=solve(script,time_limit=20,want=True)
                results.append({'triple':[a,2,2],'beta0':b0,'beta1':b1,'result':answer})
                if answer['status']=='PROVER WINS':wins.append((b0,b1))
                if answer['status']=='UNKNOWN':unknown.append((b0,b1))
        print(a,'tested',count,'wins',wins,'unknown',unknown,'seconds',round(time.monotonic()-start,1),flush=True)
        Path('logs/astra_s8_sweep.json').write_text(json.dumps(results,indent=1))


if __name__=='__main__':main()
