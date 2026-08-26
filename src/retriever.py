import re
from collections import Counter

from .models import DocumentChunk


class KnowledgeRetriever:
    def __init__(self, chunks: list[DocumentChunk]):
        self.chunks = chunks

    def _tokens(self, text: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    def _score(self, query: str, chunk: DocumentChunk) -> float:
        query_tokens = Counter(self._tokens(query))
        chunk_tokens = Counter(self._tokens(chunk.text))

        if not query_tokens or not chunk_tokens:
            return 0.0

        overlap = sum(
            min(count, chunk_tokens[token])
            for token, count in query_tokens.items()
        )

        score = overlap / max(sum(query_tokens.values()), 1)

        # Prefer active official sources when scores are similar.
        if chunk.status.lower() == "active":
            score += 0.05

        if chunk.authority.lower() == "official":
            score += 0.05

        return score

    def search(
        self,
        query: str,
        top_k: int = 4,
    ) -> list[DocumentChunk]:

        scored = [
            (self._score(query, chunk), chunk)
            for chunk in self.chunks
        ]

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            chunk
            for score, chunk in scored[:top_k]
            if score > 0
        ]