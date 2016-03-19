from bragly.cli import parse_args

# Test write argument parsing
def check_write_args(args, result_keys):
    assert(set(result_keys) == set(parse_args(args)))

def test_write_args():
    test_cases = [
        {
            'args': 'w test message',
            'result_keys': ['message', 'func', 'timestamp','tags']
        },
    ]
    for test_case in test_cases:
        check_write_args(**test_case)




