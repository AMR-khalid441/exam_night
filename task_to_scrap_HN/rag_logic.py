from creating_chroma import collection
# =========================
# User Question
# =========================
user_question = "do you know anything about samar  ?"

# =========================
# Query Chroma
# =========================
results = collection.query(
    query_texts=[user_question],
    n_results=3
)

# =========================
# Build Context from Chroma Results
# =========================
documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]

context_parts = []

for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
    similarity = 1 - dist  # convert distance to similarity
    
    context_parts.append(
        f"[Document {i+1}] (Similarity: {similarity:.3f})\n"
        f"Name: {meta.get('name', 'N/A')}\n"
        f"Role: {meta.get('role', 'N/A')}\n"
        f"Content: {doc}\n"
    )

context = "\n".join(context_parts)

print("==== Retrieved Context ====\n")
print(context)



#### quering 

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = f"""
You are a question-answering assistant.

Answer the question using ONLY the provided context.
If the answer is not found in the context, say "I don't know."

Context:
{context}

Question:
{user_question}

Answer:
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
    temperature=0,
    max_output_tokens=200
,)

answer = response.output_text

print("Final Answer:\n")
print(answer)
