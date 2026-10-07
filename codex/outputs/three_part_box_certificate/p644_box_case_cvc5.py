"""Independent exact solver and CPC proof production per saved support case."""
import sys,json,time,multiprocessing,subprocess,hashlib
from pathlib import Path
WORK=Path('/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work')
sys.path.insert(0,str(WORK/'research_dependencies'))
import cvc5

ROOT=Path('logs/astra_box_case_pipeline')
SIG=WORK/'proof_checkers/cvc5-1.4.0-signatures/cpc'
ETHOS=WORK/'proof_checkers/ethos-0.2.4/ethos'


def worker(task):
    key,seconds=task;start=time.time()
    history=[];record=ROOT/(key+'_cvc5.json')
    if record.exists():
        old=json.loads(record.read_text())
        history=old.get('previous_attempts',[])+[{k:old[k] for k in ('answer','elapsed','reason') if k in old}]
    s=cvc5.Solver();s.setLogic('QF_LRA')
    for opt,value in [('produce-proofs','true'),('check-proofs','true'),('proof-check','eager'),
                      ('proof-granularity','dsl-rewrite-strict'),('tlimit-per',str(int(seconds*1000)))]:s.setOption(opt,value)
    parser=cvc5.InputParser(s)
    source=(ROOT/key).with_suffix('.core.smt2')
    if not source.exists():source=(ROOT/key).with_suffix('.smt2')
    parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6,str(source))
    while True:
        cmd=parser.nextCommand()
        if cmd.isNull():break
        if cmd.getCommandName()=='check-sat':continue
        cmd.invoke(s,parser.getSymbolManager())
    ans=s.checkSat();out={'case':key,'answer':str(ans),'elapsed':time.time()-start,'solver':cvc5.__version__}
    out['source']=str(source)
    if history:out['previous_attempts']=history
    if ans.isUnsat():
        proofs=s.getProof();assert len(proofs)==1
        text=s.proofToString(proofs[0])
        if isinstance(text,bytes):text=text.decode()
        text=text.strip()
        (ROOT/key).with_suffix('.cpc_raw').write_text(text)
        if text.startswith('(\n') and text.endswith(')'):text=text[1:-1]
        wrapped='(include "%s")\n(include "%s")\n'%(SIG/'Cpc.eo',SIG/'expert/CpcExpert.eo')+text
        dest=(ROOT/key).with_suffix('.cpc');dest.write_text(wrapped)
        out['proof_bytes']=len(wrapped);out['proof_sha256']=hashlib.sha256(wrapped.encode()).hexdigest()
        try:
            result=subprocess.run([str(ETHOS),str(dest)],text=True,capture_output=True,timeout=120)
            out['ethos_exit_code']=result.returncode;out['ethos_stdout']=result.stdout;out['ethos_stderr']=result.stderr
        except Exception as e:out['ethos_error']=repr(e)
    elif ans.isUnknown():out['reason']=str(ans.getUnknownExplanation())
    (ROOT/(key+'_cvc5.json')).write_text(json.dumps(out,indent=2))
    return out


def main(seconds=60,workers=2,selected=None):
    keys=selected or ['000','001','003','011','012','013_line','033','111','112','113','123','133','333']
    tasks=[]
    for k in keys:
        dest=ROOT/(k+'_cvc5.json')
        if dest.exists():
            old=json.loads(dest.read_text())
            if old.get('ethos_exit_code')==0 and old.get('ethos_stdout','').strip()=='correct':continue
        tasks.append((k,seconds))
    with multiprocessing.get_context('spawn').Pool(workers,maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(worker,tasks):
            print(r['case'],r['answer'],'seconds',round(r['elapsed'],2),'external checker',r.get('ethos_exit_code'),flush=True)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--workers',type=int,default=2)
    ap.add_argument('--cases',nargs='*');a=ap.parse_args();main(a.seconds,a.workers,a.cases)
