from characters.madridista import SYSTEM_PROMPT

from core.conversation import Conversation

from ollama import ResponseError

from providers.llm.ollama import generate_reply

MAX_HISTORY_TURNS = 15


def main() -> None:

    conversation = Conversation(SYSTEM_PROMPT)

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

        conversation.add_user_message(user_input)

        try:
            reply = generate_reply(conversation.messages)
        except (ConnectionError, ResponseError) as error:
            conversation.discard_pending_user_message()
            print(f"Could not get a reply: {error}")
            continue
        except KeyboardInterrupt:
            conversation.discard_pending_user_message()
            print("\nRequest interrupted. Exiting.")
            break
        if not reply.strip():
            conversation.discard_pending_user_message()
            print("The model returned an empty reply. Try again.")
            continue

        conversation.add_assistant_message(reply)

        conversation.trim_history(MAX_HISTORY_TURNS)

        print(f"Madridista: {reply}")

if __name__ == "__main__":
    main()