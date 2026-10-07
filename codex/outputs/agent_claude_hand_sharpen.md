# Sharpening Claude's hand proof to 19/22

26 September 2026. **Proved by hand, using the closing lemmas already proved in Claude's `paper_main.tex`.** Supplementary arithmetic checks are identified separately below. This improves Claude's hand coefficient 173/200 to 19/22. It does **not** improve the project's existing, stronger computer-assisted general coefficient 6/7.

## Result

For every integer k >= 1000, a rank-at-most-k family with property (7,2) satisfies

    tau(H) <= ceil(19k/22) + 10.

In particular, its asymptotic hand-proof coefficient is 19/22 = 0.86363636..., in place of 173/200 = 0.865.

The improvement comes from using Claude's static template S1 precisely where his L31 branch loses its eighth inequality. This raises the allowable maximal intersection from `(4 beta - 3)k` to `((4 beta - 2)/3)k`. At beta = 19/22 we may take

    h = 16/33,    ell = 1/6,    ell = 2 - beta - 2h.

The difficult second case in Claude's gap-extension lemma then vanishes: a triple with one pair cell at most k/2 and the other two below k/6 has total pair-cell size below 5k/6 < beta k.

Sources used: `/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/notes_handbound.md` and the closing, local, gap and finishing sections of `paper_main.tex`. The main note and Claude's paper were not edited.

## 1. Closing lemmas used

Write a good triple as E,F,G with no common point, and let its pair-cell sizes be x,y,z, S=x+y+z, with common edge size r. If tau(H)>T, every request consisting of at most T points is avoided by an edge. A collection of at most four requests covering all candidate piercing pairs closes the triple to a bad family of at most seven edges.

We use the following exact, integer-budget lemmas from the paper. Their displayed inequalities are positively homogeneous and monotone in T, so normalized real inequalities at r=1 transfer to integer r and any larger integer budget.

* **L18:** if x,y,z<=m<=r/2, it suffices that
  `tau(H)>ceil(max((3r+m)/4,(2r+2m)/3))`.
* **L26:** it suffices that T is at least
  `max(S, r-x+z, r-y+z, r-x+y/2, r-y+x/2, (r+2x+2y+z)/3)`.
* **L32:** with T<=r, it suffices that T is at least
  `max(S, r/2+y, (r+2x-y+z)/2, (r+2x+y+3z)/3)`.
* **L31:** with T<=r, it suffices that T is at least
  `max(x+y, r/2+x, r/2+y, r+x-y-z, r-x+y-z, r-S/3, (3r+S)/5, (r+x+y+2z)/3, (2r+3z)/4)`.
* **S2:** put P=(r+y-x-z-T)_+ and Q=(r+x-y-z-T)_+. It suffices that x,y<=T and

      r-x+z+P+Q <= T,
      y+z+Q <= T,
      r+y+2z+P+2Q <= 2T.

All relabellings of the three pair cells are allowed. These lemmas have explicit hand proofs in the source paper; no search or numerical coverage statement is being substituted for them here.

We also need the following convenient sufficient form of S1, proved here.

### Lemma S1a (symmetric static closure)

Normalize r=1. Suppose m>=y>=z>=0, e=1-beta>=0, and

    y+z >= m+e,       m+y-z <= 3 beta-2,
    S=m+y+z <= 5 beta-3.

Then the S1 splits exist at real budget beta. At integer scale, rounding the splits upward gives a closing budget at most beta r+3.

**Proof.** If 3z>=e+m+y, use

    m1=(e+y+z-m)/2,
    y1=(e+m+z-y)/2,
    z1=(e+m+y-z)/2.

Their three pair sums are e+m, e+y, e+z; their total is (3e+S)/2<=beta. Their nonnegativity follows from y+z>=m+e and m>=y>=z. Also y+z<=2m and y+z>=m+e imply m>=e. Hence `e+y+z-m<=e+m<=2m`, giving m1<=m. Next y1<=y follows from m+e<=y+z<=3y-z. Finally z1<=z is the case condition 3z>=e+m+y.

If 3z<e+m+y, use

    z1=z,      y1=e+m-z,      m1=e+y-z.

The first two relevant pair sums are e+m and e+y. The third is 2e+m+y-2z>=e+z by this case condition. The total is 2e+m+y-z<=beta. Nonnegativity is immediate; y1<=y is y+z>=m+e, and m1<=m follows from the same inequality and m>=y. Thus every split lies within its cell.

For completeness the four requests are

    R0 = M1 union Y1 union Z1,
    RM = M union P_G union Y2 union Z2,
    RY = Y union P_F union M2 union Z2,
    RZ = Z union P_E union M2 union Y2,

