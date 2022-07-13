from flask_restful import Resource, abort, Api
from flask import request, Response, Blueprint, jsonify
import dataclasses
from dicttoxml import dicttoxml
from src.flask_report.config import pilots

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class ReportApi(Resource):
    def get(self, driver_id=None):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'asc')
        result = get_result_list(driver_id, desc, 'position', format_)
        return Response(result, content_type=f'application/{format_}')


class DriversApi(Resource):
    def get(self, driver_id=None):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'acs')
        result = get_result_list(driver_id, desc, 'name', format_)
        return Response(result, content_type=f'application/{format_}')


def get_result_list(driver_id, desc, sort_param, format_):
    if driver_id and driver_id.upper() not in pilots:
        abort(404, message=f'No driver {driver_id}')
    elif driver_id:
        result = get_result_pilot(pilots[driver_id.upper()], sort_param)
    else:
        result = {}
        if sort_param == 'position':
            sort_func = lambda x: x[1].position
        else:
            sort_func = lambda x: x[1].name.split()[1]
        for key, pilot in sorted(pilots.items(), key=sort_func, reverse=desc == 'desc'):
            result[key] = get_result_pilot(pilot, sort_param)
    if format_ == 'json':
        result = jsonify(result).data
        print(result)
    else:
        result = dicttoxml(result)
    return result


def get_result_pilot(pilot, sort_param):
    result = dataclasses.asdict(pilot)
    if sort_param == 'name':
        del result['lap_time']
    return result


api.add_resource(ReportApi, '/report/<driver_id>', '/report')
api.add_resource(DriversApi, '/report/drivers/<driver_id>', '/report/drivers')
