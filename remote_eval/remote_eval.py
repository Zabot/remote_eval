import json
import importlib

import remote_eval.languages.python as environment

references = {}

def array(ref_id):
    return {'type': 'reference', 'refID': ref_id}

def obj(ref_id):
    return {'type': 'obj', 'refID': ref_id}

def literal(value):
    if value is None:
        return {'type': 'none'}
    return {'type': 'literal', 'value': value}

# Flatten an object into references
def flatten(o):
    # If this object has already been flattened before, return the existing
    # reference
    if id(o) in references:
        return id(o)

    try:
        # Allocate the reference before we start recursing in case this object
        # refers to itself
        references[id(o)] = None

        # Flatten every value in a dictonary
        references[id(o)] = { key: flatten(val) for key, val in o.items() }
        return obj(id(o))

    except AttributeError:
        # o wasn't a dictonary, flatten every item in an iterable
        try:
            # Allocate the reference before we start recursing in case this object
            # refers to itself
            references[id(o)] = None

            references[id(o)] = [ flatten(item) for item in o ]
            return array(id(o))

        except TypeError:
            # o wasn't an iterable, it must be a literal
            return literal(o)


def handle_message(request):
    # If this is a request to evaluate
    if request['message'] == 'evaluate':
        # Find the right plugin and execute
        # environment = importlib.import_module(request['environment'],
                                              # package='remote_eval.languages')

        result = environment.execute(request['statement'], request['session'])
        if result is None:
            return None
        return flatten(result)

    elif request['message'] == 'interrogate':
        pass

