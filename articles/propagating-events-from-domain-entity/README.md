# Events in Domain-Driven Design: Event Propagation Strategies

A few days ago, I engaged in an interesting exchange with a fellow developer about a common dilemma in event-driven architecture: how to effectively broadcast domain events to external listeners keen on processing this information.

We revisited three known strategies for event propagation:

- **Internal Event Collection**: This involves collating events within the entity itself and later exposing them via a property.
- **Static Publication Mechanism**: This method leverages a shared event bus or message broker, often implemented as a singleton, directly within the entity.
- **Events as a Result of Method Invocation**: In this case, events are returned as an iterable collection or a generator when an entity's method is called.

Additionally, I proposed a fourth, equally viable technique:

- **Ad-hoc Event Bus Injection**: This involves passing an event bus into the entity, specifically to facilitate the dissemination of events.

In the following sections, I will elaborate on these four methodologies, discussing their potential advantages and drawbacks. We will also delve into Python code examples to illustrate how we can practically implement each strategy.

## Setting Up Our Example Domain Model

Let's consider a wallet entity that processes a transaction which could result in multiple distinct events: a `FundsDeposited` event if money is added to the account, a `FundsWithdrawn` event if money is taken out, an `OverdraftLimitHit` and the following `WalletLocked` event if the transaction results in the wallet hitting its overdraft limit and `OverdraftOccured` when wallet hits a negative value.

```python
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
```

As you may have noticed, the events in the code are instantiated but not yet dispatched/propagated. We will introduce the propagation mechanisms when we explore each of the strategies, simultaneously underscoring the advantages and disadvantages inherent to each method.

> Note: All the events are providing a `namespace` property. Main purpose of this procedure is to logically separate and organise events. It helps to avoid name collisions, brings in scalability and clarity. This approach shines in scenarios where your system becomes more complex and distributed.

## Propagation

### Internal Event Collection

The Internal Event Collection pattern is an approach where an entity collects domain events that occur during its lifecycle. These events are held internally within the entity until they can be processed at an appropriate time, usually at the end of the transaction or operation that involved the entity.

To implement this pattern in our Wallet entity, we can add an internal list to hold events:

```python
from typing import List

from domain.entity import Entity
from domain.event import DomainEvent
from domain.money import Money

...


class Wallet(Entity):
    def __init__(self, overdraft_limit: Money) -> None:
        ...
        self._events = []

    def _record_event(self, event: DomainEvent):
        self._events.append(event)

    def collect_events(self) -> List[DomainEvent]:
        events = self._events[:]
        self._events = []
        return events
```

In this setup, the `_record_event` method should be invoked to collect the generated events. Any service manipulating the entity would then retrieve these events for downstream processing by calling `collect_events` method.

The primary advantage of this pattern lies in its straightforwardness and its transactional nature — all events are gathered and can be handled en masse.

On the downside, this pattern introduces additional responsibilities to the entity (which could be seen as a violation of the Single Responsibility Principle) and creates a potential for tight coupling. It also introduces a lag in event handling; events are not processed in real time but at a subsequent point.

> Internal Event Collection is particularly advantageous for transactional event handling within a bounded context, where immediate system-wide visibility of domain events is not that important.
> Complete code is available [here](https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/propagating-events-from-domain-entity/src/domain/wallet_internal_event_collection.py)

### Static Publication Mechanism

The Static Publication Mechanism is an alternative pattern where domain events are published immediately and statically from within the entity itself. This method relies on a static event dispatcher or event bus that is accessible globally within the application context.

Incorporating this into our Wallet entity would require us to integrate a static event bus within our domain logic:

```python
from abc import abstractmethod
from typing import Protocol

from domain.entity import Entity
from domain.event import DomainEvent


class EventBus(Protocol):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        ...


class DummyEventBus:
    def __init__(self) -> None:
        self._events = []

    def publish(self, event: DomainEvent) -> None:
        self._events.append(event)


class GlobalEventBus:
    event_bus: EventBus

    @classmethod
    def publish(cls, event: DomainEvent) -> None:
        cls.event_bus.publish(event)

    @classmethod
    def init(cls) -> None:
        cls.event_bus = DummyEventBus()


GlobalEventBus.init()

class WalletLocked(DomainEvent):
    ...

# Event definitions omitted for brevity

class Wallet(Entity):
    ...
    
    def lock_wallet(self) -> None:
        self.locked = True
        GlobalEventBus.publish(WalletLocked(self.id, self.balance))
```

By integrating this pattern, entities immediately communicate with the event bus to publish events, dispensing with the need to store them.

