from ollama import ResponseError, chat
MAX_HISTORY_TURNS = 15


def main() -> None:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a passionate Real Madrid fan having casual "
                "football banter with a friend. Reply directly to their "
                "latest message in one or two short sentences. "
                "No lists, headings, or alternative answers."
            ),
        },
    ]

    print("AI Madridista — type /quit to exit.")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHala Madrid!")
            break

        if user_input.lower() == "/quit":
            print("Hala Madrid!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        request = dict(
            model="gemma4:e4b",
            messages=messages,
            think=False,
            options={
                "num_ctx": 4096,
                "num_predict": 100,
            },
        )

        try:
            response = chat(**request)
        except (ConnectionError, ResponseError) as error:
            messages.pop()
            print(f"Could not get a reply: {error}")
            continue
        except KeyboardInterrupt:
            messages.pop()
            print("\nRequest interrupted. Exiting.")
            break
        reply = response.message.content or ""

        if not reply.strip():
            messages.pop()
            print("The model returned an empty reply. Try again.")
            continue

        messages.append({"role": "assistant", "content": reply})
        # Keep the system instructions and recent complete exchanges.
        history_limit = MAX_HISTORY_TURNS * 2

        if len(messages) > 1 + history_limit:
            messages = [messages[0]] + messages[-history_limit:]

        print(f"Madridista: {reply}")

if __name__ == "__main__":
    main()