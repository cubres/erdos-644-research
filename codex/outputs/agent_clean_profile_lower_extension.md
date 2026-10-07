# A lower-side extension of the clean-profile 3/4 lemma

Status: hand proof; finite support assertions additionally checked exactly.
This adds a region to the preceding report, without claiming the arbitrary
weighted clean-profile theorem.

Use the symmetric clean six-row profile of
`agent_clean_profile_weighted_menu.md`: star triples 235,145,136,246 each
have mass c; the three cycle four-types each have mass a; their twelve
three-subtypes each have mass b. Assume the actual family has property (7,2)
and every at-most-six-row actual subfamily with empty common intersection has
at least p=3a+12b eligible endpoints. The convention includes repeated indexed
rows and avoids an exact-six distinctness assumption at degenerate parameters.
The witness row size is k0=2c+2a+6b.

**Lemma.** For nonnegative integers a,b,c such that

    a+2b <= c < a+3b,

the actual family satisfies

    tau(H) <= ceil(3k0/4).

**Proof.** Put u=a+3b-c and B=3a+9b. Then 1<=u<=b, and

    k0=4a+12b-2u,  ceil(3k0/4)=B-u-floor(u/2).

Retain old rows 2,4,5,6. Begin with the two-request table from Section 2 of
the preceding report, with no overlap donors (e9=e12=0). The first baseline
request has size B, the second has size B-2u, and the residual endpoint support
has size at most p-2u.

Make two modifications:

1. Release u points of old four-bit type 0001 from D1 to neither request.
2. Transfer v=floor(u/2) points of old type 0010 from D1 to D2.

Both cells have size b, so the modifications are possible. A type-0010 point
can pair only with type 1101: these are the only supported old types whose
union with 0010 equals 1111. All type-1101 points belong to both requests.
Thus the transferred points remain isolated in the residual pair graph; this
modification creates no endpoints.

A type-0001 point can pair only with type 1110, whose points were already
eligible in the baseline residual graph. Releasing u such points therefore
adds at most u eligible endpoints and no other new endpoint class. The
residual endpoint support after both modifications is consequently at most

    p-2u+u = p-u < p.

The two request costs are

    D1: B-u-v = ceil(3k0/4),
    D2: B-2u+v <= B-u-v,

where the inequality is 2 floor(u/2)<=u. If tau(H) exceeded the larger cost,
actual edges avoiding both requests would exist. Together with the four old
rows they would have empty common intersection and fewer than p eligible
endpoints, contrary to the global endpoint hypothesis. QED.

The argument tracks actual surviving pairs, not just a formal incidence
estimate. It puts no restriction on response ranks or on new outside points;
the four old rows have empty common intersection, so an outside point cannot
participate in a piercing pair for those rows.

## Scope of the new interval

In the notation c=a+lambda*b, this proves the target throughout
2<=lambda<3. The balanced lambda=3 case is the parent's earlier two-request
lemma, with an additive constant. The triangle lemma in the earlier report
proves the target for lambda<=1. These arguments still leave the intervals
1<lambda<2 and 3<lambda<5 unresolved, except for any additional results proved
elsewhere. In particular this report does not close lambda=4.

The transfer of type0010 improves the originally proposed release-only range
lambda>=7/3 to lambda>=2. It costs no endpoints because the unique potential
partner belongs to both requests.

Two additional nonadaptive bad-seven request menus were explored at
a=33,b=1,c=37: four old rows with three requests, and a triangle of old rows
with four requests. Unrestricted numerical cell splitting returned cost 111
for each, compared with target 109.5. These computations are discovery evidence
only; no exact lower-bound certificate for either entire menu was extracted.
They do not obstruct adaptive requests or a full clean-profile theorem.

The exploratory commands were:

    python3 work/p644_clean_symmetric_two_request.py --a 33 --b 1 --c 37 --time 30 --requests 3 --old 2456 --endpoint-bound 0
    python3 work/p644_clean_symmetric_two_request.py --a 33 --b 1 --c 37 --time 30 --requests 4 --old 135 --endpoint-bound 0

## Exact finite check

Run:

    python3 -S work/p644_clean_profile_allocation_check.py

The extension checks the modified residual support and its formal coefficient
vector, and both request-size coefficient vectors. The exact hand proof above
then supplies the integer choice of u,v and the strict endpoint decrease.

No main-note edits were made by this agent.
