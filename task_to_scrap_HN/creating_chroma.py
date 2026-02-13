import chromadb

import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

from dotenv import load_dotenv
import os

client = chromadb.PersistentClient(path="current_store")
load_dotenv()


collection = client.get_or_create_collection(
    name="my_collection",
    embedding_function=OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
)

collection.add(
    ids=["1", "2", "3", "4"],
    documents=[
        "This is a document by Amr",
        "This is a document by Khalid",
        "This is a document by Morsy",
        "This is a document by Sara"
    ],
    metadatas=[
        {"name": "Amr", "role": "student"},
        {"name": "Khalid", "role": "engineer"},
        {"name": "Morsy", "role": "researcher"},
        {"name": "Sara", "role": "teacher"}
    ]
)

results = collection.query(
    query_texts=["is amr student ?"], # Chroma will embed this for you
)
