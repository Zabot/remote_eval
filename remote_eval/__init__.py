import flask

app = flask.Flask(__name__)

@app.route('/remote_eval')
def remote_eval_endpoint():
    return flask.jsonify(**streams)

