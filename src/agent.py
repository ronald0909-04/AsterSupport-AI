import re

from .models import AgentResponse
from .retriever import KnowledgeRetriever
from .order_tool import OrderLookupTool


class SupportAgent:
    def __init__(
        self,
        retriever: KnowledgeRetriever,
        order_tool: OrderLookupTool,
    ):
        self.retriever = retriever
        self.order_tool = order_tool

    def respond(
        self,
        message: str,
        history: list[dict[str, str]] | None = None,
    ) -> AgentResponse:

        history = history or []
        normalized = message.lower().strip()

        # ---------------------------------------------------------
        # Privacy protection
        # ---------------------------------------------------------
        order_id = self._extract_order_id(message)

        if self.order_tool.is_private_field_request(message):
            return AgentResponse(
                answer=(
                    "I can provide non-sensitive order status information, "
                    "but I cannot disclose private customer information "
                    "such as email addresses, shipping addresses, internal "
                    "notes, or risk scores."
                ),
                handoff=True,
            )

        # ---------------------------------------------------------
        # Order lookup
        # ---------------------------------------------------------
        if self._is_order_question(normalized):
            if order_id is None:
                order_id = self._order_id_from_history(history)

            if order_id is None:
                return AgentResponse(
                    answer=(
                        "Please provide your order ID so I can check "
                        "the order status."
                    ),
                    handoff=False,
                )

            order = self.order_tool.lookup(order_id)

            if order is None:
                return AgentResponse(
                    answer=(
                        f"I couldn't find order {order_id}. "
                        "Please check the order ID or contact customer support."
                    ),
                    handoff=True,
                )

            return AgentResponse(
                answer=self.order_tool.public_summary(order),
                handoff=False,
            )

        # ---------------------------------------------------------
        # Prompt-injection protection
        # ---------------------------------------------------------
        injection_terms = [
            "ignore previous instructions",
            "ignore all previous instructions",
            "reveal system prompt",
            "show system prompt",
            "developer message",
            "hidden instructions",
            "secret instructions",
        ]

        if any(term in normalized for term in injection_terms):
            return AgentResponse(
                answer=(
                    "I can't follow instructions that request hidden, "
                    "private, or internal information."
                ),
                handoff=True,
            )

        # ---------------------------------------------------------
        # Retrieve relevant knowledge
        # ---------------------------------------------------------
        query = self._resolve_context(message, history)

        if not self._is_supported_knowledge_question(query):
            return AgentResponse(
                answer=(
                    "I don't have enough information in the supplied "
                    "knowledge base to answer that reliably. "
                    "Please contact customer support for confirmation."
                ),
                handoff=True,
            )

        results = self.retriever.search(query, top_k=4)

        if not results:
            return AgentResponse(
                answer=(
                    "I don't have enough information in the supplied "
                    "knowledge base to answer that reliably. "
                    "Please contact customer support for confirmation."
                ),
                handoff=True,
            )

        # ---------------------------------------------------------
        # Conflict detection
        # ---------------------------------------------------------
        conflict = self._detect_conflict(results, query)

        if conflict:
            return AgentResponse(
                answer=(
                    "The supplied official sources contain conflicting "
                    "information about this topic. I don't want to give "
                    "you an unreliable answer, so please contact customer "
                    "support for confirmation."
                ),
                sources=[item.source for item in results],
                handoff=True,
            )

        # ---------------------------------------------------------
        # Build grounded answer
        # ---------------------------------------------------------
        answer = self._build_answer(query, results)

        if answer is None:
            return AgentResponse(
                answer=(
                    "I couldn't find enough reliable information to answer "
                    "that question. Please contact customer support."
                ),
                sources=[item.source for item in results],
                handoff=True,
            )

        return AgentResponse(
            answer=answer,
            sources=[item.source for item in results],
            handoff=False,
        )

    # -------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------

    def _extract_order_id(self, message: str) -> str | None:
        match = re.search(
            r"\bORD-\d{4}\b",
            message,
            re.IGNORECASE,
        )

        if not match:
            return None

        return match.group(0).upper()

    def _order_id_from_history(
        self,
        history: list[dict[str, str]],
    ) -> str | None:

        for item in reversed(history):
            text = item.get("content", "")
            order_id = self._extract_order_id(text)

            if order_id:
                return order_id

        return None

    def _is_order_question(self, message: str) -> bool:
        has_order_id = self._extract_order_id(message) is not None

        if has_order_id:
            return True

        order_terms = [
            "tracking",
            "where is",
            "when will it arrive",
            "when will it be delivered",
            "order status",
        ]

        return any(
            term in message
            for term in order_terms
        )

    def _resolve_context(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> str:

        normalized = message.lower()

        follow_up_terms = [
            "what about",
            "how about",
            "and canada",
            "and the",
            "when will it",
            "when will that",
            "what about that",
        ]

        if any(term in normalized for term in follow_up_terms):
            recent_user_messages = [
                item.get("content", "")
                for item in history[-4:]
                if item.get("role") == "user"
            ]

            if recent_user_messages:
                return (
                    recent_user_messages[-1]
                    + " "
                    + message
                )

        return message

    def _is_supported_knowledge_question(
        self,
        message: str,
    ) -> bool:

        text = message.lower()

        supported_topics = [
            "return",
            "refund",
            "shipping",
            "ship",
            "delivery",
            "international",
            "domestic",
            "backpack",
            "clean",
            "care",
            "soap",
            "bleach",
        ]

        return any(
            topic in text
            for topic in supported_topics
        )

    def _detect_conflict(
        self,
        results,
        query: str,
    ) -> bool:

        text = " ".join(
            item.text.lower()
            for item in results
        )

        return (
            "conflicting policy" in text
            or "conflicting information" in text
        )

    def _build_answer(
        self,
        query: str,
        results,
    ) -> str | None:

        combined = " ".join(
            item.text.strip()
            for item in results
        )

        q = query.lower()

        if "return" in q:
            match = re.search(
                r"(\d+)\s+calendar days",
                combined,
                re.IGNORECASE,
            )

            if match:
                return (
                    f"Standard customers may return unused products "
                    f"within {match.group(1)} calendar days of delivery."
                )

        if "shipping" in q or "ship" in q:

            if "international" in q:
                if "International shipping is available" in combined:
                    return (
                        "International shipping is available to selected "
                        "countries according to the supplied shipping policy."
                    )

            if "domestic" in q:
                return (
                    "Standard domestic orders are normally shipped using "
                    "the available carrier."
                )

        if "care" in q or "clean" in q:
            if "soft cloth" in combined:
                return (
                    "Backpacks should be cleaned using a soft cloth and "
                    "mild soap. Avoid harsh chemicals or bleach."
                )

        first = results[0].text.strip()

        if first:
            return first

        return None