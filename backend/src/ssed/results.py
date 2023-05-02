from typing import Any
from typing import Iterable
from typing import Optional


class Results:

    def __init__(
            self,
            indices_and_scores: list[tuple[int, int]],
            embeddings: Any,
            calculation_time: Optional[float] = None,
            query: Optional[str] = None,
    ) -> None:
        self.indices_and_scores = indices_and_scores
        self.embeddings = embeddings
        self.calculation_time = calculation_time
        self.query = query

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
    def raw(self) -> list[tuple[int, float]]:
        return [
            (int(index), float(score))
            for index, score in self.indices_and_scores
        ]

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

    def as_dict(self) -> dict[str, Any]:
        return {
            'total': len(self.embeddings.ids),
            'time': self.calculation_time or 0.0,
            'results': [
                {
                    'id': d[0],
                    'score': d[1],
                    'document': d[2],
                }
                for d in zip(
                        self.ids,
                        self.scores,
                        self.documents
                )
            ]
        }
