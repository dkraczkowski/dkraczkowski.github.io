from domain.money import Money


def test_can_instantiate() -> None:
    # when
    money = Money()

    # then
    assert isinstance(money, Money)


def test_can_add_same_currency() -> None:
    # given
    five_gbp = Money(5)
    ten_gbp = Money(10)

    # when
    result = five_gbp + ten_gbp

    # then
    assert result.value == 15


def test_can_subtract_same_currency() -> None:
    # given
    five_gbp = Money(5)
    ten_gbp = Money(10)

    # when
    result = ten_gbp - five_gbp

    # then
    assert result.value == 5
