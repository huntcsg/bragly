# -*- coding: utf-8 -*-
"""Represents the needed functions and logic for a command line interface."""

import argparse
from bragly.brag import write, read, search, init, PERSIST_CHOICES
from bragly.config import BRAG_DIR, CONFIG_FILE_PATH
import arrow


def parse_args(args):
    """Parses arguments and dispatches the commands and argumnets to the
        appropriate sub parser using argparse.ArgumentParser.parse_args.
        Essentially, based on the commands given, returns a dictionary of
        options. One of the keys is "func" which is a function object
        from bragly.brag that maps to the given command.

    Args:
        args: The argments from sys.argv


    Returns:
        argpaser.ArgumentParser, dict: The parser object and a dictionary of
            options.
    """

    parser = argparse.ArgumentParser(prog='brag')
    subparsers = parser.add_subparsers(help='sub command help')

    # Writ command sub  parser
    write_parser = subparsers.add_parser('w', help='Write a new brag entry')
    write_parser.add_argument('message', metavar='message', nargs='+', type=str,
                              help='The brag message')
    write_parser.add_argument('-t', '--tags', nargs='*', type=str,
                              help='The tags associated with this brag message')
    write_parser.add_argument('-d', '--timestamp', type=arrow.get,
                              help='The time stamp to use for this entry, in ISO-8601 format')
    write_parser.set_defaults(func=write)

    # Read command sub parser
    read_parser = subparsers.add_parser('r',
                                        help='Read a group of brag entries')
    read_parser.add_argument('-s', '--start', type=arrow.get,
                             help="The start time for getting entries")
    # End date spec
    read_parser_enddate_group = read_parser.add_mutually_exclusive_group()
    read_parser_enddate_group.add_argument(
        '-p',
        '--period',
        type=str,
        help='The time period after the start datetime to get entires. One of hour, day, week, month, year'
    )
    read_parser_enddate_group.add_argument('-e', '--end', type=arrow.get,
                                           help='The end time for getting entries')
    # Other read options
    read_parser.add_argument(
        '-f',
        '--form',
        type=str,
        default='json',
        help='The format to display the results in. One of json, json-pretty, log. Default: %(default)s'
    )
    # Set the operation that will be called based on the command
    read_parser.set_defaults(func=read)

    # Search Command Sub parser
    search_parser = subparsers.add_parser('s',
                                          help='Search for a group of brag entries')
    search_parser.add_argument(
        '-s',
        '--start',
        type=arrow.get,
        help="The start time for getting entries",
    )
    # End date spec
    search_parser_enddate_group = search_parser.add_mutually_exclusive_group()
    search_parser_enddate_group.add_argument(
        '-p',
        '--period',
        type=str,
        help='The time period after the start datetime to get entires. One of hour, day, week, month, year'
    )
    search_parser_enddate_group.add_argument('-e', '--end', type=arrow.get,
                                             help='The end time for getting entries')
    # Other search options
    search_parser.add_argument('-t', '--tags', nargs='*', type=str,
                               help='Tags you want to search for')
    search_parser.add_argument('-x', '--text', nargs='*', type=str,
                               help='Keywords you want to search for')
    search_parser.add_argument(
        '-f',
        '--form',
        type=str,
        default='json',
        help='The format to display the results in. One of json, json-pretty, log. Default: %(default)s'
    )
    any_all_group = search_parser.add_mutually_exclusive_group()
    any_all_group.add_argument(
        '--any',
        action='store_true',
        help='Indicates that a result should be returned if it has at least one match in either tags or text.',
        default=True
    )
    any_all_group.add_argument(
        '--all',
        action='store_true',
        help='Indicates that a result should be returned if it matches all tags and text criteria.')

    # Set the operation that will be called based on the command
    search_parser.set_defaults(func=search)

    args = vars(parser.parse_args(args))
    # Do some additonal argument parsing if this is a search command
    if 'func' in args:
        if args['func'].__name__ == 'search':
            any_args = args.pop('any', True)
            all_args = args.pop('all', False)
            args['all_args'] = (not any_args) or all_args

    return parser, args


def parse_utility_args(args):
    parser = argparse.ArgumentParser(prog='brag-util')
    subparsers = parser.add_subparsers(help='sub command help')
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize brag. If you want a different location for brag than'
             ' {} than be sure to set BRAG_DIR environmental variable. If you '
             'want a different location for the configuration file then be sure'
             ' to set BRAG_CONFIG_PATH to something other than {}'.format(
                    BRAG_DIR,
                    CONFIG_FILE_PATH,
                ),
    )
    init_parser.add_argument(
        '-m',
        '--mechanism',
        type=str,
        choices=PERSIST_CHOICES,
        default='files',
        help='Select the persistence mechanism. Default: %(default)s.'
    ),
    init_parser.add_argument(
        '-c',
        '--clobber',
        help='If set, overwrites existing configuration files.',
        action='store_true',
    ),

    init_parser.set_defaults(func=init)
    args = vars(parser.parse_args(args))

    return parser, args
