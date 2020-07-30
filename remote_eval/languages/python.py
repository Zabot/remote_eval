environments = {}

def execute(string, session):
    if session not in environments:
        environments[session] = {}

    try:
        return eval(string, None, environments[session])
    except:
        exec(string, None, environments[session])
        return None

