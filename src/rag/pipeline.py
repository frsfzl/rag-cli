from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

from rag.chunker import chunk_text, load_pdf
from rag.embedder import embed
from rag.store import add
from rag import store

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK-API-KEY"), base_url="https://api.deepseek.com"
)


def ingest(path: str) -> None:
    text = load_pdf(path)
    chunks = chunk_text(text)
    embeddings = [embed(chunk) for chunk in chunks]
    add(chunks, embeddings, Path(path).stem)


def query(query: str, debug: bool = False) -> str:

    embedding = embed(query)
    chunks = store.query(embedding=embedding, top_k=5)

    if debug:
        for i, chunk in enumerate(chunks):
            print(f"--- chunk {i + 1}")
            print(chunk)
            print()

    context = "\n\n".join(f"Chunk {i + 1}:\n{chunk}" for i, chunk in enumerate(chunks))

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a research assistant. Answer the user's question using context provided below. Provide a complete and detailed answer. If the answer is not in the context, say \"I don't have enough information to answer that.\"",
            },
            {
                "role": "user",
                "content": f"CONTEXT:{context}\n\nQUESTION:\n{query}",
            },
        ],
    )

    return response.choices[0].message.content  # type: ignore
