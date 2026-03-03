# Repository for Privacy Economics Cost Modeling and Moderation Analysis

## Authors
Manuel Grabmayer, Matias Hakkinen

This repository now contains two complementary workflows:

- AI moderation scoring and analysis on the Jigsaw dataset.
- Figure-generation pipeline for direct and indirect cost analysis outputs.

## Moderation scoring workflow

Project context: seminar thesis for Security and Privacy Economics (IN0014, IN2107, IN2396, IN4892), TUM, Winter 25/26.

Run setup:

```bash
pip install -r requirements.txt
```

Create `.env` with API credentials:

```bash
OPENAI_API_KEY="..."
```

Run:

```bash
python3 src/main.py <task>
```

Configuration lives in `config.json`.

Available tasks:
- `score`: read data and send to configured provider for scoring.
- `analyse`: inspect cached scoring results.
- `test`: sanity-check run.

## Figure-generation pipeline

Pipeline order:
- generated CSV files: `output/files/figure_generation_sources/...`
- figure PNG outputs: `output/figures/...`
- scripts: `scripts/01` to `scripts/18`

Each figure-generation source file is staged by `scripts/09` to `scripts/18`, then consumed by figure scripts `scripts/01` to `scripts/07`.

Run all figure generation:

```bash
python3 scripts/08_run_all_figures.py
```

`08` runs staging scripts (`09`-`18`) first, then figure scripts (`01`-`07`).

Primary output figures:
- `all_ecm_combined_scenarios.png`
- `fig_tstar_heatmap_setup_all_policies_weighted.png`
- `fig_tstar_hist.png`
- `fn_direct_costs.png`
- `fn_indirect_costs.png`
- `fp_direct_costs.png`
- `fp_indirect_cost.png`
- `pr_tau_true_05.png`
- `roc_tau_true_05.png`
- `meta3_confusion_matrices_tau_030_050_070.png`
