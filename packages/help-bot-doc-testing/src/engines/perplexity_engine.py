"""Perplexity engine adapter using their API with built-in web search."""

from __future__ import annotations

import os
import time
import httpx

from .base import BaseEngine, EngineResult

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityEngine(BaseEngine):
    """Query Perplexity AI which has built-in web search and returns citations."""

    name = "perplexity"

    def __init__(self):
        self.api_key = os.environ.get("PERPLEXITY_API_KEY", "")

    async def query(self, question: str, product: str = "") -> EngineResult:
        start = time.perf_counter_ns()
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    PERPLEXITY_API_URL,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "sonar-pro",
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are a helpful technical assistant. "
                                    "Provide accurate answers with source citations."
                                ),
                            },
                            {"role": "user", "content": question},
                        ],
                        "return_citations": True,
                    },
                )
                resp.raise_for_status()
                data = resp.json()

            latency_ms = (time.perf_counter_ns() - start) // 1_000_000

            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            citations = data.get("citations", [])

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
