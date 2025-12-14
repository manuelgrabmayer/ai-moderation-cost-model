from google import genai


def queryGemini(model, endpoint, data):
    if model == "" or endpoint == "":
        raise RuntimeError("Invalid query parameters")

    sys_prompt = """
        You are a content moderator.
        Classify messages from 0.0 to 1.0 based on how toxic they are. 1.0 being most toxic.
        You will get the messages as a python list with a ',' delimiter
        Return only json(message,toxicity).
    """

    config = genai.types.GenerateContentConfig(
        system_instruction=sys_prompt, response_mime_type="application/json"
    )

    client = genai.Client(api_key=endpoint)

    print("Executing Gemini query")
    response = client.models.generate_content(model=model, contents=data, config=config)
    print("Query successful")
    printMetadata(response)


def printMetadata(response):
    tokens_used = response.usage_metadata.total_token_count
    print(f"Tokens used: {tokens_used}")
