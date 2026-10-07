# Bounded arbitrary-code request probe after the full-S pivot

**Outcome: no allocation at the target budget 109.5b was found in the
six bounded models below.** These are numerical discovery results only,
not exact lower bounds or impossibility certificates. They do not repeat
the fixed-table menu: every request code and arbitrary cell splitting
were allowed.

The actual family used for the projections consists of the original six
focused rows together with G. Here a=33b,c=37b,k=146b; G contains all of
both selected defect classes123 and124, has no outside points, and its
four A deficits are ordered as235,246,145,136. All seven actual rows have
rank146b. The two tested normalized deficit vectors are(1,1,1,1) and
(2,2,0,0).

All retained cores in the table have empty common intersection. For each
core, the model includes every request code: four codes for two requests,
eight codes for three. Support flags obey only an upper implication
`mass <= cell_capacity * flag`; there is **no minimum positive-cell
mass or occupancy cutoff**. Endpoint flags and masses account for every
pair whose old masks cover the core and whose request codes are disjoint.

The numerical endpoint upper bound was110.999b, a reduction of0.001b
from the ORIGINAL global lower bound111b. This fixed requested reduction
is an output constraint, not a restriction on positive support. The
model minimizes the largest request size.

| Deficits | Retained actual rows | Requests | Reported best budget/b |
|---|---|---:|---:|
| (1,1,1,1) | F2,F4,F5,G | 2 | 110.5005 |
| (2,2,0,0) | F2,F4,F5,G | 2 | 110.0005 |
| (1,1,1,1) | F3,F4,G | 3 | 111.0003333333 |
| (2,2,0,0) | F3,F4,G | 3 | 111.0003333333 |
| (1,1,1,1) | F5,F6,G | 3 | 112.3336666667 |
| (1,1,1,1) | F3,F4,F5,G | 2 | 110.5005 |

Each solve completed normally with a reported matching numerical dual
bound, in approximately one second or less, within its60-second limit.
No target-budget result was obtained to promote to an exact rational
request certificate or a positive parameter-region theorem.

This probe does not exhaust the choices of actual cores, all deficit
vectors, adaptive allocations, or rank-sensitive constraints on the new
response edges. It also does not rule out an allocation that only attains
a smaller strict endpoint reduction than0.001b. Numerical optima and
dual bounds are not used to assert any of those wider conclusions.

## Reproduction

The discovery program is
`work/p644_pivot_arbitrary_request_discover.py`. For example:

```
python3 work/p644_pivot_arbitrary_request_discover.py --deficits 2,2,0,0 --core 245G --requests 2 --time 60
```

The other five invocations are given by the parameter rows above, with
core strings245G,34G,56G,345G and the corresponding request count.
Outputs retain the complete numerical allocations in files matching
`outputs/agent_pivot_arbitrary_<deficits>_<core>_<requests>.json`.

The bounded task is finished. No search process remains running, and no
main-note edit was made.
