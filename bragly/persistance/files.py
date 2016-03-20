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

def get_file_path(form, file_path=None, file_dir=None):
    if file_path is None and file_dir is None:
        raise RuntimeError('No file_path or file_dir indicated.')

    if file_path is None:
        file_path = os.path.join(file_dir, 'brag-{form}.dat'.format(form=form))

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
        if not tags:
            tags = []
        else:
            tags = tags.split('|')
        message = message.strip()
        return ParsedLine(timestamp, tags, message)

    elif form == 'json':
        message_json = json.loads(line)
        return ParsedLine(message_json['timestamp'], message_json['tags'], message_json['message'])

    elif form == 'json-pretty':
        raise RuntimeError('No!')

def coerce_line(parsed_line, out_form):
    if out_form == 'parsed_line':
        return parsed_line
    timestamp = parsed_line.timestamp.isoformat()
    if out_form == 'log':
        tags = '|'.join(parsed_line.tags)
        return MESSAGE_STR_TEMPLATE.format(timestamp=timestamp, tags=tags, message=parsed_line.message).strip()

    elif out_form == 'json':
        # Translate from a named tuple to a dict, and then dump as a json string
        return json.dumps({'timestamp': timestamp, 'tags': parsed_line.tags, 'message': parsed_line.message}).strip()

    elif out_form == 'json-pretty':
        # Translate from a named tuple to a dict, and then dump as a json string
        return json.dumps({'timestamp': timestamp, 'tags': parsed_line.tags, 'message': parsed_line.message}, indent=2).strip()


def search(start, end, out_form, tags, text, all_args, form, file_dir=None, file_path=None):
    base_results = read(start, end, 'parsed_line', form, file_dir, file_path)
    for result in base_results:
        if not all_args:
            if tags and set(tags).intersection(set(result.tags)):
                yield coerce_line(result, out_form)
            elif text and set(text).intersection((set(result.message.split(' ')))):
                yield coerce_line(result, out_form)
            elif not text and not tags:
                yield coerce_line(result, out_form)
        else:
            tags_in_tags = False
            text_in_message = False
            if tags and set(tags).issubset(set(result.tags)):
                tags_in_tags = True
            elif not tags:
                tags_in_tags = True
            if text and set(text).issubset(set(result.message.split(' '))):
                text_in_message = True
            elif not text:
                text_in_message = True
            if tags_in_tags and text_in_message:
                yield coerce_line(result, out_form)