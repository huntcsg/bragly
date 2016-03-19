from bragly.cli import parse_args
import arrow

# Test argument generation
def check_args(args, result_keys):
    args = args.split()
    
    parser, args = parse_args(args)

    assert(set(result_keys) == set(args.keys()))

def test_args():
    test_cases = [
        {
            'args': 'w test message',
            'result_keys': ['message', 'func', 'timestamp','tags']
        },
        {
            'args': 's --start=2015-01-01 --period=month --tags tag1 tag2 --text text1 text2',
            'result_keys': ['period','tags','text','start','end', 'func', 'format']
        },
        {
            'args': 'r --start=2015-01-01 --period=month',
            'result_keys': ['period','start','end', 'func','format']
        },
    ]
    for test_case in test_cases:
        yield check_args, test_case['args'],test_case['result_keys']

#
# Check actuall parsing of arguments (and associated values)
#

# Check parsing of write related commands
def check_write_parsing(args, result):
    args = args.split()
    parser, args = parse_args(args)
    comp_keys = ['message','timestamp','tags']
    for key in comp_keys:
        if key in result:
            assert(args[key] == result[key])
        else:
            assert(args[key] is None)

    assert(args['func'].__name__ == result['func'])

def test_write_parsing():
    test_cases = [
        {
            'args' :  'w test message',
            'result': {'message': ['test', 'message'], 'func': 'write'},
        },        
        {
            'args': 'w test message --tags tag1',
            'result': {'message': ['test','message'], 'func': 'write', 'tags': ['tag1']},
        },
        {
            'args': 'w test message --tags tag1 tag2',
            'result': {'message': ['test','message'], 'func': 'write', 'tags': ['tag1', 'tag2']},
        },
    ]
    for test_case in test_cases:
        yield check_write_parsing, test_case['args'], test_case['result']

# Check parsing of read related commands
def check_read_parsing(args, result):
    args = args.split()
    parser, args = parse_args(args)
    comp_keys = ['start','end','period', 'format']
    for key in comp_keys:
        if key in result:
            assert(args[key] == result[key])
        else:
            assert(args[key] is None)

    assert(args['func'].__name__ == result['func'])


def test_read_parsing():
    test_cases = [
        {
            'args': 'r --start=2015-01-01 --end=2016-01-01',
            'result': {'func': 'read', 'format': 'json', 'start': arrow.get('2015-01-01'), 'end': arrow.get('2016-01-01')} 
        },
        {
            'args': 'r --start=2015-01-01 --period=month',
            'result': {'func': 'read', 'format': 'json', 'start': arrow.get('2015-01-01'), 'period': 'month'}
        },
    ]
    for test_case in test_cases:
        yield check_read_parsing, test_case['args'], test_case['result']


# Check parsing of search command
def check_search_parsing(args, result):
    args = args.split()
    parser, args = parse_args(args)
    comp_keys = ['start','end','period', 'format']
    for key in comp_keys:
        if key in result:
            assert(args[key] == result[key])
        else:
            assert(args[key] is None)

    assert(args['func'].__name__ == result['func'])


def test_serach_parsing():
    test_cases = [
        {
            'args': 's --start=2015-01-01 --end=2016-01-01',
            'result': {'func': 'search', 'format': 'json', 'start': arrow.get('2015-01-01'), 'end': arrow.get('2016-01-01')} 
        },
        {
            'args': 's --start=2015-01-01 --period=month',
            'result': {'func': 'search', 'format': 'json', 'start': arrow.get('2015-01-01'), 'period': 'month'}
        },
        {
            'args': 's --start=2015-01-01 --end=2016-01-01',
            'result': {
                'func': 'search',
                'format': 'json',
                'start': arrow.get('2015-01-01'),
                'end': arrow.get('2016-01-01'),
            },
        },
        {
            'args': 's --start=2015-01-01 --period=day --tags tag1 tag2 --text text1 text2',
            'result': {
                'func': 'search', 
                'format': 'json', 
                'start': arrow.get('2015-01-01'), 
                'period': 'day', 
                'tags': ['tag1', 'tag2'], 
                'text': ['text1', 'text2']}
        },
    ]
    for test_case in test_cases:
        yield check_search_parsing, test_case['args'], test_case['result']

