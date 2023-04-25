import numpy as np

import json

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


class Embeddings:

    def __init__(self, props: EmbeddingsProps) -> None:
        self.props = props
        self.ids: list[str] = []
        self.documents: list[dict[str, Any]] = []
        self.serialized_documents: list[str] = []
        self.values: NDArray[np.float64] = np.array([])

    def calculate_embeddings(self) -> None:
        self.values = self.props.openai.get_embeddings_for_documents(
            self.serialized_documents
        )

    def get_values(self) -> NDArray[np.float64]:
        if self.values.size == 0:
            self.calculate_embeddings()
        return self.values

    def calculate_similarities(self, query_embedding: NDArray[np.float64]) -> NDArray[np.float64]:
        return self.props.similarity_metric(query_embedding, self.get_values())

    def get_index_of_id(self, id_: str) -> int:
        return self.ids.index(id_)

    def get_document_by_id(self, id_: str) -> dict[str, Any]:
        return self.documents[self.get_index_of_id(id_)]

    def get_serialized_document_by_id(self, id_: str) -> str:
        return self.serialized_documents[self.get_index_of_id(id_)]

    def get_embedding_by_id(self, id_: str) -> NDArray[np.float64]:
        return cast(NDArray[np.float64], self.get_values()[self.get_index_of_id(id_)])

    def get_k_results_most_similar_to_query(self, query: str, k: int) -> Results:
        query_embedding = self.props.openai.get_embeddings_for_documents([query])[0]
        similarities = self.calculate_similarities(query_embedding)
        indices_and_scores = [
            (index, similarities[index])
            for index in similarities.argsort()[::-1][:k]
        ]
        return Results(
            indices_and_scores=indices_and_scores,
            embeddings=self,
        )

    def get_k_results_most_similar_to_id(self, id_: str, k: int) -> Results:
        query_embedding = self.get_embedding_by_id(id_)
        similarities = self.calculate_similarities(query_embedding)
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
        with open(f'{path}-ids.json', 'w', encoding='utf-8') as f:
            json.dump(self.ids, f)
        with open(f'{path}-documents.json', 'w', encoding='utf-8') as f:
            json.dump(self.documents, f)
        with open(f'{path}-serialized_documents.json', 'w', encoding='utf-8') as f:
            json.dump(self.serialized_documents, f)

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
        with open(f'{path}-ids.json', 'r', encoding='utf-8') as f:
            embeddings.ids = json.load(f)
        if load_documents:
            with open(f'{path}-documents.json', 'r', encoding='utf-8') as f:
                embeddings.documents = json.load(f)
        if load_serialized_documents:
            with open(f'{path}-serialized_documents.json', 'r', encoding='utf-8') as f:
                embeddings.serialized_documents = json.load(f)
        return embeddings
