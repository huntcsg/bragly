# -*- coding: utf-8 -*-
"""A module that handles dispatching to the appropriate persistance module
    based on user configuration.

    Attributes:
        MECHANISMS (dict): A mapping from configuration string to persistance
            module.
"""

from __future__ import absolute_import, print_function
from bragly.persistance import files, reldb, mongodb
from bragly.config import get_config

MECHANISMS = {
    'files': files,
    'mongodb': mongodb,
    'reldb': reldb
}


def write(message, mechanism=None):
    """Gets the users configuration and dispatches the write call to the
        proper module and function.

    Args:
        message (dict): A dictionary representation of the message.
        mechanism (str): Allows for an override to explicitly get a mechanism
            from the configuration.

    Returns:
        str: A result message indicating success or failure
    """
    mech, config = _get_module_and_kwargs_from_config(mechanism)
    result = mech.write(message=message, **config)
    return result


def read(start, end, form='log', mechanism=None):
    """Given a start and end date, and an output format, gets the persistance
        module from the configuration and passes the request to that module.
        Yields the results back to the caller.

    Args:
        start (arrow.Arrow):
        end (arrow.Arrow):
        form (str): the output format. defaults to log.
        mechanism (str): Allows for an override to explicitly get a mechanism
            from the configuration.

    Yields:
        str: A single line of the result set
    """
    mech, config = _get_module_and_kwargs_from_config(mechanism)
    results = mech.read(start, end, form, **config)
    for result in results:
        yield result


def search(start, end, form, tags, text, all_args, mechanism=None):
    """Given search criteria, finds the matching messages. Yields the results
        back to the caller.

    Args:
        start (arrow.Arrow): The star tdate after which to find messages (inclusive)
        end (arrow.Arrow): The end date before which to find messages (inclusive)
        form (str): the output format. defaults to log
        tags (list): A list of tags to search for
        text (list): A list of text tokens (words) to search for
        all_args (bool): A flag indicating whether all tags and text must be
            present to return the message in the result.
        mechanism (str): Allows for an override to explicitly get a mechanism
            from the configuration

    Yields:
        str: A single line of the result set
    """
    mech, config = _get_module_and_kwargs_from_config(mechanism)
    results = mech.search(start, end, form, tags, text, all_args, **config)
    for result in results:
        yield result


def _get_module_and_kwargs_from_config(mechanism=None):
    """Optionally given a mechanism, get the user configuration. Using the
        configuration, find the correct module and return both to the caller

    Args:
        mechanism (str): The mechanism from MECHANISMS to get configuration for

    Returns:
        module, dict : The module and associated configuration for that module
    """
    config = get_config(mechanism)
    mechanism = config.pop('mechanism')
    mech = MECHANISMS[mechanism]
    return mech, config
