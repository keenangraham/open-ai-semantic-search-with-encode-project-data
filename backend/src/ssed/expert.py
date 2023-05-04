import tiktoken

from ssed.remote.openai import OpenAI

from ssed.results import Results

from ssed.serializer import dict_to_text

from dataclasses import dataclass

from typing import Any


MAX_TOKENS = 4096 - 500

PROMPT = 'Summarize why the results match or do not match the query. Do not mention specific results.'


@dataclass
class SearchRelevancyExpertProps:
    query: str
    results: list[str]
    openai: OpenAI = OpenAI()
    prompt: str = PROMPT


class SearchRelevancyExpert:

    def __init__(self, props: SearchRelevancyExpertProps) -> None:
        self.props = props

    @classmethod
    def from_results(cls, results: Results) -> 'SearchRelevancyExpert':
        if results.query is None:
            raise ValueError('Must use Results from a user query')
        return cls(
            props=SearchRelevancyExpertProps(
                query=results.query,
                results=results.serialized_documents,
            )
        )

    @classmethod
    def from_json(
            cls,
            query: str,
            results: list[dict[str, Any]]
    ) -> 'SearchRelevancyExpert':
        return cls(
            props=SearchRelevancyExpertProps(
                query=query,
                results=[
                    dict_to_text(result)
                    for result in results
                ],
            )
        )

    def generate_messages(self) -> list[str]:
        message = (
            self.props.prompt
            + f'\n\nQuery: "{self.props.query}"'
            + '\n\nResults:'
        )
        message = size_limited_add(
            base=message,
            to_add=format_results(self.props.results),
            model=self.props.openai.props.chat_model,
        ) + '\n\nSearch relevancy summary:'
        return [
            message
        ]

    async def evaluate(self) -> str:
        evaluation = await self.props.openai.get_chat_completion_for_messages(
            messages=self.generate_messages()
        )
        return evaluation


def number_of_tokens(text: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def format_results(results: list[str]) -> list[str]:
    return [
        f'\n\n{i}. {result}'
        for i, result in enumerate(results)
    ]


def size_limited_add(base: str, to_add: list[str], model: str) -> str:
    response = base
    for item in to_add:
        if number_of_tokens(text=response + item, model=model) > MAX_TOKENS:
            break
        response += item
    return response
