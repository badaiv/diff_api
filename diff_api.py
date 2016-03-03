"""
diff_api module

RESTful service with http endpoints:\n
<host>/v1/diff/left\n
<host>/v1/diff/right\n
that accepts JSON base64 encoded binary data.

<host>/v1/diff -
return JSON response {'diff': True} or {'diff': False} after comparing
data that was received in above endpoints.
"""

from flask import Flask, jsonify, abort, make_response, request
import base64
import json
app = Flask(__name__)

# global variables
# better to use some filesystem db, dut didn't have enough time to make it
left = ""
right = ""


def byte64_to_json(data):
    """
    convert base64 binary data into JSON
    :param data: binary data
    :return:
    """
    payload = data
    payload_decoded = base64.urlsafe_b64decode(payload)
    payload_string = payload_decoded.decode('utf-8')
    payload_json = json.loads(payload_string)
    return payload_json


@app.route('/v1/diff/left', methods=['GET', 'POST', 'DELETE'])
def create_left():
    """
    Accept left side to diff
    """
    global left
    if request.method == 'POST':
        try:
            left = byte64_to_json(request.get_data())
        except (UnicodeDecodeError, ValueError):
            abort(406)
        return jsonify(left), 202
    if request.method == 'DELETE':
        left = ""
    return jsonify(left), 200


@app.route('/v1/diff/right', methods=['GET', 'POST', 'DELETE'])
def create_right():
    """
    Accept right side to diff
    """
    global right
    if request.method == 'POST':
        try:
            right = byte64_to_json(request.get_data())
        except (UnicodeDecodeError, ValueError):
            abort(406)
        return jsonify(right), 202
    if request.method == 'DELETE':
        right = ""
    return jsonify(right), 200


@app.route('/v1/diff', methods=['GET'])
def get_diff():
    """
    Make a diff
    """
    if left == "" or right == "":
        abort(412)
    diff = (right == left)
    return jsonify({'diff': diff})

# rewrite error responses into JSON format
@app.errorhandler(406)
def not_found(error):
    return make_response(jsonify({'error': 'Wrong data. Need to be JSON in base64.'}), 406)


@app.errorhandler(412)
def not_found(error):
    return make_response(jsonify({'error': 'Please POST payload to /v1/diff/left and /v1/diff/right first.'}), 412)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Wrong url.'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

if __name__ == '__main__':
    app.run(debug=True)
