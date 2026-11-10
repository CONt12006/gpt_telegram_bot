<p align="center">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/English-555555?style=for-the-badge"></a>
  <a href="README.ru.md"><img alt="Русский" src="https://img.shields.io/badge/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-1f6feb?style=for-the-badge"></a>
</p>

# gpt_telegram_bot

Минималистичный Telegram-бот, который превращает переписку с ботом в диалог с LLM.
Работает с **любым OpenAI-совместимым API**: OpenRouter, OpenAI, DeepSeek, Groq, Google Gemini, локальная Ollama и другие.

## Возможности

- Память диалога для каждого пользователя (бот помнит контекст разговора)
- `/reset` очищает историю
- Необязательный белый список пользователей, чтобы чужие не тратили твои API-кредиты
- Длинные ответы автоматически разбиваются на части (лимит Telegram 4096 символов)
- Вся настройка через переменные окружения
- Запуск одной командой через Docker Compose

## Структура проекта

```
gpt_telegram_bot/
├── src/
│   ├── __init__.py
│   ├── main.py          # точка входа: настройка бота и диспетчера
│   ├── config.py        # конфигурация из переменных окружения
│   ├── handlers.py      # обработчики команд и сообщений Telegram
│   ├── llm.py           # клиент OpenAI-совместимого LLM API
│   └── history.py       # история диалога каждого пользователя в памяти
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── README.ru.md
```

## Как это работает

```
Пользователь → Telegram → бот (aiogram) → LLM API → бот → Пользователь
```

LLM API не хранят состояние, поэтому с каждым сообщением бот отправляет последние `MAX_HISTORY` сообщений
диалога вместе с системным промптом.

## Быстрый старт

### 1. Получи токены

- **Telegram:** напиши [@BotFather](https://t.me/BotFather), выполни `/newbot`, скопируй токен.
- **Ключ LLM API:** конфигурация по умолчанию использует [OpenRouter](https://openrouter.ai/keys).
  Там есть бесплатные модели (id заканчивается на `:free`), а один ключ даёт доступ к GPT, Claude, Gemini, Llama и другим.

### 2. Настройка

Создай файл `.env` в корне проекта:

```env
TG_TOKEN=your_telegram_bot_token
LLM_API_KEY=your_llm_api_key
```

В тот же файл можно добавить необязательные переменные:

| Переменная      | Обязательна | По умолчанию                     | Описание                                       |
|-----------------|-------------|----------------------------------|------------------------------------------------|
| `TG_TOKEN`      | да          | —                                | Токен Telegram-бота                            |
| `LLM_API_KEY`   | да          | —                                | API-ключ провайдера LLM                        |
| `LLM_BASE_URL`  | нет         | `https://openrouter.ai/api/v1`   | OpenAI-совместимый эндпоинт                    |
| `LLM_MODEL`     | нет         | `google/gemma-4-31b-it:free`     | Id модели                                      |
| `SYSTEM_PROMPT` | нет         | `You are a helpful assistant...` | Системный промпт                               |
| `MAX_HISTORY`   | нет         | `20`                             | Сколько сообщений хранить на пользователя      |
| `ALLOWED_USERS` | нет         | пусто (все)                      | Telegram ID пользователей через запятую        |

### 3. Запуск

**Docker (рекомендуется):**

```bash
docker compose up -d --build
docker compose logs -f
```

**Локально:**

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

## Смена провайдера

Достаточно поменять `LLM_BASE_URL`, `LLM_API_KEY` и `LLM_MODEL`:

| Провайдер  | `LLM_BASE_URL`                                              | Пример `LLM_MODEL`           |
|------------|-------------------------------------------------------------|------------------------------|
| OpenRouter | `https://openrouter.ai/api/v1`                              | `openai/gpt-4o-mini`         |
| OpenAI     | `https://api.openai.com/v1`                                 | `gpt-4o-mini`                |
| DeepSeek   | `https://api.deepseek.com`                                  | `deepseek-chat`              |
| Groq       | `https://api.groq.com/openai/v1`                            | `llama-3.3-70b-versatile`    |
| Gemini     | `https://generativelanguage.googleapis.com/v1beta/openai/`  | `gemini-2.5-flash`           |
| Ollama     | `http://host.docker.internal:11434/v1`                      | `llama3.1`                   |

## Команды

| Команда  | Описание                         |
|----------|----------------------------------|
| `/start` | Приветствие и текущая модель     |
| `/reset` | Очистить историю диалога         |
