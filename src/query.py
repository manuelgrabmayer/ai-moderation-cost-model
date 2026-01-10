import pandas as pd
from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError,
)

# from fetch import safeFetch

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
    totalBatches = len(batches)
    batchNum = 1
    try:
        for batch in batches:
            print(f"Scoring batch ({batchNum}/{totalBatches})")
            result = queryBatch(client, batch)
            scored.append(result)
            batchNum += 1
    except RETRYABLE_ERRORS as e:
        print(f"Error {e} raised. {len(scored)} / {totalBatches} batches completed.")

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
    # results = safeFetch(executeQuery, RETRYABLE_ERRORS, client, messages.tolist())
    results = executeQuery(client, messages.tolist())
    scores = pd.DataFrame([formatOutput(r) for r in results])
    concat = pd.concat(
        [ids.reset_index(drop=True), scores.reset_index(drop=True)], axis=1
    )
    return concat


def formatOutput(output):
    scores = output.category_scores.model_dump()
    # return max(scores.values())
    return scores


def executeQuery(client, input):
    response = client.moderations.create(model="omni-moderation-latest", input=input)

    return response.results


def executeQuery2(client, input):
    # Call with raw response to ensure headers are captured
    raw = client.moderations.with_raw_response.create(
        model="omni-moderation-latest", input=input
    )

    # 1. Use the .http_response object directly (this is the most reliable way)
    headers = raw.http_response.headers

    # 2. Extract specific headers
    limit_requests = headers.get("x-ratelimit-limit-requests")
    limit_tokens = headers.get("x-ratelimit-limit-tokens")
    remaining_req = headers.get("x-ratelimit-remaining-requests")

    print(f"Request Limit: {limit_requests}")
    print(f"Token Limit: {limit_tokens}")
    print(f"Remaining: {remaining_req}")

    # Return the parsed data
    return raw.parse().results
