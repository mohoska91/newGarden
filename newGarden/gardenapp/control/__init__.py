from flask import Blueprint, jsonify, request, current_app

from connect.messanger import GardenerStartMessage, GardenerMessenger, GardenerStopMessage

blueprint_name = 'control'
control = Blueprint(blueprint_name, __name__, url_prefix="/{}".format(blueprint_name))
messanger = GardenerMessenger("configdb", 6379)


@control.route('/start', methods=['POST'])
def start():
    return _action(request.get_json(), GardenerStartMessage)


@control.route('/stop', methods=['POST'])
def stop():
    return _action(request.get_json(), GardenerStopMessage)


def _action(data, message_class):
    rh = current_app.config["REDIS_HOST"]
    rp = current_app.config["REDIS_PORT"]
    try:
        lifeline_id = data['lifeline_id']
    except KeyError as ke:
        return _get_error_response("Missing parameter {}".format(ke.args[0]), 404)
    GardenerMessenger(rh, rp).put_message(message_class(lifeline_id))
    #TODO not only 200, but real response
    return _get_request_response({}, 200)


def _get_request_response(data: (dict, list), code: int):
    resp = jsonify(data)
    resp.status_code = code
    return resp


def _get_error_response(message: str, code: int):
    resp = jsonify({"error": message})
    resp.status_code = code
    return resp