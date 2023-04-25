import os

import openai as openai_client

from ssed.remote.openai import OpenAI
from ssed.remote.openai import OpenAIProps

from ssed.embeddings import Embeddings
from ssed.embeddings import EmbeddingsProps


openai_client.api_key = os.environ['OPENAI_API_KEY']


class Search:

    def __init__(self, path: str):
        self.embeddings = Embeddings.load(
            props=EmbeddingsProps(
                openai=OpenAI(
                    props=OpenAIProps(
                        embedding_client=openai_client.Embedding
                    )
                )
            ),
            path=path,
        )
