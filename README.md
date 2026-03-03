# Figure Generation Pipeline (Minimal)

This repo follows the following order:

- generated CSV files: `output/files/figure_generation_sources/...`
- figure PNG outputs: `output/figures/...`
- scripts: `scripts/01` to `scripts/18`

## How the CSV files are calculated (provenance)

Each file below is generated in the full project `Coding - cost parameters /Cost parameters` by the listed Python script, then staged into this minimal repo by the local staging scripts.

- `output/files/figure_generation_sources/fp/costs_fp_1.csv`
  - full-project generator: `FP/Calculation_FP_Meta.py`
  - local staging: `scripts/13_generate_costs_fp_1.py`

- `output/files/figure_generation_sources/fp/costs_fp_2.csv`
  - full-project generator: `FP/Calculation_FP_Meta.py`
  - local staging: `scripts/14_generate_costs_fp_2.py`

- `output/files/figure_generation_sources/fn/costs_fn_1.csv`
  - full-project generator: `FN/False_negative_costs.py`
  - local staging: `scripts/15_generate_costs_fn_1.py`

- `output/files/figure_generation_sources/fn/threshold_calibration_results.csv`
  - full-project generator: `FN/FN_X_Shock.py`
  - local staging: `scripts/16_generate_threshold_calibration_results.py`

- `output/files/figure_generation_sources/confusion/fpfn_ecm_summary.csv`
  - full-project generator: `FP_FN_ROC_calculation.py`
  - local staging: `scripts/17_generate_fpfn_ecm_summary.py`

- `output/files/figure_generation_sources/ecm/all_ecm_costs_all_scenarios.csv`
  - full-project generator used for matching data: `Final_combined/all_ecm_compute_by_category.py`
  - local staging: `scripts/18_generate_all_ecm_costs_all_scenarios.py`

- `output/files/figure_generation_sources/fn/FN_per_Fn.csv`
  - full-project generator: `FN/FN_per_fn_export.py`
  - local staging: `scripts/09_generate_fn_per_fn.py`

- `output/files/figure_generation_sources/roc/curve_points_tau_true_0p5.csv`
  - full-project generator: `ROC_Calculations/compute_curve_points.py`
  - local staging: `scripts/10_generate_curve_points_tau_true_0p5.py`

- `output/files/figure_generation_sources/fp/fp_indirect_curve.csv`
  - full-project generator: `run_paper_pipeline.py` (`build_fp_indirect_curve`)
  - local staging: `scripts/11_generate_fp_indirect_curve.py`

- `output/files/figure_generation_sources/tstar/tstar_by_scenario.csv`
  - full-project generator: `robustness/run_robustness.py`
  - local staging: `scripts/12_generate_tstar_by_scenario.py`

## Figure scripts

- `scripts/01_generate_fp_direct_costs.py`
- `scripts/02_generate_fn_costs.py`
- `scripts/03_generate_fp_indirect_cost.py`
- `scripts/04_generate_roc_pr_tau_true_05.py`
- `scripts/05_generate_meta3_confusion_tau_030_050_070.py`
- `scripts/06_generate_all_ecm_combined_scenarios.py`
- `scripts/07_generate_tstar_figures.py`

These figure scripts read from `output/files/figure_generation_sources/...` first.

## Run everything

```bash
python3 scripts/08_run_all_figures.py
```

`08` runs staging scripts (`09`-`18`) first, then figure scripts (`01`-`07`).

## Output figures

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
