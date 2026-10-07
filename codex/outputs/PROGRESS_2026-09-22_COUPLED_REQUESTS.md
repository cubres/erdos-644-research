# Coupled-request progress checkpoint, 22 September 2026

The general three-quarter upper bound remains unproved. The main positive
result of this continuation is a complete conditional theorem for the
symmetric near-Fano defect support, together with a reusable multiple-
avoidance lemma. No public posting was made.

For globally endpoint-minimizing six rows with base class size a and
defect class size b, the theorem gives

    tau(H) <= 3a + ceil((21b+1)/2).

At a=33b the previous endpoint cover was111b and this gives109.5b+O(1).
The desired bound is108b+O(1). This halves the linear excess for this
particular configuration; it is not a claim that half the general proof
has been completed or that the general coefficient has improved.

New forward branches were tested against actual responses. One sparse
response forces a108b+1 cover. Dense responses survive two requests,
including a request that forbids all shared outside points. A third
request can eliminate the entire common part of the first two responses
and produce a good triple on exactly7r/4 points; explicit responses still
preserve all six- and seven-row tests. These are local obstructions, not
families with transversal number above the target.

The private-edge route was also narrowed precisely. Complete pair traces
with a common outside defender can encode an arbitrary original instance
at a cost of two rank units. A parity benchmark realizes a globally
minimum endpoint cover and persistent common defenses, but only constant
excess over3k/4. A further exact construction supplies every private-edge
obligation for the near-Fano endpoint cover while retaining transversal
number3. Thus true high-transversal avoidance obligations remain essential.

The parent ran each of these NEW exact checkers and reviewed the new proof arguments:

- `work/p644_near_fano_two_request_certificate.py`: symbolic request costs
  and strict endpoint decrease giving the positive conditional theorem.
- `work/p644_near_fano_two_replacements_check.py`: cyclic nine-row survivor,
  all84 six-row and36 seven-row tests, exact transversal number3.
- `work/p644_near_fano_optimized_response_check.py`: sparse closing branch,
  dense actual two-response survivor, and5,266,432 exact partial-support
  checks for twelve new five-row graphs.
- `work/p644_private_response_barrier.py`: actual extension with all private
  edges,162 exact graph computations and the hand reduction for arbitrarily
  many private edges.
- `work/p644_near_fano_outside_control_check.py`: actual two-response
  survivor with disjoint outside parts.
- `work/p644_second_request_linear_obligations.py`:51,264 whole-cell requests
  reduce to two exact inequalities, whose stated relaxation has minimum
  required response mass b.
- `work/p644_two_request_gap_obstructions.py`: the closest115b-endpoint
  tuples cannot pay their4b gap using the entire repair support.
- `work/p644_near_fano_third_response_check.py`: balanced third response,
  all210 six-row and120 seven-row tests for every even b>=2.
- `work/p644_near_fano_third_outside_free_check.py`: the stronger third
  response with no outside points, valid for every integer b>=1.
- `work/p644_third_request_seven_robust.py`: EVERY37b deletion from M=B union E preserves the seven-row property
  for the explicit complement response. The certificate was extended
  once to this larger domain after its initial E-only statement.

All completed runs returned PASS or EXACT_PASS. Numerical search failures
for later neighborhood profiles are recorded as discovery only. No old
fixed-five-row obstruction or old general6/7 certificate was rerun.

The bounded universal third-request question is now completed for the
exclusive region E=G triangle H. The compact exact checker
`work/p644_third_complement_endpoint_bound.py` proves that every partial
37b deletion in E leaves every new six-tuple with at least139b endpoints.
It checks100 no-major-deletion cases and400 one-major-deletion cases;
26 common-point cases follow directly from the response rank.

Allowing the deletion to enter the protected35b region B gives a concrete
request defeating the fixed-R complement: a new six-tuple has104b
endpoints. This forces every actual response to use at least one point
of the previously omitted8b region R. However, one point suffices.
`work/p644_third_request_singleton_repair_check.py` proves that exchanging
one retained point for one R-point repairs every new constraint for all
integer b>=1. The critical endpoint count becomes142b+1, because the
single point activates38b neighbors. This checker only verifies the126
new six-row and84 new seven-row subfamilies; it inherits the unchanged
nine-row certificate.

Both new scripts passed. All bounded agent assignments are complete and
no root-owned background job remains. The research goal remains ACTIVE.
The full3/4 theorem is still open in these notes. The next real gap is a
global high-transversal argument controlling such small response incidences;
the local tests above do not prove that high-transversal extensions exist.
