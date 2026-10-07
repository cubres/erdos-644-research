"""Exact alternatives to the forbidden A-flip response; no solver needed."""
from fractions import Fraction as F
import itertools,json
from pathlib import Path
from p644_agent_global_interval_survivor import all_six_and_seven,profile

def main():
 t=['0000','0001','0110','0111','1001','1111','1010','1011','1100','1101']
 w=list(map(F,['1/4','1/4','1/4','1/4','6/25','6/25','1/4','1/100','1/4','1/100']))
 allowed=[1,2,3,6,8]
 assert sum(w[i] for i in range(10) if i not in allowed)==F(3,4)
 out=[]
 for missing in [1,3,6,8]:
  aa=[(tuple(map(int,s))+(0 if i in allowed and i!=missing else 1,),v) for i,(s,v) in enumerate(zip(t,w))]
  for p in range(5):
   assert all(sum(v for s,v in aa if s[p]==b)==1 for b in [0,1])
  checks=all_six_and_seven(aa)
  assert F(checks['minimum_unpaired_P6'])>F(3,4)
  qq=[]
  for ps in itertools.combinations_with_replacement(range(5),3):
   q,p=profile(aa,ps);assert q>=F(6,25)
   qq.append({'pairs':[j+1 for j in ps],'Q':str(q),'P':str(p)})
  out.append({'omitted_atom':missing,'omitted_type':t[missing],
      'atoms':[{'bits':list(s),'mass':str(v)} for s,v in aa],
      'paired_profiles':qq,'checks':checks})
 data={'status':'Exact finite alternatives, not large-transversal families',
       'deletion_mass':'3/4','allowed_atom_types':[t[i] for i in allowed],
       'alternatives':out}
 path=Path('outputs/agent_global_regular_response_alternatives.json')
 path.write_text(json.dumps(data,indent=2)+'\n')
 for a in out:print(a['omitted_type'],a['checks'])
 print(path)

if __name__=='__main__':main()
