from collections import defaultdict


class DialogHistory:
    """In-memory per-user chat history, trimmed to the last N messages."""

    def __init__(self, max_messages: int):
        self._max = max_messages
        self._data: dict[int, list[dict]] = defaultdict(list)

    def get(self, user_id: int) -> list[dict]:
        return list(self._data[user_id])

    def add(self, user_id: int, role: str, content: str) -> None:
        msgs = self._data[user_id]
        msgs.append({"role": role, "content": content})
        if len(msgs) > self._max:
            del msgs[: len(msgs) - self._max]

    def clear(self, user_id: int) -> None:
        self._data.pop(user_id, None)
