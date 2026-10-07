"""Exact binomial evaluation of the new parity-core cover counts.

This does not verify property (7,2); that property is the published FKW
input.  The calculation evaluates the closed formulas in the accompanying
block-exchange averaging report.
"""
from math import comb


def signed_coefficient(a, b, degree):
    """Coefficient of x**degree in (1-x)**a * (1+x)**b."""
    return sum(
        (-1)**i * comb(a, i) * comb(b, degree-i)
        for i in range(max(0, degree-b), min(a, degree)+1)
    )


def parity_sum(a, b, degree, parity):
    return sum(
        comb(a, i) * comb(b, degree-i)
        for i in range(max(0, degree-b), min(a, degree)+1)
        if i % 2 == parity
    )


def main():
    m = 10
    q = 3*m
    omitted_b = parity_sum(4*m, 3*m, q, 0)
    omitted_a = parity_sum(4*m-1, 3*m+1, q, 1)
    assert omitted_b == (
        comb(7*m, q) + signed_coefficient(4*m, 3*m, q)
    )//2
    assert omitted_a == (
        comb(7*m, q) - signed_coefficient(4*m-1, 3*m+1, q)
    )//2
    assert omitted_a - omitted_b == 3235857120
    print('m =', m, 'rank =', 4*m, 'global tau =', 3*m+1)
    print('q =', q, 'd = 1, p = 1')
    print('old core cover count =', omitted_b)
    print('new core cover count =', omitted_a)
    print('signed change =', omitted_a-omitted_b)


if __name__ == '__main__':
    main()
