# Crafting a CI Pipeline: My Experience with GitHub Actions, Python and AWS

Integrating code consistently and ensuring it meets best practices is challenging but essential. Today, I aim to share a reliable GitHub Actions setup that I've tailored specifically for Python Serverless projects on AWS. Additionally, I'll introduce a Makefile I've designed to streamline task management. Armed with these tools, our goal is to craft software that's both well-crafted and robust.

Let's go!

> CI pipeline we are going to build will be relying on poetry: if you aren't already using it, I highly recommend giving it a glance. [Poetry](https://python-poetry.org) is a remarkable tool that provides a seamless way to manage dependencies, and ensuring a unified and reproducible build environment.

## The Magic of the "Makefile"

While the Makefile isn't frequently associated with the Python ecosystem, it's an invaluable asset when it comes to task simplification. The Makefile we'll be discussing not only facilitates executing commands on our local setup but also streamlines operations in both our CI and upcoming CD pipeline.

In our Makefile we will focus on:

 - ___Initialising___ our local environment.
 - ___Reformatting code___. It's crucial to ensure our code adheres to `PEP` standards, along with the unique coding norms set by our team.
 - ___Linting___. Linting conducts a static analysis to pinpoint potential discrepancies related to the use of mismatched or incorrect data types. This preemptive measure averts runtime errors, leading to a hassle-free development cycle and a more robust end product.
 - __Executing Tests__.
 - ___Auditing___ our codebase to uncover possible security risks.

By including these tasks, we streamline the setup and upkeep of our codebase. It becomes less arduous for developers to chip in and work together.

### The Header
Below is a glimpse of our Makefile's header:

```makefile
-include .env
SOURCE_DIR = src
TEST_DIR = tests
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_NAME ?= my-project
PROJECT_VERSION ?= v$(shell poetry version -s)
PYTHON_VERSION ?= 3.11
.DEFAULT_GOAL := all
```

This header provides vital configurations and default settings for the project. Now, let's unpack it:

```makefile
- include .env
```
This line incorporates the `.env` file, usually housing environment-specific configurations. The preceding `-` indicates that 'make' shouldn't halt if the file is missing or triggers an error.

```makefile
SOURCE_DIR = src
TEST_DIR = tests
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)
```
These lines designate our directory names, i.e., the source directory, tests directory, and project directories (comprising both the source and tests directories).

```makefile
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
```
Fetches the present working directory of the Makefile. This will be pivotal for certain tasks down the line.

```makefile
PROJECT_NAME ?= my-project
PROJECT_VERSION ?= v$(shell poetry version -s)
PYTHON_VERSION ?= 3.11
```
Here, we establish conditional values. If a particular value hasn't been set in our environment variables, these lines will set it.

```makefile
.DEFAULT_GOAL := all
```

This sets the default objective for the Makefile to `all`. If you execute the 'make' command without mentioning a target, it will default to running the `all` target.

Time to delve into defining our tasks!

### Tasks

```makefile
-include .env
SOURCE_DIR = src
TEST_DIR = tests
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_NAME ?= my-project
PROJECT_VERSION ?= v$(shell poetry version -s)
PYTHON_VERSION ?= 3.11
.DEFAULT_GOAL := all

init-env:
    touch .env
    echo "PROJECT_NAME=${PROJECT_NAME}" >> .env
    echo "PYTHON_VERSION=${PYTHON_VERSION}" >> .env

init:
    init-env
    poetry install

-reformat-toml:
    poetry run toml-sort pyproject.toml --all --in-place
    poetry check

-reformat-src:
    poetry run black $(PROJECT_DIRS)
    poetry run isort $(PROJECT_DIRS)

-lint-src:
    poetry run ruff check $(SOURCE_DIR)
    poetry run mypy --install-types --show-error-codes --non-interactive $(SOURCE_DIR)

format: -reformat-toml -reformat-src

lint: -lint-src

audit:
    poetry run bandit -r $(SOURCE_DIR) -x $(TEST_DIR)

test:
    poetry run pytest $(TEST_DIR)

all: format lint audit test

info:
    echo "Project version: ${PROJECT_VERSION}"
    echo "Project name: ${PROJECT_NAME}"
    echo "Python version: ${PYTHON_VERSION}"
```

The tasks in our Makefile rely on poetry, as previously highlighted. Notably, some tasks begin with a `-` sign. I employ this convention to designate _"private"_ tasks, signifying they are intended for internal use and shouldn't be invoked outside the Makefile's context. 
> I'm curious to hear your thoughts on this approach and the broader integration of Makefiles within the Python ecosystem.

## My Tried and Battle-Tested GitHub Actions Workflow

