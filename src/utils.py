import pandas as pd
from dotenv import dotenv_values


def helloworld():
    print("Hello world!")


def setup():
    # Loading environment variables
    config = dotenv_values(".env")

    gemini_endpoint = config.get("GEMINI_API_KEY")
    if gemini_endpoint is None or gemini_endpoint == "":
        raise RuntimeError("Gemini endpoint MISSING")

    print("Gemini endpoint FOUND")

    return gemini_endpoint


def readCSV(path):
    df = pd.read_csv(path)

    messages = df[["id", "comment_text"]]
    targets = df[["id", "target"]]

    return messages, targets


def readCache(path):
    return pd.read_json(path)


def analysis(results, targets):
    res = pd.merge(results, targets, how="inner", on="id")
    print(res)
