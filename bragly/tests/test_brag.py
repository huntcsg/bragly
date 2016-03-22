from __future__ import absolute_import, print_function
import bragly.brag as brag
from bragly.brag import write, read, search, _get_end_date, init
import bragly.persist
import mock
import six
import arrow
import tempfile
import builtins
import os

time_now = arrow.now()
mocked_arrow_now = mock.Mock(return_value=time_now)

def test_export():
    bragly_exports = [
        'write',
        'read',
        'search',
    ]
    assert(set(brag.__all__) == set(bragly_exports))

def check_write(args, persist_args):

    with mock.patch('bragly.persist.write', autospec=True) as mocked_write:
        with mock.patch('arrow.now', mocked_arrow_now) as arrow_now:
            test_result = write(*args)
            write_call_args = mocked_write.call_args
            assert(write_call_args is not None)
            if write_call_args is not None:
                positional, keyword = write_call_args

            for key, value in six.iteritems(keyword):
                for sub_key, sub_value in six.iteritems(value):
                    print(persist_args[key][sub_key], sub_value)
                    print(persist_args[key][sub_key] == sub_value)
                    assert(persist_args[key][sub_key] == sub_value)


def test_write():
    test_cases = [
            {
                'args': ('test',),
                'write_kwargs': {'message': {
                    'message': 'test',
                    'timestamp': time_now,
                    'tags': []
                    }
                },
            },
            {
                'args': ('test', None, arrow.get('2015-01-01')),
                'write_kwargs': {'message': {
                    'message': 'test',
                    'timestamp': arrow.get('2015-01-01'),
                    'tags': []
                    }
                },
            },
            {
                'args': ('test', ['test'], arrow.get('2015-01-01')),
                'write_kwargs': {'message': {
                    'message': 'test',
                    'timestamp': arrow.get('2015-01-01'),
                    'tags': ['test']
                    }
                },
            },
            {
                'args': (['test', 'message'],),
                'write_kwargs': {'message': {
                    'message': 'test message',
                    'timestamp': time_now,
                    'tags': []
                    }
                },
            },
            {
                'args': (None, None, None),
                'write_kwargs': {'message': {
                    'message': ' ',
                    'timestamp': time_now,
                    'tags': []
                    }
                },
            },
    ]

    for test_case in test_cases:
        yield (
            check_write,
            test_case['args'],
            test_case['write_kwargs']
        )

def check_read(args, result):

    with mock.patch('bragly.persist.read', autospec=True) as mocked_read:
        mocked_read.return_value = iter(result)
        read_result = read(*args)
        assert(list(read_result) == result)
        # Needed to run the iterator prior to looking at the args.
        read_call_args = mocked_read.call_args
        assert(read_call_args is not None)

def test_read():
    test_cases = [
        {
            'args': (None, None, None),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (arrow.get('2015-01-01'),),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (None, arrow.get('2015-01-01-'),),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (arrow.get('2015-01-01'), None, 'week'),
            'result': ['test1', 'test2', 'test3']
        }
    ]

    for test_case in test_cases:
        yield check_read, test_case['args'], test_case['result']

def check_search(args, search_args, result):

    with mock.patch('bragly.persist.search', autospec=True) as mocked_search:
        with mock.patch('arrow.now', mocked_arrow_now) as arrow_now:

            mocked_search.return_value = iter(result)
            search_result = search(*args)
            # print(search_result)
            # print(result)
            # print(list(search_result))
            assert(list(search_result) == result)
            # Needed to run the iterator prior to looking at the args.
            search_call_args = mocked_search.call_args
            assert(search_call_args is not None)
            positional, keyword = search_call_args
            print (positional)
            print(search_args)
            assert(positional == search_args)

def test_search():
    test_cases = [
        {
            'args': (None, None, None, 'json', None, None),
            'search_args': (None, time_now, 'json', [], [], False),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (arrow.get('2015-01-01'),),
            'search_args': (arrow.get('2015-01-01'), time_now, 'json', [], [], False),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (None, arrow.get('2015-01-01-'),),
            'search_args': (None, arrow.get('2015-01-01'), 'json', [], [], False),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (None, None, None, 'json', ['test']),
            'search_args': (None, time_now, 'json', ['test'], [], False),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (None, None, None, 'json', None, ['test']),
            'search_args': (None, time_now, 'json', [], ['test'], False),
            'result': ['test1', 'test2', 'test3']
        },
        {
            'args': (None, None, None, 'json', None, ['test'], True),
            'search_args': (None, time_now, 'json', [], ['test'], True),
            'result': ['test1', 'test2', 'test3']
        }
    ]

    for test_case in test_cases:
        yield (
            check_search,
            test_case['args'],
            test_case['search_args'],
            test_case['result'],
        )

