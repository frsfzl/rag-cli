from pypdf import PdfReader


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunk_list = []
    cursor = 0
    while cursor < len(text):
        chunk_list.append(text[cursor : cursor + chunk_size])
        cursor += chunk_size - overlap
    return chunk_list


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text())

    return "\n".join(pages)


if __name__ == "__main__":
    text = load_pdf(
        "/home/faris/Projects/rag-cli/The Intersection of Visual Science and Art in Renaissance Italy.pdf"
    )
    print(text[:10000])