where each pair cell is split into its subscript-1 part and remainder. Their sizes are the split total and `1+m-y1-z1`, `1+y-m1-z1`, `1+z-m1-y1`, hence at most beta. They cover every candidate product: a pair cell and its opposite private part lie in the corresponding request; for two distinct pair cells, if either point lies in its subscript-2 part an appropriate one of the last three requests contains both, and otherwise R0 contains both. Thus four responses close the original triple.

At scale r round each split size upward. Because the actual cell sizes are integers, the rounded parts still fit. All lower bounds on pair sums survive, and the total increases by less than 3. This proves the integer assertion. QED.

## 2. Parametric local closing proposition

**Proposition.** Let

    19/22 <= beta <= 7/8,
    M = (4 beta-2)/3.

Let H be r-uniform with tau(H)>T, where T is an integer satisfying beta r+3<=T<=r. Any good triple with pair-cell sizes m>=y>=z satisfying

    m <= M r,             m+2y <= (2-beta)r

extends to a bad subfamily of at most seven edges.

**Proof.** Normalize by r and write

    e=1-beta,    a=beta-1/2,    s0=(3 beta-2)/2,
    S=m+y+z,    u=m+y,    d=m-y.

We verify the closing lemmas at normalized budget beta. Integer scaling and the rounding described above finish the proof.

### Case (a): m<=s0

L18 applies because `(2+2m)/3<=beta` and `(3+m)/4<=beta`; the second follows from beta>=4/5. Its separate integer budget is at most ceil(beta r).

### Case (b): m>s0 and y<=a

First suppose y-z>m-e. Apply L32 with (x,y,z)=(m,y,z). Its four inequalities follow from

    S < 2y+e <= beta,
    1/2+y <= beta,
    2m-y+z < m+e <= M+e <= 2 beta-1,
    2m+y+3z < 4y-m+3e <= 3y+3e <= 3/2 <= 3 beta-1.

Here `M+e<=2 beta-1` follows from beta>=4/5, and the last comparison follows from beta>=5/6.

Next suppose y-z<=m-e and S<3e. Apply L32 with (x,y,z)=(z,y,m). Its requirements follow from

    S<3e<=beta,    1/2+y<=beta,
    2z-y+m<=S<3e<=2 beta-1,
    2z+y+3m<=3S<9e<=3 beta-1.

The numerical comparisons follow from beta>=5/6.

It remains that

    y-z<=m-e,       S>=3e.

Apply L31 with (x,y,z)=(z,y,m) if `y+z+2m<=3 beta-1`. Indeed its conditions other than this one hold as follows:

1. y+z<=2a<=beta.
2. Both 1/2+y and 1/2+z are at most beta.
3. y+m-z>=m>s0>=e, while m+z-y>=e is the case assumption.
4. S>=3e is the case assumption.
5. S<=m+2y<=2-beta<=5 beta-3.
6. `(2+3m)/4<=beta` because m<=M.

The only remaining possibility is the **new static branch**

    y+z+2m>3 beta-1.

Since 3m<=4 beta-2,

    y+z > 3 beta-1-2m >= m+e.

Also y<=a gives

    m+y-z = m+2y-(y+z)
            < 3m-beta <= 3 beta-2.

Finally S<=2-beta<=5 beta-3 as above. These are exactly Lemma S1a's conditions, so its four static requests close the triple. This is the step missing from Claude's original case division.

### Case (c): y>a

The balanced constraint m+2y<=2-beta implies

    m < 3e,
    2 beta-1 < u < 5/2-2 beta,
    d < 7/2-4 beta,
    2m-y < 13/2-7 beta,
    2m+3y < 9/2-3 beta,
    2m+y < 11/2-5 beta.                  (C)

For example m<=2-beta-2y, and substitution of y>a proves each displayed upper bound. Define

    L = 3 beta-1-2u,
    U = (2 beta-1-y)/2.

The remaining split is: z<=L; otherwise z<e-d; otherwise z<=U; otherwise z>U.

**(c1) z<=L.** Use L26 with (m,y,z). First S<=3 beta-1-u<beta. Further z<=y-e follows from `2m+3y>5a>=2 beta`; hence also z<=m-e. The remaining two bounds follow from

    m-y/2 >= y/2 > a/2 >= e,
    y-m/2 > a-3e/2 >= e.

These comparisons use only beta>=5/6 and beta>=6/7. The last L26 inequality is exactly z<=L.

**(c2) z>L and z<e-d.** Use S2 with (x,y,z)=(y,m,z). Here P=e+d-z>0 and Q=e-d-z>0. Its conditions reduce to

    z>=3e-y,      y<=2 beta-1,      z>=y+4-5 beta.