Below is the GitHub Actions template that has become an indispensable tool in my development toolkit:

```yaml
name: CI Pipeline

on:
  pull_request:
    branches:
      - dev
      - test
      - main

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Setup Poetry
        run: |
          pip install poetry
          poetry config virtualenvs.create true
          poetry config virtualenvs.in-project true
      - name: Install dependencies from cache
        id: poetry-cache
        uses: actions/cache@v2
        with:
          path: .venv
          key: poetry-ci-dependencies-${{ hashFiles('**/poetry.lock') }}
      - name: Install dependencies
        run: poetry install --no-interaction --no-root
        if: steps.poetry-cache.outputs.cache-hit != 'true'

      - name: Formatting
        run: |
          make format
  lint-source:
    needs: format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Setup Poetry
        run: |
          pip install poetry
          poetry config virtualenvs.create true
          poetry config virtualenvs.in-project true
      - name: Install dependencies from cache
        id: poetry-cache
        uses: actions/cache@v2
        with:
          path: .venv
          key: poetry-ci-dependencies-${{ hashFiles('**/poetry.lock') }}
      - name: Install dependencies
        run: poetry install --no-interaction --no-root
        if: steps.poetry-cache.outputs.cache-hit != 'true'

      - name: Linting
        run: |
          make lint
  tests:
    needs: format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start container with dependencies
        run: docker-compose -f "docker-compose.yml" up -d --build
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Setup Poetry
        run: | 
          pip install poetry
          poetry config virtualenvs.create true
          poetry config virtualenvs.in-project true
      - name: Install dependencies from cache
        id: poetry-cache
        uses: actions/cache@v2
        with:
          path: .venv
          key: poetry-tests-dependencies-${{ hashFiles('**/poetry.lock') }}
      - name: Install dependencies
        run: poetry install --no-interaction --no-root
        if: steps.poetry-cache.outputs.cache-hit != 'true'
      - name: Run tests
        run: |
          make test
  audit:
    needs:
      - format
      - tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Setup Poetry
        run: | 
          pip install poetry
          poetry config virtualenvs.create true
          poetry config virtualenvs.in-project true
      - name: Install dependencies from cache
        id: poetry-cache
        uses: actions/cache@v2
        with:
          path: .venv
          key: poetry-ci-dependencies-${{ hashFiles('**/poetry.lock') }}
      - name: Install dependencies
        run: poetry install --no-interaction --no-root
        if: steps.poetry-cache.outputs.cache-hit != 'true'

      - name: Run audit
        run: |
          make audit
```

> If you are new to GitHub Actions, this template might seem a bit overwhelming. However, it's quite straightforward once you get the hang of it. Each template begins with a `name` and `on` section. The `name` section is self-explanatory, while the `on` section defines the triggers for the pipeline. Lastly, we have the `jobs` section, which is where the magic happens.

> To learn more about GitHub Actions, check out the [official documentation](https://docs.github.com/en/actions).

This pipeline activates every time a pull request targets the `dev`, `test`, or `main` branch. Depending on your workflow, these triggers can be tailored to fit your needs.

I've established four jobs in this workflow, each corresponding to the tasks we discussed in our Makefile: `format`, `lint`, `tests`, and `audit`. 

The structure of each job is methodical:
    
__Environment Setup__: We initiate with setting up the desired Python version using the actions/setup-python action. ```

- __Poetry Configuration__: Poetry is then installed and configured to manage our project's dependencies.
- __Dependency Management__: Before installing dependencies, an attempt is made to restore them from cache to expedite the CI process. If this step is unsuccessful, poetry installs them anew.
- __Task Execution__: Finally, a corresponding task from our Makefile is executed, ensuring that the CI environment mirrors our local development setup closely.

You might notice that certain jobs depend on others within this workflow. For instance, the __`lint`__ job depends on the successful completion of the __`format`__ job. This structure is intentional, ensuring that more resource-intensive tasks are executed only if their preceding tasks succeed. 
This dependency chain is managed using the __`needs`__ section.

Makefile usage within our CI pipeline, guarantees a harmonized development and testing environment, minimizing unexpected discrepancies between local and CI builds.

> All the code discussed in this article, as always is available on my GitHub repository. You can find it [here](https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/github_actions_python_aws).

## Conclusion

Throughout this article, we've explored a CI pipeline that I've found to be a reliable and robust solution for Python Serverless projects on AWS. We've also discussed a Makefile that streamlines task management and ensures consistency between our local and CI environments.

In the upcoming article in this series, we'll explore how to leverage this pipeline to deploy our code to AWS Lambda. Stay tuned!

That's all folks!
