import chromadb

from rag.embedder import embed

client = chromadb.PersistentClient()

collection = client.get_or_create_collection(name="rag_cli")


def add(chunks: list[str], embeddings: list[list[float]], doc_id: str) -> None:
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    collection.add(
        ids=ids,
        embeddings=embeddings,  # type: ignore
        documents=chunks,
    )


def query(embedding: list[float], top_k: int = 5) -> list[str]:
    return collection.query(query_embeddings=[embedding], n_results=top_k)["documents"][  # type: ignore
        0
    ]


def reset() -> None:
    client.delete_collection(name="rag_cli")


if __name__ == "__main__":
    sample_chunks = [
        "the rover uses LIDAR",
        "SLAM is used for mapping",
        "path planning with D* Lite",
    ]
    sample_embeddings = [embed(chunk) for chunk in sample_chunks]

    add(sample_chunks, sample_embeddings, "test_doc")
    query_vector = embed("how does the rover navigate?")
    results = query(query_vector)
    print(results)
