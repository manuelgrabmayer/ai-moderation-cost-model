import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from numpy.polynomial import Polynomial

def visualise(results):

    figure, axis = plt.subplots(figsize=(10, 6))

    thresholds = results["Threshold"]
    fpr = results["FPR"]
    fpr[0] = fpr[1]
    fnr = results["FNR"]

    poly_fpr = Polynomial.fit(thresholds,fpr,3)
    poly_fnr = Polynomial.fit(thresholds,fnr,3)

    poly_fpr_points = poly_fpr(thresholds)
    poly_fnr_points = poly_fnr(thresholds)

    print(f"FPR Polynomial: {poly_fpr}")
    print(f"FPR Polynomial: {poly_fnr}")

    data_lines = [
        axis.plot(thresholds, fpr, lw=2, color='red', label='False Positive Rate (FPR)')[0],
        axis.plot(thresholds, fnr, lw=2, color='blue', label='False Negative Rate (FNR)')[0],
        axis.plot(thresholds, poly_fpr_points, lw=2, color='maroon', label='FPR Polynomial')[0],
        axis.plot(thresholds, poly_fnr_points, lw=2, color='navy', label='FNR Polynomial')[0],
    ]

    legend = axis.legend(loc='upper center', fancybox=True, shadow=True)

    legend_lines = legend.get_lines()

    line_dict = {}

    # Building dict
    for d_line, l_line in zip(data_lines, legend_lines):
        l_line.set_picker(10)
        line_dict[l_line] = d_line

    def on_pick(event):
        l_line = event.artist
        d_line = line_dict[l_line]
        # print(f"Pick event: {d_line}")

        visible = not d_line.get_visible()
        d_line.set_visible(visible)
        l_line.set_alpha(1.0 if visible else 0.2)
        figure.canvas.draw()

    figure.canvas.mpl_connect('pick_event', on_pick)

    plt.show()

def threshold(target,model,thresholdCount):
    thresholds = np.linspace(0,1,thresholdCount)
    target = np.array(target)
    model = np.array(model)

    results = []

    for t in thresholds:
        target_above = target >= t
        model_above = model >= t

        tp = np.sum(target_above & model_above)
        tn = np.sum(~target_above & ~model_above)
        fp = np.sum(~target_above & model_above)
        fn = np.sum(target_above & ~model_above)

        results.append({"Threshold": t, "TP": tp, "TN": tn, "FP": fp, "FN": fn})

    return pd.DataFrame(results)
