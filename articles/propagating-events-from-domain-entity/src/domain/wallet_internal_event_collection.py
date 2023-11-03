from __future__ import annotations

from typing import List

from domain.entity import Entity
from domain.event import DomainEvent
from domain.money import Money
from domain.wallet import FundsDeposited, FundsWithdrawn, OverdraftLimitHit, WalletLocked, OverdraftOccurred


class Wallet(Entity):
    def __init__(self, overdraft_limit: Money) -> None:
        self.balance = Money(0)
        self.overdraft_limit = overdraft_limit
        self.locked = False
        self._events = []
        super().__init__()

    def _record_event(self, event: DomainEvent):
        self._events.append(event)

    def collect_events(self) -> List[DomainEvent]:
        events = self._events[:]
        self._events = []
        return events

    def transact(self, amount: Money) -> None:
        if self.locked:
            raise Exception("Wallet is locked, transactions are not possible")

        if amount > 0:
            self.balance += amount
            self._record_event(FundsDeposited(self.id, amount))
            return

        if amount < 0:
            if self.balance + amount < -self.overdraft_limit:
                self.balance += amount
                self._record_event(FundsWithdrawn(self.id, amount))
                self._record_event(OverdraftOccurred(self.id, amount))
                self._record_event(OverdraftLimitHit(self.id, amount))
                self.lock_wallet()
            else:
                self.balance += amount
                self._record_event(FundsWithdrawn(self.id, amount))
                if self.balance < 0:
                    self._record_event(OverdraftOccurred(self.id, amount))

    def lock_wallet(self) -> None:
        self.locked = True
        self._record_event(WalletLocked(self.id, self.balance))