The middle condition follows from y<=m<3e<=2 beta-1. For the other two use z>L and

    L >= 3e-y     iff 2m+y<=6 beta-4,
    L >= y+4-5 beta iff 2m+3y<=8 beta-5.

Both follow from (C), precisely because

    11/2-5 beta <= 6 beta-4,
    9/2-3 beta <= 8 beta-5

are equivalent to beta>=19/22.

**(c3) z>L, z>=e-d and z<=U.** Use S2 with (x,y,z)=(m,y,z). Now P=0 and Q=(e+d-z)_+.

If Q=0, its requirements reduce to

    z<=m-e,       y+z<=beta,       y+2z<=2 beta-1.

The third is the case condition. The first follows from U<=m-e, which is equivalent to 2m+y>=1 and follows from 2m+y>=3y>3a>=1. The second follows from y+z<=a+y/2<a+3e/2<=beta.

If Q>0, its three requirements reduce to

    y>=2e,        m<=2 beta-1,      2m-y<=4 beta-3.

The first two follow from y>a>=2e and m<3e<=2 beta-1. The third follows from (C) and

    13/2-7 beta <= 4 beta-3,

again exactly beta>=19/22.

**(c4) z>U** (with z>L and z>=e-d inherited). The bounds (C) and beta>=19/22 imply

    U>=e+d       iff 2m-y<=4 beta-3,
    U>=u-(3 beta-2) iff 2m+3y<=8 beta-5.

Consequently y+z>=m+e and m+y-z<=3 beta-2. Also S<=2-beta<=5 beta-3. Apply Lemma S1a.

These cases exhaust the domain. All nonstatic branches have budget at most beta r (or ceil(beta r) in L18); the two S1 branches have budget at most beta r+3. QED.

## 3. From the local proposition to a global bound

Set

    beta=19/22,       h=16/33,       ell=1/6,
    K=ceil(beta r)+10,              T=ceil(beta r)+4.

Let r>=1000, suppose H is r-uniform with property (7,2), and suppose tau(H)>K. Both K and T are at most r.

### Step 1: the interval [ell r,h r] is empty

Let h0=floor(h r). Request an edge avoiding K points of an edge. This produces a distinct pair with intersection at most r-K<h0. Thus the largest pair intersection m<=h0 exists. Choose E,G attaining it.

Suppose m>=ell r. A balanced request of K points produces a good triple E,F,G such that both new intersections are at most

    r-floor((K+m)/2)
        <= r-(K+m-1)/2
        <= h r-9/2 < h0,

because beta+ell=2-2h. Maximality gives y,z<=m. Label so m>=y>=z. Moreover

    m+2y <= 2r-K+1 <= (2-beta)r-9.

Now m<=h r=((4 beta-2)/3)r, so the parametric local proposition closes the triple at budget K, a contradiction. Hence m<ell r. Every pair intersection is therefore below ell r or above h r.

### Step 2: extend the gap to r/2

Suppose distinct E,F have x=|E cap F| in [h r,r/2]. A balanced request with budget ceil(beta r) produces a good triple E,F,G with the other intersections y,z at most

    (1-(beta+h)/2)r+1/2 = (43/132)r+1/2 < h r.

By the gap, y,z<ell r=r/6. Consequently

    S=x+y+z < (1/2+2ell)r = 5r/6 < T.

Thus only the first case of Claude's gap-extension construction is needed. Here are all its requests and bounds, specialized to the new parameters.

Use pair cells X=E cap F, Y=E cap G, Z=F cap G and private parts P_E,P_F,P_G. Let

    p=(r-x-y-h0)_+,      q=(r-x-z-h0)_+.

Choose P1 subset P_E of size p and P2 subset P_F of size q. The size C0 of their union with X,Y,Z is

    C0=x+max(y,r-x-h0)+max(z,r-x-h0).

Its four possible linear expressions are S, r-h0+y, r-h0+z, and 2r-x-2h0. Hence

    C0 <= max(T, (1-h+ell)r+1, (2-3h)r+2)
        = max(T, (15/22)r+1, (6/11)r+2) = T.

Choose W subset P_G with |W|=T-C0. This fits because C0>=S and T-S<=r-y-z. Request H avoiding

    D=X union Y union Z union P1 union P2 union W.

Then E cap H and F cap H have at most h0 points, and H is distinct from E,F because it misses X. The gap therefore gives

    c=|E cap H|<ell r,       a=|F cap H|<ell r.

Put B=G cap H and b=|B|. The request's W component gives

    b<=r-T+x+p+q.

