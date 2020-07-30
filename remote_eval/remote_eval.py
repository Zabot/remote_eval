import json
import importlib

import remote_eval.languages.python as environment

references = {}

def array(ref_id):
    return {'type': 'array', 'refID': ref_id}

def obj(ref_id):
    return {'type': 'obj', 'refID': ref_id}

def literal(value):
    if value is None:
        return {'type': 'none'}
    return {'type': 'literal', 'value': value}

# Flatten an object into references
def flatten(o):
    if o is None:
        return {'type': 'none'}

    # If this object has already been flattened before, return the existing
    # reference
    if id(o) in references:
        return { 'type': references[id(o)]['type'], 'refID': id(o) }

    if type(o) is dict:

        # Allocate the reference before we start recursing in case this object
        # refers to itself
        references[id(o)] = { 'type': 'obj' }

        # Flatten every value in a dictonary
        references[id(o)]['value'] = {
                key: flatten(val) for key, val in o.items()
            }
        return obj(id(o))

    elif type(o) is list:

        # o wasn't a dictonary, flatten every item in an iterable
        # Allocate the reference before we start recursing in case this object
        # refers to itself
        references[id(o)] = { 'type': 'array' }

        references[id(o)]['value'] = [ flatten(item) for item in o ]
        return array(id(o))

    else:
        # o wasn't an iterable, it must be a literal
        return literal(o)

def handle_message(request):
    # If this is a request to evaluate
    if request['message'] == 'evaluate':
        # Find the right plugin and execute
        # environment = importlib.import_module(request['environment'],
                                              # package='remote_eval.languages')

        result = environment.execute(request['statement'], request['session'])

        return flatten(result)

    elif request['message'] == 'interrogate':
        try:
            return references[request['refID']]
        except KeyError:
            return None

