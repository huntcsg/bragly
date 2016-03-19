import arrow

def write(message=None, tags=None, timestamp=None):
    if message is None:
        message = ''
    elif isinstance(message, (list,)):
        message = ' '.join(message)

    if tags is None:
        tags = []
    
    if timestamp is None:
        timestamp = arrow.now().isoformat()

    return ("Wrote: ", '{} {} {}'.format(message, '|'.join(tags), timestamp))

def read(**kwargs):
    print("read: ", kwargs)

def search(**kwargs):
    print("searched: ", kwargs)
