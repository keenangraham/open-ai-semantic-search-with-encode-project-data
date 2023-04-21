import asyncio

import numpy as np

import openai

from numpy.typing import ArrayLike

from openai import Embedding

from dataclasses import dataclass


async def aget_embedding(
        embedding_client: Embedding,
        text: str,
        model: str = 'text-embedding-ada-002'
) -> ArrayLike:
    response = await embedding_client.acreate( # type: ignore
        input=text,
        model=model,
    )
    return np.array(response['data'][0]['embedding'])



@dataclass
class OpenAIProps:
    embedding_client: Embedding


class OpenAI:

    def __init__(self, props: OpenAIProps):
        self.props = props

    async def aget_embeddings_for_documents(self, documents: list[str]) -> ArrayLike:
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

    def get_embeddings_for_documents(self, documents: list[str]) -> ArrayLike:
        return asyncio.run(self.aget_embeddings_for_documents(documents))
