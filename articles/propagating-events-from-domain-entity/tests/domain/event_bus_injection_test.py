from domain.money import Money
from domain.wallet import WalletLocked
from domain.wallet_event_bus_injection import Wallet, InMemoryEventBus


def test_event_bus_injection() -> None:
    # given
    local_bus = InMemoryEventBus()
    wallet = Wallet(Money(10))

    # when
    wallet.transact(Money(10), local_bus)

    # then
    assert len(local_bus.events) == 1

    # when
    wallet.transact(Money(-15), local_bus)
    wallet.transact(Money(-15), local_bus)

    # then
    assert len(local_bus.events) == 7
    assert isinstance(local_bus.events[-1], WalletLocked)

