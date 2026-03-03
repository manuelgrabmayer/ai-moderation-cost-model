#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / 'scripts'
OUT_DIR = ROOT / 'output' / 'figures'
CACHE_DIR = Path('/tmp/cost_parameters_mpl_cache')

SCRIPTS = [
    '13_generate_costs_fp_1.py',
    '14_generate_costs_fp_2.py',
    '15_generate_costs_fn_1.py',
    '16_generate_threshold_calibration_results.py',
    '17_generate_fpfn_ecm_summary.py',
    '18_generate_all_ecm_costs_all_scenarios.py',
    '09_generate_fn_per_fn.py',
    '10_generate_curve_points_tau_true_0p5.py',
    '11_generate_fp_indirect_curve.py',
    '12_generate_tstar_by_scenario.py',
    '01_generate_fp_direct_costs.py',
    '02_generate_fn_costs.py',
    '03_generate_fp_indirect_cost.py',
    '04_generate_roc_pr_tau_true_05.py',
    '05_generate_meta3_confusion_tau_030_050_070.py',
    '06_generate_all_ecm_combined_scenarios.py',
    '07_generate_tstar_figures.py',
]

EXPECTED = [
    'all_ecm_combined_scenarios.png',
    'fig_tstar_hist.png',
    'fn_direct_costs.png',
    'fn_indirect_costs.png',
    'fp_direct_costs.png',
    'fp_indirect_cost.png',
    'pr_tau_true_05.png',
    'roc_tau_true_05.png',
    'meta3_confusion_matrices_tau_030_050_070.png',
]


def main() -> int:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault('MPLCONFIGDIR', str(CACHE_DIR))

    for script in SCRIPTS:
        path = SCRIPTS_DIR / script
        print(f'Running: {path.name}')
        subprocess.run([sys.executable, str(path)], check=True, env=env)

    print('\nExpected outputs:')
    for name in EXPECTED:
        p = OUT_DIR / name
        print(f' - {name}: {"OK" if p.exists() else "MISSING"}')

    heatmaps = sorted(OUT_DIR.glob('fig_tstar_heatmap_setup_*.png'))
    print(f' - fig_tstar_heatmap_setup_*.png: {len(heatmaps)} file(s)')
    for p in heatmaps:
        print(f'   -> {p.name}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
