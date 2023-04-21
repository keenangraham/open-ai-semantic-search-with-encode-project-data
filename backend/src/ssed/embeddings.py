from ssed.serializer import dict_to_text


from dataclasses import dataclass

from typing import Any
from typing import Callable

from numpy.typing import ArrayLike


@dataclass
class EmbeddingsProps:
    openai_client: Any
    serializer: Callable[[dict[str, Any]], str] = dict_to_text
    similarity_metric: str = 'cosine-similary'
    

class Embeddings:

    def __init__(self, props: EmbeddingsProps) -> None:
        self.props = props
        self.ids: list[str] = []
        self.documents: list[dict[str, Any]] = []
        self.serialized_documents: list[str] = []
        self.embeddings: ArrayLike = []

    def set_similarity_metric(self, similarity_metric: str) -> None:
        self.props.similarity_metric = similarity_metric

    def calculate_embeddings(self) -> None:
        pass

    def get_embeddings(self) -> ArrayLike:
        if not self.embeddings:
            self.calculate_embeddings()
        return self.embeddings

    @classmethod
    def from_documents(
            cls,
            props: EmbeddingsProps,
            documents: list[dict[str, Any]],
            id_key: str = 'accession',
    ) -> Embeddings:
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
