from domain.event import DomainEvent
from domain.money import Money
from domain.wallet import WalletLocked
from domain.wallet_event_as_a_result_of_method_invocation import Wallet


def test_static_publication_mechanism() -> None:
    # given
    wallet = Wallet(Money(10))

    # when
    for event in wallet.transact(Money(10)):
        assert isinstance(event, DomainEvent)

    # when
    for event in wallet.transact(Money(-15)):
        assert isinstance(event, DomainEvent)

    # when
    collected = []
    for event in wallet.transact(Money(-15)):
        assert isinstance(event, DomainEvent)
        collected.append(event)

    assert isinstance(collected[-1], WalletLocked)
