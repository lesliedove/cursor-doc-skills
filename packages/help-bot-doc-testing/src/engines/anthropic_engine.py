"""Anthropic/Claude engine adapter with web search tool."""

from __future__ import annotations

import os
import time
from anthropic import AsyncAnthropic

from .base import BaseEngine, EngineResult


class AnthropicEngine(BaseEngine):
    """Query Claude with web search enabled."""

    name = "claude"

    def __init__(self):
        self.client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def query(self, question: str, product: str = "") -> EngineResult:
        start = time.perf_counter_ns()
        try:
            response = await self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                tools=[
                    {
                        "type": "web_search",
                        "name": "web_search",
                        "max_uses": 5,
                    }
                ],
                messages=[{"role": "user", "content": question}],
            )
            latency_ms = (time.perf_counter_ns() - start) // 1_000_000

            text = ""
            citations = []
            for block in response.content:
                if block.type == "text":
                    text += block.text
                    if hasattr(block, "citations") and block.citations:
                        for cite in block.citations:
                            if hasattr(cite, "url") and cite.url:
                                citations.append(cite.url)

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
