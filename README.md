## Semantic search over ENCODE project data using OpenAI embeddings

### Run API with:

```bash
$ docker compose up --build
```

Browse frontend at `localhost:3000` and backend at `localhost:8000`.

### Run example Jupyter notebook.

Install dependencies in clean Python (>=3.10) environment:

```bash
$ pip install -e backend/.
$ pip install jupyter
```

Define your `OPENAI_API_KEY` in your environment:
```bash
$ export OPENAI_API_KEY=xyz123
```

Run notebook:

```bash
$ jupyter notebook
```

Open `semantic_search_example.ipynb`. Note the code assumes your OpenAI API key (for making calls to the OpenAI API) is defined in your environment.