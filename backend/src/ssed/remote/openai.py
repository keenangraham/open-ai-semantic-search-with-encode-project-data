import asyncio

import numpy as np

from numpy.typing import NDArray

from openai import Embedding

from dataclasses import dataclass

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_random_exponential

from typing import Type


@retry(
    wait=wait_random_exponential(
        min=1,
        max=60
    ),
    stop=stop_after_attempt(1000)
)
async def aget_embedding(
        embedding_client: Type[Embedding],
        text: str,
        model: str = 'text-embedding-ada-002'
) -> NDArray[np.float64]:
    response = await embedding_client.acreate( # type: ignore
        input=text,
        model=model,
    )
    return np.array(response['data'][0]['embedding'])



@dataclass
class OpenAIProps:
    embedding_client: Type[Embedding]


class OpenAI:

    def __init__(self, props: OpenAIProps):
        self.props = props

    async def get_embeddings_for_documents(self, documents: list[str]) -> NDArray[np.float64]:
        embeddings = await asyncio.gather(
            *[
                aget_embedding(
                    embedding_client=self.props.embedding_client,
                    text=document,
                )
                for document in documents
            ]
        )
        return np.array(embeddings)
