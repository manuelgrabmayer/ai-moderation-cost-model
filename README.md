## Repository for Python scripts used in a seminar thesis for Security and Privacy Economics (IN0014, IN2107, IN2396, IN4892), TUM, Winter 25/26

### Authors: Manuel Grabmayer, Matias Häkkinen

In this project, we conduct tests on the [Jigsaw dataset](https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/data/).

The goal is to have the messages relabeled by a few AI tools currently available in the market and compare the results to human labels provided in the dataset.

A small example dataset is provided with the repository. (Taken from train.csv)

### Setup:

Dependencies are listed in requirements.txt. Install with pip:
```
pip install -r requirements.txt
```

Api keys should be provided in a .env file. Only supported provider is Google Gemini.

In .env:
```
GEMINI_API_KEY="..."
```
