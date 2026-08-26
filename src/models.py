from dataclasses import dataclass, field


@dataclass
class DocumentChunk:
    source: str
    title: str
    text: str
    status: str = "active"
    authority: str = "official"


@dataclass
class OrderRecord:
    order_id: str
    status: str
    carrier: str | None
    estimated_delivery: str | None
    customer_email: str
    shipping_address: str
    internal_note: str
    risk_score: int


@dataclass
class AgentResponse:
    answer: str
    sources: list[str] = field(default_factory=list)
    handoff: bool = False