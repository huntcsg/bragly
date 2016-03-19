import argparse
from bragly.brag import write, read, search
import sys

def parse_args(args):

    parser = argparse.ArgumentParser(prog='brag')
    subparsers = parser.add_subparsers(help='sub command help')
    
    # Writ command sub  parser
    write_parser = subparsers.add_parser('w', help='Write a new brag entry')
    write_parser.add_argument('message', metavar='message', nargs='+', type=str, help='The brag message')
    write_parser.add_argument('-t','--tags', nargs='*', type=str, help='The tags associated with this brag message')
    write_parser.add_argument('-d', '--timestamp', type=str, help='The time stamp to use for this entry, in ISO-8601 format')
    write_parser.set_defaults(func=write)

    # Read command sub parser
    read_parser = subparsers.add_parser('r', help='Read a group of brag entries')
    read_parser.add_argument('-s', '--start', type=str, help="The start time for getting entries")
    # End date spec
    read_parser_enddate_group =  read_parser.add_mutually_exclusive_group()
    read_parser_enddate_group.add_argument(
        '-p', 
        '--period', 
        type=str, 
        help='The time period after the start datetime to get entires. One of hour, day, week, month, year'
    )
    read_parser_enddate_group.add_argument('-e', '--enddate', type=str, help='The end time for getting entries')
    # Other read options
    read_parser.add_argument('-f', '--format', type=str, default='json', help='The format to display the results in. One of json, json-pretty, log. Default: %(default)s')
    read_parser.set_defaults(func=read)
    # Search Command Sub parser
    search_parser = subparsers.add_parser('s', help='Search for a group of brag entries')
    search_parser.add_argument('-s', '--start', type=str, help="The start time for getting entries")
    # End date spec
    search_parser_enddate_group = search_parser.add_mutually_exclusive_group()
    search_parser_enddate_group.add_argument(
        '-p', 
        '--period', 
        type=str, 
        help='The time period after the start datetime to get entires. One of hour, day, week, month, year'
    )
    search_parser_enddate_group.add_argument('-e', '--enddate', type=str, help='The end time for getting entries')
    # Other search options
    search_parser.add_argument('-t', '--tags', nargs='*', type=str, help='Tags you want to search for')
    search_parser.add_argument('-x', '--text', nargs='*', type=str, help='Keywords you want to search for')
    search_parser.set_defaults(func=search)
    
    args = vars(parser.parse_args(args))
    if not args:
        parser.print_usage()
        sys.exit()
    return args

if __name__ == '__main__':
    #import sys

    #print(parse_args(sys.argv[1:]))
    #sys.exit()
    
    #parse_args(['--help'])
    
    args = 'w this is a message --tags apache this that'.split()
    print(parse_args(args))

    args = 'w this is a message, no tags'.split()
    print(parse_args(args))

    args = 'r --start=2016-03-01 --period=week'.split()
    print(parse_args(args))

    args = 's --tags help process'.split()
    print(parse_args(args))

    args = 's --text process caching'.split()
    print(parse_args(args))

