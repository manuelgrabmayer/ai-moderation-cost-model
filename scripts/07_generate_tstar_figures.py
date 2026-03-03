#!/usr/bin/env python3
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN_TSTAR_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'tstar' / 'tstar_by_scenario.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'tstar' / 'tstar_by_scenario.csv',
]
OUT_DIR = ROOT / 'output' / 'figures'
OUT_HIST = OUT_DIR / 'fig_tstar_hist.png'


def sanitize_filename(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]+', '_', str(s)).strip('_').lower()


def _format_axis_vals(vals: list[float]) -> list[str]:
    labels: list[str] = []
    for v in vals:
        if pd.isna(v):
            labels.append('NA')
        else:
            labels.append(f"{float(v):.3f}".rstrip('0').rstrip('.'))
    return labels


def _resolve_first(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of the input files exist: {paths}')


def make_histogram(df: pd.DataFrame) -> None:
    counts = df['t_star'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.bar(counts.index.astype(float), counts.values, width=0.008, color='#4C78A8', edgecolor='white')
    ax.set_title('Distribution of optimal thresholds across scenarios', fontsize=12)
    ax.set_xlabel('Optimal threshold t*')
    ax.set_ylabel('Count of scenarios')
    ax.grid(axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT_HIST, dpi=300, bbox_inches='tight')
    plt.close(fig)


def make_setup_heatmaps(df: pd.DataFrame) -> list[Path]:
    produced: list[Path] = []
    if 'setup' not in df.columns or df['setup'].isna().all():
        return produced

    work = df.copy()
    work['s_fp'] = pd.to_numeric(work['s_fp'], errors='coerce')
    work['s_fn'] = pd.to_numeric(work['s_fn'], errors='coerce')
    work['t_star'] = pd.to_numeric(work['t_star'], errors='coerce')
    work = work.dropna(subset=['setup', 's_fp', 's_fn', 't_star'])

    for setup in sorted(work['setup'].astype(str).unique()):
        sub = work[work['setup'].astype(str) == setup]
        if sub.empty:
            continue

        x_vals = sorted(sub['s_fp'].unique().tolist())
        y_vals = sorted(sub['s_fn'].unique().tolist())
        pivot = sub.pivot_table(index='s_fn', columns='s_fp', values='t_star', aggfunc='median')
        pivot = pivot.reindex(index=y_vals, columns=x_vals)
        mat = pivot.to_numpy(dtype=float)

        fig, ax = plt.subplots(figsize=(6.2, 4.8))
        im = ax.imshow(mat, aspect='auto', origin='lower', cmap='viridis')
        ax.set_xticks(range(len(x_vals)), labels=_format_axis_vals(x_vals))
        ax.set_yticks(range(len(y_vals)), labels=_format_axis_vals(y_vals))
        ax.set_xlabel('s_fp')
        ax.set_ylabel('s_fn')
        ax.set_title(f'Median t* by s_fp and s_fn (setup={setup})', fontsize=11)

        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = mat[i, j]
                if np.isfinite(v):
                    ax.text(j, i, f'{v:.2f}', ha='center', va='center', color='white', fontsize=8)

        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('median t*')
        fig.tight_layout()

        out_path = OUT_DIR / f"fig_tstar_heatmap_setup_{sanitize_filename(setup)}.png"
        fig.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        produced.append(out_path)

    return produced


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(_resolve_first(IN_TSTAR_PATHS))

    make_histogram(df)
    setup_files = make_setup_heatmaps(df)

    print(f'Wrote: {OUT_HIST}')
    for p in setup_files:
        print(f'Wrote: {p}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
