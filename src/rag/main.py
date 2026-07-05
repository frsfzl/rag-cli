import typer

from rag import pipeline, store

app = typer.Typer()


@app.command()
def ingest(path: str):
    pipeline.ingest(path)


@app.command()
def query(query: str, debug: bool = False):
    print(pipeline.query(query, debug=debug))


@app.command()
def reset():
    store.reset()


if __name__ == "__main__":
    app()
