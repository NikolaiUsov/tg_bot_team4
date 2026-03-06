from transformers import pipeline

"""
do_sample=True — использовать семплинг, чтобы текст был более плавным и человечным.

temperature=0.7 или другая температура, чтобы текст был более "предсказуемый" (ближе к 0), 
                 или наоборот более креативный и неожиданный (ближе к 1).

Можно задавать top_p или top_k для ограничения вероятностей.

Можно задать stop_tokens (или stop_strings) — чтобы остановить генерацию, 
                                         если модель начала генерировать что-то нежелательное или длинную бессмыслицу.

repetition_penalty=1.2 → штраф за повторение токенов, что уменьшает шансы повторить те же фразы.

no_repeat_ngram_size=3 → не допускает повторения триграмм (3-словных последовательностей).
"""


pipe = pipeline("text-generation", model='Qwen/Qwen1.5-4B-Chat') #"Qwen/Qwen1.5-4B-Chat"
messages = [
    {"role": "user", "content": "Привет! кто ты и что умеешь делать?"},
]
pipe(messages)


# pipe = pipeline("text-generation", model='напишите здесь адрес выбранной модели на HF') # ищем подходящую модельку вот здесь 

# messages = "Напишите здесь свой вопрос"
# output = pipe(messages, max_new_tokens=2000, do_sample=True, temperature=1)
# print(output[0]["generated_text"])
      


# messages = "бла блаа"
# output = pipe(messages, max_new_tokens=2000, do_sample=True, temperature=1)
# print(output[0]["generated_text"])


# Не работает. 