# Removing the extra point from the general six-sevenths bound

26 September 2026. Complete hand proof, independently checked internally by the parent and other agents. No numerical sweep is a proof dependency. External peer review and formal verification are not claimed. Existing manuscript and notes are unchanged.

## The result

**Theorem.** For every integer k>=8, every k-uniform family with property (7,2) satisfies

    tau(H)<=ceil(6k/7).

The same bound holds for nonempty families of rank at most k, by private padding. Combined with the classical f(k,6)=k, the bound is also valid for2<=k<=6. This proof does not settle k=7, nor the conjectured asymptotic coefficient3/4.

The proof uses the exact integral local constructions L29,L31,L32,L33,S0,S1 and the exact gap constructions G0,G1,G2 given below. Its new feature is the choice of integer gap endpoints from the actual budget. Fixed rational endpoints are unnecessary.

## 1. Exact gap-closing lemmas

For a good triple E,F,G, let x=|E intersect F|, y=|E intersect G|, z=|F intersect G|, S=x+y+z. Suppose L,H,T are integers with0<=L<=H<k and0<=T<=k, and every intersection of size at most H has size at most L. All requests have budget T.

These are exact forms of the existing hand constructions L35,L37,L46, with integer trace cutoffs instead of a rounded real cutoff. Their avoidance requests and candidate-pair arguments are unchanged.

**G0.** Put p=(k-x-y-H)_+, t=(k-x-z-H)_+. The triple closes if

    S+p+t<=T,
    k+3x+p+t<=3T,
    y+z+2L<=T.                                      (G0)

Indeed request an edge avoiding all pair cells plus p,t private points in E,F, then pad with private G-points to budget T. Its E,F traces are at most H, hence at most L. Its G-trace b satisfies b<=k-T+x+p+t. Consequently x+ceil(b/2)<=T by the second inequality. Two requests contain X and the two parts of that trace; a third contains Y,Z and the small E,F traces. They cover all three complementary products of candidate piercing pairs.

**G1.** Put Q=(S-T)_+. The triple closes if

    x+y<=T,
    k-x-y<=H,  k-x-z+Q<=H,
    2x+2Q+k-y-z<=2T,
    y+z+2L<=T,
    2k+x-y+L+Q<=3T.                                 (G1)

Request an edge avoiding X,Y and min(z,T-x-y) points of Z. Its sole possible triple cell has size q<=Q; write its remaining F,G,E traces as a,b,c. The two cutoff inequalities give c<=L and a+q<=L. Split its G-private trace B into two parts, with bases X union Q union B_i. The fourth displayed inequality makes each base fit T, including integer division. The third base is Y union Z union A union C. Distribute the remaining points of E among the three requests. Their total required load is at most2k+x-y+L+Q<=3T. This is precisely the earlier L37 construction and eliminates the same four candidate-pair products. Unlike the earlier statement, no separate condition S>=beta*k is needed.

**G2.** Put g=(k-y-H)_+. The triple closes if

    g<=min(x,z),  y+2g<=T,
    x+L<=T, z+L<=T, k+2y<=2T,
    3k<=4T, 3k+S<=5T.                              (G2)

Request an edge avoiding Y and g points from each of X,Z, and complete the request inside F to budget T, using remaining X,Z points first. Its E,G traces are at most H, hence at most L. The remaining three request bases are X union(G intersect H4), Z union(E intersect H4), Y union(F intersect H4). The first two fit by x+L,z+L; the third fits by k+2y<=2T. The two possible triple cells lie in all three requests. As in L46, the total base load plus the remaining E,G private points is at most3k-T+(S-T)_+, which is at most3T by the last two inequalities. Integral allocation completes the construction.

The hypotheses also ensure the hosts used in these constructions. In G0, p,t never exceed their private cells, and padding fits because T<=k and the initial request contains all pair cells. In G1, T-x-y>=0. In G2, the displayed g condition gives the hosts, and the remaining F allocation fits since T-y<=k. Thus these lemmas add no rounding allowance.

## 2. Integer endpoints and elementary identities

Put

    h=floor(k/7), s=k-7h, T=k-h=6h+s,
    A=floor(T/2),
    B=floor((4T-2k)/3),
    C=T-ceil(k/2),
    D=2k-T-2B,
    L=D-1,
    U=2T-k-ceil(k/2).

