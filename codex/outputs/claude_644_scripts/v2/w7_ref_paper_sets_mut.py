# mutation harness for w7_ref_paper_sets.py: accept parameters whose hypotheses hold only at T+1
import w7_ref_paper_sets as S
for nm in ['hyp_L26','hyp_L32','hyp_L31']:
    orig = getattr(S, nm)
    setattr(S, nm, (lambda o: (lambda r,x,y,z,T: o(r,x,y,z,T+1) and T>=x+y and T>=0))(orig))
for f,name in [(S.t_L26,'L26'),(S.t_L32,'L32'),(S.t_L31,'L31')]:
    before=len(S.FAIL); n=sum(f(r) for r in range(1,8)); print(name,'mutated instances',n,'failures',len(S.FAIL)-before)
