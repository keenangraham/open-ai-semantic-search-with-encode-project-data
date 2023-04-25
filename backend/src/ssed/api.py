from fastapi import FastAPI
from fastapi import HTTPException

from ssed.search import Search

from typing import Any


app = FastAPI()

search = Search(
    path='/data/awards'
)


@app.get('/')
async def root() -> dict[str, Any]:
    return {
        'message': 'success'
    }


@app.get('/search-by-query')
async def search_by_query(query: str, k: int = 5) -> dict[str, Any]:
    results = await search.embeddings.get_k_results_most_similar_to_query(
        query=query,
        k=k,
    )
    return {
        'results': results.as_dict()
    }


@app.get('/search-by-id')
async def search_by_id(id: str, k: int = 5) -> dict[str, Any]:
    results = await search.embeddings.get_k_results_most_similar_to_id(
        id_=id,
        k=k,
    )
    return {
        'results': results.as_dict()
    }
