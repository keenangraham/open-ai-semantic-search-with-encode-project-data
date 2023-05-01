import asyncio

import numpy as np

from numpy.typing import NDArray

from openai import Embedding
from openai import ChatCompletion

from dataclasses import dataclass

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_random_exponential

from typing import Type


@retry(
    wait=wait_random_exponential(
        min=1,
        max=60,
    ),
    stop=stop_after_attempt(1000)
)
async def aget_embedding(
        embedding_client: Type[Embedding],
        text: str,
        model: str,
) -> NDArray[np.float64]:
    response = await embedding_client.acreate( # type: ignore
        input=text,
        model=model,
    )
    return np.array(response['data'][0]['embedding'])


@retry(
    wait=wait_random_exponential(
        min=1,
        max=60,
    ),
    stop=stop_after_attempt(10)
)
async def aget_chat_completion(
        chat_client: Type[ChatCompletion],
        model: str,
        messages: list[dict[str, str]],
        temperature: float,
) -> str:
    response = await chat_client.acreate( # type: ignore
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response['choices'][0]['message']['content']


@dataclass
class OpenAIProps:
    embedding_client: Type[Embedding] = Embedding
    embedding_model: str = 'text-embedding-ada-002'
    chat_client: Type[ChatCompletion] = ChatCompletion
    chat_model: str = 'gpt-3.5-turbo'


class OpenAI:

    def __init__(self, props: OpenAIProps = OpenAIProps()):
        self.props = props

    async def get_embeddings_for_documents(self, documents: list[str]) -> NDArray[np.float64]:
        embeddings = await asyncio.gather(
            *[
                aget_embedding(
                    embedding_client=self.props.embedding_client,
                    text=document,
                    model=self.props.embedding_model,
                )
                for document in documents
            ]
        )
        return np.array(embeddings)

    async def get_chat_completion_for_messages(self, messages: list[str], temperature: float = 1) -> str:
        content = await aget_chat_completion(
            chat_client=self.props.chat_client,
            model=self.props.chat_model,
            messages=[
                {
                    'role': 'user',
                    'content': user_content
                }
                for user_content in messages
            ],
            temperature=temperature,
        )
        return content
