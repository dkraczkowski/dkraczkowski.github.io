from __future__ import annotations

from abc import abstractmethod
from typing import Protocol

from domain.entity import Entity
from domain.event import DomainEvent
from domain.money import Money
from domain.wallet import FundsDeposited, FundsWithdrawn, OverdraftLimitHit, WalletLocked, OverdraftOccurred


class EventBus(Protocol):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        ...


class DummyEventBus:
    def __init__(self) -> None:
        self.events = []

    def publish(self, event: DomainEvent) -> None:
        self.events.append(event)


class GlobalEventBus:
    event_bus: EventBus

    @classmethod
    def publish(cls, event: DomainEvent) -> None:
        cls.event_bus.publish(event)

    @classmethod
    def init(cls, event_bus: EventBus) -> None:
        cls.event_bus = event_bus


GlobalEventBus.init(DummyEventBus())


class Wallet(Entity):
    def __init__(self, overdraft_limit: Money) -> None:
        self.balance = Money(0)
        self.overdraft_limit = overdraft_limit
        self.locked = False
        super().__init__()

    def transact(self, amount: Money) -> None:
        if self.locked:
            raise Exception("Wallet is locked, transactions are not possible")

        if amount > 0:
            self.balance += amount
            GlobalEventBus.publish(FundsDeposited(self.id, amount))
            return

        if amount < 0:
            if self.balance + amount < -self.overdraft_limit:
                self.balance += amount
                GlobalEventBus.publish(FundsWithdrawn(self.id, amount))
                GlobalEventBus.publish(OverdraftOccurred(self.id, amount))
                GlobalEventBus.publish(OverdraftLimitHit(self.id, amount))
                self.lock_wallet()
            else:
                self.balance += amount
                GlobalEventBus.publish(FundsWithdrawn(self.id, amount))
                if self.balance < 0:
                    GlobalEventBus.publish(OverdraftOccurred(self.id, amount))

    def lock_wallet(self) -> None:
        self.locked = True
        GlobalEventBus.publish(WalletLocked(self.id, self.balance))