Here h>=1 and0<=s<=6. Set r=floor((h+2s)/3). Then

    A=3h+floor(s/2),       B=3h+r,
    C=floor((5h+s)/2),     D=2h+s-2r,
    L=2h+s-2r-1,          U=floor((3h+s)/2)=C-h.     (I)

In particular

    6k/7<=T<=k,   B>=A,   B>=3h,
    L<=U,         4L<=T.                              (II)

To prove L<=U, it is enough that2r+1>=ceil((h+s)/2). Since r>=floor((h+s)/3), this follows from

    2floor(n/3)+1>=ceil(n/2)  for every integer n>=0.

For n=3a+b,0<=b<=2, we have n<=3a+2<=4a+2, and therefore ceil(n/2)<=2a+1=2floor(n/3)+1. To prove4L<=T, write h+2s=3r+t,0<=t<=2. Then

    4L-T=2t-2r-s-4<=0.

We will also use

    k-B-1+L<=T.                                     (III)

Indeed the difference between the two sides is h-B-1+L=s-3r-2<=-h-s<=0, because3r>=h+2s-2.

A cap request from a pair of intersection q retains u,v private points and avoids their common intersection together with the other private points. Its size is2k-q-u-v. Thus a size-T request with both retained caps at most K exists whenever

    0<=2k-T-q<=2K,  K<=k-q.

The avoiding response makes a good triple whose two new pair intersections are at most K. The retained caps may be different integers; no separate flooring is used.

## 3. First integer gap

We exclude every integer intersection

    A+1<=q<=min(B,floor(k/2)).                        (GAP1)

For such a q, use both retained caps at most C. Their hosts fit because C<=floor(k/2)<=k-q. Their required total is nonnegative, and

    2k-T-2C=3h+(k mod2)<=A+1<=q,

so the cap request is legal at size T.

Its good triple has pair sizes x=q and0<=z<=y<=C. In particular x>y. Put d=y-z and v=y+z. We give three cases.

**Case1: d>x-h.** Use L32(x,y,z). Since v+d=2y<=2T-k,

    S=x+v<T,
    k/2+y<=T,
    (k+2x-d)/2<(k+x+h)/2<=T,
    (k+2x+2v-d)/3<(2k+T-x)/3<=T.

For the third inequality use x<=B<=(4T-2k)/3<=3T-2k; for the fourth use x>=A+1>=3h+1>2h. The comparison of the two upper bounds for x uses T>=4k/5, which follows from T>=6k/7.

**Case2: d<=x-h and v<=3T-k-2x.** Use L31(y,z,x). Its nine expressions fit T:

    v<=2T-k<=T,
    k/2+y,k/2+z<=T,
    k+d-x<=k-h=T,   k-d-x<=k-x<=T,
    k-S/3<=T,
    (3k+S)/5<=T,
    (k+v+2x)/3<=T,
    (2k+3x)/4<=T.

Here S>=x>=3h makes the sixth expression fit. Also S<=x+2T-k, and x<=3T-2k, make the seventh fit. The last two use the case assumption and x<=B.

**Case3: v>3T-k-2x.** Apply exact S1 with sorted largest pair x. Its four required inequalities are

    k+x-v<T,
    (k+x)/2<=T,
    (2k+x+d)/3<T,
    (3k+S)/5<=T.

For the first, k+x-v<2k+3x-3T<=T. The second uses x<=B<=2T-k. For the third, d<=2T-k-v, giving2k+x+d<2k-T+3x<=3T. The fourth is the estimate already used in Case2.

Thus every triple closes, proving(GAP1).

If B>=floor(k/2), this already excludes every intersection greater than A and at most k/2. Skip to the finisher. Henceforth assume

    B<floor(k/2).                                    (IV)

## 4. Second integer gap

We exclude every integer intersection

    D<=q<=C.                                        (GAP2)

This is a nonempty valid interval: (IV) gives D>k-T=h>=1, while L<=U=C-h gives D<=C. Use both retained caps at most B. Their hosts fit since q<=C<=floor(k/2) and B<floor(k/2); their total fits because q>=D. By(GAP1), every new trace at most B is at most A.

