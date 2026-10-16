import json

from time import perf_counter

from ollama import chat


def main() -> None:
    print("Connecting to Gemma...")

    request = dict(
        model="gemma4:e4b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a passionate Real Madrid fan having casual "
                    "football banter with a friend. Reply in one or two "
                    "short sentences. No lists, headings, or alternative answers."
                ),
            },
            {
                "role": "user",
                "content": "Barcelona is better than Real Madrid.",
            },
        ],
        think=False,
        options={
            "num_ctx": 4096,
            "num_predict": 100,
        },
    )

    print("\n--- Request to Ollama ---")
    print(json.dumps(request, indent=2, ensure_ascii=False))
    print("--- End request ---\n", flush=True)
    
    started = perf_counter()
    response = chat(**request)

    print(f"\nMadridista: {response.message.content}")
    print(f"\nResponse time: {perf_counter() - started:.1f} seconds")


if __name__ == "__main__":
    main()