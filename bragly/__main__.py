#!/usr/bin/env python
from bragly.cli import parse_args
import sys

def main(args=None):
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
    result = func(**args)
    print(result)
    return 0
if __name__ == '__main__':
    main()
