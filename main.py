from flask import Flask, jsonify, request, send_file, abort
from routeviz.routeviz import parse_schema_for_blocks, construct_graph
from urllib.parse import unquote_plus
from io import BytesIO
import requests

app = Flask(__name__)

@app.route("/status")
def status():
  return jsonify({
    "status": "OK"
  })

def convert_schema_to_svg(schema_json):
  blocks = parse_schema_for_blocks(schema_json)
  graph = construct_graph('svg', blocks)
  bytesIO = BytesIO(graph.pipe())
  return bytesIO


@app.route("/visualise", methods=['GET'])
def get_visualise():
  urlencoded_uri = request.args.get('uri')
  if urlencoded_uri is None:
    abort(200)

  url = unquote_plus(urlencoded_uri)
  result = requests.get(url)
  if result.status_code != 200:
    abort(404)

  return send_file(convert_schema_to_svg(result.json()), mimetype='image/svg+xml')


@app.route("/visualise", methods=['POST'])
def post_visualise():
  schema_json = request.get_json(force=True)
  return send_file(convert_schema_to_svg(schema_json), mimetype='image/svg+xml')

@app.route("/")
def index():
  return "Hello from the route visualiser"


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)