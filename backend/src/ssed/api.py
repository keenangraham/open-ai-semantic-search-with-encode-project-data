import os

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query

from pydantic import BaseModel

from ssed.search import Search

from typing import Annotated
from typing import Any


MAX_RESULTS = 50


app = FastAPI()


search = Search(
    path=os.environ['DATA_SOURCE']
)


@app.get('/')
async def root() -> dict[str, Any]:
    return {
        'message': 'success'
    }


@app.get('/search-by-query/')
async def search_by_query(query: str, k: Annotated[int, Query(ge=0, le=MAX_RESULTS)] = 3) -> dict[str, Any]:
    results = await search.embeddings.get_k_results_most_similar_to_query(
        query=query,
        k=k,
    )
    return results.as_dict()


@app.get('/search-by-id/')
async def search_by_id(id: str, k: Annotated[int, Query(ge=0, le=MAX_RESULTS)] = 3) -> dict[str, Any]:
    if id not in search.embeddings.ids:
        raise HTTPException(
            status_code=404,
            detail='ID not found'
        )
    results = await search.embeddings.get_k_results_most_similar_to_id(
        id_=id,
        k=k,
    )
    return results.as_dict()


class SearchResults(BaseModel):
    query: str
    results: list[dict[str, Any]]


@app.post('/evaluate-search-relevancy/')
async def evaluate_search_relevancy(
        search_results: SearchResults
) -> dict[str, Any]:
    expert = search.relevancy_expert_factory.from_json(
        query=search_results.query,
        results=search_results.results,
    )
    return {
        'evaluation': await expert.evaluate()
    }
