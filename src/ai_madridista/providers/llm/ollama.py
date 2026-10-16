from ollama import chat

from ai_madridista.config import MODEL, NUM_CTX, NUM_PREDICT

def generate_reply(messages: list[dict[str, str]]) -> str:
    request = dict(
        model=MODEL,
        messages=messages,
        think=False,
        options={
            "num_ctx": NUM_CTX,
            "num_predict": NUM_PREDICT,
        },
    )

    response = chat(**request)
    return response.message.content or ""