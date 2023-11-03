from domain.money import Money
from domain.wallet import WalletLocked
from domain.wallet_static_publication_mechanism import Wallet, DummyEventBus, GlobalEventBus


def test_static_publication_mechanism() -> None:
    # given
    eb = DummyEventBus()
    GlobalEventBus.init(eb)
    wallet = Wallet(Money(10))

    # when
    wallet.transact(Money(10))

    # then
    assert len(eb.events) == 1

    # when
    wallet.transact(Money(-15))
    wallet.transact(Money(-15))

    # then
    assert len(eb.events) == 7
    assert isinstance(eb.events[-1], WalletLocked)

