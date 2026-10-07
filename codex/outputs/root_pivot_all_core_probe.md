# Direct request probes on the expanded actual support

Status: numerical discovery only. No new general upper bound, exact
infeasibility result, or impossibility theorem is claimed.

The root extended the six bounded models in
`agent_pivot_arbitrary_request_probe.md` to every empty-common retained
core containing the actual response G, with one, two, or three further
requests, at the same two deficit points. This specifically includes
cores in the row3-through6 replacements that leave the Fano-containing
class; the probe is not restricted to the row1 pivot.

The seven available actual rows are the six focused rows and G, with
a=33b,c=37b,k=146b. G takes both full selected defect classes123,124,
has no outside points, and has deficits(1,1,1,1)b or(2,2,0,0)b in
the four A classes235,246,145,136. The original global endpoint lower
bound is111b. The requested endpoint upper bound is110.999b, and the
target maximum request size is109.5b.

For q requests the retained core contains G and5-q old rows. The old
membership types met by G are235,246,145,136,123,124. A retained core
has a common point exactly when its old row set is contained in one
of those six types. Thus the allowed choices number15 for q=1,
14 for q=2, and2 for q=3, per deficit vector:62 models in total.
All request codes and all continuous splits are allowed. There is
no minimum positive-cell mass. The prescribed endpoint saving0.001b
is an output constraint, not an occupancy cutoff.

| A deficits/b | Requests | Cores | Smallest reported maximum request/b |
|---|---:|---:|---:|
|(1,1,1,1)|1|15|112.001|
|(1,1,1,1)|2|14|110.5005|
|(1,1,1,1)|3|2|111.0003333333|
|(2,2,0,0)|1|15|112.001|
|(2,2,0,0)|2|14|110.0005|
|(2,2,0,0)|3|2|111.0003333333|

All62 solves completed normally with reported matching numerical dual
bounds. None supplied an allocation at109.5b. Existing six-model
outputs were reused; only the additional56 models were solved. Each
new model had a20- or30-second limit, and all completed before it.

The model constrains the endpoint support allowed by the requests.
It does not constrain the ranks or additional incidences of actual
future response edges. Its negative numerical outcome therefore
does not rule out arguments exploiting those ranks, adaptive requests,
cores with common points and a separately controlled outside part,
other deficit vectors, or other actual G traces. It also does not
exclude a strict endpoint saving smaller than0.001b. No floating-point
optimum is promoted to an exact lower certificate.

Reproduction and cached-result aggregation:

```
python3 work/p644_pivot_arbitrary_core_batch.py
```

The batch program preserves and reuses existing per-model JSON outputs.
The full aggregate is `outputs/root_pivot_arbitrary_core_batch.json`.
The underlying discovery program is
`work/p644_pivot_arbitrary_request_discover.py`; the root added the
one-request option to the same formulation. All processes completed.
