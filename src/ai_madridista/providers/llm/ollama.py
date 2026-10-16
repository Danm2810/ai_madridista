from ollama import chat


def generate_reply(messages: list[dict[str, str]]) -> str:
    request = dict(
        model="gemma4:e4b",
        messages=messages,
        think=False,
        options={
            "num_ctx": 4096,
            "num_predict": 100,
        },
    )

    response = chat(**request)
    return response.message.content or ""