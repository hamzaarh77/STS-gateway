from dataclasses import dataclass


@dataclass
class Order:
    id: int
    customer: str
    drug: str
    quantity: str
    total: int
    status: str | None
