import os
import json
import re
from collections import namedtuple
import arrow

MESSAGE_STR_TEMPLATE = "[{timestamp}][{tags}] {message}\n"

def write(message, file_path=None, file_dir=None, form='json'):
    if form == 'json':
        message_str = json.dumps(message)
    if form == 'json-pretty':
        message_str = json.dumps(message, indent=2)
    if form == 'log':
        tags = '|'.join(message['tags'])
        timestamp = message['timestamp'].isoformat()
        message_str = MESSAGE_STR_TEMPLATE.format(timestamp=timestamp, tags=tags, message=message['message'])

    file_path = get_file_path(form, file_path, file_dir)

    with open(file_path, 'a') as f:
        f.write(message_str)
    
    return "success"

def get_file_path(form=None, file_path=None, file_dir=None):
    if file_path is None and file_dir is None:
        raise RuntimeError('No file_path or file_dir indicated.')

    if file_path is None:
        file_path = os.path.join(file_dir, 'brag-{form}.dat')

    return file_path


def read(start, end, out_form, form, file_dir=None, file_path=None):
    file_path = get_file_path(form, file_path, file_dir)

    if form == 'json-pretty':
        raise NotImplementedError('json-pretty format is not yet supported')
    with open(file_path, 'rb') as f:
        for line in f:
            line = line.decode('utf-8').strip()
            parsed_line = parse_line(line, form=form)
            if parsed_line.timestamp >= start and parsed_line.timestamp <= end:
                if out_form != form:
                    yield coerce_line(parsed_line, out_form)
                else:
                    yield line

ParsedLine = namedtuple('ParsedLine', ['timestamp', 'tags', 'message'])
def parse_line(line, form):
    if form == 'log':
        line_regex = re.compile(r'\[(.*)\]\[(.*)] (.*)')
        timestamp, tags, message = line_regex.findall(line)[0]
        timestamp = arrow.get(timestamp)
        tags = tags.split('|')
        message = message.strip()
        if not tags:
            tags = []
        return ParsedLine(timestamp, tags, message)

    elif form == 'json':
        message_json = json.loads(line)
        return ParsedLine(message_json['timestamp'], message_json['tags'], message_json['message'])

    elif form == 'json-pretty':
        raise RuntimeError('No!')

def coerce_line(parsed_line, out_form):
    timestamp = parsed_line.timestamp.isoformat()
    if out_form == 'log':
        tags = '|'.join(parsed_line.tags)
        return MESSAGE_STR_TEMPLATE.format(timestamp=timestamp, tags=tags, message=parsed_line.message)

    elif out_form == 'json':
        # Translate from a named tuple to a dict, and then dump as a json string
        return json.dumps({'timestamp': timestamp, 'tags': parsed_line.tags, 'message': parsed_line.message})

    elif out_form == 'json-pretty':
        # Translate from a named tuple to a dict, and then dump as a json string
        return json.dumps({'timestamp': timestamp, 'tags': parsed_line.tags, 'message': parsed_line.message}, indent=2)


def search(*args, **kwargs):
    raise NotImplementedError
