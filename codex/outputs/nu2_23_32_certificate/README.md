# Local proof bundle: a two-anchor family with limiting coefficient 23/32

Theorem: for every n>=1 the explicit family in THEOREM.md has rank k=28000n, matching number2, and transversal number20125n-54=(23/32)k-54. This is a partial construction, not a resolution of Erdős Problem644 or a novelty claim.

Run from this directory on macOS ARM64:

```sh
python3 -B -S p644_agent_audit_anchor_parametric_check.py --ethos proof_checkers/ethos-0.2.4/ethos --signatures proof_checkers/cvc5-1.4.0-signatures/cpc
```

The independent checker uses only Python standard library and the included Ethos binary/signatures. It reconstructs225 symbolic-q mathematical assertions, binds the225 proof assumptions, and checks the contradiction. On another platform supply an appropriate Ethos0.2.4 executable with --ethos. The SMT input and CPC proof are platform independent.

The generation scripts are included for provenance. Their original configured solver/dependency paths are local to the research environment; generation is not required for replay. MANIFEST.json records SHA256 hashes for all supplied files. No external application or publication is modified.
