import pandas as pd
from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError,
)


def formatOutput(output):
    scores = output.category_scores.model_dump()
    return max(scores.values())


# Potential async method
def queryBatch(client, input):
    ids = input["id"]
    messages = input["comment_text"]

    # Actual query
    results = executeQuery(client, messages.tolist())
    scores = [formatOutput(r) for r in results]

    ids = input["id"]
    joined = pd.DataFrame({"id": ids.tolist(), "score": scores})
    return joined


def queryOpenAI(endpoint, input, batchSize, cacheFile=None):
    client = OpenAI(api_key=endpoint)

    batches = [input.iloc[i : i + batchSize] for i in range(0, len(input), batchSize)]

    scored = []

    try:
        for batch in batches:
            result = queryBatch(client, batch)
            scored.append(result)
    except RETRYABLE_ERRORS as e:
        print(f"Error {e} raised. {len(scored)} / {len(batches)} batches completed.")

    joined = pd.concat(scored, axis=0)

    if cacheFile:
        joined.to_csv("cache/results.csv", index=False, float_format="%.6f")

    return joined


RETRYABLE_ERRORS = (
    RateLimitError,
    APIConnectionError,
    InternalServerError,
    APITimeoutError,
)


def executeQuery(client, input):
    return client.moderations.create(
        model="omni-moderation-latest", input=input
    ).results
