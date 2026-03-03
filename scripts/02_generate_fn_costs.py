#!/usr/bin/env python3
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN_DIRECT_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'fn' / 'costs_fn_1.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'fn' / 'costs_fn_1.csv',
]
IN_FN_PER_FN_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'fn' / 'FN_per_Fn.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'fn' / 'FN_per_Fn.csv',
]
IN_THRESH_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'fn' / 'threshold_calibration_results.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'fn' / 'threshold_calibration_results.csv',
]
OUT_DIRECT = ROOT / 'output' / 'figures' / 'fn_direct_costs.png'
OUT_INDIRECT = ROOT / 'output' / 'figures' / 'fn_indirect_costs.png'

PROACTIVE_RATE_SCENARIOS = [0.50, 0.625]
TIME_PER_REVIEW_HOURS = 0.005
HOURLY_WAGE_EUR = 33.5
DIRECT_COLOR = '#5B8FF9'


def _marker_map(values: list[str]) -> dict[str, str]:
    cycle = ['o', 's', '^', 'D', 'P', 'X']
    return {v: cycle[i % len(cycle)] for i, v in enumerate(sorted(values))}


def _resolve_first(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of the input files exist: {paths}')


def plot_direct() -> None:
    df = pd.read_csv(_resolve_first(IN_DIRECT_PATHS))
    df['name'] = df['name'].astype(str).str.strip()
    df['app'] = df['app'].astype(str).str.strip()

    has_proactive = df['app'].str.startswith('Proactive').any()
    if not has_proactive:
        categories = sorted(df['name'].unique())
        rows = []
        for rate in PROACTIVE_RATE_SCENARIOS:
            scenario_cost = (1.0 - rate) * TIME_PER_REVIEW_HOURS * HOURLY_WAGE_EUR
            label = f'Proactive {rate * 100:.1f}%'
            for name in categories:
                rows.append({'app': label, 'name': name, 'complaint_review_cost': scenario_cost})
        df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

    app_order = ['Proactive 50.0%', 'Proactive 62.5%', 'Facebook', 'Instagram']
    extras = sorted([a for a in df['app'].unique() if a not in app_order])
    apps = [a for a in app_order if a in df['app'].unique()] + extras
    x_pos = {app: idx for idx, app in enumerate(apps)}
    category_markers = _marker_map(sorted(df['name'].unique()))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    for _, row in df.iterrows():
        app = row['app']
        if app not in x_pos:
            continue
        ax.scatter(
            x_pos[app],
            float(row['complaint_review_cost']),
            color=DIRECT_COLOR,
            marker=category_markers.get(str(row['name']), 'o'),
            s=80,
            edgecolors='white',
            linewidths=0.7,
            alpha=0.95,
        )

    ax.set_xticks([x_pos[a] for a in apps])
    ax.set_xticklabels(apps)
    ax.set_ylabel('Direct FN cost (EUR)')
    ax.set_title('Direct FN Costs by Category and App')
    ax.grid(True, axis='y', linewidth=0.5, alpha=0.25)

    cost_handles = [Line2D([0], [0], marker='o', color='none', markerfacecolor=DIRECT_COLOR, markersize=8, label='Direct FN cost')]
    category_handles = [
        Line2D([0], [0], marker=category_markers[k], color='black', linestyle='None', markersize=7, label=k)
        for k in sorted(category_markers)
    ]
    ax.legend(handles=cost_handles + category_handles, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)

    OUT_DIRECT.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_DIRECT, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plot_indirect() -> None:
    fn_curve = pd.read_csv(_resolve_first(IN_FN_PER_FN_PATHS))[['tau', 'volume_scenario', 'scenario_s_fn', 'eur_per_FN']]
    thresh = pd.read_csv(_resolve_first(IN_THRESH_PATHS))[['tau', 'FN']]

    for col in ['tau', 'scenario_s_fn', 'eur_per_FN']:
        fn_curve[col] = pd.to_numeric(fn_curve[col], errors='coerce')
    for col in ['tau', 'FN']:
        thresh[col] = pd.to_numeric(thresh[col], errors='coerce')

    fn_curve = fn_curve.dropna(subset=['tau', 'volume_scenario', 'scenario_s_fn', 'eur_per_FN'])
    thresh = thresh.dropna(subset=['tau', 'FN'])

    merged = fn_curve.merge(thresh, on='tau', how='inner')
    merged['indirect_fn_cost'] = merged['FN'] * merged['eur_per_FN']

    volumes = sorted(merged['volume_scenario'].unique())
    scenarios = sorted(merged['scenario_s_fn'].unique())
    vol_palette = ['#5B8FF9', '#5AD8A6', '#F4664A']
    style_palette = ['-', '--', ':', '-.']
    vol_colors = {vol: vol_palette[i % len(vol_palette)] for i, vol in enumerate(volumes)}
    scen_styles = {scen: style_palette[i % len(style_palette)] for i, scen in enumerate(scenarios)}

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    for (vol, scen), grp in merged.groupby(['volume_scenario', 'scenario_s_fn']):
        grp = grp.sort_values('tau')
        ax.plot(
            grp['tau'],
            grp['indirect_fn_cost'],
            color=vol_colors.get(vol, 'black'),
            linestyle=scen_styles.get(scen, '-'),
            linewidth=1.4,
            alpha=0.9,
        )

    ax.set_xlabel('Threshold (tau)')
    ax.set_ylabel('Indirect FN cost (EUR)')
    ax.set_title('Indirect FN Costs by Scenario')
    ax.grid(True, axis='y', linewidth=0.5, alpha=0.25)

    vol_handles = [Line2D([0], [0], color=vol_colors[v], lw=2, label=f'volume={v}') for v in volumes]
    scen_handles = [Line2D([0], [0], color='black', lw=2, linestyle=scen_styles[s], label=f's_fn={s:g}') for s in scenarios]
    ax.legend(handles=vol_handles + scen_handles, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)

    OUT_INDIRECT.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_INDIRECT, dpi=300, bbox_inches='tight')
    plt.close(fig)


def main() -> int:
    plot_direct()
    plot_indirect()
    print(f'Wrote: {OUT_DIRECT}')
    print(f'Wrote: {OUT_INDIRECT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
