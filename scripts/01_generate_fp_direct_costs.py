#!/usr/bin/env python3
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN_FP1_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'fp' / 'costs_fp_1.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'fp' / 'costs_fp_1.csv',
]
IN_FP2_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'fp' / 'costs_fp_2.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'fp' / 'costs_fp_2.csv',
]
OUT_PNG = ROOT / 'output' / 'figures' / 'fp_direct_costs.png'

COST_COLORS = {
    'human_review_cost': '#5B8FF9',
    'complaint_review_cost': '#F4664A',
}


def _app_label(row: pd.Series) -> str:
    app = str(row['app']).strip()
    if app.lower() != 'human':
        return app

    rate = row.get('complaint_rate')
    try:
        rate = float(rate)
    except (TypeError, ValueError):
        return 'Human'

    if rate >= 0.245:
        return 'Human 25%'
    if rate <= 0.155:
        return 'Human 15%'
    return f'Human {rate:.2f}'


def _resolve_first(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of the input files exist: {paths}')


def main() -> int:
    fp1 = pd.read_csv(_resolve_first(IN_FP1_PATHS))
    fp2 = pd.read_csv(_resolve_first(IN_FP2_PATHS))

    fp1['name'] = fp1['name'].astype(str).str.strip()
    fp1['app'] = fp1['app'].astype(str).str.strip()
    fp2['name'] = fp2['name'].astype(str).str.strip()
    fp2['app'] = fp2['app'].astype(str).str.strip()

    direct_df = fp1.merge(fp2, on=['app', 'name'], how='inner')
    direct_df['app_label'] = direct_df.apply(_app_label, axis=1)

    app_order = ['Human 25%', 'Human 15%', 'Facebook', 'Instagram']
    extras = sorted([a for a in direct_df['app_label'].unique() if a not in app_order])
    apps = [a for a in app_order if a in direct_df['app_label'].unique()] + extras
    x_pos = {app: idx for idx, app in enumerate(apps)}

    unique_categories = sorted(direct_df['name'].dropna().astype(str).unique())
    marker_cycle = ['o', 's', '^', 'D', 'P', 'X']
    category_markers = {
        c: marker_cycle[i % len(marker_cycle)]
        for i, c in enumerate(unique_categories)
    }

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    for _, row in direct_df.iterrows():
        app = row['app_label']
        if app not in x_pos:
            continue

        marker = category_markers.get(str(row['name']), 'o')
        x = x_pos[app]
        for cost_col, color in COST_COLORS.items():
            y = float(row[cost_col])
            ax.scatter(
                x,
                y,
                color=color,
                marker=marker,
                s=80,
                edgecolors='white',
                linewidths=0.7,
                alpha=0.95,
            )

    ax.set_xticks([x_pos[a] for a in apps])
    ax.set_xticklabels(apps)
    ax.set_ylabel('Direct FP cost (EUR)')
    ax.set_title('Direct FP Costs by Category and App')
    ax.grid(True, axis='y', linewidth=0.5, alpha=0.25)

    cost_handles = [
        Line2D([0], [0], marker='o', color='none', markerfacecolor=COST_COLORS[k], markersize=8, label=k.replace('_', ' ').title())
        for k in COST_COLORS
    ]
    category_handles = [
        Line2D([0], [0], marker=category_markers[k], color='black', linestyle='None', markersize=7, label=k)
        for k in unique_categories
    ]
    ax.legend(handles=cost_handles + category_handles, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Wrote: {OUT_PNG}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
