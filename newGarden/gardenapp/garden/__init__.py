from flask import Blueprint, jsonify
from sqlalchemy_serializer import SerializerMixin

from connect.gardensession import GardenSession

blueprint_name = 'garden'
data = Blueprint('garden', __name__, url_prefix="/{}".format(blueprint_name))


@data.route('/', methods=['GET'])
def get_plants():
    with GardenSession() as session:
        return _get_response(
             session.get_all_plant(), 200
        )


@data.route('/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    with GardenSession() as session:
        plant = session.get_plant_by_id(plant_id)
    if plant is None:
        return _get_error_response("Not found plant!", 404)
    return _get_response(
         plant, 200
    )


@data.route('/<int:plant_id>/lifelines', methods=['GET'])
def get_lifelines_of_plant(plant_id):
    with GardenSession() as session:
        if not session.is_plant_exists(plant_id):
            return _get_error_response("Not found plant!", 404)
        return _get_response(
             session.get_plant_lifelines(plant_id), 200
        )


@data.route('/<int:plant_id>/lifelines/<int:lifeline_id>', methods=['GET'])
def get_lifeline_of_plant(plant_id, lifeline_id):
    with GardenSession() as session:
        if not session.is_plant_exists(plant_id):
            return _get_error_response("Not found plant!", 404)
        lifeline = session.get_plant_lifeline(plant_id, lifeline_id)
    if lifeline is None:
        return _get_error_response("Not found lifeline!", 404)
    return _get_response(
         lifeline, 200
    )


def _to_dict(data: (SerializerMixin, list)):
    if isinstance(data, list):
        return [serializer_mixin.to_dict() for serializer_mixin in data]
    return data.to_dict()


def _get_response(data, code: int):
    resp = jsonify(_to_dict(data))
    resp.status_code = code
    return resp


def _get_error_response(message: str, code: int):
    resp = jsonify({"error": message})
    resp.status_code = code
    return resp