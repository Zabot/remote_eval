import json
import requests

host='http://localhost:5000/remote_eval'

# Deserialize a reply from the remote_eval server
def deserialize(data):

    if data['type'] == 'none':
        return None

    # If the result is populated, no reference objects are needed
    if 'value' in data:
        value = data['value']
        if data['type'] == 'obj':
            return { k: deserialize(v) for k, v in value.items() }
        elif data['type'] == 'array':
            return [ deserialize(item) for item in value ]

        return data['value']

    return Reference(data)

def execute(statement, environment='python'):
    data = {
            'message': 'evaluate',
            'environment': 'python',
            'statement': statement,
            'session': 1
            }
    r = requests.post(host, json=data)

    data = r.json()

    return deserialize(data)

def interrogate(ref_id):
    data = {
            'message': 'interrogate',
            'refID': ref_id
            }
    r = requests.post(host, json=data)

    data = r.json()
    return deserialize(data);

class Reference:
    def __init__(self, data):
        self.type = data['type']
        self.ref_id = data['refID']
        self.expanded = False

    def expand(self):
        if not self.expanded:
            self.expanded = interrogate(self.ref_id)
        return self.expanded

    def __getitem__(self, key):
        if not self.expanded:
            self.expand()
        return self.expanded[key]

    def __str__(self):
        if not self.expanded:
            if self.type == 'array':
                return '[...]'
            elif self.type == 'obj':
                return '{...}'
        else:
            return str(self.expanded)

    def __repr__(self):
        return str(self)

