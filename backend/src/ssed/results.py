from typing import Any
from typing import Iterable


class Results:

    def __init__(
            self,
            indices_and_scores: list[tuple[int, int]],
            embeddings: Any
    ) -> None:
        self.indices_and_scores = indices_and_scores
        self.embeddings = embeddings

    def __str__(self) -> str:
        ids_and_scores = [
            f'{id_}: {score}'
            for id_, score in zip(self.ids, self.scores)
        ]
        return '\n'.join(ids_and_scores)

    def __iter__(self) -> Iterable[tuple[dict[str, Any], int]]:
        for item in self.documents_with_scores:
            yield item

    @property
    def raw(self) -> list[tuple[int, int]]:
        return self.indices_and_scores

    @property
    def scores(self) -> list[int]:
        return [
            score
            for index, score in self.indices_and_scores
        ]

    @property
    def ids(self) -> list[str]:
        return [
            self.embeddings.ids[index]
            for index, score in self.indices_and_scores
        ]

    @property
    def documents(self) -> list[dict[str, Any]]:
        return [
            self.embeddings.documents[index]
            for index, score in self.indices_and_scores
        ]

    @property
    def documents_with_scores(self) -> list[tuple[dict[str, Any], int]]:
        return [
            (self.embeddings.documents[index], score)
            for index, score in self.indices_and_scores
        ]

    @property
    def serialized_documents(self) -> list[str]:
        return [
            self.embeddings.serialized_documents[index]
            for index, score in self.indices_and_scores
        ]

    def as_dict(self) -> list[dict[str, Any]]:
        return [
            {
                'id_': d[0],
                'score': d[1],
                'document': d[2],
                'serialized_document': d[3]
            }
            for d in zip(
                    self.ids,
                    self.scores,
                    self.documents,
                    self.serialized_documents,
            )
        ]
