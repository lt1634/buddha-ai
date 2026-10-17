"""In-memory conversation and crisis state."""

from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict


class SessionStore:
    """Per-user conversation history, crisis round count, and model choice."""

    def __init__(self, default_model: str) -> None:
        self.conversations: DefaultDict[int, list[dict[str, str]]] = defaultdict(list)
        self.crisis_rounds: DefaultDict[int, int] = defaultdict(int)
        self.user_models: DefaultDict[int, str] = defaultdict(lambda: default_model)
        self._default_model = default_model

    def clear(self, user_id: int) -> None:
        """Reset conversation history and crisis counter for *user_id*."""
        self.conversations[user_id] = []
        self.crisis_rounds[user_id] = 0

    def reset_model(self, user_id: int) -> None:
        """Restore default model for *user_id*."""
        self.user_models[user_id] = self._default_model
