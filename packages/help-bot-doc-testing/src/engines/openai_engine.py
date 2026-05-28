"""OpenAI/ChatGPT engine adapter with web search."""

from __future__ import annotations

import os
import time
from openai import AsyncOpenAI

from .base import BaseEngine, EngineResult


class OpenAIEngine(BaseEngine):
    """Query ChatGPT with web search enabled."""

    name = "chatgpt"

    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def query(self, question: str, product: str = "") -> EngineResult:
        system_prompt = (
            "You are a helpful assistant. When answering questions about software products, "
            "cite your sources with URLs. Be specific and accurate."
        )
        start = time.perf_counter_ns()
        try:
            response = await self.client.responses.create(
                model="gpt-4o",
                input=question,
                instructions=system_prompt,
                tools=[{"type": "web_search_preview"}],
            )
            latency_ms = (time.perf_counter_ns() - start) // 1_000_000

            text = ""
            citations = []
            for item in response.output:
                if item.type == "message":
                    for content in item.content:
                        if content.type == "output_text":
                            text = content.text
                            if hasattr(content, "annotations"):
                                for ann in content.annotations:
                                    if hasattr(ann, "url"):
                                        citations.append(ann.url)

            result = self._analyze_result(question, text, citations, product)
            result.latency_ms = latency_ms
            return result

        except Exception as e:
            latency_ms = (time.perf_counter_ns() - start) // 1_000_000
            return EngineResult(
                engine=self.name,
                question=question,
                response_text="",
                error=str(e),
                latency_ms=latency_ms,
            )
