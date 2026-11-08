import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _parse_ids(raw: str) -> set[int]:
    return {int(x) for x in raw.replace(" ", "").split(",") if x}


@dataclass(frozen=True)
class Config:
    tg_token: str = os.getenv("TG_TOKEN", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    llm_model: str = os.getenv("LLM_MODEL", "google/gemma-4-31b-it:free")
    system_prompt: str = os.getenv(
        "SYSTEM_PROMPT", "You are a helpful assistant. Answer concisely."
    )
    max_history: int = int(os.getenv("MAX_HISTORY", "20"))
    allowed_users: set[int] = field(
        default_factory=lambda: _parse_ids(os.getenv("ALLOWED_USERS", ""))
    )

    def validate(self) -> None:
        missing = [n for n in ("TG_TOKEN", "LLM_API_KEY") if not os.getenv(n)]
        if missing:
            raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")


config = Config()
