# -*- coding: utf-8 -*-
"""A module for writing, reading, and searching files for persistance of brags.
    Implements the three public methods necessary for the bragly.persist API:
        write : saves a message.
        read : reads all messages in the relevant timeframe.
        search: searches all messages according to a number of criteria

Attributes:
    MESSAGE_STR_TEMPLATE (str): A template string for the 'log' format.

"""

from __future__ import absolute_import, print_function
import os
import json
import re
from collections import namedtuple
import arrow

MESSAGE_STR_TEMPLATE = "[{timestamp}][{tags}] {message}\n"


def write(message, file_path=None, file_dir=None, form='json'):
    """Writes a message to a file in the given format.

    Args:
        message (dict): A message, it's timestamp, and any associated tags.
        form (str): A message format, one of log, json, json-pretty
        file_path (str): The file path for the source file. If None, the
            file_path will be generated from the file_dir and the form
        file_dir (str): The file directory for the source file. If None,
            the file_path will be used

    Returns:
        str: On success returns the word "success"
    """
    timestamp = message['timestamp'].isoformat()
    tags = message['tags']
    message = message['message']

    if form == 'json':
        message_str = "{}\n".format(json.dumps(
            dict(
                message=message,
                tags=tags,
                timestamp=timestamp
            ),
        ))
    elif form == 'json-pretty':
        message_str = "{}\n".format(json.dumps(
            dict(
                message=message,
                tags=tags,
                timestamp=timestamp
            ),
            indent=2
        ))
    elif form == 'log':
        tags = '|'.join(tags)
        message_str = MESSAGE_STR_TEMPLATE.format(
            timestamp=timestamp,
            tags=tags,
            message=message,
        )
    else:
        raise RuntimeError('Form {form} not supported or missing.'.format(form))

    file_path = _get_file_path(form, file_path, file_dir)

    with open(file_path, 'a') as f:
        f.write(message_str)

    return "success"


def _get_file_path(form, file_path=None, file_dir=None):
    """Given a format, and either a filepath or file directory, returns the
        proper filepath.
        The format of the file, if dynamically generated from the file_dir
            will be: /path/to/file/dir/brag-{format}.dat
    Args:
        form (str): A message format, one of log, json, json-pretty
        file_path (str): The file path for the source file. If None, the
            file_path will be generated from the file_dir and the form
        file_dir (str): The file directory for the source file. If None, the
            file_path will be used

    Returns:
        str: A file path for the source file
    """
    if file_path is None and file_dir is None:
        raise RuntimeError('No file_path or file_dir indicated.')

    if file_path is None:
        file_path = os.path.join(file_dir, 'brag-{form}.dat'.format(form=form))

    return file_path


def read(start, end, out_form, form, file_dir=None, file_path=None):
    """Reads out entries within the given time frame.

    Args:
        start (arrow.Arrow): The start date time to look for messages
        end (arrow.Arrow): The end date time to look for messages
        out_form (str): The output format. One of log, json, json-pretty
        form (str): The format that the source file is in
        file_dir (str): The file directory for the source file. If None, the
            file_path will be used.
        file_path (str): The file path for the source file. If None, the
            file_path will be generated from the file_dir and the form.
    Yields:
        str: A message line, in the requested format
    """
    file_path = _get_file_path(form, file_path, file_dir)

    if form == 'json-pretty':
        raise NotImplementedError('json-pretty format is not yet supported')
    with open(file_path, 'rb') as f:
        for line in f:
            line = line.decode('utf-8').strip()
            parsed_line = _parse_line(line, form=form)

            if ((start is None and parsed_line.timestamp <= end) or
                    (start is not None and
                        start <= parsed_line.timestamp <= end
                     )):
                if out_form != form:
                    yield _coerce_line(parsed_line, out_form)
                else:
                    yield line


ParsedLine = namedtuple('ParsedLine', ['timestamp', 'tags', 'message'])


def _parse_line(line, form):
    """Parse a message line according to the form that is passed in, returning
        a ParsedLine object.

    Args:
        line (str): A line from the data file
        form (str): Indicates the form that the line is in, one of log or json
            (json-pretty not supported)

    Returns:
        ParsedLine: The message in a convenient namedtuple
    """
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
        return ParsedLine(
            arrow.get(message_json['timestamp']),
            message_json['tags'],
            message_json['message']
        )

    elif form == 'json-pretty':
        raise RuntimeError('No!')


def _coerce_line(parsed_line, out_form):
    """ Coerce's a parsed line (named tuple) into the requested output format.

    Args:
        parsed_line (ParsedLine): A named tuple of the message.
        out_form (str): The output format, one of log, json, json-pretty

    Returns:
        str OR ParsedLine: The line in the format requested
    """
    if out_form == 'parsed_line':
        return parsed_line
    timestamp = parsed_line.timestamp.isoformat()
    if out_form == 'log':
        tags = '|'.join(parsed_line.tags)
        return MESSAGE_STR_TEMPLATE.format(
            timestamp=timestamp,
            tags=tags,
            message=parsed_line.message
        ).strip()

    elif out_form == 'json':
        # Translate from a named tuple to a dict, and then dump as a json string
        return json.dumps({
            'timestamp': timestamp,
            'tags': parsed_line.tags,
            'message': parsed_line.message
        }).strip()

    elif out_form == 'json-pretty':
        # Translate from a named tuple to a dict, and then dump as a json string
        return json.dumps({
            'timestamp': timestamp,
            'tags': parsed_line.tags,
            'message': parsed_line.message
        }, indent=2).strip()


def search(start, end, out_form, tags, text,
           all_args, form, file_dir=None, file_path=None):
    """Given a file path or a file directory and form, searches the files
        according to the search parameters.

    Args:
        start (arrow.Arrow): The start date time to look for messages
        end (arrow.Arrow): The end date time to look for messages
        out_form (str): The output format. One of log, json, json-pretty
        tags (list): A list of tags to look for
        text (list): A list of text tokens (words) to look for
        all_args (bool): Indicates whether all tags and text must exist for the
            message to be surfaces
        form (str): The format that the source file is in
        file_dir (str): The file directory for the source file. If None, the
            file_path will be used.
        file_path (str): The file path for the source file. If None, the
            file_path will be generated from the file_dir and the form.

    Yields:
        str: A line of text representing one result of the search
    """
    base_results = read(start, end, 'parsed_line', form, file_dir, file_path)
    for result in base_results:
        if not all_args:
            if tags and set(tags).intersection(set(result.tags)):
                yield _coerce_line(result, out_form)
            elif text and set(text).intersection(
                    set(result.message.split(' '))):
                yield _coerce_line(result, out_form)
            elif not text and not tags:
                yield _coerce_line(result, out_form)
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
                yield _coerce_line(result, out_form)
