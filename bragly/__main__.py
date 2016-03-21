#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point(s) for the command line interface"""
from bragly.cli import parse_args, parse_utility_args
import sys


def main(args=None):
    """Either takes arguments or gets them from sys.argv. Calls the bragly.cli
        parsing function parse_args, and then executes the returned function.
        See the usage at the command line by passing --help as an option.
    Args:
        args (list): A list of arguments that would be in sys.argv. If None,
            args will be populated from sys.argv.

    Returns:
        int:
            0 - If the program runs without exception.
            1 - If the program runs but there is an unexpected exception
            2 - If the program runs and no arguments are parsed form the command
                line.
    """
    if args is None:
        args = sys.argv[1:]
    parser, args = parse_args(args)
    if not args:
        parser.print_help()
        return 2

    func = args.pop('func', None)
    if func is None:
        print("Operation failed for unexpected reason")
        return 1
    results = func(**args)
    for result in results:
        print(result, flush=True)
    return 0

def util(args=None):
    """Entry point for brag utilities.

    Args:
        args (list): A list of arguments that would be in sys.argv. If None,
            args will be populated from sys.argv.

    Returns:

    """
    if args is None:
        args = sys.argv[1:]
    parser, args = parse_utility_args(args)
    if not args:
        parser.print_help()
        return 2

    func = args.pop('func', None)
    if func is None:
        print("Operation failed for unexpected reason")
        return 1
    results = func(**args)
    for result in results:
        print(result, flush=True)
    return 0


if __name__ == '__main__':
    main()
