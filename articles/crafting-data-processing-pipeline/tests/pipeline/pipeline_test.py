from dataclasses import dataclass, field
from typing import Dict, Any, List, Generator, Iterable

from pipeline.pipeline import Pipeline, PipelineStep, NextStep


def test_can_instantiate_pipeline() -> None:
    # given
    class PipelineContext:
        record: Dict[str, Any]

    class MyStep:
        def __call__(self, context: PipelineContext, next_step: NextStep) -> None:
            pass

    # when
    instance = Pipeline[PipelineContext](
        MyStep()
    )

    # then
    assert isinstance(instance, Pipeline)


def test_can_run_pipeline() -> None:
    # given
    @dataclass
    class Context:
        executed_steps: List[PipelineStep] = field(default_factory=list)

    class MyStep:
        def __init__(self, name: str) -> None:
            self.name = name

        def __call__(self, context: Context, next_step: NextStep) -> None:
            context.executed_steps.append(self)
            next_step(context)

        def __repr__(self) -> str:
            return f"Step({self.name})"

    context = Context()
    steps = [MyStep("step-1"), MyStep("step-2"), MyStep("step-3"), MyStep("step-4"), ]
    pipeline = Pipeline[Context](*steps)

    def _error_handler(error: Exception, context: Context, next_step: NextStep) -> None:
        next_step(context)

    # when
    pipeline(context, _error_handler)

    # then
    assert context.executed_steps == steps

