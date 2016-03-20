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
    result = ''.join(mech.read(start, end, form, **config))
    return result

def search(start, end, form, tags, text):
    config = get_config(mechanism)
    mechanism = config.pop('mechanism')
    mech = MECHANISMS[mechanism]
    result = mech.search(start, end, form, tags, text, **config)
    return result

