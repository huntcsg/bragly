import arrow
import bragly.persist as persist
import json
import sys

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

    try:
        result = persist.read(start, end, form)
        return result
    except Exception as e:
        return "Failure in read: {}".format(sys.exc_info()[0])

def search(**kwargs):
    print("searched: ", kwargs)

