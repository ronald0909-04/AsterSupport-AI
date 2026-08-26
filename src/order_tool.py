import json
from pathlib import Path

from .models import OrderRecord


class OrderLookupTool:
    def __init__(self, path: str):
        self.path = Path(path)
        self.orders = self._load_orders()

    def _load_orders(self) -> dict:
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def lookup(self, order_id: str) -> OrderRecord | None:
        order_id = order_id.strip().upper()

        record = self.orders.get(order_id)

        if record is None:
            return None

        return OrderRecord(
            order_id=order_id,
            status=record["status"],
            carrier=record["carrier"],
            estimated_delivery=record["estimated_delivery"],
            customer_email=record["customer_email"],
            shipping_address=record["shipping_address"],
            internal_note=record["internal_note"],
            risk_score=record["risk_score"],
        )

    def public_summary(self, order: OrderRecord) -> str:
        if order.status.lower() in {"cancelled", "returned"}:
            return f"Order {order.order_id} is currently {order.status}."

        answer = f"Order {order.order_id} is currently {order.status}"

        if order.carrier:
            answer += f" with {order.carrier}"

        if order.estimated_delivery:
            answer += f" and is estimated to arrive on {order.estimated_delivery}"

        return answer + "."

    def is_private_field_request(self, message: str) -> bool:
        private_terms = [
            "email",
            "address",
            "internal note",
            "internal notes",
            "risk score",
            "customer information",
            "private information",
        ]

        text = message.lower()

        return any(term in text for term in private_terms)