import json
import requests

host='http://localhost:5000/remote_eval'

# Deserialize a reply from the remote_eval server
def deserialize(data):
    if type(data) is list:
        return [ deserialize(item) for item in data ]

    # elif type(data) is dict:
        # return { key: deserialize(value) for key, value in data.items() }

    else:
        if data['type'] == 'none':
            return None

        # If the result is a literal, no need to store
        if 'value' in data:
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

execute('names = "zach"')
execute('names = ["zach", "dan"]')
execute('more_names = ["zach", "dan", names]')
names = execute('more_names')
print(names)
print(names.expand())
print(names)
print(names[0])
print(names[1])
print(names[2])
print(names[2].expand())
print(names)

