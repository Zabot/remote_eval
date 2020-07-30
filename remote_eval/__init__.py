import flask

from remote_eval.remote_eval import handle_message

app = flask.Flask(__name__)

@app.route('/remote_eval', methods=['POST'])
def remote_eval_endpoint():
    response = handle_message(flask.request.json)
    return flask.jsonify(response)

