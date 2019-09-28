import argparse
from argparse import ArgumentDefaultsHelpFormatter
import warnings

import inspect
from typing import Callable, Optional

from numpydoc.docscrape import NumpyDocString


_autocli_parser = argparse.ArgumentParser()
_autocli_subparsers = _autocli_parser.add_subparsers()


def add_command(docstring_parser=NumpyDocString) -> Callable:
    def decorator(function: Callable) -> Callable:
        name = function.__name__

        # Try to parse docstring
        try:
            doc = docstring_parser(function.__doc__)
        except ParseError:
            doc = dict()

        # Get summary from docstring
        if 'Summary' in doc:
            description = doc['Summary'][0]
        else:
            description = None

        # Get parameter descriptions from docstring
        if 'Parameters' in doc:
            param_descs = {p.name: p.desc[0] for p in doc['Parameters']}
        else:
            param_descs = dict()

        # Create parser
        parser = _autocli_subparsers.add_parser(name,
                                                description=description,
                                                formatter_class=ArgumentDefaultsHelpFormatter)

        # Add parameters to parser
        signature = inspect.signature(function)
        for param_name, param in signature.parameters.items():
            param_desc = param_descs.get(param_name, None)
            if param.default == inspect._empty:
                parser.add_argument(f'--{param_name}',
                                    required=True,
                                    type=param.annotation,
                                    help=param_desc)
            else:
                parser.add_argument(f'--{param_name}',
                                    default=param.default,
                                    type=param.annotation,
                                    help=param_desc)

        parser.set_defaults(_autocli_function=function)
        return function
    return decorator


def parse_and_run():
    args = _autocli_parser.parse_args()
    if '_autocli_function' in dir(args):
        function = args._autocli_function
        del args._autocli_function
        function(**vars(args))
    else:
        _autocli_parser.print_help()
