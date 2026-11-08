from functools import lru_cache

from openai import AsyncOpenAI

from src.config import config


@lru_cache(maxsize=1)
def _client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)


async def ask(messages: list[dict]) -> str:
    """Send the dialog to any OpenAI-compatible API and return the reply text."""
    resp = await _client().chat.completions.create(
        model=config.llm_model,
        messages=[{"role": "system", "content": config.system_prompt}, *messages],
    )
    return resp.choices[0].message.content or "(empty response)"
