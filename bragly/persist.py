from bragly.persistance import files, reldb, mongodb
from bragly.config import get_config
MECHANISMS = {
    'files' : files,
    'mongodb': mongodb,
    'rel-db': reldb
}

def write(message, mechanism=None):
    config = get_config(mechanism)
    mechanism = config.pop('mechanism')
    mech = MECHANISMS[mechanism]
    result = mech.write(message=message, **config)
    return result

def read(start, end, form='log', mechanism=None):
    config = get_config(mechanism)
    mechanism = config.pop('mechanism')
    mech = MECHANISMS[mechanism]
    results = mech.read(start, end, form, **config)
    for result in results:
        yield result

def search(start, end, form, tags, text, all_args, mechanism=None):
    config = get_config(mechanism)
    mechanism = config.pop('mechanism')
    mech = MECHANISMS[mechanism]
    results = mech.search(start, end, form, tags, text, all_args, **config)
    for result in results:
        yield result
