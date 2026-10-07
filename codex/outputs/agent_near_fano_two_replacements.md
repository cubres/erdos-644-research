# Two actual responses to the cyclic 108b requests

**Status: [C], exact positive obstruction for this specified pair of requests.** This is not a high-transversal family and does not obstruct a different adaptive request. The stronger `p=t` hypothesis is not realized: the resulting actual family has transversal number three. Root's independent static two-request argument supersedes that hypothesis for this support.

The construction works for every integer `b>=1`, has rank `k=144b+1`, and includes the original seven restored near-Fano rows together with two actual response rows. Its globally minimum six-row endpoint/pair potential is exactly `(111b,3669b^2)`. Both avoidance requests cost `108b<3k/4`; all 36 seven-row subfamilies are two-pierceable. Thus these two legal requests plus the complete six-row minimum-potential constraints do not force a contradiction.

## Exact construction

Coordinates are `0,...,6`. The Fano lines are the triples for which the xor of their three indices plus one is zero. For every line `L`, take a base class of `33b` points whose complementary type is `L`, and four defect classes of `b` points whose complementary types are `L union {h}`, one for each `h notin L`. A point belongs to old row `j` iff `j` is absent from its complementary type.

Choose `x` from the base class assigned to `012` and restore its incidence in row zero. This creates the original seven actual rows; row zero has size `144b+1`, and every other old row has size `144b`. Let `F` be the six rows `1,...,6`. Its piercing graph has endpoint set `P` consisting of the classes assigned to the three lines through zero, including `x`. Therefore `|P|=111b` and its number of unordered pairs of distinct points is `3669b^2`.

Let `A` be all classes whose assigned Fano line does not contain zero. Let `R` consist of the eight defect classes assigned to either `135` or `146`; `|A|=148b` and `|R|=8b`. Introduce one new outside class `Y` of size `b`, contained in no old row.

Define the two three-class allowances, writing `(L,h)` for the defect class assigned to line `L` with extra missing coordinate `h`:

- `C1={(012,3),(034,5),(056,1)}`;
- `C2={(012,4),(034,6),(056,2)}`.

These are disjoint, each has size `3b`, and each contains one defective class from each eligible Fano class. Set

`D1=P\C1`, `D2=P\C2`,

`G=(A\R) union C1 union Y`,

`H=(A\R) union C2 union Y`.

Then `|D1|=|D2|=108b`, `G` avoids `D1`, `H` avoids `D2`, and `|G|=|H|=144b`. In particular the shared outside defence is included explicitly, rather than excluded by the model.

## Exact certificate and scope

Run from the task directory:

```
python3 -S work/p644_near_fano_two_replacements_check.py
```

The standard-library checker independently reconstructs all classes and rows from this description. It computes every pair graph symbolically, with affine class sizes in `b`. For all 84 six-row subfamilies it proves lexicographic potential at least `(111b,3669b^2)` for every integer `b>=1`; for all 36 seven-row subfamilies it proves a strictly positive pair count. Polynomial inequalities are certified by nonnegative coefficients after substituting `b=u+1`. Repeated rows and subfamilies with fewer rows follow by completing to a distinct six- or seven-row subfamily and monotonicity of piercing graphs.

The output is `outputs/agent_near_fano_two_replacements_certificate.json`. At `b=100`, every new six-tuple has at least `17900` endpoints, and every six-tuple containing both new rows has at least `18400`, compared with the minimum `11100`. Some new six-tuples have fewer than `36690000` pairs, but have strictly more endpoints; the checker correctly uses lexicographic minimization and does not impose the stronger invalid separate pair minimum.

The checker also proves that the full nine-row family has transversal number exactly three. This prevents interpreting it as an extension with `tau>3k/4` or with `p=t`. It only certifies simultaneous compatibility of this specific pair of response obligations, all the resulting `(7,2)` tests, and the complete joint-potential constraints. In particular, the fact that `F` is a global potential minimum is already true in this finite family and supplies no contradiction by itself.

## New-graph neighborhood probe

For the first actual response `G`, the discovery script `work/p644_near_fano_second_request_discover.py` tested the twelve five-row graphs formed by `G` and four rows of `F` with empty common intersection. It included all partial type masses and an integer strict margin of one at `b=100`. Numerical optima for the global-cover neighborhood criterion ranged from `14301` to `14801`, all above the `10800` request budget. These are discovery results, not exact lower certificates, and are not needed to validate the explicit survivor. They suggest that this particular first response weakens the one-step neighborhood route. No claim is made about other choices of the first avoidance set or other adaptive arguments.

