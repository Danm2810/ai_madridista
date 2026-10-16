class Conversation:
    def __init__(self, system_prompt: str) -> None:
        self.messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]
    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def discard_pending_user_message(self) -> None:
        if self.messages[-1]["role"] == "user":
            self.messages.pop()

    def trim_history(self, max_turns: int) -> None:
        history_limit = max_turns * 2

        if len(self.messages) > 1 + history_limit:
            self.messages[:] = (
                [self.messages[0]] + self.messages[-history_limit:]
            )