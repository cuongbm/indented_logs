Decorators to log function calls with parameter and timing

# Usage

Decorators to track down function call with indent.
Both logging function and indent characters are configurable

**Decorate a function**:

```python
@log_call()
def method1(arg1, arg2):
    return arg1 + arg2
method1(3, 4)
```

Output:

```python
...CALL: method1(3, 4)
...'method1' RETURN: 7
...'method1' FINISHED in 0.000003 secs
```

**Customize indent characters**:

```python
@log_call(indent='___')
def method1(arg1, arg2):
return arg1 + arg2
method1(3, 4)

```

Output:

```python

___CALL: method1(3, 4)
___'method1' RETURN: 7
___'method1' FINISHED in 0.000006 sec

```

# Development

## Conda environment

Create conda environment

```console
conda env create -f environment.yml
```

If any dependency is added, remember to update conda environment file

```console
conda env export --from-history > environment.yml
```

## Tests

Run using pytest:

```console
pytest --cov=src
```

## Build and publish

Increase the version number in setup.py, run:

```console
python -m build .
```

Publish to test Pypi:

```console
python -m twine upload --repository testpypi dist/* --skip-existing
```

Publish to Pypi:

```console
python -m twine upload --repository pypi dist/* --skip-existing
```
