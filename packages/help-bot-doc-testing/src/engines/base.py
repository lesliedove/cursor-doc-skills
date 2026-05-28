"""Base class and data structures for AI engine adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from abc import ABC, abstractmethod


@dataclass
class EngineResult:
    """Structured result from querying an AI engine."""

    engine: str
    question: str
    response_text: str
    citations: list[str] = field(default_factory=list)
    mentions_ansys: bool = False
    mentions_product: bool = False
    cites_ansys_help: bool = False
    error: str | None = None
    latency_ms: int = 0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "engine": self.engine,
            "question": self.question,
            "response_text": self.response_text,
            "citations": self.citations,
            "mentions_ansys": self.mentions_ansys,
            "mentions_product": self.mentions_product,
            "cites_ansys_help": self.cites_ansys_help,
            "error": self.error,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
        }


class BaseEngine(ABC):
    """Abstract base for all AI engine adapters."""

    name: str = "base"

    @abstractmethod
    async def query(self, question: str, product: str = "") -> EngineResult:
        """Send a question to the AI engine and return structured result."""
        ...

    def _analyze_result(
        self, question: str, text: str, citations: list[str], product: str
    ) -> EngineResult:
        """Common post-processing: detect mentions, citations, etc."""
        text_lower = text.lower()
        cites_help = any("ansyshelp.ansys.com" in c for c in citations)

        return EngineResult(
            engine=self.name,
            question=question,
            response_text=text,
            citations=citations,
            mentions_ansys="ansys" in text_lower,
            mentions_product=product.lower() in text_lower if product else False,
            cites_ansys_help=cites_help,
        )
