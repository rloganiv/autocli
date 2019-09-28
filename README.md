Automatic CLI
===

Ceate command line interfaces for your Python code in seconds.


Installation
---

```
pip install git+https://github.com/rloganiv/autocli
```


Usage
---

Automatic CLI is very simple, it takes a Python function and turns it into a command-line function.
To do this, all you need to do is add type hints and wrap the function.
For example, you can convert the functions in this `example.py` script:
```python
def hello(name: str) -> None:
    """
    Say hello.

    Parameters
    ==========
    name : str
      Name to greet.
    """
    print(f'Hello {name}!')

def annoying_hello(name: str, repeats: int = 3) -> None:
    """
    Say hello in an obnoxious manner.

    Parameters
    ==========
    name : str
      Name to greet.
    repeats : int
      Number of times to repeat the greeting.
    """
    for _ in range(repeats):
        print(f'Hello {name}!')
```
into terminal commands like so:
```python
import autocli

@autocli.add_command()
def hello(name: str) -> None:
    """
    Say hello.

    Parameters
    ==========
    name : str
      Name to greet.
    """
    print(f'Hello {name}!')

@autocli.add_command()
def annoying_hello(name: str, repeats: int = 3) -> None:
    """
    Say hello in an obnoxious manner.

    Parameters
    ==========
    name : str
      Name to greet.
    repeats : int
      Number of times to repeat the greeting.
    """
    for _ in range(repeats):
        print(f'Hello {name}!')

if __name__ == '__main__':
    autocli.parse_and_run()
```
Now you can use them in the terminal!
```
> python example.py hello --name "world"
Hello world!

> python example.py annoying_hello --name "world" --repeats 2
Hello world!
Hello world!
```
Automatic CLI even knows to use default parameters...
```
> python example.py annoying_hello --name "world"
Hello world!
Hello world!
Hello world!
```
...and can automatically create help documentation if you use NumPy style docstrings.
```
> python example.py annoying_hello -h
usage: example.py annoying_hello [-h] --name NAME [--repeats REPEATS]

Say hello in an obnoxious manner.

optional arguments:
  -h, --help         show this help message and exit
  --name NAME        Name to greet. (default: None)
  --repeats REPEATS  Number of times to repeat the greeting. (default: 3)
```
