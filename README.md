# rag-cli

A CLI tool that lets you ask natural language questions about your PDF documents using retrieval-augmented generation

## How it works

Ingest: PDF -> extract text -> chunk -> embed -> store in ChromaDB

Query: question -> embed -> cosine similarity search -> top-3 chunks -> LLM prompt -> response

First, you provide the path to the PDF document you want to use. Next, it extracts the text from the pdf using PyPDF and chunks it into smaller pieces. Using sentence-transformers (a local all-MiniLM-L6-v2 model), each chunk is embedded into a 384-dimensional vector stored in ChromaDB, a persistent vector database. Next, you submit a query. The query is embedded using the same transformer model and returns a vector. Cosine similarity is used to find the top 5 most semantically relevant chunks. Then, it passes those chunks into an LLM (deepseek-v4-flash) as grounded context and asks it to respond to the query. The LLM's response is returned to the user. You may also reset the vector database.

## Stack

sentence-transformers: embedding model. local, no API key
ChromaDB: Vector database and search. Persistent vector storage
DeepSeek: LLM used to answer queries from retrieved context.

## Installation

Install UV:
```bash
pip install uv
```

Run:
```bash
git clone https://github.com/frsfzl/rag-cli.git
cd rag-cli
```

Create a .env file in the project root with:
```bash
DEEPSEEK_API_KEY=your_api_key_here
```

Create virtual environment:
```bash
uv venv
```

Enter virtual environment:
```bash
source .venv/bin/activate
```

Install the package:
```bash
uv pip install -e .
```

## Usage

Ingest a PDF:
```bash
rag ingest /path/to/document.pdf
```

Query your documents:
```bash
rag query "your question here"
```

Reset the database:
```bash
rag reset
```

## Example
```bash

rag ingest The\ Intersection\ of\ Visual\ Science\ and\ Art\ in\ Renaissance\ Italy.pdf
rag query "What was unusual about the lighting in Piero della Francesca's Flagellation painting?"
```

**Response:**
In Piero della Francesca's *Flagellation*, the lighting is unusual because it cannot be attributed to the natural sunlight that floods the exterior scene. Instead, the artist has apparently supposed an internal light source—specifically, some form of firebrand or torch held aloft—even though the outdoor setting is brightly sunlit. This bizarre, artificial illumination gives the scene a hallucinatory quality, as the light in the flagellation chamber is inconsistent with the external daylight. Moreover, the lighting arrangement is deliberately constructed to create a distinct perspective effect, contributing to the painting's eerie and frozen atmosphere.
