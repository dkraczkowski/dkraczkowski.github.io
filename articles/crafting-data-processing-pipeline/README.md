# The Elegance of Modular Data Processing with Python’s Pipeline Approach

Diving into the intricacies of data processing can often feel like navigating an intricate labyrinth. We build these elaborate processes, only to leave them untouched for fear of breaking them. But what if we could improve it? Here's my perspective on crafting a more maintainable, modular data processing workflow in Python which leans into the "pipe and filter" architectural pattern.

## Understanding the Pipe & Filter Paradigm

Imagine a relay race: runners (filters) effortlessly pass the baton (data) in a sequence, following a designated path (pipes). This perfectly encapsulates the "pipe and filter" architecture: data flows through sequential processing units (filters), linked by conduits (pipes) which enable modular transformations. 

Within this framework, elements like Pipeline, Context, and Step shine, complemented by PipelineCursor, PipelineStatus, and PipelineResult.



In our version of this race, key players include the `Pipeline`, `Context`, and `Step`, supported by structures like `PipelineCursor`, `PipelineStatus`, and `PipelineResult`.

> Note: Our narrative centers around synchronous processing. Venturing into asynchronous terrains offers another layer of complexity worth exploring separately.

## The Real-World Relay: A Practical Scenario

Consider this: we're handed a CSV to extract user data and slot it into a database. Sounds straightforward, right? Right? ...

Given below is a sample CSV that encapsulates the kind of data we're dealing with:
```csv
Name,Email,Age
Alice Kooper,alice@example.com,28
Bob Smith,bob_at_example.com,32
Charlie Doe,charlie@example.com,24
David Haselkof,david_example.com,40
```

Before going further, let’s define a class that will represent user's entity we'd store in our database:
```python
from dataclasses import dataclass

@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    age: int
```

To successfully process this data, our solution might be composed of the following logical components:

- _Loading Data and Format Validation_: Is our CSV structurally sound?
- _Data Validation_: Does our data meets the set standards?
- _Uniqueness Verification_: Have we seen this record before, should we import it?
- _User Creation and Storage_: Transform our data for the storage.
- _Metrics Compilation_: What went good, what went wrong, are we satisfied?


## Traditional Tactics

A typical initial thought on tackling this problem might look something like this:

```python
import csv

def import_users_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        
        existing_emails = fetch_existing_emails_from_db()
        
        # Format Validation
        if headers != ["Name", "Email", "Age"]:
            print("Format validation failed, invalid csv file.")
            return

        for row in reader:
            name, email, age = row
            
            # Data validation
            if not (name and email and age.isdigit()):
                print(f"Invalid data for {name}")
                continue
                
            if '@' not in email:
                print(f"Invalid email format for {name}")
                continue 
            
            # Check for uniqueness
            if email in existing_emails:
                print(f"User with email {email} already exists")
                continue   
            
            # Create user entity and store
            first_name, last_name = name.split(" ")
            user = User(first_name=first_name, last_name=last_name, email=email, age=int(age))
            store_user_in_db(user)

    # Metrics
    print(f"Imported {len(existing_emails) - len(fetch_existing_emails_from_db())} users successfully.")

def fetch_existing_emails_from_db():
    return ["example1@email.com", "example2@email.com"]

def store_user_in_db(user):
    print(f"Stored {user.first_name} {user.last_name} in the database.")
```

While this direct method might seem appealing initially, its linearity can become a bottleneck. Over time, the function can become bulky, hard to tweak, and testing can turn into nightmare.

> The start is quick, but the meta might quickly become unreachable.

## Enter: The Pipeline Paradigm

An alternative way to the above implementation might be moving towards more flexible solution involving the pipeline approach.

At our disposal, Python offers two core structures to encapsulate logic; functions and classes.

While each structure shines in its specific scenarios, a universal interface can be crafted using Python's dunder (double underscore) method: `__call__`.

Let's draft a foundational interface, outlining the essential contract for our code:

```python
from typing import Protocol

class PipelineStep(Protocol):
    def __call__(self) -> None:
        ...
```

