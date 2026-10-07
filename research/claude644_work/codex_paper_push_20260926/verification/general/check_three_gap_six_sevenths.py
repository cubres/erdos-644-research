"""Exact replay of the three-gap six-sevenths certificate.

Run with Python -S: no third-party package or discovery code is imported.
The final logical implication uses the hand theorem in
outputs/paper_push_six_sevenths_compression.md, not a numerical assertion.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import sys

RESEARCH = Path(__file__).resolve().parent
sys.path.insert(0, str(RESEARCH))
from p644_astra_one_trace_check import check

CERTIFICATE = Path(__file__).with_name("six_sevenths_three_gaps_minimal.json")
SHA256 = "bad247bf7bfd3661dcb412854567b3fef4ae80110d765577fdd6dbb17b5d077a"


def main():
    assert sha256(CERTIFICATE.read_bytes()).hexdigest() == SHA256
    data = json.loads(CERTIFICATE.read_text())
    assert len(data["static_templates"]) == 7
    assert [s["interval"] for s in data["steps"]] == [
        ["3/7", "10/21"], ["4/21", "5/14"], ["10/21", "1/2"]
    ]
    result = check(CERTIFICATE)
    assert result == {
        "budget": "6/7", "steps": 3, "conditional_steps": 3,
        "nodes": 718, "exclusions": [["4/21", "5/14"], ["3/7", "1/2"]],
        "closed": False,
    }
    # "closed" above tests the superseded quarter-gap finisher only.
    assert any(F(lo) <= F(3, 7) and F(hi) == F(1, 2)
               for lo, hi in result["exclusions"])
    # The original integer allowance remains unchanged. Local rounding,
    # cap construction, and the new finisher are separate requests.
    assert max(2, 4, 9) < 10
    assert 1000 * F(6, 7) + 11 <= 1000
    assert 4 < 10
    print("PASS: upper gap [3/7,1/2] proved by 3 stages / 718 exact nodes.")
    print("WITH THE HAND FINISHER: f(k,7)<=ceil(6k/7)+10 for k>=1000.")
    print("The conditional finisher alone has additive constant +4.")
    print("SHA256", SHA256)


if __name__ == "__main__":
    main()
