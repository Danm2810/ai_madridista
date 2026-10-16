from ai_madridista.characters.madridista import SYSTEM_PROMPT

from ollama import ResponseError

from ai_madridista.providers.llm.ollama import generate_reply

MAX_HISTORY_TURNS = 15


def main() -> None:
    messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
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

        try:
            reply = generate_reply(messages)
        except (ConnectionError, ResponseError) as error:
            messages.pop()
            print(f"Could not get a reply: {error}")
            continue
        except KeyboardInterrupt:
            messages.pop()
            print("\nRequest interrupted. Exiting.")
            break
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