# notes_handbound.md  (w4 handbound run, 23 Sep 2026)

## 0. Status at start
Previous handbound run (salvage/w3_handbound.txt) died before doing anything. Starting fresh.
Plan: hand route = Lemma 7.50 (finishing: all pair intersections <= (3b-2)/2 or > 1/2 => tau <= b r + 4,
uses only Lemma 7.18 + Lemma 7.41) + a hand exclusion of the case m := largest pair intersection <= r/2
lies in ((3b-2)/2, 1/2]. In that case a pair E,G with |E cap G| = m, a balanced request gives a good
triple (m,y,z), y,z <= min(m, 1-(b+m)/2), AND the global gap: every pair intersection <= m or > 1/2.
Step 1: numerically find which few hand lemmas cover this region, for which b.

## 1. Numerical exploration (scripts w4_handbound_*.py; float, exploratory only)  [NUMERICAL]
* Max-small framework (m = largest pair intersection <= 1/2, Lemma 7.50 finisher) with the note's hand
  adaptive lemmas (7.18,7.20,7.23,7.25,7.26/7.30,7.29,7.31,7.32,7.33,7.35,7.37,7.15, GT*) FAILS below 7/8:
  tight spots (a) triple (3/8,3/8,z), z in [1/8,3/8]  (L31 term 1/2+x),  (b) m = 1/2, y,z in [0.08,0.32].
* Static 4-request optimum (MILP over label antichains, w4_handbound_static.py) fixes spot (a):
  (3/8,3/8,1/8)->0.85, (3/8,3/8,3/8)->0.825. Near x=1/2 static optimum ~ (3+x)/4 -> 7/8 (Lemma 7.13).
* Spot (b) is avoided by a two-step chain with threshold h (e.g. h=0.45):
  Step 1: m = largest intersection <= h; if m >= l := 2-b-2h then caps w=1-(b+m)/2 <= h so y,z <= m;
          cover region {(m,y,z): y,z<=min(m,w)} with gap (m,h].
  Step 2: q in (h,1/2]: y,z <= 1-(b+q)/2 < h so y,z < l (gap [l,h]); cover.
  Step 3: all intersections < l or > 1/2, l <= (3b-2)/2 -> Lemma 7.50.
  At b=0.87, h=0.45 (l=0.23) grid-covered by {L26(+7.30), L31, L32, L35, L37, static P4, P0, P5}.
  (P4 = symmetric template: R_C = X u P_C u Y2 u Z2 (cyclic), R_core = X1 u Y1 u Z1.)

## 2. Chain chosen (tentative): beta = 173/200, h = 23/50, l = 2-beta-2h = 43/200   [NUMERICAL so far]
Step 2 == note Lemma 7.27 exactly (same constants!). Step 3 == Lemma 7.50 (needs l <= (3b-2)/2 = 0.2975).
Step 1 fine-grid (N=30) covered by {L18, L26, L31, L32, P0, P4}; P5/L37/L35 not needed in step 1.
P4 closed form (derived): requests R_C = X u P_C u Y2 u Z2, R_B = Y u P_B u X2 u Z2, R_A = Z u P_A u X2 u Y2,
  R_0 = X1 u Y1 u Z1 (X=AB,Y=AC,Z=BC). Sizes 1+x-y1-z1, 1+y-x1-z1, 1+z-x1-y1, x1+y1+z1.
  Feasible iff T >= (3+S)/5, (1+w)/2, 1+x-y-z (cyclic), (2+x+y-z)/3 (cyclic)  [to be proved].
P0 (hub A: X=AB, Y=AC): R0 = X u PC0, R2 = Y u PB2, R1 = X01 u Y u Z u PA u PB1 u PC13, R3 = X03 u Y u Z u PC13.
  At x=y=m: covers z in [4+m-5T, (2T-1-m)/2] roughly.
Spot A cover: L26 (z small), P0 (z ~ .05-.18), P4 (z >= .155).

## 3. Step-1 cover at beta=173/200, h=23/50 (l=43/200)  -- hand-provable structure found
Region: (3b-2)/2 < m <= h, 0 <= z <= y <= min(m, w), w = 1-(b+m)/2  (WLOG y>=z).
(a) m <= (3b-2)/2 = 119/400: L18 (all three <= m).
(b) y <= b-1/2 = 73/200: L31 with (a,b,c)=(z,y,m) [c = partially avoided cell = m] fails only if
    (4) y-z > m-(1-b) or (5) S < 3(1-b). Its condition (7) (1+y+z+2m)/3<=b reduces to m <= 4b-3 = h (!).
    (4) fails -> L32 (a,b,c)=(m,y,z) (checked by hand: S<2y+1-b<=b, 2m+z-y<m+1-b<=0.595<=2b-1, 2m+y+3z<4y-m+0.405<=3y+.405).
    (5) fails -> L32 (a,b,c)=(z,y,m) (m+2z-y<=S<.405<=2b-1, 2z+y+3m<=3S).
