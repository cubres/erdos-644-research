"""Exact supplementary arithmetic checks of the PARAMETRIC hand proof.

This is not a theorem certificate: the report supplies the parameter proof.
Run with Python 3; no dependencies.
"""
from fractions import Fraction as F
from collections import Counter


def close(r, m, y, z, beta):
    t = beta * r
    e = r - t
    s = m + y + z
    a = t - F(r, 2)
    def static_s1(case):
        assert y+z >= m+e
        assert m+y-z <= 3*t-2*r
        assert s <= 5*t-3*r
        if 3*z >= e+m+y:
            xx, yy, zz = (e+y+z-m)/2,(e+m+z-y)/2,(e+m+y-z)/2
        else:
            xx, yy, zz = e+y-z,e+m-z,F(z)
        assert 0 <= xx <= m and 0 <= yy <= y and 0 <= zz <= z
        assert xx+yy+zz <= t
        assert yy+zz >= e+m and xx+zz >= e+y and xx+yy >= e+z
        ceil = lambda q: -(-q.numerator // q.denominator)
        xx, yy, zz = map(ceil,(xx,yy,zz))
        T=ceil(t)+3
        assert xx <= m and yy <= y and zz <= z
        assert xx+yy+zz <= T
        assert yy+zz >= r+m-T and xx+zz >= r+y-T and xx+yy >= r+z-T
        return case
    if m <= (3*t-2*r)/2:
        assert F(3*r+m,4) <= t and F(2*r+2*m,3) <= t
        return 'a'
    if y <= a:
        if y-z > m-e:
            x, yy, zz = m, y, z
            case = 'b2'
        elif s < 3*e:
            x, yy, zz = z, y, m
            case = 'b3'
        else:
            if y+z+2*m > 3*t-r:
                return static_s1('b4')
            x, yy, zz = z, y, m
            assert max(x+yy, F(r,2)+x, F(r,2)+yy,
                       r+x-yy-zz, r-x+yy-zz, r-F(s,3),
                       F(3*r+s,5), F(r+x+yy+2*zz,3),
                       F(2*r+3*zz,4)) <= t
            return 'b1'
        assert max(s, F(r,2)+yy, F(r+2*x-yy+zz,2),
                   F(r+2*x+yy+3*zz,3)) <= t
        return case
    u, d = m+y, m-y
    if z <= 3*t-r-2*u:
        assert max(s,r-m+z,r-y+z,r-m+F(y,2),r-y+F(m,2),
                   F(r+2*m+2*y+z,3)) <= t
        return 'c1'
    if z < e-d:
        x, yy, zz = y,m,z
        case='c2'
    elif z <= (2*t-r-y)/2:
        x, yy, zz = m,y,z
        case='c3'
    else:
        assert z >= max(e+d,u-(3*t-2*r))
        if 3*z >= e+u:
            xx, yy, zz = (e+y+z-m)/2,(e+m+z-y)/2,(e+m+y-z)/2
            case='c4A'
        else:
            xx, yy, zz = e+y-z,e+m-z,F(z)
            case='c4B'
        assert 0 <= xx <= m and 0 <= yy <= y and 0 <= zz <= z
        assert xx+yy+zz <= t
        assert yy+zz >= e+m and xx+zz >= e+y and xx+yy >= e+z
        ceil = lambda q: -(-q.numerator // q.denominator)
        xx, yy, zz = map(ceil,(xx,yy,zz))
        T=ceil(t)+3
        assert xx <= m and yy <= y and zz <= z
        assert xx+yy+zz <= T
        assert yy+zz >= r+m-T and xx+zz >= r+y-T and xx+yy >= r+z-T
        return case
    p=max(0,r+yy-x-zz-t)
    q=max(0,r+x-yy-zz-t)
    assert x <= t and yy <= t
    assert r-x+zz+p+q <= t and yy+zz+q <= t
    assert r+yy+2*zz+p+2*q <= 2*t
    return case


if __name__ == '__main__':
    for beta, scales in [(F(19,22),(44,110,220)),
                         (F(32,37),(74,148,296)),
                         (F(7,8),(64,128))]:
        counts=Counter()
        for r in scales:
            for m in range(int((4*beta-2)*r/3)+1):
                for y in range(m+1):
                    if m+2*y > (2-beta)*r:
                        continue
                    for z in range(y+1):
                        counts[close(r,m,y,z,beta)]+=1
        print('PASS',beta,dict(sorted(counts.items())), 'total',sum(counts.values()))
