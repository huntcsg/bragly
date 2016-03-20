# -*- coding: utf-8 -*-
"""A module to munge arguments comming from a front end and pass those requests
    to the persistence module.
"""
from __future__ import absolute_import, print_function
import arrow
import bragly.persist as persist

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

def read(start, end=None, period=None, form='json'):
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

def search(start, end=None, period=None, form='json', tags=None, text=None, all_args=False):
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

def _get_end_date(start, end=None, period=None):
    if end is None and period is None:
        end = arrow.now()
    elif end is None:
        _, end = start.span(period)

    return end
