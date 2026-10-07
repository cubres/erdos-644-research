"""Second exact solver for the saved two-box SMT problem. Discovery only."""
import json,sys,time
from pathlib import Path
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import cvc5
import z3


def main(seconds=180):
    s=cvc5.Solver();s.setLogic('QF_LRA');s.setOption('produce-proofs','true')
    s.setOption('produce-models','true');s.setOption('tlimit-per',str(int(seconds*1000)))
    parser=cvc5.InputParser(s)
    # Z3's un-simplified printer may emit unary (+ x), which cvc5 rejects.
    clean=z3.Solver()
    for a in z3.parse_smt2_file('logs/astra_two_box_smt_0.smt2'):clean.add(z3.simplify(a))
    Path('logs/astra_two_box_portable.smt2').write_text(clean.to_smt2())
    parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6,'logs/astra_two_box_portable.smt2')
    while True:
        cmd=parser.nextCommand()
        if cmd.isNull():break
        if cmd.getCommandName()=='check-sat':continue
        cmd.invoke(s,parser.getSymbolManager())
    print('Second solver loaded exact problem.',flush=True)
    start=time.time();ans=s.checkSat()
    out={'answer':str(ans),'elapsed':time.time()-start,'solver':cvc5.__version__}
    if ans.isUnsat():
        proofs=s.getProof()
        for i,pr in enumerate(proofs):
            Path('logs/astra_two_box_cvc5_%s.proof'%i).write_text(s.proofToString(pr))
        out['proof_count']=len(proofs)
    elif ans.isUnknown():out['reason']=str(ans.getUnknownExplanation())
    else:
        out['model']=str(s.getModel([],parser.getSymbolManager().getDeclaredTerms()))
    Path('logs/astra_two_box_cvc5.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':main()