> For defining our interfaces, we harness the power of Python's Protocol from the typing package. If you're unfamiliar with Protocol, it allows us to define structural subtyping - essentially allowing us to specify what methods a class should have, without mandating inheritance. It's a powerful tool for crafting flexible, well-defined interfaces. If you're keen on deep-diving into Protocol, [Python's official documentation](https://docs.python.org/3/library/typing.html#typing.Protocol) provides an excellent starting point.

That's it? Yeah... not really. 

Although it might seem great at a first sight, it lacks a vital component: input. Input is crucial as it holds the context for executing our logic. Drawing from our relay race metaphor, think of this input as the baton, orchestrating seamless transitions and preserving continuity. Effectively our "baton" should be versitale, be it a stick, a stone, or anything else.

With this in mind let's refine our interface:

```python
from typing import TypeVar, Protocol

Context = TypeVar("Context")

class PipelineStep(Protocol[Context]):
    def __call__(self, context: Context) -> None:
        ...
```

Looks better now... but how do we pass the context to the subsequent runner? 

While returning it seems straightforward, this method inherently favours a linear approach. 
Such a structure can be too restrictive, especially in scenarios demanding alternative routes or altered execution sequences. 

So, what would be a more flexible approach?

Provide a control function `next_step` to our method, which can influence its flow. This opens doors to diverse execution patterns, from pre-step tasks to splitting the pipeline into parallel paths.

```python
from typing import TypeVar, Protocol, Callable, Any, runtime_checkable

Context = TypeVar("Context")
NextStep = Callable[[Any], None]

@runtime_checkable
class PipelineStep(Protocol[Context]):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        ...
```

> Note: The `@runtime_checkable` decorator is another gem from Python's typing module. It allows our Protocol to be used with Python's built-in isinstance checks.

### Implementing the `FormatValidationStep`

With our interface in place, it's time to breathe life into our pipeline by creating concrete implementations - validating the format of incoming files.

```python
import csv
from typing import List

...

class FormatValidationStep:
    def __init__(self, headers: List[str]) -> None:
        self._headers = headers

    @property
    def headers(self) -> List[str]:
        return self._headers

    def __call__(self, context: Context, next_step: NextStep) -> None:
        if not context.file.name.endswith(".csv"):
            raise ValueError("Unsupported file type.")
        context.file.seek(0)
        reader = csv.reader(context.file)
        headers = next(reader)
        self.validate_headers(headers)

        for item in reader:
            record = dict(zip(headers, item))
            context.record = record
            context.total_records += 1
            next_step(context)

    def validate_headers(self, headers: List[str]) -> None:
        if headers != self._headers:
            raise ValueError(f"Invalid headers in the csv file. Expected: {self._headers}, got: {headers}")
```

The `FormatValidationStep` accepts the CSV `headers` as a parameter. These headers define the contract that CSV files need to adhere to when being processed by our pipeline.

The `context` variable in the `__call__` method acts as a shared state across the pipeline steps. The `next_step` function moves us to the next phase. For each CSV record, we execute the entire pipeline. This approach divides the complexity, making each step handle its specific task, promoting simplicity and modularity.


> Note: Additional steps are available on my [Github repository](https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/crafting-data-processing-pipeline/src/example) for brevity.


### The Pipeline

With steps defined, we need a mechanism to string them together and manage their execution in a seamless and coordinated manner. We need the `Pipeline`.

The foundational `Pipeline` class is centered around the steps it will execute. This class provides a way to compose the steps into a pipeline, manage their addition, and track the pipeline's length.

```python
from typing import Generic, TypeVar

...

Context = TypeVar("Context")

class Pipeline(Generic[Context]):
    def __init__(self, *steps: PipelineStep):
        # Dereference list
        self.queue = [step for step in steps]

    def append(self, step: PipelineStep) -> None:
        self.queue.append(step)

    def __call__(self, context: Context) -> None:
        # Here we will execute the steps
        pass

    def __len__(self) -> int:
        return len(self.queue)
```
The intuitive `append` method mirrors the list-like behavior, a familiarity most Python developers would appreciate, it can be helpful in adding new steps to our pipeline.

While the basic architecture of our Pipeline seems intuitive and straightforward, managing the execution of the steps dynamically poses a challenge. How do we ensure each step is executed in sequence, handle exceptions, and account for deviations or alternate paths within the pipeline? While we could be tempted to run all these steps in a loop and wrap it in a try/catch exception block, our `PipelineStep` is designed for adaptability, we don't want to waste its flexible design. One of the strategies I have learned during my career is using an orchestration component, specially designed to keep track of the executed items and providing mechanisms for error handling and managing alternative execution paths. 

### The Pipeline Cursor

Since, we know that our `PipelineStep` accepts the `next_step` callable object for controlling the flow from within the step our `PipelineCursor` must adhere to this interface:

```python
from typing import Generic, TypeVar
...
Context = TypeVar("Context")

class PipelineCursor(Generic[Context]):
    def __call__(self, context: Context) -> None:
        ...
```

For orchestrating the flow, the cursor needs a structure, a queue in this case, to hold and manage the steps:

```python
from typing import Generic, List, TypeVar
...
Context = TypeVar("Context")

class PipelineCursor(Generic[Context]):
    def __init__(self, steps: List[PipelineStep]):
        self.queue = steps
        
    def __call__(self, context: Context) -> None:
        ...
```

Still we are missing the orchestration logic. Again, iteration is not our chosen approach. We're seeking elegance and flexibility. Recursion fits all of the above, this will be our base for the cursor's algorithm. 

To succeed the algorithm must follow a certain path:
    1. Dequeue the `current step` from the pipeline. This ensures we aren't stuck in an infinite execution loop.
    2. Construct a new `next_step` callable, designed to invoke the succeeding step.
    3. Invoke the `current step` with the context and the newly formed `next_step`. Post execution, this `next_step` callable would essentially loop back, triggering the `next step`, and ensuring our recursion continues gracefully.

This method ensures each step has autonomy to control its subsequent actions, offering us a resilient and flexible pipeline architecture.

```python
from typing import Generic, List, TypeVar
...
Context = TypeVar("Context")

class PipelineCursor(Generic[Context]):
    def __init__(self, steps: List[PipelineStep]):
        self.queue = steps

    def __call__(self, context: Context) -> None:
        current_step = self.queue[0]
        next_step = PipelineCursor(self.queue[1:])

        current_step(context, next_step)
```

We should also revisit the `Pipeline` class:

```python
from typing import Generic, TypeVar

...

Context = TypeVar("Context")

class Pipeline(Generic[Context]):
    def __init__(self, *steps: PipelineStep):
        self.queue = [step for step in steps]

    def append(self, step: PipelineStep) -> None:
        self.queue.append(step)

    def __call__(self, context: Context) -> None:
        execute = PipelineCursor(self.queue)

        return execute(context)

    def __len__(self) -> int:
        return len(self.queue)
```

Now we are getting closer, if we try to run the code now:

```python
from dataclasses import dataclass, field
from typing import List
...

@dataclass
class MyContext:
    executed_steps: List[str] = field(default_factory=list)

def my_step(context: MyContext, next_step: NextStep) -> None:
    context.executed_steps.append("step")
    next_step(context)

pipeline = Pipeline(my_step, my_step())
pipeline(MyContext())
```

Attempting this would throw the `IndexError: list index out of range`.  This isn't unusual, but it indicates an area that necessitates our attention: halting the cursor when it's done. To manage this, we implement a check for an empty queue:

```python
from typing import Generic, List, TypeVar
...
Context = TypeVar("Context")

class PipelineCursor(Generic[Context]):
    def __init__(self, steps: List[PipelineStep]):
        self.queue = steps

    def __call__(self, context: Context) -> None:
        if not self.queue:
            return
        current_step = self.queue[0]
        next_step = PipelineCursor(self.queue[1:])

        current_step(context, next_step)
```

Though it addresses the immediate issue, our Pipeline stands as a foundational scaffold, sparking numerous potential directions for further enhancement, including threading, asynchronous processing, or multiprocessing.

To set the right foundations, we are still missing one component of any robust system: Error Handling.

### Anticipating failures

Considering an importing task as an example, and envisioning a scenario where we would like to report the quantity of failed records, it becomes clear that passing a context object to an error handler is necessary. Additionally, for instances where an error isn't critically severe, we would like enable the possibility of continuing pipeline's course. To accommodate this, we'd need the error itself and a way to execute the next step. 

This thought process helps us to build an interface for the error handler:

```python
from typing import Callable
...

ErrorHandler = Callable[[Exception, Context, NextStep], None]
```

In this layout, our error handler will accept an exception, context, and a next step to meet all our requirements. Since no return is needed here, the output is designated as `None`.

With the `ErrorHandler` interface in place, it's now time to integrate it with our `Pipeline` and `PipelineCursor`.

Let's combine everything:

```python
from __future__ import annotations

from abc import abstractmethod
from typing import Generic, List, TypeVar, Callable, Protocol, Generator, Union, Iterable, Optional

Context = TypeVar("Context")


class PipelineError(Exception):
    pass


NextStep = Callable[[Context], Iterable[Union[Exception, Context]]]
ErrorHandler = Callable[[Exception, Context, NextStep], None]


class PipelineStep(Protocol[Context]):
    @abstractmethod
    def __call__(
        self, context: Context, next_step: NextStep
    ) -> Generator[Context]:
        ...


def _default_error_handler(error: Exception, context: Context, next_step: NextStep) -> None:
    raise error


class PipelineCursor(Generic[Context]):
    def __init__(self, steps: List[PipelineStep], error_handler: ErrorHandler):
        self.queue = steps
        self.error_handler: ErrorHandler = error_handler

    def __call__(self, context: Context) -> None:
        if not self.queue:
            return
        current_step = self.queue[0]
        next_step = PipelineCursor(self.queue[1:], self.error_handler)

        try:
            current_step(context, next_step)
        except Exception as error:
            self.error_handler(error, context, next_step)


class Pipeline(Generic[Context]):
    def __init__(self, *steps: PipelineStep):
        self.queue = [step for step in steps]

    def append(self, step: PipelineStep) -> None:
        self.queue.append(step)

    def __call__(self, context: Context, error_handler: Optional[ErrorHandler] = None) -> None:
        execute = PipelineCursor(self.queue, error_handler or _default_error_handler)
        execute(context)

    def __len__(self) -> int:
        return len(self.queue)
```

> Please note: `_default_error_handler` function was added here to simplify `PipelineCursor` implementation.

## Conclusion

Using a pipeline approach just makes things easier and more reliable. It helps manage and change data efficiently, increase the maintainability, testability, and guiding towards better practices.

> The complete code, along with various test scenarios and the finalized pipeline, are available on my [GitHub](https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/crafting-data-processing-pipeline/src)