def check_get_end_date(kwargs, result):
    with mock.patch('arrow.now', mocked_arrow_now) as arrow_now:
        end = _get_end_date(**kwargs)
        assert(end == result)

def test_get_end_date():
    test_cases = [
        {
            'kwargs': {
                'start': arrow.get('2015-01-01'),
            },
            'result': time_now,
        },
        {
            'kwargs': {
                'start': arrow.get('2015-01-01'),
                'end': arrow.get('2015-01-03'),
            },
            'result': arrow.get('2015-01-03')
        },
        {
            'kwargs': {
                'end': arrow.get('2015-01-01'),
            },
            'result': arrow.get('2015-01-01')
        },
        {
            'kwargs': {
                'start': arrow.get('2015-01-01'),
                'period': 'day'
            },
            'result': arrow.get('2015-01-01').span('day')[1]
        },
    ]

    for test_case in test_cases:
        yield check_get_end_date, test_case['kwargs'], test_case['result']

def test_init():
    try:
        temp_brag_dir = tempfile.TemporaryDirectory()
        temp_brag_dir_path = temp_brag_dir.name
    except AttributeError:
        temp_brag_dir_path = tempfile.mkdtemp()

    temp_config_file = tempfile.NamedTemporaryFile()

    test_cases = []
    start_lines = 0
    end_lines = 0

    with mock.patch('bragly.brag.BRAG_DIR', temp_brag_dir_path) as brag_dir:
        with mock.patch('bragly.brag.CONFIG_FILE_PATH', temp_config_file.name) as config_file:
            with mock.patch('builtins.print') as print_output:
                temp_config_file.close()
                # TEST CASE Initial Call no Directory
                os.rmdir(brag_dir)
                init('files')
                output_tokens = [
                    ['Checking if', 'exists...'],
                    ['making directory...'],
                    ['success'],
                    ['OK'],
                    ['Getting example configuration for mechanism: files...'],
                    ['OK'],
                    ['Writing to', '...'],
                    ['OK'],
                ]
                end_lines += 8
                test_cases.append((output_tokens, print_output.call_args_list[start_lines:end_lines]))
                start_lines += 8
                os.remove(temp_config_file.name)

                # TEST CASE 1 Initial CALL
                init('files')
                output_tokens = [
                    ['Checking if', 'exists...'],
                    ['OK'],
                    ['Getting example configuration for mechanism: files...'],
                    ['OK'],
                    ['Writing to', '...'],
                    ['OK'],
                ]
                end_lines += 6
                test_cases.append((output_tokens, print_output.call_args_list[start_lines: end_lines]))
                start_lines += 6

                # TEST CASE 2 Subsequent call, no clobber
                init('files', clobber=False)
                output_tokens = [
                    ['Checking if', 'exists...'],
                    ['OK'],
                    ['Getting example configuration for mechanism: files...'],
                    ['OK'],
                    ['Not clobbering file']
                ]
                end_lines += 5
                test_cases.append((output_tokens, print_output.call_args_list[start_lines:end_lines]))
                start_lines += 5
                # TEST CASE 3 Subsequent call, clobber
                init('files', clobber=True)
                output_tokens = [
                    ['Checking if', 'exists...'],
                    ['OK'],
                    ['Getting example configuration for mechanism: files...'],
                    ['OK'],
                    ['Clobbering file '],
                    ['Writing to', '...'],
                    ['OK'],
                ]
                end_lines += 7
                test_cases.append((output_tokens, print_output.call_args_list[start_lines:end_lines]))
                start_lines += 7

    for test_case in test_cases:
        yield check_init_output, test_case[0], test_case[1]

def check_init_output(line_tokens, output_lines):
    print(line_tokens)
    print(output_lines)
    for tokens, output_line in zip(line_tokens, output_lines):
        positional, keywords = output_line  # Since the line is actually the print call
        output = positional[0]
        for token in tokens:
            print(token)
            print(output)
            assert(token in output)

