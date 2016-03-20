import arrow
import bragly.persist as persist
import json
import sys

__all__ = [
    'write',
    'read',
    'search',
]

def write(message=None, tags=None, timestamp=None):
    if message is None:
        message = ''
    elif isinstance(message, (list,)):
        message = ' '.join(message)

    if tags is None:
        tags = []
    
    if timestamp is None:
        timestamp = arrow.now()

    message_struct = {'message': message, 'tags': tags, 'timestamp': timestamp}
    persist.write(message=message_struct)
    return ["Success"]

def read(start, end=None, period=None, form='json'):
    if end is None and period is None:
        end = arrow.now()
    elif end is None:
        _, end = start.span(period)

    results = persist.read(start, end, form)
    for result in results:
        yield result

def search(start, end=None, period=None, form='json', tags=None, text=None, all_args=False):
    if end is None and period is None:
        end = arrow.now()
    elif end is None:
        _, end = start.span(period)
    if tags is None:
        tags = []
    if text is None:
        text = []

    results = persist.search(start, end, form, tags, text, all_args=all_args)
    for result in results:
        yield result