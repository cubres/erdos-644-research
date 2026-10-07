"""Exact affine vertex check of the full fan-in parameter cone.

Uses the independently established fourteen-form NEW223 capacity formula.
All inequalities tested are affine in (t,g,h,j); checking the five vertices
therefore proves their validity throughout the closed parameter polytope.
The separate four-box covering argument yields tau* <= 3/4-g+j.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from check_new223_facets import FORMS

ZERO = F(0)
END = F(1, 50)
VERTICES = ((ZERO, ZERO, ZERO, ZERO),
            (END, 2*END/3, ZERO, ZERO),
            (END, END, ZERO, ZERO),
            (END, 2*END/3, END/3, ZERO),
            (END, 2*END/3, ZERO, END/3))


def data(t, g, h, j):
    x = (F(3, 4)+t, F(3, 4), F(3, 4))
    a = (F(1, 2)+g, ZERO, F(1, 2)-g)
    b = (ZERO, F(1, 2)+h, F(1, 2)-h)
    c = (ZERO, F(1, 2)-j, F(1, 2)+j)
    r = g-j
    boxes = ((x[0], F(1, 2)-4*h, r),
             (F(1, 2)+4*t-5*g, x[1], r),
             (F(5, 8)+3*t/2-g, F(1, 2)+j/2, r),
             (F(1, 2)+2*t-2*g, F(5, 8)+j, r))
    return x, a, b, c, boxes


def v4_forms(a, b, c, d):
    return (a, b, c, (a+b+c)/2, d+(b+c)/2, d+(a+b+c)/4)


def new_forms(a, b, c):
    return tuple(v[0]*a+v[1]*b+v[2]*c for v in FORMS)


def main():
    capacity_checks = 0
    records = []
    for t, g, h, j in VERTICES:
        assert 0 <= t <= END and g >= 2*t/3 and min(h, j) >= 0 and g+h+j <= t
        x, a, b, c, boxes = data(t, g, h, j)
        r = g-j
        assert r >= t/3
        for anchor in (a, b, c):
            assert sum(anchor) == 1
            assert all(0 <= anchor[i] <= x[i] for i in range(3))
        margins = []
        for k, u in enumerate(boxes):
            assert all(0 <= u[i] <= x[i] for i in range(3))
            for i in range(3):
                forms = (v4_forms(c[i], a[i], u[i], b[i]) if k == 0 else
                         v4_forms(a[i], b[i], u[i], a[i]) if k == 1 else
                         new_forms(c[i], u[i], a[i]) if k == 2 else
                         new_forms(a[i], u[i], c[i]))
                assert all(v <= x[i] for v in forms), (t, g, h, j, k, i, forms)
                capacity_checks += len(forms)
                margins.append(x[i]-max(forms))
        R, S, P, Q = boxes
        assert R[0] == x[0] and S[1] == x[1]
        assert all(u[2] == r for u in boxes)
        assert P[0]+R[1] >= 1
        assert S[0]+Q[1] >= 1
        assert P[1]+Q[0] >= 1
        assert sum(x)-sum((x[0], x[1], r)) == F(3, 4)-g+j
        records.append(dict(parameters=(t, g, h, j), boxes=boxes,
                            minimum_part_margins=margins))
    out = dict(status='PASS_EXACT_FIVE_VERTEX_CONE_CHECK',
               parameter_domain='0<=t<=1/50, g>=2t/3, h,j>=0, g+h+j<=t',
               bound='tau*<=3/4-g+j<=3/4-t/3',
               vertices=records, capacity_inequalities=capacity_checks,
               capacity_dependency='check_new223_facets.py: complete fourteen-form proof; V4 hand capacity lemma')
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, default=str, indent=2))
    print('PASS five parameter vertices;', capacity_checks,
          'exact capacity inequalities; four-box cover; tau*<=3/4-g+j<=3/4-t/3')


if __name__ == '__main__':
    main()
