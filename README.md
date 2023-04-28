## Semantic search over ENCODE project data using OpenAI embeddings

### Run example Jupyter notebook

The [Semantic Search Example](https://github.com/keenangraham/open-ai-semantic-search-with-encode-project-data/blob/main/semantic_search_example.ipynb) Jupyter notebook shows an example of using the
underlying Python library to load JSON documents, calculate OpenAI embeddings, and perform semantic search.

You can run locally by installing the following dependencies in clean Python (>=3.10) environment:

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

### Run UI and API application

You can also run the search application (NextJS and FastAPI for the frontend and backend, respectively) locally if you have Docker installed:

```bash
$ docker compose up --build
```

Browse frontend at `localhost:3000` and backend at `localhost:8000`.

img style="float:center;" src="/images/search.gif">

Automated API documentation is available at `localhost:8000/docs` or `localhost:8000/redoc`:

<img style="float:left;" width="300" src="/images/api-doc-example.png">