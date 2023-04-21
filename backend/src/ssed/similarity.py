import numpy as np

from numpy.typing import NDArray


def openai_cosine_similarity(
        query_embedding: NDArray[np.float64],
        document_embeddings: NDArray[np.float64]
) -> NDArray[np.float64]:
    # OpenAI embeddings are normalized to length 1 so this is
    # identical to np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    # https://platform.openai.com/docs/guides/embeddings/which-distance-function-should-i-use
    return document_embeddings.dot(query_embedding)
