import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

def visualise(results):
    plt.plot(results["Threshold"], results["FPR"], lw=2, color='red', label='False Positive Rate')
    plt.plot(results["Threshold"], results["FNR"], lw=2, color='blue', label='False Negative Rate')
    plt.legend()
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
