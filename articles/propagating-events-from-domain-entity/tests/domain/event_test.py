from domain.event import DomainEvent


def test_can_define_event() -> None:
    # given
    class MyEvent(DomainEvent):
        @property
        def namespace(self) -> str:
            return "test"

    # then
    assert issubclass(MyEvent, DomainEvent)


def test_can_instantiate_custom_event() -> None:
    # given
    class MyEvent(DomainEvent):
        @property
        def namespace(self) -> str:
            return f"test"

    # when
    instance = MyEvent()

    # then
    assert isinstance(instance, MyEvent)
    assert isinstance(instance, DomainEvent)
    assert instance.name == "test.MyEvent"
