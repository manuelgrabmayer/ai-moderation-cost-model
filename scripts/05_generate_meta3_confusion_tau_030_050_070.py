#!/usr/bin/env python3
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN_SUMMARY_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'confusion' / 'fpfn_ecm_summary.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'confusion' / 'fpfn_ecm_summary.csv',
]
OUT_PNG = ROOT / 'output' / 'figures' / 'meta3_confusion_matrices_tau_030_050_070.png'

TARGET_TAU_TRUE = 0.5
TARGET_TAU_PRED = [0.3, 0.5, 0.7]


def _row_for_tau(df: pd.DataFrame, tau: float) -> pd.Series:
    exact = df[np.isclose(df['tau_pred'], tau)]
    if exact.empty:
        raise ValueError(f'Missing META3_ANY row for tau_pred={tau}')
    return exact.iloc[0]


def _resolve_first(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of the input files exist: {paths}')


def main() -> int:
    df = pd.read_csv(_resolve_first(IN_SUMMARY_PATHS))
    df['tau_true'] = pd.to_numeric(df['tau_true'], errors='coerce')
    df['tau_pred'] = pd.to_numeric(df['tau_pred'], errors='coerce')

    sub = df[(df['category'] == 'META3_ANY') & (np.isclose(df['tau_true'], TARGET_TAU_TRUE))].copy()
    if sub.empty:
        raise ValueError('No META3_ANY rows found for tau_true=0.5.')

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))

    for ax, tau in zip(axes, TARGET_TAU_PRED):
        row = _row_for_tau(sub, tau)
        mat = np.array([[row['TN'], row['FP']], [row['FN'], row['TP']]], dtype=float)
        img = ax.imshow(mat, cmap='Blues')
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{int(mat[i, j]):,}", ha='center', va='center', color='black', fontsize=13)
        ax.set_xticks([0, 1], labels=['Pred 0', 'Pred 1'])
        ax.set_yticks([0, 1], labels=['True 0', 'True 1'])
        ax.set_title(f'tau = {tau:.2f}')

    fig.suptitle('META3_ANY: Confusion Matrices at Representative Thresholds', y=0.98)
    fig.tight_layout()

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Wrote: {OUT_PNG}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
