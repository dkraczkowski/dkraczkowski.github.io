from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Optional

from domain.entity import Entity
from domain.event import DomainEvent
from domain.money import Money
from domain.wallet import FundsDeposited, FundsWithdrawn, OverdraftLimitHit, WalletLocked, OverdraftOccurred


class EventBus(Protocol):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        ...


class InMemoryEventBus:
    def __init__(self) -> None:
        self.events = []

    def publish(self, event: DomainEvent) -> None:
        self.events.append(event)


class Wallet(Entity):
    def __init__(self, overdraft_limit: Money) -> None:
        self.balance = Money(0)
        self.overdraft_limit = overdraft_limit
        self.locked = False
        super().__init__()

    def transact(self, amount: Money, event_bus: EventBus) -> None:
        if self.locked:
            raise Exception("Wallet is locked, transactions are not possible")

        if amount > 0:
            self.balance += amount
            event_bus and event_bus.publish(FundsDeposited(self.id, amount))
            return

        if amount < 0:
            if self.balance + amount < -self.overdraft_limit:
                self.balance += amount
                event_bus.publish(FundsWithdrawn(self.id, amount))
                event_bus.publish(OverdraftOccurred(self.id, amount))
                event_bus.publish(OverdraftLimitHit(self.id, amount))
                self.lock_wallet(event_bus)
            else:
                self.balance += amount
                event_bus.publish(FundsWithdrawn(self.id, amount))
                if self.balance < 0:
                    event_bus.publish(OverdraftOccurred(self.id, amount))

    def lock_wallet(self, event_bus: Optional[EventBus] = None) -> None:
        self.locked = True
        event_bus.publish(WalletLocked(self.id, self.balance))
