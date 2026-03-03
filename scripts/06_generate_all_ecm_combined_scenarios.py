#!/usr/bin/env python3
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN_ECM_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'ecm' / 'all_ecm_costs_all_scenarios.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'ecm' / 'all_ecm_costs_all_scenarios.csv',
]
OUT_PNG = ROOT / 'output' / 'figures' / 'all_ecm_combined_scenarios.png'

SCENARIO_COLS = ['app', 'policy_area', 'volume_scenario', 'scenario_s_fp', 'scenario_s_fn']
X_COL = 'tau'
Y_COL = 'ecm_total_cost'


def _resolve_first(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of the input files exist: {paths}')


def main() -> int:
    in_ecm = _resolve_first(IN_ECM_PATHS)
    df = pd.read_csv(in_ecm)

    required = SCENARIO_COLS + [X_COL, Y_COL]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns in {in_ecm.name}: {missing}')

    df[X_COL] = pd.to_numeric(df[X_COL], errors='coerce')
    df[Y_COL] = pd.to_numeric(df[Y_COL], errors='coerce')
    df = df.dropna(subset=[X_COL, Y_COL]).sort_values(X_COL)

    fig, ax = plt.subplots(figsize=(12, 7))

    for _, grp in df.groupby(SCENARIO_COLS):
        ax.plot(grp[X_COL], grp[Y_COL], color='black', alpha=0.12, linewidth=0.5)

    median = df.groupby(X_COL, as_index=False)[Y_COL].median()
    ax.plot(median[X_COL], median[Y_COL], color='red', linewidth=2.4, label='Median across scenarios')

    ax.set_title('ECM Cost Across All Scenarios')
    ax.set_xlabel('Threshold (tau)')
    ax.set_ylabel('ECM total cost (EUR, log scale)')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.25)
    ax.legend(loc='best')

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Wrote: {OUT_PNG}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
