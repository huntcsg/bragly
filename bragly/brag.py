import arrow
import bragly.persist as persist
import json
import sys

__all__ [
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
    return "Success"

def read(start, end=None, period=None, form='json'):
    if end is None and period is None:
        end = arrow.now()
    elif end is None:
        _, end = start.span(period)

    result = persist.read(start, end, form)
    return result

def search(**kwargs):
    print("searched: ", kwargs)

