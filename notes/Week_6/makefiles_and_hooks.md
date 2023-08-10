[Previous](code_quality.md) | [Next](terraform_intro.md)

# Using Pre-Commit Hooks for Code Quality Checks

We will be using pre-commit hooks to automate the execution of code quality checks such as formatting, linting, and testing. This will help us ensure that our code adheres to the set standards before it is committed to the repository.

## What are Pre-Commit Hooks?

Pre-commit hooks are scripts that run automatically before each commit is made to the repository. They are used to inspect the snapshot that's about to be committed. If the pre-commit hook script exits with a non-zero status, the commit is aborted.

## Setting Up the Repository

The first step is to initialize a Git repository in your project directory. If your project is not already a Git repository, you can initialize it with the following command:

```bash
git init
```

## Setting Up Pre-Commit Hooks

We will be using the `pre-commit` Python package to manage our pre-commit hooks. To install it, we can use pipenv:

```bash
pipenv install --dev pre-commit
```

Next, we need to create a configuration file for our pre-commit hooks. This file is named `.pre-commit-config.yaml` and should be placed in the root directory of our repository. 

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v3.2.0
  hooks:
    - id: trailing-whitespace
    - id: end-of-file-fixer
    - id: check-yaml
    - id: check-added-large-files
```
This configuration installs four pre-commit hooks from the pre-commit-hooks repository. These hooks will trim trailing whitespace, ensure that files end with a newline, check if YAML files are well formed, and prevent the addition of large files.

You can also add more hooks to your configuration file. For example, you can add the isort and black hooks to sort your imports and format your code, respectively.

```yaml
repos:
  ...
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://github.com/psf/black
    rev: 22.6.0
    hooks:
      - id: black
        language_version: python3.9
```

You can also add local hooks that are run from your local environment. Here's how to add local pylint and pytest hooks:

```yaml
repos:
  ...
  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: pylint
        language: system
        types: [python]
        args: ["-rn", "-sn", "--recursive=y"]
      - id: pytest-check
        name: pytest-check
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: ["tests/"]
```

These hooks will run pylint and pytest on your Python code.

## Running the Pre-Commit Hooks

After setting up the configuration file, we can install the pre-commit hooks using the following command:

```bash
pre-commit install
```

Now, every time we make a commit, the pre-commit hooks will be run automatically. If any of the hooks fail, the commit will be aborted.
For example, if we make a change to a Python file and then try to commit it, the `isort`, `black`, `pylint`, and `pytest-check` hooks will be run. If the file has any import sorting issues, formatting issues, linting issues, or test failures, the commit will be aborted, and we will be shown an error message. This way, we can ensure that all our commits adhere to our code quality standards.


# Using Makefiles

We will be discussing the use of Makefiles for engineering practices. Makefiles serve as a powerful tool to automate the processes of building, testing, and publishing in a project.
A Makefile is a file containing a set of directives used with the make build automation tool. It describes the relationships among files in your program and provides commands for updating each file.

## Understanding the Makefile

The Makefile is broken down into several targets, each performing a specific task:

- `make test`: Runs the pytest tool on the tests directory.
- `make quality_checks`: Runs several quality checks on your Python code.
- `make build`: Ensures that the quality checks and tests pass before building a Docker image.
- `make integration_test`: Runs the `build` target, then runs an integration test script.
- `make publish`: Runs the `build` and `integration_test` targets, then runs a script to publish the Docker image.
- `make setup`: Installs the project dependencies and sets up a pre-commit hook.

## Running the Makefile

We demonstrate the use of the make command to execute the targets defined in the Makefile, thereby automating the tasks involved in building, testing, and publishing a Docker image.
Run any of these targets by typing `make <target>` in your terminal, where `<target>` is replaced by the name of the target you want to run. For example, to run the tests, type:

```bash
make test
```

Next, we will talk about concepts of Infrastructure-as-Code and Terraform. Stay tuned!


[Previous](code_quality.md) | [Next](terraform_intro.md)