All four triple intersections among E,F,G,H are empty. Thus every two-point transversal lies in one of X times B, Y times (F cap H), or Z times (E cap H). Split B=B1 disjoint-union B2 as equally as possible, and request three more edges avoiding

    X union B1,
    X union B2,
    Y union Z union (E cap H) union (F cap H).

The third set has fewer than 4ell r=2r/3<T points. The first two have size at most

    x+ceil(b/2) <= (r+3x+p+q-T+1)/2.

Expanding the positive parts,

    r+3x+p+q
      <= max( (5/2)r,
              (3-h)r+1,
              (7/2-2h)r+2 )
       = max( (5/2)r, (83/33)r+1, (167/66)r+2 )
      <= (167/66)r+2.

This is at most 3T-1 because 3T>=(171/66)r+12. Thus the first two requests also have size at most T. They cover all three candidate products, giving a bad seven-edge subfamily. Contradiction.

Every pair intersection is now below r/6 or greater than r/2.

### Step 3: finish

Claude's hand finishing lemma states: if 5/6<=gamma<1 and every pair intersection is at most `((3 gamma-2)/2)r` or exceeds r/2, then

    tau(H)<=ceil(gamma r)+4

whenever that budget is at most r. Its proof uses only the displayed L18 and the paper's explicit two-large-pair-cells lemma L41; it is independent of the older numerical constants.

Apply it with gamma=19/22, since

    ell=1/6 < (3 beta-2)/2 = 13/44.

This gives tau(H)<=T<K, the desired contradiction. Hence

    f(r,7)<=ceil(19r/22)+10        for r>=1000.

Private padding of each edge to rank r preserves both tau and property (7,2), so the same bound holds for rank-at-most-r families. QED.

## 4. Exact local obstruction to pushing this menu below 19/22

The new coefficient is a limitation of the local closing menu, not a lower bound for f and not an obstruction to additional adaptive scripts.

Let b0=19/22 and take 0<delta<1/1000. Set

    beta=b0-delta,
    m=9/22+delta,
    y=4/11,
    z=2/11+delta.

These are valid good-triple parameters: m>=y>=z, every pair sum is less than 1, m+2y=2-beta, and m<((4 beta-2)/3). Nevertheless NONE of L18, L26, L31, L32, S1, S2 (including every permutation) applies at budget beta.

* **L18:** its smallest usable max-cell bound is m, and (2+2m)/3>=31/33>beta.
* **L26:** its first condition requires S<=beta, but S=21/22+2delta>beta.
* **L31:** its two half-plus-cell conditions require two distinct pair cells at most beta-1/2=4/11-delta. Only z qualifies.
* **L32:** the half-plus condition forces its middle role to be z. The other two roles are m,y. Its third term is then respectively 1+delta/2 or 43/44, both above beta.
* **S1:** one pair-sum requirement necessarily asks y1+z1>=1+m-beta=m+e, but y+z=m+e-delta. This violates even a necessary feasibility condition of this static template.
* **S2, (x,y,z)=(m,y,z):** P=0, Q=delta. Its third left side minus 2beta is 6delta>0.
* **S2, (x,y,z)=(y,m,z):** P>0, Q=0. The third left side exceeds 2beta already by 1/22 at delta=0 and increases with delta.
* **Other four S2 orientations:** their first condition implies T>=1-x+z. If the last role is m this is at least 1. For (x,y,z)=(z,m,y) it is >1. For (x,y,z)=(m,z,y) it is 21/22-delta>beta. Thus each fails.

So there is a genuine uncovered local configuration for every beta immediately below 19/22. To go below this coefficient using the maximality pipeline, one must add a closing lemma or exploit extra global gap information at this configuration. Reassigning the same six available lemmas cannot suffice. This is a proof-method obstruction only: these cell masses do not construct an entire high-tau (7,2) family.

## 5. Supplementary exact arithmetic checks [C]

Script: `/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/check_claude_hand_param.py`.

It uses only Python integers and Fraction, exhaustively enumerates integer good-triple parameters on several scales at beta=19/22, 32/37 and 7/8, follows the stated case decision, checks every selected closing inequality, and checks the rounded S1 splits against integer budgets. These finite checks supplement the symbolic proof; they do not establish the continuum coverage or replace the hand argument.

Command: `python3 work/check_claude_hand_param.py` from the task directory. The enlarged-threshold run completed successfully:

* beta=19/22 at r=44,110,220: **198,329** triples; the new branch b4 was used 34 times.
* beta=32/37 at r=74,148,296: **486,077** triples; branch b4 was used 72 times.
* beta=7/8 at r=64,128: **42,110** triples.

Total: **726,516** exact arithmetic checks, all passing. No new claim of a best general coefficient is intended.
