Automatic CLI
===

Ceate command line interfaces for your Python code in seconds.


Installation
---

```{bash}
pip install git+https://github.com/rloganiv/autocli
```


Usage
---

Automatic CLI is very simple, it takes a Python function and turns it into a command-line function.
To do this, all you need to do is add type hints and wrap the function.
For example, you can convert the `add` and `multiply` functions in this `math.py` script:
```{python}
def add(a: int, b: int) -> int:
    print(a + b)

def multiply(a: int, b: int) -> int:
    print(a * b)
```
into terminal commands like so:
```{python}
import autocli

@autocli.register_command('add')
def add(a: int, b: int) -> int:
    print(a + b)

@autocli.register_command('multiply')
def multiply(a: int, b: int) -> int:
    print(a * b)

if __name__ == '__main__':
    autocli.parse_and_run()
```
Now you can use `add` and `multiply` in the terminal!
```{bash}
> python math.py add 1 2
3
> python math.py multiply 1 2
2