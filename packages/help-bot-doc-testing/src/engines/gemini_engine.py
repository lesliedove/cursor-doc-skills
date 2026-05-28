"""Google Gemini engine adapter with grounding (Google Search)."""

from __future__ import annotations

import os
import time
import httpx

from .base import BaseEngine, EngineResult

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class GeminiEngine(BaseEngine):
    """Query Google Gemini with Google Search grounding enabled."""

    name = "gemini"

    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY", "")

    async def query(self, question: str, product: str = "") -> EngineResult:
        start = time.perf_counter_ns()
        try:
            url = f"{GEMINI_API_URL}?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": question}]}],
                "tools": [{"google_search": {}}],
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()

            latency_ms = (time.perf_counter_ns() - start) // 1_000_000

            text = ""
            citations = []

            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                for part in content.get("parts", []):
                    text += part.get("text", "")

                grounding = candidates[0].get("groundingMetadata", {})
                for chunk in grounding.get("groundingChunks", []):
                    web = chunk.get("web", {})
                    if web.get("uri"):
                        citations.append(web["uri"])

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
