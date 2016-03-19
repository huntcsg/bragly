import arrow
import bragly.persist as persist
import json

def write(message=None, tags=None, timestamp=None):
    if message is None:
        message = ''
    elif isinstance(message, (list,)):
        message = ' '.join(message)

    if tags is None:
        tags = []
    
    if timestamp is None:
        timestamp = arrow.now().isoformat()

    message_struct = {'message': message, 'tags': tags, 'timestamp': timestamp}
    try:
        persist.write(json.dumps(message_struct))
        return "Success"
    except Exception as e:
        return "Failure: {}".format(e)

def read(**kwargs):
    print("read: ", kwargs)

def search(**kwargs):
    print("searched: ", kwargs)

