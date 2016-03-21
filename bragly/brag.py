# -*- coding: utf-8 -*-
"""A module to munge arguments comming from a front end and pass those requests
    to the persistence module.
"""
from __future__ import absolute_import, print_function
import arrow
import bragly.persist as persist
from bragly.config import BRAG_DIR, CONFIG_FILE_PATH
import os
import pkg_resources

PERSIST_CHOICES = list(persist.MECHANISMS.keys())

__all__ = [
    'write',
    'read',
    'search',
]

def write(message=None, tags=None, timestamp=None):
    """Given a message, tags, and timestamp, creates the proper structure for
        the persistance mechanism.

    Args:
        message: Can be one of None, list of strs or strs. If it is a list or
            None, it will be changed to a string.
        tags (list): A list of tags to associate with this message.
        timestamp (arrow.Arrow): An override date to associate with this message

    Returns:
        list: A list containing one element, representing the result status of
            the write operation.
    """
    if message is None:
        message = ''
    elif isinstance(message, (list,)):
        message = ' '.join(message)

    if tags is None:
        tags = []
    
    if timestamp is None:
        timestamp = arrow.now()

    message_struct = {'message': message, 'tags': tags, 'timestamp': timestamp}
    result = persist.write(message=message_struct)
    return [result]

def read(start=None, end=None, period=None, form='json'):
    """Reads previously saved messages.

    Args:
        start (arrow.Arrow): The start date time to read messages from
        end (arrow.Arrow): The end date time to read messages until
        period (str): A human readable description of a time period
        form (str): The output format, one of log, json, json-pretty

    Yields:
        str: A single line of the result set
    """
    end = _get_end_date(start, end, period)

    results = persist.read(start, end, form)
    for result in results:
        yield result

def search(start=None, end=None, period=None, form='json', tags=None, text=None, all_args=False):
    """Given search criteria, finds the matching messages. Yields the results
        back to the caller.

    Args:
        start (arrow.Arrow): The start date time to read messages from
        end (arrow.Arrow): The end date time to read messages until
        period (str): A human readable description of a time period
        form (str): The output format, one of log, json, json-pretty
        tags (list): A list of tags to search for
        text (list): A list of tokens (words) to search for
        all_args (bool): A flag indicating whether all tags and text must be
            present to return the message in the result.

    Yields:
        str: A single line of the result set
    """
    end = _get_end_date(start, end, period)

    if tags is None:
        tags = []
    if text is None:
        text = []

    results = persist.search(start, end, form, tags, text, all_args=all_args)
    for result in results:
        yield result

def _get_end_date(start=None, end=None, period=None):
    if end is None and period is None:
        end = arrow.now()
    elif end is None and start is not None:
        _, end = start.span(period)
    elif start is None:
        end = arrow.now()

    return end

def init(mechanism, clobber=True):
    directory = BRAG_DIR
    print('Checking if {} exists...'.format(directory), end='', flush=True)
    if not os.path.exists(directory):
        print('\nmaking directory...', end='', flush=True)
        os.makedirs(directory)
        print('success', flush=True)
    print('OK', flush=True)

    print('Getting example configuration for mechanism: {}...'.format(
        mechanism), end='', flush=True)

    config_example = pkg_resources.resource_filename(
        'bragly',
        'config_examples/config-{}.ini'.format(mechanism)
    )

    with open(config_example, 'r') as f:
        config_data = f.read()
    print('OK')

    config_file_path = CONFIG_FILE_PATH
    file_exists = os.path.exists(config_file_path)

    if (file_exists and clobber) or not file_exists:
        if file_exists:
            print('Clobbering file {}.'.format(config_file_path), flush=True)
        print('Writing to {}...'.format(config_file_path), end='', flush=True)
        with open(config_file_path, 'w') as f:
            f.write(config_data)
        print('OK')
    else:
        print(
            'Not clobbering file at {}. See example config file at {}.'.format(
                config_file_path, config_example
            )
        )

    return ['Initialization finished']
