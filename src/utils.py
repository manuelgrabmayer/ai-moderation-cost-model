import json
import sys

import pandas as pd
from dotenv import dotenv_values


def readConfig(path):
    with open(path, "r") as f:
        config = json.load(f)

    return config["Provider"], config["Model"], config["Data"], config["Cache"]


def readArgs(availableTasks):
    args = sys.argv

    print(f"Available tasks: {availableTasks}")

    if len(args) != 2:
        print("Usage: python3 src/main.py <task>")
        raise RuntimeError("No task specified!")

    task = args[1].lower()
    if task not in availableTasks:
        raise RuntimeError("Invalid task!")

    return task


def resolveEndpoints(envPath, targetProvider):
    # MAKE SURE NOT TO PRINT SECRETS
    env = dotenv_values(envPath)
    pattern = "_API_KEY"
    endpointsDict = {
        key.removesuffix(pattern): value
        for key, value in env.items()
        if key.endswith(pattern)
    }
    providers = list(endpointsDict.keys())

    print("Available endpoints:")
    if not providers:
        raise RuntimeError("No provider endpoints configured")

    print(providers)

    if targetProvider not in providers:
        raise RuntimeError(
            f'Endpoint for provider is missing. In {envPath}: {targetProvider}{pattern}="<API_KEY>"'
        )

    return endpointsDict[targetProvider]


def readAndSeparateData(path):
    df = pd.read_csv(path)

    messages = df[["id", "comment_text"]]

    targets = df[
        [
            "id",
            "comment_text",
            "target",
            "severe_toxicity",
            "obscene",
            "identity_attack",
            "insult",
            "threat",
        ]
    ].copy()

    targets.rename(
        inplace=True,
        columns=lambda column: "JIGSAW_" + column
        if (column != "id") and (column != "comment_text")
        else column,
    )

    return messages, targets


def mergeAndCache(results, targets, cache=None, cacheFile=None):
    merged = pd.merge(targets, results, how="inner", on="id")
    if cache is not None:
        merged = pd.concat([cache, merged], axis=0)
    merged = merged.round(6)
    if cacheFile is not None:
        merged.to_csv(cacheFile, index=False)
    return merged


def readCache(path):
    return pd.read_csv(path)


def fetchData(dataPath, rowLimit, cachePath=None):
    data = pd.read_csv(dataPath)
    cache = None

    startIdx = 0
    if cachePath is not None:
        try:
            cache = pd.read_csv(cachePath)
            cacheLen = len(cache)
        except FileNotFoundError as e:
            print("Cache file does not exist. Starting from beginning")
            cacheLen = 0

        if cacheLen < len(data):
            print(f"Continuing scoring from cache (startIndex = {cacheLen})")
            startIdx = cacheLen
        else:
            print("Data has already been fully scored.")
            return None, None
    else:
        print("Starting scoring from beginning (startIndex = 0)")

    data = data[startIdx : startIdx + rowLimit]

    return data, cache


def separateData(data):
    messages = data[["id", "comment_text"]]

    targets = data[
        [
            "id",
            "comment_text",
            "target",
            "severe_toxicity",
            "obscene",
            "identity_attack",
            "insult",
            "threat",
        ]
    ].copy()

    targets.rename(
        inplace=True,
        columns=lambda column: "JIGSAW_" + column
        if (column != "id") and (column != "comment_text")
        else column,
    )

    return messages, targets


def verifyCacheIntegrity(dataPath, cachePath):
    data = pd.read_csv(dataPath)
    cache = pd.read_csv(cachePath)

    cacheLen = len(cache)
    dataLen = len(data)

    print(
        f"Comparing original dataset (length = {dataLen}) to cache (length = {cacheLen})"
    )

    if cacheLen > dataLen:
        raise RuntimeError("Original data cannot be shorter than cache!")

    ids = data.head(cacheLen)["id"]
    cacheIds = cache["id"]

    if ids.equals(cacheIds):
        if cacheLen == dataLen:
            print("Cache and Original data match completely")
        else:
            print(f"Cache and Original data match up to cache length = {cacheLen}")
    else:
        raise RuntimeError(
            f"Cache does not match with original data up to cache length = {cacheLen}"
        )

    print("Verifying that no entries are missing from cache columns")

    failures = [column for column in cache.columns if cache[column].count() != cacheLen]
    if not failures:
        print("No values are missing from cache columns")
    else:
        raise RuntimeError(f"Values missing from cache columns ({failures})")

    return True


def analysis(results, targets):
    res = pd.merge(targets, results, how="inner", on="id")
    print(res)
