import argparse
from bragly.brag import write, read, search
import arrow
import sys

def parse_args(args):

    parser = argparse.ArgumentParser(prog='brag')
    subparsers = parser.add_subparsers(help='sub command help')
    
    # Writ command sub  parser
    write_parser = subparsers.add_parser('w', help='Write a new brag entry')
    write_parser.add_argument('message', metavar='message', nargs='+', type=str, help='The brag message')
    write_parser.add_argument('-t','--tags', nargs='*', type=str, help='The tags associated with this brag message')
    write_parser.add_argument('-d', '--timestamp', type=arrow.get, help='The time stamp to use for this entry, in ISO-8601 format')
    write_parser.set_defaults(func=write)

    # Read command sub parser
    read_parser = subparsers.add_parser('r', help='Read a group of brag entries')
    read_parser.add_argument('-s', '--start', type=arrow.get, help="The start time for getting entries")
    # End date spec
    read_parser_enddate_group =  read_parser.add_mutually_exclusive_group()
    read_parser_enddate_group.add_argument(
        '-p', 
        '--period', 
        type=str, 
        help='The time period after the start datetime to get entires. One of hour, day, week, month, year'
    )
    read_parser_enddate_group.add_argument('-e', '--end', type=arrow.get, help='The end time for getting entries')
    # Other read options
    read_parser.add_argument(
            '-f', 
            '--format', 
            type=str, 
            default='json', 
            help='The format to display the results in. One of json, json-pretty, log. Default: %(default)s'
    )
    # Set the operation that will be called based on the command
    read_parser.set_defaults(func=read)
    
    # Search Command Sub parser
    search_parser = subparsers.add_parser('s', help='Search for a group of brag entries')
    search_parser.add_argument('-s', '--start', type=arrow.get, help="The start time for getting entries")
    # End date spec
    search_parser_enddate_group = search_parser.add_mutually_exclusive_group()
    search_parser_enddate_group.add_argument(
        '-p', 
        '--period', 
        type=str, 
        help='The time period after the start datetime to get entires. One of hour, day, week, month, year'
    )
    search_parser_enddate_group.add_argument('-e', '--end', type=arrow.get, help='The end time for getting entries')
    # Other search options
    search_parser.add_argument('-t', '--tags', nargs='*', type=str, help='Tags you want to search for')
    search_parser.add_argument('-x', '--text', nargs='*', type=str, help='Keywords you want to search for')
    # Set the operation that will be called based on the command
    search_parser.set_defaults(func=search)
    
    args = vars(parser.parse_args(args))
    return parser, args

