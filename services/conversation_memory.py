from threading import Lock

class ConversationMemoryService:
    def __init__(self, max_turns: int = 5):
        self.max_messages = max_turns * 2
        self.conversations = {}
        self.lock = Lock()

    def get_history(self, conversation_id: str) -> list[dict]:
        with self.lock:
            return list(self.conversations.get(conversation_id, []))

    def add_exchange(
        self,
        conversation_id: str,
        question: str,
        answer: str
    ) -> None:
        with self.lock:
            history = self.conversations.setdefault(
                conversation_id, []
            )

            history.append({
                "role": "user",
                "content": question
            })

            history.append({
                "role": "assistant",
                "content": answer
            })

            self.conversations[conversation_id] = history[
                -self.max_messages:
            ]
