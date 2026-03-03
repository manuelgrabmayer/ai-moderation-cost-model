#!/usr/bin/env python3
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
IN_POINTS_PATHS = [
    ROOT / 'output' / 'files' / 'figure_generation_sources' / 'roc' / 'curve_points_tau_true_0p5.csv',
    ROOT / 'input' / 'figure_generation_sources' / 'roc' / 'curve_points_tau_true_0p5.csv',
]
OUT_ROC = ROOT / 'output' / 'figures' / 'roc_tau_true_05.png'
OUT_PR = ROOT / 'output' / 'figures' / 'pr_tau_true_05.png'


def _plot_roc(df: pd.DataFrame) -> None:
    categories = ['BULLYING_HARASSMENT', 'HATEFUL_CONDUCT', 'VIOLENCE_INCITEMENT', 'META3_ANY']
    fig, ax = plt.subplots(figsize=(8, 6))

    for cat in categories:
        sub = df[df['category'] == cat].copy().sort_values('FPR')
        fpr = sub['FPR'].to_numpy()
        tpr = sub['TPR'].to_numpy()
        m = np.isfinite(fpr) & np.isfinite(tpr)
        fpr = fpr[m]
        tpr = tpr[m]
        auc = np.trapezoid(tpr, fpr) if len(fpr) else np.nan
        label = f'{cat} (AUC={auc:.3f})' if np.isfinite(auc) else cat
        ax.plot(fpr, tpr, label=label)

    ax.plot([0, 1], [0, 1], 'k--', label='chance')
    ax.set_xlabel('False Positive Rate (FPR)')
    ax.set_ylabel('True Positive Rate (TPR)')
    ax.set_title('ROC curves (tau_true=0.5)')
    ax.legend(loc='lower right')

    OUT_ROC.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_ROC, dpi=300, bbox_inches='tight')
    plt.close(fig)


def _plot_pr(df: pd.DataFrame) -> None:
    categories = ['BULLYING_HARASSMENT', 'HATEFUL_CONDUCT', 'VIOLENCE_INCITEMENT', 'META3_ANY']
    fig, ax = plt.subplots(figsize=(8, 6))

    for cat in categories:
        sub = df[df['category'] == cat].copy().sort_values('Recall')
        recall = sub['Recall'].to_numpy()
        precision = sub['Precision'].to_numpy()
        m = np.isfinite(recall) & np.isfinite(precision)
        recall = recall[m]
        precision = precision[m]
        base = sub['prevalence'].iloc[0] if len(sub) else np.nan
        label = f'{cat} (base={base:.3f})' if np.isfinite(base) else cat
        ax.plot(recall, precision, label=label)

    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_title('Precision-Recall curves (tau_true=0.5)')
    ax.legend(loc='best')

    OUT_PR.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_PR, dpi=300, bbox_inches='tight')
    plt.close(fig)


def _resolve_first(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f'None of the input files exist: {paths}')


def main() -> int:
    df = pd.read_csv(_resolve_first(IN_POINTS_PATHS))
    _plot_roc(df)
    _plot_pr(df)
    print(f'Wrote: {OUT_ROC}')
    print(f'Wrote: {OUT_PR}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
