# P10 — source bath terminal and installed approach
Scope: the current `SOURCE_FIT207_COMPACT_PAIR` path only. The 18×20 pair and
one-unit branches are unchanged. The original P04 acceptance evidence at
`09403734568eecd9125284e610dd1163b41118a9` is a separate immutable version.

- In `source_fit_candidate207.py`, the bathroom terminal is tied to the
  placed bath origin by (+1.525 m, −0.5 m), and the source row group forbids
  dining overlap with each reserved apron piece. Rectangles and network
  points in its output are serialized by the producer with `round(...,6)`.
  Construction consumes the serialized decimal geometry via `F(str(x))`.
- P10 does not re-round, clamp, add an epsilon, or interpret the solver row
  residual as a placement tolerance. It checks exact decimal-token
  equality in the producer representation and preserves the separate
  binary64 equality observation, which can be false for the same decimal
  coordinate. P208 still owns the exact JSON/binary64 transport receipt.
- The pinned wet-room builder and installer reconstruct the expected A
  translation and B Y-reflection from the same proposal rectangle.
  Placement/module/port/opening/apron and installed standing activity
  identity are checked. Apron and the nominal 0.7 m body square must be
  contained in typed living/entry floor for this observation to align;
  dining intersection is checked separately. Stored activity endpoints,
  when present, must match the exact installed activity centres. This
  does not re-evaluate path traversal or override the original checker.
- The observation is retained separately in `bath_alignment_p10`, pinned
  with the original physical report and preconstruction fit report.
  Current completed-P04 readback rederives it from that same data.
  Geometric mismatch or unavailable input is an observed issue or UNKNOWN
  in the supplemental report, not a new architectural/admission rule.
  Rehashed tampering of the supplemental report is an evidence error.
- Tests use detached, source-built components and synthetic floors and
  destinations, with no optimizer or subprocess permitted by the P10
  fixtures. These tests do not establish fresh current whole-plan coverage,
  current quality, product readiness or admission.
