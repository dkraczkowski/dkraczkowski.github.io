from domain.money import Money
from domain.wallet import WalletLocked
from domain.wallet_internal_event_collection import Wallet


def test_event_collection_strategy() -> None:
    # given
    wallet = Wallet(Money(10))

    # when
    wallet.transact(Money(10))
    events = wallet.collect_events()

    # then
    assert len(events) == 1
    assert len(wallet._events) == 0

    # when
    wallet.transact(Money(-15))
    wallet.transact(Money(-15))
    events = wallet.collect_events()

    # then
    assert len(events) == 6
    assert isinstance(events[-1], WalletLocked)

