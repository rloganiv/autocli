import argparse
from argparse import ArgumentDefaultsHelpFormatter
import warnings

import inspect
import typing
from typing import Callable, Generic, Optional, _GenericAlias

from numpydoc.docscrape import NumpyDocString, ParseError


_autocli_parser = argparse.ArgumentParser()
_autocli_subparsers = _autocli_parser.add_subparsers()


def get_origin(tp):
    if isinstance(tp, _GenericAlias):
        return tp.__origin__
    if tp is Generic:
        return Generic
    return None


def get_args(tp):
    """Get type arguments with all substitutions performed.
    For unions, basic simplifications used by Union constructor are performed.
    Examples::
        get_args(Dict[str, int]) == (str, int)
        get_args(int) == ()
        get_args(Union[int, Union[T, int], str][int]) == (int, str)
        get_args(Union[int, Tuple[T, int]][str]) == (int, Tuple[str, int])
        get_args(Callable[[], T][int]) == ([], int)
    """
    if isinstance(tp, _GenericAlias) and not tp._special:
        res = tp.__args__
        return res
    return ()


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
            try:
                param_descs = {p.name: p.desc[0] for p in doc['Parameters']}
            except IndexError:
                raise DocumentationError(
                    f'Error automatically generating documentation from "{name}" docstring.'
                    'Please check that all parameters are properly documented.'
                )
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
            args = [f'--{param_name}',]
            kwargs = {
                'type': param.annotation,
                'help': param_desc
            }
            if param.default == inspect._empty:
                kwargs['required'] = True
            else:
                kwargs['default'] = param.default
            # Special types
            origin = get_origin(param.annotation)
            if origin == list:
                kwargs['nargs'] = '+'
                param_type = get_args(param.annotation)
                if len(param_type) != 1:
                    raise TypeError(
                        'Cannot infer type of List parameter. Make sure exactly one '
                        'type hint is provided.'
                    )
                kwargs['type'] = param_type[0]
            parser.add_argument(*args, **kwargs)
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
