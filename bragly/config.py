import configparser
import os

BRAG_DIR = os.environ.get('BRAG_DIR', os.path.expanduser('~/.brag'))
CONFIG_FILE_PATH = os.environ.get('BRAG_CONFIG_PATH', os.path.join(BRAG_DIR, 'config.ini'))

def get_config(mechanism=None):

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
        print("No configuration found, using default configuration: ", end='')

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

        config[mechanism] = dict(default_config.get(mechanism, {}), **overide_config)

    config[mechanism]['mechanism'] = mechanism
    return config[mechanism]
