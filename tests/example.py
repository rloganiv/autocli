from typing import List

import autocli


@autocli.add_command()
def hello(name: str) -> None:
    """
    Say hello

    Parameters
    ==========
    name : str
        Who to say hi to.
    """
    print(f'Hello {name}!')


@autocli.add_command()
def annoying_hello(name: str, repeats: int = 3) -> None:
    """
    Say lots of hellos

    Parameters
    ==========
    name : str
        Who to say hi to.
    repeats : int
        How many times.
    """
    for _ in range(repeats):
        print(f'Hello {name}!')


@autocli.add_command()
def read_list(elements: List[str]) -> None:
    """
    Read a list of elements and print them to stdout

    Parameters
    ==========
    elements : List[str]
        List of elements to print out.
    """
    print(elements)


if __name__ == '__main__':
    autocli.parse_and_run()
