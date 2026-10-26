from typing import cast

from crewai import LLM
from crewai.utilities.types import LLMMessage


class GroqLLM(LLM):
    def _format_messages_for_provider(
        self, messages: list[LLMMessage]
    ) -> list[dict[str, str]]:
        cleaned_messages = [
            cast(
                LLMMessage,
                {
                    key: value
                    for key, value in message.items()
                    if key != "cache_breakpoint"
                },
            )
            for message in messages
        ]
        return super()._format_messages_for_provider(cleaned_messages)
