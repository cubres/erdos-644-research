# Enlarged third requests, uniform seven-row survival, and a singleton repair

Status: hand deductions from exact finite certificates [C]. These are
actual local response constructions. They are not high-transversal
counterexamples, and they do not close the general three-quarter bound.

Use the nine-row family from7.150 and its verified certificate
`outputs/agent_near_fano_outside_control_certificate.json`. On its ground
V=U union Y, of size260b, put

    I=G intersect H, |I|=71b,
    E=G triangle H, |E|=146b,
    R=cell37, |R|=8b,
    B=V\(G union H union R), |B|=35b,
    M=B union E=V\(I union R), |M|=181b.

For any actual point subset X of M of size37b, the request
D3=I union X has size108b. The complement-shaped response

    J0=M\X

has size144b and avoids D3 and R. In this section X may enter B,
unlike the restricted universal endpoint theorem of7.152.

## 1. Every such complement preserves the seven-row property

[C] For every six-row subset S of the old nine-row family, let P(S)
be its actual piercing-graph endpoint set on V. The exact inequality is

    |P(S) intersect M| >=39b.                         (1)

The least coefficient39 occurs for S=[1,2,3,5,6,H], whose endpoints
in M are the base class034 together with six defect classes. The exact
cell indices are[1,10,11,12,13,14,16].

Consequently every X of size37b leaves a point of P(S) in J0. That
point has an old piercing partner; their pair meets S and J0. Thus
all new seven-row subfamilies are two-pierceable. The old seven-row
conditions are unchanged. Repetitions and fewer rows follow by
extension to distinct rows and monotonicity. This proves property
(7,2) for the entire extended actual family, uniformly over all X.

The checker `work/p644_third_request_seven_robust.py` verifies(1) on
all84 old six-row subsets using exact affine masses. It also records
the earlier, more restrictive argument for X subset E:74 tuples have
a fixed endpoint in B, and the other ten have107b,108b,or143b endpoints
in E. The stronger bound(1) handles all partial X in M directly.
The output is `outputs/root_third_request_seven_robust.json`.

This is a seven-row statement only. The global six-row endpoint
minimum can fail, as the next example shows.

## 2. Removing the protected major class defeats the fixed-R response

Take X to consist of certificate cells

    {1,7,11,12,13}.

Cell1 is the base class034 of size33b. The other four are defect
classes0123,0134,0234,0345, each of size b. Thus |X|=37b.
For the resulting J0, the actual six-tuple

    [F1,F2,F6,G,H,J0]

has exactly104b endpoints. This is below the assumed global minimum
p=111b, so J0 cannot be an actual response in a family where that
minimum is enforced.

The five retained rows F1,F2,F6,G,H have empty common intersection.
Their endpoints therefore lie in V even if the ambient family contains
additional unseen points. Their piercing graph after adjoining any
edge avoiding D3 union R is a subgraph of the graph obtained from J0.
Hence the result is stronger than rejection of one rank-filling choice:

    Every actual response avoiding D3 must meet R.     (2)

Equivalently D3 union R is a global transversal. Its size116b exceeds
the target budget, so this alone does not yield the desired bound.

This establishes a genuine new forced incidence into a region which
the preceding complement responses had omitted entirely. It does not
establish that the forced R-trace has positive proportional mass.

## 3. One point of R suffices to repair the response

Choose r in R and choose z in the base class012 outside the distinguished
restored point x. That base class is retained in J0. Define

    J=(J0\{z}) union {r}.

The response still has exactly144b points and avoids the108b request.
Its R-trace has size one, so its normalized mass tends to zero as b
increases.

[C] For every integer b>=1, all126 new six-tuples containing J have
strictly more than111b endpoints, and all84 new seven-tuples have a
piercing pair. The old nine-row tests are unchanged. Hence the full
actual ten-row family again has property(7,2) and retains the original
global endpoint/pair minimum(111b,3669b^2).

For the particular six-tuple rejected in Section2, the endpoint count
jumps from104b to

    142b+1.

The one new point r has38b neighboring points in the five-row piercing
graph, all of which become eligible when r belongs to J. The removed
point z was not an endpoint of that critical five-row graph, so its
removal does not cancel this activation. This explains the entire jump
by an exact support calculation.

The independently reconstructible certificate is

    python3 -S work/p644_third_request_singleton_repair_check.py

with output `outputs/root_third_request_singleton_repair_certificate.json`.
It reads the already verified nine-row data, splits one point from each
of the two stated classes, and checks the NEW subfamilies only. Affine
endpoint inequalities prove the assertions for every b>=1, and all
positive point classes are retained exactly. The secondary pair minimum
needs no new equality check because all new endpoint counts exceed p.
The unchanged old rows keep their previous minimum and pair count.

## 4. Precise consequence for the current attack

Requests confined to I plus37b of E admit the entire universal survivor
family of7.152. Requests entering B can rule out the fixed-R complement
and force a real R-incidence. The explicit larger request above still
admits the singleton repair, however. Thus neither eliminating the full
common intersection nor forcing a newly used region ensures a linear
saving in the endpoint potential.

A next argument must control these small but strategically placed
actual incidences, or use the full high-transversal avoidance hypothesis
to force a larger incompatible collection of responses. Replacing a
positive R-trace by a fixed positive fractional lower bound would be
unsound: the exact surviving trace here is just one point. No claim is
made that all possible next requests survive, or that the available
research directions are exhausted.
