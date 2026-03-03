#!/usr/bin/env python3
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN_CURVE_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'fp' / 'fp_indirect_curve.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'fp' / 'fp_indirect_curve.csv',
]
OUT_PNG = ROOT / 'output' / 'figures' / 'fp_indirect_cost.png'


def _resolve_first(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of the input files exist: {paths}')


def main() -> int:
    in_curve = _resolve_first(IN_CURVE_PATHS)
    df = pd.read_csv(in_curve)

    required = ['tau', 'volume_scenario', 's_fp', 'fp_total_cost_sample']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns in {in_curve.name}: {missing}')

    df['tau'] = pd.to_numeric(df['tau'], errors='coerce')
    df['s_fp'] = pd.to_numeric(df['s_fp'], errors='coerce')
    df['fp_total_cost_sample'] = pd.to_numeric(df['fp_total_cost_sample'], errors='coerce')
    df = df.dropna(subset=['tau', 'volume_scenario', 's_fp', 'fp_total_cost_sample']).copy()

    volumes = sorted(df['volume_scenario'].astype(str).unique())
    s_fp_values = sorted(df['s_fp'].unique())

    vol_palette = ['#5B8FF9', '#5AD8A6', '#F4664A']
    style_palette = ['-', '--', ':', '-.']
    vol_colors = {v: vol_palette[i % len(vol_palette)] for i, v in enumerate(volumes)}
    s_styles = {s: style_palette[i % len(style_palette)] for i, s in enumerate(s_fp_values)}

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    for (vol, s_fp), grp in df.groupby(['volume_scenario', 's_fp']):
        grp = grp.sort_values('tau')
        ax.plot(
            grp['tau'],
            grp['fp_total_cost_sample'],
            color=vol_colors.get(str(vol), 'black'),
            linestyle=s_styles.get(float(s_fp), '-'),
            linewidth=1.4,
            alpha=0.9,
        )

    ax.set_xlabel('Threshold (tau)')
    ax.set_ylabel('Indirect FP cost (EUR)')
    ax.set_title('Indirect FP Costs by Scenario')
    ax.grid(True, axis='y', linewidth=0.5, alpha=0.25)

    vol_handles = [Line2D([0], [0], color=vol_colors[v], lw=2, label=f'volume={v}') for v in volumes]
    s_handles = [Line2D([0], [0], color='black', lw=2, linestyle=s_styles[s], label=f's_fp={s:g}') for s in s_fp_values]
    ax.legend(handles=vol_handles + s_handles, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Wrote: {OUT_PNG}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
