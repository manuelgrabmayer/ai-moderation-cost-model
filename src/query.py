import pandas as pd
from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError,
)

from fetch import safeFetch

RETRYABLE_ERRORS = (
    RateLimitError,
    APIConnectionError,
    InternalServerError,
    APITimeoutError,
)


def queryOpenAI(endpoint, input, batchSize):
    client = OpenAI(api_key=endpoint)

    batches = [input.iloc[i : i + batchSize] for i in range(0, len(input), batchSize)]

    scored = []

    try:
        for batch in batches:
            result = queryBatch(client, batch)
            scored.append(result)
    except RETRYABLE_ERRORS as e:
        print(f"Error {e} raised. {len(scored)} / {len(batches)} batches completed.")

    full = pd.concat(scored, axis=0)
    full.rename(
        inplace=True,
        columns=lambda column: "OPENAI_" + column if column != "id" else column,
    )

    return full


def queryBatch(client, input):
    ids = input["id"]
    messages = input["comment_text"]

    # Actual query
    results = safeFetch(executeQuery, RETRYABLE_ERRORS, client, messages.tolist())
    scores = pd.DataFrame([formatOutput(r) for r in results])

    concat = pd.concat([ids, scores], axis=1)
    return concat


def formatOutput(output):
    scores = output.category_scores.model_dump()
    # return max(scores.values())
    return scores


def executeQuery(client, input):
    return client.moderations.create(
        model="omni-moderation-latest", input=input
    ).results
