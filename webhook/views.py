from flask_login import login_required
from webhook import rabbit, validations
from flask import request, Blueprint, abort
from flask import current_app
from flask import jsonify
import requests
from jsonschema import validate
import json

app = Blueprint('main', __name__)

@app.errorhandler(400)
def internal_error(error):
    return jsonify(error='Internal Error'), 500


@app.errorhandler(500)
def internal_error(error):
    return jsonify(error='Internal Error'), 500


@app.errorhandler(401)
def internal_error(error):
    return jsonify(error='Internal Error'), 500


@app.route("/<routing_key>/street", methods=['POST'])
@login_required
def handle_street(routing_key):
    content = request.get_json(force=True)

    validate(content, validations.street_schema)

    r = requests.post('https://roads.googleapis.com/v1/nearestRoads?points={},{}&key={}'
                      .format(content.get('long'), content.get('lat'), current_app.config['GOOGLE_KEY']))

    if r.status_code != 200:
        abort(500)

    validate(r.json(), validations.street_schema_result)

    result = rabbit.channel.basic_publish(exchange=current_app.config['RABBITMQ_EXCHANGE'],
                                          routing_key=routing_key, body=r.json(indent=None))

    return jsonify(success=result)


@app.route("/<routing_key>/geo", methods=['POST'])
@login_required
def handle_geo(routing_key):
    content = request.get_json(force=True)

    validate(content, validations.geo_schema)

    r = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key={}'
                      .format(current_app.config['GOOGLE_KEY']), json=content)

    if r.status_code != 200:
        abort(500)

    validate(r.json(), validations.geo_schema_result)

    result = rabbit.channel.basic_publish(exchange=current_app.config['RABBITMQ_EXCHANGE'],
                                          routing_key=routing_key, body=r.json(indent=None))

    return jsonify(success=result)


@app.route("/<routing_key>", methods=['POST'])
@login_required
def handle_hook(routing_key):

    content = request.get_json(force=True)

    if content is not None:
        result = rabbit.channel.basic_publish(exchange=current_app.config['RABBITMQ_EXCHANGE'],
                                              routing_key=routing_key, body=content)

    return jsonify(success=result)
