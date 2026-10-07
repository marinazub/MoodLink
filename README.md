# MoodLink

Study of LLM capabilities for CFIR coding.

## Rationale codebook and reliability analysis

Analysis of GPT-6 and MedGemma explanations, restricted to rationale, critic_rationale, and critic_coverage_rationale across five comparison categories.

- [Codebook definitions](rationale-codebook-validation/protocol/codebook_definitions.json)
- [Independent-agent agreement report](rationale-codebook-validation/reports/Agreement_report.md)
- [Code and reproduction requirements](rationale-codebook-validation/README.md)
- [Per-code agreement](rationale-codebook-validation/reports/per_code.csv)
- [Agreement by category](rationale-codebook-validation/reports/by_category.csv)

| Comparison | Agreement | Cohen κ |
|---|---:|---:|
| All 21 codes, all 259 cases | 93.0% | 0.704 |
| M01–M15, all 259 cases | 94.2% | 0.694 |
| M01–M15, 137 paired-model cases | 92.1% | 0.686 |

The primary paired-model comparison has 73.1% positive agreement. Ratings distinguish documented mechanisms from unclear evidence; shared unclear ratings contribute to overall agreement. The report details the original iterative coding, blinded independent-agent recoding, code-level limitations and bootstrap interval.

A blinded human-validation sample of 70 cases has been prepared locally. Human validation is pending. This publication includes code and aggregate results; underlying evidence, case-level coding, reviewer workbooks and coordinator keys remain local.
