import argparse
import inspect
from typing import Callable, Optional


_autocli_parser = argparse.ArgumentParser()
_autocli_subparsers = _autocli_parser.add_subparsers()


def add_command(name: str, help: Optional[str] = None) -> Callable:
    parser = _autocli_subparsers.add_parser(name, help=help)
    def decorator(function: Callable) -> Callable:
        signature = inspect.signature(function)
        for param_name, param in signature.parameters.items():
            parser.add_argument(f'--{param_name}', type=param.annotation, default=param.default)
        parser.set_defaults(_autocli_function=function)
        return function
    return decorator


def parse_and_run():
    args = _autocli_parser.parse_args()
    function = args._autocli_function
    def args._autocli_function
    function(**vars(args))