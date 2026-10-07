"""Standalone standard-library exact replay of the static obstruction."""
from fractions import Fraction as F
from pathlib import Path
import json
from p644_static_obstruction import enumeration,labels,valid_dual


def main():
    data=json.loads((Path(__file__).parent/'logs/astra_static_obstruction.json').read_text())
    families,blocks,reps,raw=enumeration()
    assert len(families)==166
    assert raw==data['raw_templates']
    assert [tuple(c['triple']) for c in data['cases']]==reps
    weights=list(map(F,data['weights']));target=F(data['target'])
    assert weights==list(map(F,[5,1,1,4,4,8])) and target==F(35,4)
    duals=[list(map(F,d)) for d in data['duals']]
    assert all(len(d)==10 for d in duals)
    for case in data['cases']:
        assert valid_dual(labels(families,blocks,case['triple']),duals[case['dual']],weights,target)
    print('PASS:',raw,'label templates;',len(reps),'orbits;',len(duals),'exact duals; static budget >= 7r/8')


if __name__=='__main__':main()
