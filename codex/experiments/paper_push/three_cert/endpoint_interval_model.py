"""Rational data for the four-box closure of the entire endpoint interval."""
from fractions import Fraction as F
V4=(3,60,77,86,92,106,108,113,116,120)
NEW223=(11,19,46,54,60,78,86,92,101,102,106,114,120)
ASSIGNMENTS=((0,3,1,1,1,1,2),(1,3,0,0,0,0,0),(2,2,3,3,0,0,0),(0,0,3,3,2,2,2))
PARENTS=(V4,V4,NEW223,NEW223)
END=F(1,100)
def family(t):
 x=(F(3,4)+t,F(3,4),F(3,4))
 T=((F(1,2)+F(849,1000)*t,0,F(1,2)-F(849,1000)*t),
    (0,F(1,2)+F(99,1000)*t,F(1,2)-F(99,1000)*t),
    (0,F(1,2)-F(49,1000)*t,F(1,2)+F(49,1000)*t))
 return x,T
def boxes(t):
 x,_=family(t)
 return ((x[0],F(1,2)-F(347,1000)*t,F(1047,1000)*t),
         (F(1,2)-F(245,1000)*t,F(3,4),F(1797,1000)*t),
         (F(5,8)+F(651,1000)*t,F(1,2)+F(49,2000)*t,F(12,5)*t),
         (F(1,2)+F(151,500)*t,F(5,8)+F(49,1000)*t,F(12,5)*t))
def retained(t):
 x,_=family(t);return (x[0],x[1],F(1047,1000)*t)
def bound(t):return F(3,4)-F(1047,1000)*t
