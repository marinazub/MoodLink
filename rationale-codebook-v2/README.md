# Codebook revision 2 — 2026-10-07

This revision distinguishes assignment/abstention actions (D01), critic challenges (R01), and standalone questions (Q01). U is retired. Unchanged interpretation codes use the completed independent coder B application, including systematic A01 coding. New R01 judgments were manually reviewed; this is not a new independent coding run.

- [Codebook](Codebook.md)
- [Aggregate findings](Findings.md)
- [Machine-readable definitions](codebook_definitions.json)
- [Aggregate counts](aggregate_results.json)

The earlier agreement and Cohen’s kappa apply to version 1 only. Independent and human validation of version 2 remain pending.

## Code and restricted inputs

`revise.py` assembles the revised coding, `build.mjs` authors the Excel workbook using @oai/artifact-tool, and `verify.py` checks exact evidence against the source workbook using openpyxl. Manual coding judgments are inputs, not automatically recreated by these scripts. Published code omits case-specific worked examples from its report template. Public definitions also omit case anchors.

Full reproduction requires restricted local inputs: version 1 analysis.json; rationale_cases.json and coder_B.json; action_metadata.json; critic_review.json; and critic_candidates.json. Raw rationales, case-level coding, reviewer packets, source workbooks and these restricted inputs are not included. Scripts retain the local analysis directory layout and source-workbook provenance path; adapt paths before running elsewhere. Place the revision scripts and restricted inputs in outputs/rationale-revision-20261007 beneath the project root, with the existing outputs/rationale-only-codebook-20261006 and rationale-codebook-validation directories beside it.

Run `python3 revise.py`, `node build.mjs`, then `python3 verify.py` from the revision directory after restoring those inputs. The published repository alone cannot reproduce the full case analysis.

The local combined workbook additionally contains GPT6_vs_Medgemma_NoMatch (104 units, 194 assignment rows) and Medgemma_vs_GPT6_NoMatch (17 units, 44 assignment rows). One unit in the latter has a mixed core/outcome record rather than exclusive abstention. Those evidence-bearing workbooks remain local.
