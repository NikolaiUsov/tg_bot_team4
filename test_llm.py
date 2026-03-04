"""
Простой способ поговорить с бесплатной моделью LLM
"""

from langchain_openrouter import ChatOpenRouter
import os
from dotenv import load_dotenv


# Загружаем переменные из .env
load_dotenv()

# Получаем API‑ключ
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY не найден в .env")


# Создаём экземпляр модели
llm = ChatOpenRouter(
    model="arcee-ai/trinity-large-preview:free",  # конкретная модель или "openrouter/free" - специальный роутер, 
    api_key=api_key,                              # который автоматически выбирает доступную бесплатную модель
    temperature=0.9,
    max_tokens=100,
    max_retries=2,
)

# Отправляем запрос
response = llm.invoke("Привет. Кто ты?")


# Выводим ответ
print(response.content)
