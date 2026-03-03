import pandas as pd

inPath = "data/full/data-jigsaw.csv"
outPath = "data/random-sample/data-jigsaw-random-100k.csv"
sampleSize = 100000

data = pd.read_csv(inPath)

sample = data.sample(n=sampleSize)

sample.to_csv(outPath)
