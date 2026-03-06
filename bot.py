import telebot
from langchain_openrouter import ChatOpenRouter
from langchain.messages import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv
from typing import Dict, List
from rag import collection

# Загружаем переменные из .env
load_dotenv()

# Получаем API‑ключ
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY не найден в .env")

# Получаем токен на бота
bot_token = os.getenv("BOT_TOKEN")


# Создаём экземпляр модели
llm = ChatOpenRouter(
    model="openrouter/free",  # конкретная модель или "openrouter/free" - специальный роутер,
    api_key=api_key,  # который автоматически выбирает доступную бесплатную модель
    temperature=0.7,
    max_tokens=1000,
    max_retries=2,
)

# Бот
bot = telebot.TeleBot(bot_token)


# История сообщений: по пользователю (или чату) храним список пар "вопрос-ответ"
UserId = int
HistoryPair = Dict[str, str]
user_histories: Dict[UserId, List[HistoryPair]] = {}
MAX_HISTORY_PAIRS = 10


def build_prompt_with_history(user_id: int, current_question: str) -> str:
    """
    Собираем промпт так, чтобы в контекст попали
    последние MAX_HISTORY_PAIRS вопросов и ответов данного пользователя.
    """
    history = user_histories.get(user_id, [])
    history_text_parts: List[str] = []

    for idx, pair in enumerate(history[-MAX_HISTORY_PAIRS:], start=1):
        q = pair.get("user", "")
        a = pair.get("assistant", "")
        history_text_parts.append(
            f"Диалог {idx}:\n"
            f"Пользователь: {q}\n"
            f"Ассистент: {a}\n"
        )

    history_text = "\n".join(history_text_parts)

    if history_text:
        prompt = (
            "Ты — умный и вежливый помощник. "
            "Отвечай по-русски и учитывай историю диалога.\n\n"
            f"{history_text}\n"
            f"Текущий запрос пользователя: {current_question}\n"
            "Ответ ассистента:"
        )
    else:
        prompt = (
            "Ты — умный и вежливый помощник. "
            "Отвечай по-русски.\n\n"
            f"Вопрос пользователя: {current_question}\n"
            "Ответ ассистента:"
        )

    return prompt


@bot.message_handler(func=lambda message: True)
def handle_llm_message(message):
    try:
        user_id = message.from_user.id
        user_text = message.text or ""

        print(f"[{user_id}] USER:", user_text)

        prompt = build_prompt_with_history(user_id, user_text)

        # Отправляем промпт в LLM (включает последние 10 вопросов и ответов)
        response = llm.invoke(prompt).content

        print(f"[{user_id}] ASSISTANT:", response)

        # Сохраняем очередную пару вопрос-ответ
        history = user_histories.setdefault(user_id, [])
        history.append({"user": user_text, "assistant": response})

        # Ограничиваем историю (по желанию можно хранить больше, чем 10)
        if len(history) > MAX_HISTORY_PAIRS * 5:
            # мягкое усечение, чтобы не разрасталось слишком сильно
            user_histories[user_id] = history[-MAX_HISTORY_PAIRS * 3 :]

        # Отвечаем пользователю
        bot.reply_to(message, response)
    except Exception as e:
        # Обработка ошибок (напр. проблемы с API)
        bot.reply_to(message, f"Ошибка: {str(e)}. Попробуйте позже.")


# Запуск бота
bot.polling()