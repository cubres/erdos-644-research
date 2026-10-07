"""Small independent checker for LRAT proofs containing RUP additions only.

Positive clause hints are replayed in their stated order by exact unit
propagation. RAT hints are rejected. Deleting clauses only weakens the formula.
An accepted empty clause is required. No SAT solver or external package is used.
"""
from pathlib import Path
import argparse
import gzip
import time


def lines(path):
    path=Path(path)
    return gzip.open(path,'rt') if path.suffix=='.gz' else path.open()


def check(cnf_path,proof_path):
    started=time.time();database={};header=None;clause=[];counter=0
    with lines(cnf_path) as source:
        for line in source:
            if not line.strip() or line.startswith('c'):continue
            if line.startswith('p'):
                assert header is None;header=line.split();assert header[:2]==['p','cnf'];continue
            assert header is not None
            for value in map(int,line.split()):
                if value:
                    assert abs(value)<=int(header[2]);clause.append(value)
                else:
                    counter+=1;database[counter]=tuple(dict.fromkeys(clause));clause=[]
    assert not clause and counter==int(header[3]);last_id=counter;additions=0;units=0;empty=False
    with lines(proof_path) as source:
        for number,line in enumerate(source,1):
            tokens=line.split()
            if not tokens or tokens[0]=='c':continue
            identifier=int(tokens[0])
            if tokens[1]=='d':
                assert tokens[-1]=='0'
                for old in map(int,tokens[2:-1]):database.pop(old,None)
                continue
            values=list(map(int,tokens[1:]));end=values.index(0)
            candidate=tuple(dict.fromkeys(values[:end]));hints=values[end+1:]
            assert hints and hints[-1]==0 and all(v>0 for v in hints[:-1]),('non-RUP hint',number)
            assert identifier>last_id;last_id=identifier
            assignment={};conflict=False
            for literal in candidate:
                variable=abs(literal);value=literal<0
                if variable in assignment and assignment[variable]!=value:conflict=True
                assignment[variable]=value
            for hint in hints[:-1]:
                if conflict:break
                assert hint in database,('missing clause',number,hint)
                unassigned=0;unit=None;satisfied=False
                for literal in database[hint]:
                    variable=abs(literal)
                    if variable not in assignment:
                        unassigned+=1;unit=literal
                        if unassigned>1:break
                    elif assignment[variable]==(literal>0):satisfied=True;break
                assert not satisfied and unassigned<=1,('invalid unit hint',number,hint)
                if not unassigned:conflict=True
                else:assignment[abs(unit)]=unit>0;units+=1
            assert conflict,('addition not proved',number,identifier)
            database[identifier]=candidate;additions+=1
            if not candidate:empty=True;break
            if additions%10000==0:print('CHECKED',additions,'additions;',units,'unit steps;',round(time.time()-started,2),'seconds',flush=True)
    assert empty
    print('PASS: RUP-only LRAT proof;',additions,'derived clauses;',units,'unit steps; empty clause verified;',round(time.time()-started,2),'seconds.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('cnf');parser.add_argument('proof');args=parser.parse_args()
    check(args.cnf,args.proof)
