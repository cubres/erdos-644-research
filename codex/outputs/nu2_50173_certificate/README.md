# Local proof bundle: a two-anchor (7,2) family

Theorem: for k=140000m the explicit family in THEOREM.md has matching number 2 and transversal number 100346m+2. This is a partial construction, not a resolution of Erdős Problem 644 or a novelty claim.

Run from this directory on macOS ARM64:

```sh
python3 -B -S p644_agent_audit_anchor_check.py --ethos proof_checkers/ethos-0.2.4/ethos --signatures proof_checkers/cvc5-1.4.0-signatures/cpc
```

The checker requires only Python standard library and the included Ethos binary/signatures. It reconstructs the mathematical input, binds the proof assumptions, and checks the contradiction. On another platform supply an appropriate Ethos 0.2.4 binary using --ethos. The included mathematical input and CPC proof are platform independent.

The generation scripts are included for provenance. Their original configured solver/dependency paths are local to the research environment; they are not needed to replay this bundle. MANIFEST.json records SHA256 hashes for every supplied file. No external application or publication is modified by replay.
