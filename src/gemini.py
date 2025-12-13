from google import genai


def queryGemini(model, endpoint):
    if model == "" or endpoint == "":
        raise RuntimeError("Invalid query parameters")

    sys_prompt = """
        You are a content moderator.
        Classify messages from 0.0 to 1.0 based on how toxic they are. 1.0 being most toxic.
        Return only json.
    """

    config = genai.types.GenerateContentConfig(system_instruction=sys_prompt)

    client = genai.Client(api_key=endpoint)

    response = client.models.generate_content(
        model=model, contents="You are stupid", config=config
    )
    print(response.text)
    printMetadata(response)


def printMetadata(response):
    tokens_used = response.usage_metadata.total_token_count
    print(f"Tokens used: {tokens_used}")
