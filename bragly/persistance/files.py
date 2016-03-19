def write(message, file_path, form):
    if form == 'json':
        message_str = json.dumps(message)
    if form == 'json-pretty':
        message_str = json.dumps(message, indent=2)
    if form == 'log':
        tags = '|'.join(message['tags'])
        timestamp = message['timestamp'].isoformat()
        message_str = "[{timestamp}][{tags}] {message}\n".format(timestamp=timestamp, tags=tags, message=message['message'])
    with open(file_path, 'a') as f:
        f.write(message_str)
    
    return "success"

def read(*args, **kwargs):
    raise NotImplementedError

def search(*args, **kwargs):
    raise NotImplementedError
