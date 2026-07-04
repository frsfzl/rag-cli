from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()


if __name__ == "__main__":
    vector = embed("the rover detects obstacles using LIDAR")
    print(len(vector))
    print(type(vector[0]))