We therefore obtain a good triple with

    D<=x<=C,   0<=z<=y<=A.

If x+z>=k-B, use G2 in orientation(a,b,c)=(y,x,z), with cutoff H=B and resulting trace bound A. The g-point cuts fit their hosts because x+y>=x+z>=k-B. Their cost is

    max(x,2k-x-2B)<=T,

by x>=D. The other G2 bounds are

    y+A,z+A<=2A<=T,
    k+2x<=k+2C<=2T,
    3k<=4T,
    3k+S<=3k+C+2A<=5k/2+2T<=5T.

If x+z<k-B, apply S0 with distinguished pair a=y and other pairs b=x,c=z. We have a<=A, b<=C, and

    c<=k-B-x-1<=k-B-D-1=T+B-k-1<=C,
    b+c<=k-B-1<=3T-2k,

where the last bound uses B>=3h. The seven exact Hall inequalities for S0 follow:

    k+2b,k+2c<=2T,
    k+3a<=k+3T/2<=3T,
    2k+b+c<=3T,
    2k+2a+b,2k+2a+c<=3k/2+2T<=4T,
    3k+a<=3k+T/2<=4T.

Its base capacities are nonnegative: a+b,a+c<=A+C<=T and b+c<=k-B-1<=T. The integral Hall allocation therefore closes this case too. This proves(GAP2).

## 5. Third integer gap

We exclude the remaining intersections

    B+1<=q<=floor(k/2).                              (GAP3)

Use both retained caps at most C. The same cap-host calculation as in Stage1 is valid, because q>=B+1>=3h+1. By(GAP2), its new traces are at most L=D-1. Thus the triple has

    B+1<=x<=floor(k/2),   0<=z<=y<=L.

Use the gap implication trace<=C =>trace<=L. Define

    J=2k-C+2floor(k/2)-3T=floor((h-s)/2).

Four cases suffice.

**Case1: S<=2T-k.** Use L29. Its three bounds follow from

    (k+S)/2<=T,
    k-x+|y-z|<=k-B-1+L<=T,
    k/3+x<=5k/6<=T.

**Case2: 2T-k<=S<=T and z<J.** Use L33(x,z,y). Its first three bounds are S<=T, k/3+x<=T, and k-x+y<=T by(III). For the last bound, z<J<=h/2, y<=L<=2h+s, and2x<=k give

    k+2x+3z+y<=2k+3h/2+2h+s
                       =35h/2+3s<=18h+3s=3T.

If J<=0, this case is empty.

**Case3: 2T-k<=S<=T and z>=J.** Apply G0 with H=C and resulting trace bound L. Expanding its first maximum gives

    S+p+t=max(S,k-C+y,k-C+z,2k-2C-x)<=T.

Indeed L<=U=C-h handles the middle two, while

    2k-2C-T=3h+(k mod2)<=B+1<=x

handles the last. Expanding its split numerator gives

    k+3x+p+t
       =max(k+3x,2k-C+2x-y,2k-C+2x-z,
                    3k-2C+x-y-z)<=3T.

The first term is at most5k/2<=3T. The next two fit since y>=z>=J and2x<=2floor(k/2). Finally

    3k-2C+x-y-z=3k-2C+2x-S
       <=4k-2C+2floor(k/2)-2T
        =6k-4T<=3T.

The equality uses C=T-ceil(k/2), so the parity errors cancel. Its third request fits since y+z+2L<=4L<=T.

**Case4: S>=T.** Apply G1 with H=C and resulting bound L; now Q=S-T. Its conditions follow directly from L<=U=C-h and4L<=T:

    x+y<=floor(k/2)+L<=floor(k/2)+C<=T,
    k-x-y<=k-T+z<=h+L<=C,
    k-x-z+Q=h+y<=C,
    2x+2Q+k-y-z
       =4x+y+z+k-2T
       <=4floor(k/2)+2U+k-2T
        =2T-3(k mod2)<=2T,
    y+z+2L<=4L<=T,
    2k+x-y+L+Q
       =2k+2x+z+L-T
       <=2k+2floor(k/2)+2U-T
        =3T-2(k mod2)<=3T.

