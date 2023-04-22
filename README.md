### Semantic search over ENCODE project data using OpenAI embeddings

Run API with:

```bash
$ docker compose up --build
```

Browse frontend at localhost:3000 and backend at localhost:8000.

Run example Jupyter notebook `semantic_search_example.ipynb`.

Install dependencies in clean Python (>=3.10) environment:

```bash
$ pip install -e backend/.
$ pip install jupyter
```

Run notebook:

```bash
$ jupyter notbook
```

Open `semantic_search_example.ipynb`.