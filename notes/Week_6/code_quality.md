[Previous](tests.md) | [Next](makefiles_and_hooks.md)

# Code Quality: Using Pylint, Black, and isort

In this tutorial, we will learn how to improve the quality of our Python code using three tools: Pylint, Black, and isort. These tools help us to maintain a consistent code style, catch potential errors and bugs, and automatically format our code.

## Setting Up Pylint

Pylint is a tool that checks for errors in Python code, and enforces a coding standard. It can also look for certain type errors, it can recommend suggestions about how particular blocks can be refactored and can offer you details about the code's complexity.

Let's start by installing Pylint:

```bash
pipenv install --dev pylint
```

To run Pylint on your Python script, you can use the following command:

```bash
pipenv shell
pylint model.py
```

Pylint will then print a report that includes information about any issues it found in your code.

If you want to run Pylint on all Python files in the current directory and all its subdirectories, you can use the `--recursive=y` option:

```bash
pylint --recursive=y .
```

## Customizing Pylint with [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)

You can customize the behavior of Pylint using a `pyproject.toml` configuration file. Here is an example configuration:

```toml
[tool.pylint.messages_control]
disable = [
    "missing-function-docstring",
    "missing-final-newline",
    "missing-class-docstring",
    "missing-module-docstring",
    "invalid-name",
    "too-few-public-methods"
]
```

This configuration disables certain Pylint warnings such as missing docstrings, invalid names, and classes with too few public methods.

## Using Black for Code Formatting

Black is a code formatter for Python. It helps to maintain a consistent code style, and can automatically format your code.

First, let's install Black:

```bash
pipenv install --dev black
```

Once Black is installed, you can run it on a Python file or directory like this:

```bash
black .
```

This will reformat all the Python files according to the Black code style.

If you want to see what changes Black will make without actually applying them, you can use the `--diff` option:

```bash
black --diff . | less
```
This command will output a diff of the changes that Black would make to the files in the current directory and all its subdirectories. The `| less` part of the command pipes the output to the `less` command, which lets you scroll through the diff.


## [Customizing Black](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)

Black's formatting can be also customized:

```toml
[tool.black]
line-length = 88
target-version = ['py39']
skip-string-normalization = true
```

where we setting the maximum line length to 88 characters, specifying that the target Python version is 3.9, and telling Black to skip string normalization (i.e., it won't change single quotes to double quotes).

In conclusion, Black is a useful tool for maintaining a consistent code style in your Python projects. By automatically formatting your code, it can save you time and help you focus on writing code rather than worrying about formatting.

## Using isort for Import Sorting

isort is a Python utility / library to sort imports alphabetically, and automatically separated into sections and by type. It provides a command line utility, Python library and plugins for various editors to quickly sort all your imports.

First, let's install isort:

```bash
pipenv install --dev isort
```

Once isort is installed, you can run it on a Python file or directory like this:

```bash
isort .
```

This will sort and organize the imports in all Python files in the current directory and its subdirectories according to the isort style.

If you want to see what changes isort will make without actually applying them, you can use the `--diff` option:

```bash
isort --diff . | less
```

## Customizing [isort](https://pycqa.github.io/isort/docs/configuration/config_files.html)

isort's behavior can be customized using a configuration file (pyproject.toml). Here is an example configuration:

```toml
[tool.isort]
multi_line_output = 3
length_sort = true
```

where we are setting the `multi_line_output` option to 3, which tells isort to use a style that puts each import on its own line. We're also setting `length_sort` to true, which tells isort to sort imports by their length.

## Running the Tools

You can run these tools in the following order:

1. Run isort to sort the imports.
2. Run Black to format the code.
3. Run Pylint to catch any remaining issues.
3. Run pytest tests/ after all the code quality checks have passed


By running these in this order, you can ensure that your code is clean, well-formatted, and works as expected.

Next, we will look at how to use Makefiles and pre-commit hooks to further automate our development workflow. See you soon!


[Previous](tests.md) | [Next](makefiles_and_hooks.md)
