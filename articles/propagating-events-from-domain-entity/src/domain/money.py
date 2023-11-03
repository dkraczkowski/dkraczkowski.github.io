from __future__ import annotations

from decimal import Decimal
from typing import TypeAlias

# The following are simplified types only to represent potential value objects
Currency: TypeAlias = str
Amount: TypeAlias = Decimal | int | float


class Money:
    def __init__(self, value: Amount = 0, currency: Currency = "GBP") -> None:
        if isinstance(value, Decimal):
            value = Decimal(value)
        self.value = value
        self.currency = currency

    def __add__(self, amount: Amount | Money) -> Money:
        if not isinstance(amount, Money):
            return Money(self.value + amount, self.currency)

        if self.currency != amount.currency:
            raise ValueError("Currencies mismatch")

        return Money(self.value + amount.value, self.currency)

    def __sub__(self, amount: Amount | Money) -> Money:
        if not isinstance(amount, Money):
            return Money(self.value - amount, self.currency)

        if self.currency != amount.currency:
            raise ValueError("Currencies mismatch")

        return Money(self.value - amount.value, self.currency)

    def __lt__(self, amount: Amount | Money) -> bool:
        if not isinstance(amount, Money):
            return self.value < amount

        if self.currency != amount.currency:
            raise ValueError("Currencies mismatch")

        return self.value < amount.value

    def __gt__(self, amount: Amount | Money) -> bool:
        if not isinstance(amount, Money):
            return self.value > amount

        if self.currency != amount.currency:
            raise ValueError("Currencies mismatch")

        return self.value < amount.value

    def __neg__(self) -> Money:
        return Money(-self.value, self.currency)

    def __str__(self) -> str:
        return f"{self.value} {self.currency}"
