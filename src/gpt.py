import statistics

import pandas as pd
from openai import OpenAI

pd.options.display.float_format = "{:.6f}".format


def formatOutput(output):
    scores = output.category_scores.model_dump()
    return statistics.mean(scores.values())


def executeQuery(client, input):
    results = client.moderations.create(
        model="omni-moderation-latest", input=input
    ).results

    return [formatOutput(r) for r in results]


def queryOpenAI(endpoint, input, batches, limit):
    client = OpenAI(api_key=endpoint)

    ids = input["id"]
    messages = input["comment_text"]
    scores = executeQuery(client, messages.tolist())
    joined = pd.DataFrame({"id": ids.tolist(), "score": scores})

    return joined
