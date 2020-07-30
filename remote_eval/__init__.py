import flask

from remote_eval.remote_eval import handle_message

app = flask.Flask(__name__)

@app.route('/remote_eval')
def remote_eval_endpoint():
    return flask.jsonify(**handle_message(flask.request.json))

