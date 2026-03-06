from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions


with open("guide_to_the_world.md", encoding='utf-8') as f:
    guide_to_the_world = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=150,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ":", ";", "?", "!", ""]
)

# Делим текст на чанки
chunks = text_splitter.split_text(guide_to_the_world)
print("Всего фрагментов", len(chunks)) # Выведем кол-во чанок 

# Выделим индексы чанок
ids = [str(i) for i in range(len(chunks))]

client = chromadb.Client() # Создаем БД
# Русскоязычная embedding функция работает с локальными моделями      ### sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
russian_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="cointegrated/rubert-tiny2"   # HuggingFaceTB/SmolLM3-3B  /// cointegrated/rubert-tiny2 /// IlyaGusev/saiga_llama3_8b
)
collection = client.create_collection(
    "The_Witchers_guide", 
    embedding_function=russian_ef
)
collection.add(documents=chunks, ids=ids) # Добавляем чанки в коллекцию

if __name__ =="__main__":
    query = "Какие опасности ожидают путника в землях Нильфгаарда?"
    result= collection.query(query_texts=[query], n_results=5)
    print(result)