The merits of this method are apparent: instant feedback as events are processed at once, crucial for time-sensitive operations, and an uncomplicated, decoupled design of entities—entities solely emit events and do not oversee their lifecycles.

However, this can introduce global state complexities, potentially complicating test scenarios, and introducing hidden dependencies. A global state may also be prone to misuse, potentially resulting in the inadvertent broadcast of events, and it can compromise transactional integrity since events could be published even when the initiating operations are at risk of failing.


> The Static Publication Mechanism fits scenarios demanding prompt event processing and when operations are unlikely to require rollback.
> Complete code is available [here](https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/propagating-events-from-domain-entity/src/domain/wallet_static_publication_mechanism.py)


### Events as a Result of Method Invocation

Another great pattern for event propagation within domain-driven design is to have methods directly return the events they generate. This method not only changes the state of the entity but also produces a result-in this case, an event or a sequence of events that indicate what changes have occurred.

To apply this pattern to our Wallet entity, we might refactor the `transact` method to yield events as they occur:

```python
from domain.entity import Entity
from domain.event import DomainEvent
from domain.money import Money
from typing import Iterator

...

class Wallet(Entity):
    ...
    
    def transact(self, amount: Money) -> Iterator[DomainEvent]:
        ...
            yield FundsDeposited(self.id, amount)
        ...
```
> Complete code is available [here](https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/propagating-events-from-domain-entity/src/domain/wallet_event_as_a_result_of_method_invocation.py)

In this approach, events become immediate outcomes of the transact method, offering a clear and expressive way of indicating the effects of an operation. This explicitness can be particularly valuable in testing scenarios, as it simplifies the assessment of outcomes without the need to inspect the internal state of the entity.

However, this explicitness can be a double-edged sword. On one hand, it does indeed simplify the entity's internals by doing away with the need for an event collection mechanism. On the other hand, it increases the responsibility of the method's caller to correctly handle these events, adding a layer of complexity to the client code.


In addition to the approach where events are yielded as an iterator, a sibling implementation might collect events within the entity and return them as a single collection upon method completion. This variation merges the explicitness of the direct-yield approach with the benefits of internal event collection, offering a snapshot of all events resulting from a method's execution in one package. However, it does not afford the instant feedback provided by yielding events as they occur. 


> This approach to event propagation by direct method result is particularly applicable for systems where the clear delineation of operation outcomes is required and where the subsequent event handling is orchestrated outside the entity's boundaries.

### Event Bus Injection
In this variant of event propagation, the method does not return events or declare them statically but instead receives an event bus as a parameter. This strategy hinges on the use of an interface to abstract the event handling, creating a clear separation between entity's responsibilities and event propagation. An optional event bus parameter also serves to simplify the interface, offering greater adaptability in how events are managed.

Here's a snapshot of how this would be set up:
```python
from domain.entity import Entity
from domain.money import Money
from domain.event import DomainEvent
from typing import Optional, Protocol

class EventBus(Protocol):
    def publish(self, event: DomainEvent) -> None:
        ...

class InMemoryEventBus:
    def __init__(self) -> None:
        self._events = []

    def publish(self, event: DomainEvent) -> None:
        self._events.append(event)
...

class Wallet(Entity):
    ...

    def transact(self, amount: Money, event_bus: Optional[EventBus] = None) -> None:
        if event_bus is None:
            event_bus = InMemoryEventBus()
        ...
            event_bus.publish(FundsDeposited(self.id, amount))
        ...
```
> Complete code is available [here](https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/propagating-events-from-domain-entity/src/domain/wallet_event_bus_injection.py)

The key advantage of injecting an event bus is the decoupling it achieves; the entity's methods can remain agnostic to the intricacies of event handling and distribution. This maintains a clean separation of concerns and facilitates a lightweight, uncluttered domain model.

On the downside, this approach necessitates an additional parameter, which can slightly complicate method signatures. This might be seen as a burden, especially in contexts where event handling is not always needed. Yet, this is a relatively minor inconvenience when weighed against the benefits of such an adaptable and decoupled system.

> This method is particularly suitable for scenarios where clean architecture and flexibility are prioritized. It effectively avoids the global state and the coupling issues associated with static event publication.


# Wrap Up
Alright, we’ve taken quite the tour through the different ways you can handle event propagation in your domain 
entities. Staring from a simple strategy and ending up with a external-focused solution. Which one should you consider? 

The real trick is finding which pattern plays nice with your architecture and simplifies your life. Whether you’re all about that immediate feedback or you're looking to keep your entities clean and mean, your choice sets the stage for how your application behaves.

Happy Coding!
