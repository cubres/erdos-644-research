# Three-part two-box theorem without intersectingness

Theorem 7.73 in the adjacent research note proves that a continuous type-closed family given by two sliced boxes over three parts, with transversal coefficient above 3/4, contains a bad seven-tuple. It does not solve the unrestricted problem.

```sh
python3 -B -S p644_three_part_general_certificate_check.py
```

The replay checks the earlier thirteen intersecting cases, then thirteen mixed-disjoint cases. Mathematical inputs are independently reconstructed, every proof assumption is matched, and standalone Ethos verifies the CPC inference proofs. The U and V construction certificates are checked rationally. The note supplies the hand reductions and other explicit constructions.

The bundled Ethos executable is for macOS arm64. Use --ethos with an Ethos 0.2.4 executable on another platform. The original checker signatures, licenses and provenance remain in the intersecting subdirectory. No SMT solver is required for replay. Rational witnesses scale to suitable integer multiples; no uniform finite bound for all three-part box families is asserted here.

The discovery program is included for provenance; its supporting research modules are in the working directory. It is unnecessary for replay. Nothing has been published. External review and a comprehensive priority check remain outstanding.
