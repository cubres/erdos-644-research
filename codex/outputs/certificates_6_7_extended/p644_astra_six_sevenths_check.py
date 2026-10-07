"""Independent standard-library entry point for the complete6/7 certificate."""
from pathlib import Path
from p644_astra_one_trace_check import check


if __name__=='__main__':
    result=check(Path(__file__).parent/'logs/astra_interval_finished_6_7.json')
    assert result=={'budget':'6/7','steps':256,'conditional_steps':215,'nodes':18270,'exclusions':[['143/1000','1/2']],'closed':True}
    print('PASS: c7<=6/7; f(k,7)<=ceil(6k/7)+10 for k>=1000, with the hand proof in Theorem7.48')
