from __future__ import annotations

from typing import Iterator

from domain.entity import Entity
from domain.event import DomainEvent
from domain.money import Money
from domain.wallet import FundsDeposited, FundsWithdrawn, OverdraftLimitHit, WalletLocked, OverdraftOccurred


class Wallet(Entity):
    def __init__(self, overdraft_limit: Money) -> None:
        self.balance = Money(0)
        self.overdraft_limit = overdraft_limit
        self.locked = False
        super().__init__()

    def transact(self, amount: Money) -> Iterator[DomainEvent]:
        if self.locked:
            raise Exception("Wallet is locked, transactions are not possible")

        if amount > 0:
            self.balance += amount
            yield FundsDeposited(self.id, amount)
            return

        if amount < 0:
            if self.balance + amount < -self.overdraft_limit:
                self.balance += amount
                yield FundsWithdrawn(self.id, amount)
                yield OverdraftOccurred(self.id, amount)
                yield OverdraftLimitHit(self.id, amount)
                for event in self.lock_wallet():
                    yield event
            else:
                self.balance += amount
                yield FundsWithdrawn(self.id, amount)
                if self.balance < 0:
                    yield OverdraftOccurred(self.id, amount)

    def lock_wallet(self) -> Iterator[DomainEvent]:
        self.locked = True
        yield WalletLocked(self.id, self.balance)
