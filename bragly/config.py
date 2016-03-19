import os
def get_config(mechanism=None):
    if mechanism is None:
        mechanism = 'files'

    default_config = {
        'files': {
            'file_path': os.path.expanduser('~/.brag/brag.dat'),
            'form': 'log',
        },
    }

    config = default_config[mechanism] # add logic to check a user ccnfiguration file
    config['mechanism'] = mechanism

    return config