(c) spot A: y > b-1/2 (so m in (0.365,0.405), u=m+y in (0.73,0.77]):
    L26 (m,y,z) covers z <= 3b-1-2u;  P4 covers z >= max(1-b+m-y, u-(3b-2)); P0 (either hub orientation) covers middle.
    Exact rational grids N=60, N=97: all points covered (w4_handbound_step1_exact.py).

## 4. Re-derivations done (by hand, line by line) [FULL_PROOF-level checks in my head; to be written]
L18 (7.18) OK; L26 (7.26) OK; L31 (7.31) OK incl. case 3 interval; L32 (7.32) OK; L41 OK; L50 OK;
L27 (7.27, step 2) OK at b=173/200, l=43/200, h=23/50 (constants rechecked: 0.755r+1<T, 2.58r+3<=3T, 1.715r+.5<=2T, 2.565r<=3T).
P0 static: R0=X u PC0, R1=X01 u Y u Z u PA u PB1 u PC13, R2=Y u PB2, R3=X03 u Y u Z u PC13;
  P=(r+y-x-z-T)+, Q=(r+x-y-z-T)+; conditions (i) T>=r-x+z+P+Q (ii) T>=y+z+Q (iii) 2T>=r+y+2z+P+2Q; exactly integral.
P4 static: need m1+y1+z1<=T, y1+z1>=r+m-T etc.; explicit splits in spot A.
STEP-1 HAND COVER (r=1, b=173/200):
 (a) m<=119/400: L18.  (b) y<=73/200: (b1) y-z<=m-27/200 & S>=81/200: L31(z,y,m); (b2) y-z>m-27/200: L32(m,y,z);
 (b3) S<81/200: L32(z,y,m).  (c) y>73/200 [u=m+y in (146,154)/200, d=m-y<8/200, m<81/200]:
 (c1) z<=319/200-2u: L26(m,y,z); (c2) z<27/200-d: P0(y,m,z) [needs z>=max(81/200-y, y-65/200)];
 (c3) 27/200-d<=z<=(146/200-y)/2: P0(m,y,z); (c4) z>=max(27/200+d, u-119/200): P4 explicit splits.

## 5. RESULT (checkpoint): hand proof of f(r,7) <= ceil(173r/200)+10 for r>=1000  (c = 0.865 < 7/8)
Chain: K=ceil(br)+10, tau>K.  Step 1 (m = max intersection <= floor(hr); if m >= lr: balanced request
 -> triple (m,y,z), y,z<=m by maximality -> cases (a)(b)(c) of section 4 -> contradiction).  Step 2: note
 Lemma 7.27 verbatim.  Step 3: Lemma 7.50 (L18 + L41).  Padding -> rank<=k families.
Checks (all PASS):
 * w4_handbound_step1_proof_check.py 80 : exact rationals, grid N=80 + 200k random points, decision procedure
   exactly as written; also w4_handbound_step1_exact.py 60/97.
 * w4_handbound_e2e_lemmas.py : random integer games (adversarial random responses), L18,L26,L31,L32,P0,P4:
   requests <= T and final <=7 edges have no 2-transversal (~14k runs).
 * w4_handbound_e2e_gap.py : Lemma 7.27 both cases at r in {1000..2000}, gap-respecting adversary (400 runs).
 * w4_handbound_e2e_l50.py : Lemma 7.41 branch of 7.50 (555 runs).
Limit of this chain: spot A static optimum ~0.8621 (MILP) -> cannot go below ~0.862 without new adaptive idea.

## 6. Final packaging (checkpoint before final answer)
Prop 10 (local, NO gap hypothesis): b=173/200, br+3 <= T <= r, tau>T. Any good triple with |E&G|=m, |E&F|=y,
|F&G|=z, z<=y<=m<=23r/50, m+2y<=227r/200 extends to a bad <=7-subfamily. Proof = cases (a),(b1-3),(c1-4).
Main theorem: f(k,7) <= ceil(173k/200)+10 for k>=1000 (K=ceil(bk)+10). Steps: max intersection <= floor(hr)
-> Prop 10 => all intersections < lr or > hr; Lemma 7.27 => < lr or > r/2; Lemma 7.50 => tau <= ceil(br)+4.
L26 branch 'both big' rarely hit by random e2e (2 hits, PASS); proof checked by hand.
Status: writing final structured answer now.
