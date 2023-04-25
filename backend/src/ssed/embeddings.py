import gzip

import json

import numpy as np

from ssed.cache import SimpleCache

from ssed.similarity import openai_cosine_similarity

from ssed.serializer import dict_to_text

from ssed.remote.openai import OpenAI

from ssed.results import Results

from dataclasses import dataclass

from typing import Any
from typing import Callable
from typing import cast

from numpy.typing import NDArray


@dataclass
class EmbeddingsProps:
    openai: OpenAI
    serializer: Callable[[dict[str, Any]], str] = dict_to_text
    similarity_metric: Callable[[NDArray[np.float64], NDArray[np.float64]], NDArray[np.float64]] = openai_cosine_similarity
    query_to_embedding_cache_size: int = 5000


class Embeddings:

    def __init__(self, props: EmbeddingsProps) -> None:
        self.props = props
        self.ids: list[str] = []
        self.documents: list[dict[str, Any]] = []
        self.serialized_documents: list[str] = []
        self.values: NDArray[np.float64] = np.array([])
        self.query_to_embedding_cache: SimpleCache = SimpleCache(
            maxsize=props.query_to_embedding_cache_size,
        )

    async def calculate_embeddings(self) -> None:
        self.values = await self.props.openai.get_embeddings_for_documents(
            self.serialized_documents
        )

    async def get_values(self) -> NDArray[np.float64]:
        if self.values.size == 0:
            await self.calculate_embeddings()
        return self.values

    async def calculate_similarities(self, query_embedding: NDArray[np.float64]) -> NDArray[np.float64]:
        return self.props.similarity_metric(query_embedding, await self.get_values())

    def get_index_of_id(self, id_: str) -> int:
        return self.ids.index(id_)

    def get_document_by_id(self, id_: str) -> dict[str, Any]:
        return self.documents[self.get_index_of_id(id_)]

    def get_serialized_document_by_id(self, id_: str) -> str:
        return self.serialized_documents[self.get_index_of_id(id_)]

    async def get_embedding_by_id(self, id_: str) -> NDArray[np.float64]:
        embeddings = await self.get_values()
        return cast(NDArray[np.float64], embeddings[self.get_index_of_id(id_)])

    async def get_embedding_for_query(self, query: str) -> NDArray[np.float64]:
        if query not in self.query_to_embedding_cache:
            embeddings = await self.props.openai.get_embeddings_for_documents([query])
            self.query_to_embedding_cache[query] = embeddings[0]
        return cast(NDArray[np.float64], self.query_to_embedding_cache[query])

    async def get_k_results_most_similar_to_query(self, query: str, k: int) -> Results:
        query_embedding = await self.get_embedding_for_query(query)
        similarities = await self.calculate_similarities(query_embedding)
        indices_and_scores = [
            (index, similarities[index])
            for index in similarities.argsort()[::-1][:k]
        ]
        return Results(
            indices_and_scores=indices_and_scores,
            embeddings=self,
        )

    async def get_k_results_most_similar_to_id(self, id_: str, k: int) -> Results:
        query_embedding = await self.get_embedding_by_id(id_)
        similarities = await self.calculate_similarities(query_embedding)
        indices_and_scores = [
            (index, similarities[index])
            for index in similarities.argsort()[::-1][:k]
        ]
        return Results(
            indices_and_scores=indices_and_scores,
            embeddings=self,
        )

    @classmethod
    def from_documents(
            cls,
            props: EmbeddingsProps,
            documents: list[dict[str, Any]],
            id_key: str = 'accession',
    ) -> 'Embeddings':
        embeddings = cls(props=props)
        embeddings.ids = [
            document[id_key]
            for document in documents
        ]
        embeddings.documents = documents
        embeddings.serialized_documents = [
            props.serializer(document)
            for document in documents
        ]
        return embeddings

    def save(self, path: str) -> None:
        np.savez_compressed(
            path,
            data=self.values
        )
        save_as_compressed_json(
            f'{path}-ids.json.gz',
            self.ids,
        )
        save_as_compressed_json(
            f'{path}-documents.json.gz',
            self.documents,
        )
        save_as_compressed_json(
            f'{path}-serialized_documents.json.gz',
            self.serialized_documents,
        )

    @classmethod
    def load(
            cls,
            props: EmbeddingsProps,
            path: str,
            load_documents: bool = True,
            load_serialized_documents: bool = True,
    ) -> 'Embeddings':
        embeddings = cls(props=props)
        embeddings.values = np.load(f'{path}.npz')['data']
        embeddings.ids = load_from_compressed_json(
            f'{path}-ids.json.gz'
        )
        if load_documents:
            embeddings.documents = load_from_compressed_json(
                f'{path}-documents.json.gz'
            )
        if load_serialized_documents:
            embeddings.serialized_documents = load_from_compressed_json(
                f'{path}-serialized_documents.json.gz'
            )
        return embeddings


def save_as_compressed_json(path: str, values: Any) -> None:
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        json.dump(values, f)


def load_from_compressed_json(path: str) -> Any:
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return json.load(f)