## Follow-up: the first request from coupled optimization

**Status: one exact closing branch and one exact surviving branch.** Use the four old rows `(2,4,5,6)`, writing their membership masks in that order. The optimized first request `D1` consists of masks `0010,0110,1001,1011,1101`, with total size `108b`.

A sparse actual response obtained by deleting eight defect classes has rank `144b`, satisfies the eight-row `(7,2)` and minimum-potential constraints, but is killed asymptotically by the new graph on these four old rows plus the response. That graph has `184b` endpoints and admits `S` of size `73b+1` with closed neighborhood `108b+1`. Consequently this response forces a global cover of size `108b+1=(3/4)k+1/4`. The exact classes are encoded in the new checker below.

There is a different actual response that avoids this conclusion. Let `V` denote the old union of `259b` points. Take a subset `Z` of size `8b` from the base class assigned to line `245`, which has four-row membership mask `1000`. With a new outside class `Y` of size `b`, set

`G_dense=(V\D1)\Z union Y`.

It has rank `144b`, avoids `D1`, and keeps a positive portion of every available old class. The entire rank deficit is placed in a class that is not an endpoint of the retained four-row piercing graph. This is the structural distinction from the sparse closing branch.

The optimized static second request consists of four-row masks `0011,1010,1100,1101,1110`; call it `D2`. It too has size `108b`. The response

`H_dense=(V\D2)\Z union Y`

also has rank `144b`. The original seven rows and these two dense responses satisfy all 36 seven-row tests and all 84 six-row lexicographic minimum-potential tests for every integer `b>=1`. Shared outside points are included explicitly. This is a positive survivor for the particular optimized pair, not a survivor for every adaptive second request or for high-transversal extension obligations.

The exact script is

```
python3 -S work/p644_near_fano_optimized_response_check.py
```

It writes `outputs/agent_near_fano_optimized_response_certificate.json`. Besides the actual-row checks, it exhaustively analyzes the twelve new five-row graphs consisting of `G_dense` and four rows from `F` whose common intersection is empty. The merged type counts range from ten to 21. Across all 5,266,432 supports it allows arbitrary continuous partial selected masses. At the weak threshold `|S|>=|P5|-111b`, every closed neighborhood has size at least `111b`. The exact minima, in old-row lexicographic order, are

`182,180,148,111,180,182,182,148,182,179,180,111`, times `b`.

For an activated type support `J`, the exact continuous lower envelope is

`w(N(J)) + max(0, h-w(J intersect N(J)))`,

provided `w(J)>=h`, where `h=|P5|-111b`. This enumerates all actual supports and all partial masses, rather than imposing a positive-mass cutoff. It also rules out the stronger endpoint/pair tie test for any proposed `D` of size below `111b`: if the residual graph after deleting pairs wholly inside `D` has at most `111b` endpoints, its isolated vertices form `S` with `|S|>=h` and `N[S] subseteq D`.

This exact lower certificate covers only the twelve stated empty-intersection cores. A numerical discovery scan also found no neighborhood of cost near `108b` among the twelve empty-intersection four-old cores that contain row zero, but that scan is not promoted to an exact lower certificate. Cores with a common intersection require explicit control of points outside the old union and remain a separate route.

## Follow-up: forcing the second response away from all first-response outside points

**Status: [C] exact actual-row survivor, with no shared outside point.** For the dense `G` above, choose

`C={(012,5),(012,6),(056,1),(056,2)}`,

`D2=(P\C) union Y`, and `H=(A\Z) union C`.

Here `Z` is the same `8b` subset of the base class `245` omitted by `G`. Then `|D2|=108b`, `|H|=144b`, and `H` has no point outside the old union at all. In particular it is disjoint from `G`'s entire outside class `Y`.

For every integer `b>=1`, the original seven rows together with `G,H` satisfy every seven-row two-piercing test and every six-row lexicographic lower bound `(111b,3669b^2)`. The exact independent checker is

```
python3 -S work/p644_near_fano_outside_control_check.py
```

Its output is `outputs/agent_near_fano_outside_control_certificate.json`, including all affine class sizes and all nine membership masks. This is again a finite compatibility certificate for the stated two requests, not an actual high-transversal extension.

