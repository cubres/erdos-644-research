# Hand coverage of the first and third rational gap stages

26 September 2026. Full scalar proofs for Stages 1 and 3 of the frozen three-gap certificate. Stage 2 is being handled independently. These statements use beta=6/7 and normalized rank one. All closing tools below have integer constructions at budget ceil(6k/7)+4; none requires the static-template +9 allowance.

## Stage 1: the gap [3/7,10/21]

Suppose a good triple has pair sizes

    3/7<=x<=10/21,       0<=z<=y<=5/14.

Put s=y+z, d=y-z and S=x+s. We use the hand lemmas L31, L32 and S1a, with the statements recorded in `paper_push_six_sevenths_compression.md`.

**Case A: d>x-1/7.** Apply L32(x,y,z). Since s+d=2y<=5/7,

    S=x+s<=x+5/7-d<6/7,
    1/2+y<=6/7,
    (1+2x-d)/2 < (8/7+x)/2 <=17/21<6/7,
    (1+2x+2s-d)/3
       <=(1+2x+10/7-3d)/3
       <(20/7-x)/3<=17/21<6/7.

These are precisely its four budget inequalities.

**Case B: d<=x-1/7 and s<=11/7-2x.** Apply L31 in orientation (y,z,x). Its nine expressions are bounded as follows:

    s<=5/7,
    1/2+y, 1/2+z <=6/7,
    1+d-x<=6/7,
    1-d-x<=4/7,
    1-S/3<=6/7                 (because S>=x>=3/7),
    (3+S)/5<=88/105<6/7        (because S<=25/21),
    (1+s+2x)/3<=6/7,
    (2+3x)/4<=6/7              (because x<=10/21).

**Case C: s>11/7-2x.** This is the only remaining case. Since x<=10/21,

    s>11/7-2x>=x+1/7.

Also d<=5/7-s, and therefore

    x+y-z=x+d<3x-6/7<=4/7=3beta-2.

Finally S<=25/21<9/7=5beta-3. These are exactly the three S1a conditions. Its split construction has fewer than three points of integer rounding loss.

The three cases cover the entire box. Thus an initial pair intersection q in [3/7,10/21], with cap u=5/14 and v(q)=11/14-q, always closes. The cap at the left endpoint is v(3/7)=5/14; the cap-host conditions hold throughout the interval. The resulting initial request costs at most beta*k+2.

## Stage 3: extending the upper gap to 1/2

Assume the gap [4/21,5/14] is already established. Consider a good triple with

    10/21<=x<=1/2,       0<=z<=y<=4/21.

Put s=y+z, d=y-z and S=x+s. Set ell=4/21 and h=5/14.

**Case A: S<=5/7.** Lemma 7.29 applies with dominant pair x. Its bounds are

    (1+S)/2<=6/7,
    1-x+d<=1-10/21+4/21=5/7,
    1-x-d<=1-x+d<=5/7,
    1/3+x<=5/6<6/7.

**Case B: 5/7<=S<=6/7 and z<=1/14.** Apply Lemma 7.33 in orientation (x,z,y). Its first bound S<=beta is given; its remaining bounds satisfy

    1/3+x<=5/6,
    1-x+y<=5/7,
    2x+y+3z<=1+4/21+3/14=59/42<11/7.

The last inequality is equivalent to its final budget expression (1+2x+y+3z)/3<=beta.

**Case C: 5/7<=S<=6/7 and z>=1/14.** Apply Lemma 7.35 with dominant x and gap [ell,h]. Its nine inequalities follow from

    S<=6/7,
    1-h+y, 1-h+z <=9/14+4/21=5/6,
    2-2h-x<=9/7-10/21=17/21,
    1/3+x<=5/6,
    2x-y, 2x-z <=1-1/14=13/14,
    x-y-z=2x-S<=1-5/7=2/7,
    2ell+y+z<=16/21.

Indeed, the sixth and seventh displayed lemma forms are at most
(23/14+13/14)/3=6/7, and its eighth is at most
(16/7+2/7)/3=6/7. The integer rounding allowance of this lemma is at most four.

**Case D: S>=6/7.** Apply Lemma 7.37 with dominant x and gap [ell,h]. Its domain condition is precisely this case. Its remaining bounds are

    x+y<=1/2+4/21=29/42,
    1-h+y, 1-h+z<=5/6,
    1/4+x+(y+z)/4<=3/4+2/21=71/84<6/7,
    2ell+y+z<=16/21,
    1/2+x/2+(z+ell)/4<=3/4+2/21=71/84<6/7.

Its integer rounding allowance is again at most four. This exhausts Stage 3.

For an initial pair q in [10/21,1/2], use u=1/3 and v(q)=17/21-q. Both traces are at most 1/3. The previously established gap [4/21,5/14] forces both below 4/21, giving exactly the covered box. The initial request costs at most beta*k+2.

## Additive constant bookkeeping

These two stages fit an integer budget T=ceil(6k/7)+4. The initial cap request and subsequent closing requests are separate and their rounding errors are not added. L31, L32, L29 and L33 use integer constructions at any integer budget satisfying their real inequalities; S1a costs fewer than three extra points, and L35/L37 use at most four. The conditional finisher already proved in the companion report also uses +4. If Stage 2 is fully converted to hand tools with allowance at most four, the same argument yields the stronger finite bound

    f(k,7)<=ceil(6k/7)+4,   k>=28,

since then ceil(6k/7)+4<=k. This final strengthened bound is contingent here on completion of the separate Stage 2 hand proof; the frozen, independently replayed general theorem remains +10 until then.
