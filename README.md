# gpt_telegram_bot

A minimal Telegram bot that turns a chat with the bot into a conversation with an LLM.
Works with **any OpenAI-compatible API**: OpenRouter, OpenAI, DeepSeek, Groq, Google Gemini, local Ollama, and more.

## Features

- Per-user dialog memory (the bot remembers the context of the conversation)
- `/reset` to clear the history
- Optional user whitelist so strangers don't burn your API credits
- Long answers are split automatically (Telegram's 4096-char limit)
- Configured entirely through environment variables
- Runs with one command via Docker Compose

## Project structure

```
gpt_telegram_bot/
├── src/
│   ├── __init__.py
│   ├── main.py          # entry point: bot + dispatcher setup
│   ├── config.py        # env-based configuration
│   ├── handlers.py      # Telegram command and message handlers
│   ├── llm.py           # OpenAI-compatible LLM client
│   └── history.py       # in-memory per-user dialog history
├── .env.example         # configuration template
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## How it works

```
User → Telegram → bot (aiogram) → LLM API → bot → User
```

LLM APIs are stateless, so on every message the bot sends the last `MAX_HISTORY` messages
of the dialog together with the system prompt.

## Quick start

### 1. Get the tokens

- **Telegram:** message [@BotFather](https://t.me/BotFather), run `/newbot`, copy the token.
- **LLM API key:** the default config uses [OpenRouter](https://openrouter.ai/keys).
  It offers free models (ids ending in `:free`) and a single key gives access to GPT, Claude, Gemini, Llama and others.

### 2. Configure

```bash
cp .env.example .env
# then fill in TG_TOKEN and LLM_API_KEY
```

| Variable        | Required | Default                          | Description                                    |
|-----------------|----------|----------------------------------|------------------------------------------------|
| `TG_TOKEN`      | yes      | —                                | Telegram bot token                             |
| `LLM_API_KEY`   | yes      | —                                | API key of the LLM provider                    |
| `LLM_BASE_URL`  | no       | `https://openrouter.ai/api/v1`   | OpenAI-compatible endpoint                     |
| `LLM_MODEL`     | no       | `google/gemma-4-31b-it:free`     | Model id                                       |
| `SYSTEM_PROMPT` | no       | `You are a helpful assistant...` | System prompt                                  |
| `MAX_HISTORY`   | no       | `20`                             | Messages kept per user                         |
| `ALLOWED_USERS` | no       | empty (everyone)                 | Comma-separated Telegram user IDs              |

### 3. Run

**Docker (recommended):**

```bash
docker compose up -d --build
docker compose logs -f
```

**Locally:**

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

## Switching providers

Only `LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL` need to change:

| Provider   | `LLM_BASE_URL`                                              | Example `LLM_MODEL`          |
|------------|-------------------------------------------------------------|------------------------------|
| OpenRouter | `https://openrouter.ai/api/v1`                              | `openai/gpt-4o-mini`         |
| OpenAI     | `https://api.openai.com/v1`                                 | `gpt-4o-mini`                |
| DeepSeek   | `https://api.deepseek.com`                                  | `deepseek-chat`              |
| Groq       | `https://api.groq.com/openai/v1`                            | `llama-3.3-70b-versatile`    |
| Gemini     | `https://generativelanguage.googleapis.com/v1beta/openai/`  | `gemini-2.5-flash`           |
| Ollama     | `http://host.docker.internal:11434/v1`                      | `llama3.1`                   |

## Commands

| Command  | Description                 |
|----------|-----------------------------|
| `/start` | Greeting and current model  |
| `/reset` | Clear the dialog history    |
