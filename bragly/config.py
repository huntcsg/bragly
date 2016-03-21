# -*- coding: utf-8 -*-
"""Loads, parses and returns values related to configuration

    Attributes:
        BRAG_DIR (str): The directory to use when reading and writing data.
            defaults to '~/.brag' (~/ is the user directory, and will be the
             correct value based on the platform. It can be overridden by the
             environmental variable BRAG_DIR.
        CONFIG_FILE_PATH (str): The file path for the configuration file.
            Defaults to $BRAG_DIR/config.ini, but can be overridden by setting
            the environmental variable BRAG_CONFIG_PATH.
"""
from __future__ import print_function, absolute_import
from six.moves import configparser
import os

BRAG_DIR = os.environ.get('BRAG_DIR', os.path.expanduser('~/.brag'))
CONFIG_FILE_PATH = os.environ.get('BRAG_CONFIG_PATH', os.path.join(BRAG_DIR, 'config.ini'))


def get_config(mechanism=None):
    """Gets the configuration from a file, if possible. If not, uses the
        default.

    Args:
        mechanism (str): The mechanism to use for persistance. One of 'files',
            'reldb' (relational database), or 'mongdb'.

    Returns:
        dict: A dictionary of configuration values relevant to the given
            persistence mechanism.
    """

    default_config = {
        'files': {
            'file_dir': BRAG_DIR,
            'form': 'log',
        },
    }

    conf_parser = configparser.ConfigParser()
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            conf_parser.read_file(f)
    except IOError:
        print("No configuration found, using default configuration: ")

    if mechanism is None:
        if 'mechanism' in conf_parser:
            mechanisms = [
                mech for mech, onoff
                in conf_parser['mechanism'].items()
                if onoff.lower() == 'on'
            ]
            if len(mechanisms) > 1:
                raise RuntimeError('Multiple mechanisms are on. Please turn all'
                                   ' but one off.')
        else:
            mechanisms = ['files']
    else:
        mechanisms = [mechanism]

    config = {}
    for mechanism in mechanisms:
        if mechanism in conf_parser:
            overide_config = dict(conf_parser[mechanism])
        else:
            overide_config = {}

        # Sets the configuration as the default configuration, and then
        # overrides from the configuration file.
        config[mechanism] = dict(
            default_config.get(mechanism, {}),
            **overide_config
        )

    config[mechanism]['mechanism'] = mechanism
    return config[mechanism]