The previously unsafe four-row core `(1,2,5,6)` has common intersection exactly the base class `034`. Both responses omit that entire class. A piercing pair with one endpoint outside the old union would therefore need its old endpoint in that common class and in the other response, which is impossible. Thus this core is now finite despite having a common intersection. Its six-row endpoint set nevertheless has size `151b`, above `111b`.

The closest new six-row graphs have `115b` endpoints, but they contain only `H` and five old rows:

- `(1,2,3,5,6,H)`, with `3596b^2` pairs;
- `(1,2,4,5,6,H)`, with `3876b^2` pairs.

Both are valid because endpoint count is strictly larger than the global minimum. Their pair count cannot be compared separately to `3669b^2`. This identifies the remaining possible adaptive route: exploit the five-row graphs created by the actual responses or obtain a third row with controlled intersections, rather than infer a contradiction from the six-row potential alone.

## Forward probe after both actual responses

The discovery script `work/p644_near_fano_double_response_neighborhood.py` tested all 22 five-row tuples consisting of `G,H` and three of the original seven rows whose **actual** common intersection is empty. This includes all seven Fano-line triples, tested first. Thus unseen points outside the known tuple union cannot enter these piercing graphs. The script allows arbitrary partial masses and uses the strict integer threshold `|S|>=|P5|-111b+1` at `b=100`.

No closed-neighborhood witness of size `108b+O(1)` was found. The smallest returned objective was `11400`, for old triple `(1,2,6)`, whose five-row endpoint count is `18600` and strict selected-size threshold is `7501`. The next smallest was `11601`, for `(2,5,6)`. The full numerical results are in `outputs/agent_near_fano_double_response_neighborhood.json`. These are bounded MILP discovery results only; they are not exact lower certificates and do not exclude an argument using other global obligations. No further exhaustive support enumeration was run for these failures. A separate agent is pursuing a third actual response forced to avoid the entire `71b` intersection `G intersect H`.

## Third actual response with empty triple intersection

Agent `critical_literature` constructed a third legal request and actual response; the following certificates check that construction independently. Let `I=G intersect H`, so `|I|=71b`, and retain the deleted base-class subset `Z` of size `8b`. Choose `18b` ordinary points from base class `012`, excluding the restored singleton `x`, and `18b` points from base class `135`; call their union `B`. Put

`D3=I union Y union B`,

`J=U\(I union B union Z)`.

Then `|D3|=108b`, `|J|=144b`, and `J` has no outside point. The exact intersection data are

`G intersect H intersect J = empty`,

`|G intersect H|=71b`, `|G intersect J|=54b`, `|H intersect J|=55b`,

`|G union H union J|=252b`.

For every integer `b>=1`, the ten actual rows satisfy every one of the 210 six-row joint-potential comparisons and all 120 seven-row piercing tests. The global six-row minimum remains `(111b,3669b^2)`. The closest new six-tuple containing `J` is `(2,3,5,6,H,J)`, with `177b` endpoints and `4552b^2` pairs.

Run

```
python3 -S work/p644_near_fano_third_outside_free_check.py
```

The output `outputs/agent_near_fano_third_outside_free_certificate.json` includes exact affine class sizes and ten-row membership masks. This strengthens the response obstruction by removing both the shared-outside defence and the common intersection of the three responses. It remains a certificate for three specified request obligations, not for the full high-transversal extension property.

An earlier variant, also certified, uses `18.5b` cuts in each of the two base classes and allows `J` to contain `Y`. It works for every even `b>=2`, with pair intersections `54.5b,54.5b`. Its checker is `work/p644_near_fano_third_response_check.py`. The outside-free version above is the stronger continuation state.

The subsequent bounded discovery scan tested all 21 new five-row graphs `G,H,J` plus two old rows for the outside-free version. Their common intersections are all empty because `G intersect H intersect J` is empty. No `108b+O(1)` neighborhood witness was found. At `b=100`, the smallest returned objective was `16801`, for old pair `(2,6)` with five-row endpoint count `21400`. These outputs are discovery-only, with no exact infeasibility claim: `work/p644_near_fano_triple_response_neighborhood.py` and `outputs/agent_near_fano_triple_response_neighborhood.json`. The useful exact result remains the ten-row compatibility certificate, while further progress must exploit a different global constraint or a more effective request.
