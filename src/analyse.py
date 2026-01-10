import matplotlib.pyplot as plt
import pandas as pd


def visualise(data):
    histogram(data, "JIGSAW_obscene", "OPENAI_sexual")


def histogram(data, columnA, columnB):
    print(f"ColumnA ({columnA}) size = {(data[columnA].count(),)}")
    print(
        f"ColumnB ({columnB}) size = {(data[columnB].count(),)}"
    )  # Output: ColumnB (OPENAI_sexual) size = (2000,)

    plt.title("Histogram")

    # plt.hist(
    #    [data[columnA], data[columnB]],
    #    bins=1,
    #    label=["JIGSAW", "OPENAI"],
    #    color=["green", "red"],
    # )

    plt.hist(data[columnB], bins=1, color="green")  # Columns add up to 30

    plt.show()
