"""EXACT certificate (Motzkin/Farkas, rational) for the key step of Theorem IRR (one light part L, generic
helpers): see docstring of the earlier version; every overlap case must be infeasible."""
from fractions import Fraction as F
from farkas_strict import certify
VARS = ['xA','xB','xL','alA','alB','alL','beA','beB','beL','aA','aB','aL','bA','bB','bL']
total = 0; bad = []
for helpA, helpB in [(1,1),(1,0),(0,1),(0,0)]:
    for order in (0, 1):
        for pab in 'ABL':
            for pa in ('ABL' if helpA else 'X'):
                for pb in ('ABL' if helpB else 'X'):
                    R = []
                    def le(d, r=0, st=False): R.append((d, F(r), st))
                    types = ['al','be'] + (['a'] if helpA else []) + (['b'] if helpB else [])
                    for T in types:
                        for P in 'ABL':
                            le({T+P: 1, 'x'+P: -1}); le({T+P: -1})
                        le({T+'A': 1, T+'B': 1, T+'L': 1}, 1)
                    le({'xA': 2, 'alA': -3}, 0, True); le({'xB': 2, 'beB': -3}, 0, True)
                    le({'alB': 7, 'xB': -4}); le({'alL': 7, 'xL': -4}); le({'beA': 7, 'xA': -4}); le({'beL': 7, 'xL': -4})
                    if helpA: le({'alA': 1, 'aA': -1}); le({'aB': 7, 'xB': -4}); le({'aL': 7, 'xL': -4})
                    if helpB: le({'beB': 1, 'bB': -1}); le({'bA': 7, 'xA': -4}); le({'bL': 7, 'xL': -4})
                    le({'xA': -1, 'alA': 1, 'xB': -1, 'beB': 1}, F(-3, 4), True)
                    big, small = ('alL', 'beL') if order == 0 else ('beL', 'alL')
                    le({small: 1, big: -1})
                    d = {big: -1}
                    if helpA: d.update({'xA': -1, 'aA': 1})
                    if helpB: d.update({'xB': -1, 'bB': 1})
                    le(d, F(-3, 4), True)
                    if helpA: le({'aL': 1, 'xL': -1, big: 1})
                    if helpB: le({'bL': 1, 'xL': -1, big: 1})
                    for (u, w), P in [(('al','be'), pab), (('a','be'), pa), (('al','b'), pb)]:
                        if P == 'X': continue
                        le({u+P: -1, w+P: -1, 'x'+P: 1}, 0, True)
                    total += 1
                    ok, msg = certify(R, VARS)
                    if ok is not True: bad.append(((helpA, helpB, order, pab, pa, pb), ok, msg))
print("cases", total, "not certified:", bad if bad else "NONE -- all cases exactly infeasible")
