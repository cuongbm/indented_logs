Decorators to log function calls with parameter and timing

# Usage

Decorators to track down function call with indent.
Both logging function and indent characters are configurable

**Decorate a function**:

```python
from indented_logs import log_call

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

**Multiple functions**:

```python
from indented_logs import log_call

@log_call()
def get_data():
    get_parameters()
    query_db(conn="sample_conn_str")

@log_call()
def get_parameters():
    pass

@log_call()
def query_db(conn):
    return covert_data("1", "2")

@log_call()
def covert_data(a, b):
    return (int(a), int(b))

get_data()
```

Output:

```python
...CALL: get_data()

......CALL: get_parameters()
......get_parameters RETURN: None
......get_parameters FINISHED in 0.000004 secs


......CALL: query_db(, conn=sample_conn_str)

.........CALL: covert_data(1, 2)
.........covert_data RETURN: (1, 2)
.........covert_data FINISHED in 0.000005 secs

......query_db RETURN: (1, 2)
......query_db FINISHED in 0.000870 secs

...get_data RETURN: None
...get_data FINISHED in 0.002771 secs
```

**Decorate class**:
Using `log_call_cls`

```python
from indented_logs import log_call_cls

@log_call_cls(indent="***", log_time=False, logger_func=log_with_capture)
class MyClass:
    def method1(self, arg1, arg2):
        self.method2(arg1)

    def method2(self, arg1):
        pass

obj = MyClass()
obj.method1("aaaaa", "bbbbbbb")
```

Ouput:

```python
***CALL: method1(aaaaa, bbbbbbb)

******CALL: method2(aaaaa)
******method2 RETURN: None
******method2 FINISHED in 0.000005 secs

***method1 RETURN: None
***method1 FINISHED in 0.000916 secs
```

**Customize indent characters:**

```python
from indented_logs import log_call

@log_call(indent='___')
def method1(arg1, arg2):
    return arg1 + arg2

method1(3, 4)

```

**Turn off logtime:**

```python
from indented_logs import log_call

@log_call(indent='___', log_time=False)
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
pytest -s --cov=src
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
