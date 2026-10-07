"""Exact symbolic certificate for the weighted full two-response obstruction.
No optimization libraries. Every bound is proved for every integer M >= 20.
Run: python3 work/p644_agent_alternative_two_response_certificate.py
"""
from itertools import combinations
import json
from pathlib import Path

# name, old-row mask, G1 flag, coefficient of M, constant mass.
CELLS = [
 ('A+',19,1,3,0),('A-',19,0,9,0),('B+',44,1,12,0),
 ('C-',14,0,8,0),('D+',21,1,7,0),('D-',21,0,1,0),
 ('E-',41,0,8,0),('F+',50,1,5,0),('F-',50,0,3,0),
 ('u',7,0,0,1),('v',26,0,0,1),('w',38,0,0,1),
 ('p1',1,0,0,2),('p3',4,0,0,1),('p4',8,0,0,2),
 ('p5',16,0,0,2),('p6',32,0,0,2)]
PRINCIPAL=9
MIN_M=20
BUDGET=(21,12)

def graph(rows, first):
 return [set(j for j,(_,other,flag2,_,_) in enumerate(CELLS)
             if i!=j and ((mask|other)&rows)==rows and (not first or flag or flag2))
         for i,(_,mask,flag,_,_) in enumerate(CELLS)]

def weight(indices):
 indices=tuple(indices)
 return (sum(CELLS[i][3] for i in indices),sum(CELLS[i][4] for i in indices))

def positive_forever(line):
 slope,constant=line
 return slope>=0 and MIN_M*slope+constant>=1

def verify():
 # Every original row has rank 28M+3; original endpoint set is A union B.
 for i in range(6):
  assert weight(j for j,c in enumerate(CELLS) if c[1]>>i&1)==(28,3)
 old=graph(63,False)
 assert {i for i,nb in enumerate(old) if nb}=={0,1,2}
 assert all(old[i]==({2} if i<2 else {0,1}) for i in [0,1,2])
 # G1 has 27M old points and M+3 fresh points. Both cores are met.
 assert weight(i for i,c in enumerate(CELLS) if c[2])==(27,0)
 first_checks=[]
 for omitted in range(6):
  gr=graph(63^(1<<omitted),False)
  available={i for i,c in enumerate(CELLS) if c[2]}
  eligible={i for i,nb in enumerate(gr) if nb & available}
  eligible |= {i for i in available if gr[i]}
  slope,const=weight(eligible)
  assert positive_forever((slope-24,const))
  first_checks.append({'omitted':omitted+1,'endpoint_affine':[slope,const]})
 six=[('five_old_omit_'+str(i+1),graph(63^(1<<i),False)) for i in range(6)]
 six += [('four_old_'+''.join(str(i+1) for i in rows),graph(sum(1<<i for i in rows),True))
         for rows in combinations(range(6),4)]
 seven=[('six_old',graph(63,False))]
 seven += [('five_old_first_omit_'+str(i+1),graph(63^(1<<i),True)) for i in range(6)]
 # Each seven-row condition is maintained because G2 meets every available cell,
 # while the eligible principal cells cannot all be deleted at this budget.
 seven_checks=[]
 for name,gr in seven:
  slope,const=weight(i for i in range(PRINCIPAL) if gr[i])
  assert positive_forever((slope-21,const-12))
  seven_checks.append({'tuple':name,'eligible_principal_affine':[slope,const]})
 records=[];mask_count=0;worst_at_min=10**9
 for deleted in range(1<<PRINCIPAL):
  cost=sum(CELLS[i][3] for i in range(PRINCIPAL) if deleted>>i&1)
  # For M>=20, a support of whole deleted cells is affordable iff cost<=21.
  # Indeed (22-21)M > 12. Additional points deleted outside these cells can
  # only reduce the budget available for partial principal deletions.
  if cost>21:continue
  mask_count+=1
  available={i for i in range(PRINCIPAL) if not(deleted>>i&1)}
  for name,gr in six:
   full={i for i,nb in enumerate(gr) if nb & available}
   own={i for i in available if gr[i] and not(gr[i]&available)}
   core=own & {0,1,2}
   cloud=own-core
   base_slope,base_const=weight(full)
   core_slope,_=weight(core)
   # The endpoint lower bound is the maximum of these two affine forms,
   # after subtracting the old 24M endpoints. The first spends all remaining
   # deletion budget on the relevant core; the second leaves >=1 point in
   # each nonempty core cell, as required by the fixed support.
   lines=[(base_slope+core_slope+cost-45,base_const+len(cloud)-12),
          (base_slope-24,base_const+len(core)+len(cloud))]
   assert any(positive_forever(line) for line in lines),(deleted,name,lines)
   worst_at_min=min(worst_at_min,max(MIN_M*a+b for a,b in lines))
   records.append({'deleted_mask':deleted,'tuple':name,'margin_lower_bound_max_of':lines})
 assert 24*MIN_M+6 <= 28*MIN_M+3 # G2 fits rank; inequality strengthens with M.
 result={'status':'PASS','integer_parameter':'M >= 20','rank':'28M+3',
         'deletion_budget':'21M+12','original_endpoint_count':'24M',
         'old_pair_count':'144M^2','whole_deleted_supports':mask_count,
         'symbolic_six_checks':len(records),'minimum_margin_at_M20':worst_at_min,
         'first_response_checks':first_checks,'seven_checks':seven_checks,
         'endpoint_certificates':records}
 path=Path(__file__).resolve().parents[1]/'outputs'/'agent_weighted_full_two_response_certificate.json'
 path.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({key:value for key,value in result.items()
                   if key not in ['endpoint_certificates','first_response_checks','seven_checks']}))
 return result

if __name__=='__main__':verify()