All cases close, proving(GAP3). Together with(GAP1), this excludes every intersection in(A,k/2].

## 6. The finishing theorem at the actual budget

The earlier exact conditional finishing theorem extends as follows.

**Finishing lemma.** Let k>=8, T=ceil(6k/7), and suppose every intersection is at most T/2 or greater than k/2. Then tau<=T.

The small-maximum part is unchanged from Section3 of `submission_644_integer_refinement.md`: its four exact requirements

    6T>5k+1, 3T>=2k+ceil(k/2),
    2T>=3k/2+1/2, 12T>=10k+4

hold for every k>=8. It handles the largest small intersection M<=2k/7.

If M>2k/7, a balanced request on a pair attaining M gives a good triple whose other traces are at most k-floor((T+M)/2)<3k/7+1/2<=k/2, hence at most M. It remains to close any sorted triple M>=y>=z with M<=T/2 under the full maximum-small gap. Put h=k-T and c=T-k/2. The former four-case proof generalizes with the thresholds c,h.

**(i) y<=c.** If y-z>M-h, L32(M,y,z) fits: S<2y+h<=T, k/2+y<=T, its third form is below(k+M+h)/2<=k-T/4<=T, and its fourth is at most5k/6<=T. If y-z<=M-h but S<3h, L32(z,y,M) fits, with the last two forms bounded by(k+3h)/2<=T and(k+9h)/3<=T. Otherwise use L31(z,y,M). Here M>=h, both difference conditions fit, S>=3h, and

    S<=M+2y<=5T/2-k,
    (3k+S)/5<=2k/5+T/2<=T,
    (k+y+z+2M)/3<=T,
    (2k+3M)/4<=k/2+3T/8<=T.

The other five L31 forms fit directly. All auxiliary comparisons use only T>=6k/7.

**(ii) y>c and h<z<=c.** Use G2(M,z,y) with H=floor(k/2), L=M. The domain sums exceed c+h=k/2 and hence are at least ceil(k/2). Its initial request has size max(z,k-z+(k mod2))<=T because the integer z is at least h+1. Its other forms fit by2M<=T, M+y<=2M, k+2z<=2T, and

    3k+S<=3k+2M+c<=5k/2+2T<=5T.

**(iii) y>c and z>c.** Exact S1 fits, since its four forms are at most

    2k-3T/2<=T,
    k/2+T/4<=T,
    5k/6<=T,
    (3k+3T/2)/5<=T.

**(iv) y>c and z<=h.** Use the near-core or omitted-core construction in orientation(M,z,y). Its common inequalities follow from

    y+z<=T/2+h=k-T/2<=T,
    M+y<=2M<=T,
    k+z-y<k+h-c=5k/2-2T<=T,
    2k+M-2y<3k-3T/2<=2T,
    2k+2M-y<5k/2<=3T,
    2M<=T.

If S<=T, the extra omitted-core bounds follow from k-M+z<=k-y+z<T and2k-2M+y<=2k-M<2k-c=5k/2-T<=2T. If S>T, the four remaining near-core bounds reduce to

    k+y+2z<=3k-3T/2<=2T,
    2k-M+2y+z<=2k+y+z<=3k-T/2<=3T,
    2k+M+z<=3k-T/2<=3T,
    3k+y<=3k+T/2<=4T.

This proves the finishing lemma.

Finally(A,k/2] is empty of intersections and A=floor(T/2), so every intersection is at most T/2 or greater than k/2. The lemma contradicts tau>T and proves the theorem. QED.

## 7. Scope and independent checks

The argument is a hand proof based on integral subsets and integral allocations. No computational enumeration of ranks, residues, point configurations, or parameter grids is used to establish a universal assertion. A short exact arithmetic replay may be retained separately as a transcription check. The previously proved42n and42n-1 special cases are subsumed. The asymptotic bound remains6/7; the3/4 conjecture remains open.

Arithmetic transcription check: `python3 -B -S work/submission_644_checks/check_rounding_push.py` passed endpoint identities for ranks8..10000 and all476049 prescribed-branch triple inequalities for ranks8..84. The script uses exact integers and tests the chosen proof branch; it performs no template search. These finite checks are supplementary diagnostics only.
