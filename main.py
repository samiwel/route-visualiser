from urllib.parse import unquote_plus
from io import BytesIO
from flask import Flask, jsonify, request, send_file, abort, json
import requests
from routeviz.routeviz import parse_schema_for_blocks, construct_graph
import config

app = Flask(__name__)

app.config.from_object(config)

@app.route('/favicon.ico')
def favicon():
    abort(200)

@app.route("/status")
def status():
    return jsonify({
        "status": "OK"
    })

def convert_schema_to_svg(schema_json):
    blocks = parse_schema_for_blocks(schema_json)
    graph = construct_graph('svg', blocks)
    bytes_io = BytesIO(graph.pipe())
    return bytes_io

def validate_json(json_to_validate):
    res = requests.post(app.config.get('EQ_SCHEMA_VALIDATOR_URL'), \
        data=json.dumps(json_to_validate), headers={'Content-Type': 'text/plain'})
    if res.status_code != 200:
        raise ValueError("Validator service returned {} status code.".format(res.status_code))

    validation_result = res.json()
    if 'errors' in validation_result and validation_result.get('errors'):
        raise ValueError("Validator service returned errors. {}" \
            .format(validation_result.get('errors')))


@app.route("/visualise", methods=['GET'])
def get_visualise():
    urlencoded_uri = request.args.get('uri')
    if urlencoded_uri is None:
        abort(200)

    url = unquote_plus(urlencoded_uri)
    result = requests.get(url)
    if result.status_code != 200:
        abort(404)

    validate_json(result.json())

    return send_file(convert_schema_to_svg(result.json()), mimetype='image/svg+xml')


@app.route("/visualise", methods=['POST'])
def post_visualise():
    schema_json = request.get_json(force=True)
    validate_json(schema_json)
    return send_file(convert_schema_to_svg(schema_json), mimetype='image/svg+xml')

@app.route("/")
def index():
    return "Hello from the route visualiser"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config.get('PORT'), debug=app.config.get('DEBUG'))
