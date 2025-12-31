## Repository for Python scripts used in a seminar thesis for Security and Privacy Economics (IN0014, IN2107, IN2396, IN4892), TUM, Winter 25/26

### Authors: Manuel Grabmayer, Matias Häkkinen

In this project, we conduct tests on the [Jigsaw dataset](https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/data/).

The goal is to have the messages re-scored by a few AI tools currently available in the market and compare the results to human scores provided in the dataset.

A small example dataset is provided with the repository. (Taken from train.csv)

### Setup:

Dependencies are listed in requirements.txt. Install with pip:
```
pip install -r requirements.txt
```

Api keys should be provided in a .env file. Only supported provider is OpenAI.

In .env:
```
OPENAI_API_KEY="..."
```

Run the program with command:
```
python3 src/main.py <task>
```

Run config is stored in config.json.

Available tasks:
  score: Read datafile and send it to specified provider for scoring. Store result in cache file.
  analyse: Prints a part of the cache file. In future, use this task to perform analysis without scoring.
  test: Sanity check
