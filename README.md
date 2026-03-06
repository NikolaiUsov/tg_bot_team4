## Телеграм-чат-бот «Геральт — гид по миру Ведьмака»

### Описание
Чат-бот в Telegram, который отвечает **в стиле Геральта из Ривии** и **только по тематике мира «Ведьмака»**.  
Перед генерацией ответа бот использует RAG: находит релевантные фрагменты в локальной базе знаний и добавляет их в промпт (контекст), чтобы ответы были точнее.

### Использованные технологии
- **Python**
- **Telegram Bot API**: `telebot` 
- **LLM**: OpenAI через LangChain (`langchain_openai`)
- **RAG / векторный поиск**: ChromaDB (`chromadb`)
- **Эмбеддинги**: `sentence-transformers` (в коде: `cointegrated/rubert-tiny2`)
- **Разбиение текста**: `langchain_text_splitters`
- **Переменные окружения**: `python-dotenv` (в коде импортируется как `dotenv`)

### Требования
- **Python 3.10+**
- Файл **`.env`** в корне проекта со следующими переменными:
  - `BOT_TOKEN` — токен Telegram-бота
  - `OPENROUTER_API_KEY` — ключ OpenRouter (получить на [OpenRouter](https://openrouter.ai/))
- **`Файл базы знаний`** в корне проекта  
  Он читается в `rag.py` и используется для построения коллекции в ChromaDB.

### Установка
В PowerShell (Windows):

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

Примечание: если установка из `requirements.txt` падает из-за несовместимых/опечатанных пакетов, установите зависимости вручную по импортам из файлов  `bot_local.py`, `rag.py`.

### Запуск
1) Убедитесь, что в корне проекта есть:
- `.env` с `BOT_TOKEN` и `OPENROUTER_API_KEY`
- `текстовая база знаний` 

2) Запустите бота:

- Вариант 1 (через `langchain_openrouter`, модель-роутер `openrouter/free`):

```bash
python bot.py
```

- Вариант 2 (через `langchain_openai` с OpenRouter endpoint и явным `MODEL_NAME`):

```bash
python bot_local.py
```

### Что где лежит
- `bot.py` — Telegram-бот + история диалога + RAG-контекст + OpenRouter через `ChatOpenRouter`
- `bot_local.py` — альтернативный запуск LLM через `ChatOpenAI` (OpenRouter base URL)
- `rag.py` — подготовка коллекции ChromaDB из `Текстовая база знаний` (создаётся при импорте модуля)

