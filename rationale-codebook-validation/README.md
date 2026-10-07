# Rationale codebook: code and aggregate reliability results

Published materials include the 21-code definitions, analysis/sampling/workbook scripts, and aggregate independent-agent reliability results. Underlying rationale records, individual coding/evidence, reviewer assignments, completed/blank evidence workbooks, and coordinator/model keys remain local and are not included in this public package.

## Results

See [Agreement report](reports/Agreement_report.md), [per-code table](reports/per_code.csv), and [category table](reports/by_category.csv). These describe 259 cases and 892 assignment rows. Agreement is computed on documented yes versus unclear, not proven presence versus absence. Human validation is pending.

## Running the code

```sh
python3 scripts/test_reliability.py
```

The core statistics use Python's standard library. Optional XLSX reading requires `requirements.txt`; workbook creation requires the Codex-provided `@oai/artifact-tool` runtime.

Full reproduction requires the privately retained inputs in their original layout:

- `data/rationale_cases.json`: whitelist source extract.
- `coding/coder_A.json`, `coding/coder_A_evidence.json`, `coding/coder_B.json`: frozen coder judgments and evidence.
- `protocol/manifest.json`: source provenance for artifact verification.
- Human scoring additionally requires `human_validation/coordinator_key.csv` and completed responses.

Once those authorized local inputs are supplied, run `python3 scripts/reliability.py` to reproduce the reported scores. The source fields are restricted to rationale, critic_rationale and critic_coverage_rationale. Never replace missing human ratings with unclear.

The scripts generate detailed local outputs; inspect them before any future publication. The aggregate results here are pre-adjudication. A separate agent is not a human validator or necessarily a different model family.
