import csv

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


def readCSV(path, limit):
    data = []
    with open(path, mode="r") as file:
        csvFile = csv.DictReader(file)
        i = 0
        for line in csvFile:
            if i > limit:
                break

            data.append(line["comment_text"])
            i += 1

    return data
