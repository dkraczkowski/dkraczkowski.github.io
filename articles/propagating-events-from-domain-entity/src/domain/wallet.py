from __future__ import annotations

from domain.entity import Entity, Id
from domain.event import DomainEvent
from domain.money import Money


class FundsDeposited(DomainEvent):
    def __init__(self, wallet_id: Id, amount: Money):
        self.wallet_id = wallet_id
        self.amount = amount
        super().__init__()

    @property
    def namespace(self) -> str:
        return "wallet"


class FundsWithdrawn(DomainEvent):
    def __init__(self, wallet_id: Id, amount: Money):
        self.wallet_id = wallet_id
        self.amount = amount
        super().__init__()

    @property
    def namespace(self) -> str:
        return "wallet"


class OverdraftOccurred(DomainEvent):
    def __init__(self, wallet_id: Id, amount: Money):
        self.wallet_id = wallet_id
        self.amount = amount
        super().__init__()

    @property
    def namespace(self) -> str:
        return "wallet"


class OverdraftLimitHit(DomainEvent):
    def __init__(self, wallet_id: Id, amount: Money):
        self.wallet_id = wallet_id
        self.amount = amount
        super().__init__()

    @property
    def namespace(self) -> str:
        return "wallet"


class WalletLocked(DomainEvent):
    def __init__(self, wallet_id: Id, amount: Money):
        super().__init__()
        self.wallet_id = wallet_id
        self.amount = amount

    @property
    def namespace(self) -> str:
        return "wallet"


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
            FundsDeposited(self.id, amount)
            return

        if amount < 0:
            if self.balance + amount < -self.overdraft_limit:
                self.balance += amount
                FundsWithdrawn(self.id, amount)
                OverdraftOccurred(self.id, amount)
                OverdraftLimitHit(self.id, amount)
                self.lock_wallet()
            else:
                self.balance += amount
                FundsWithdrawn(self.id, amount)
                if self.balance < 0:
                    OverdraftOccurred(self.id, amount)

    def lock_wallet(self) -> None:
        self.locked = True
        WalletLocked(self.id, self.balance)
