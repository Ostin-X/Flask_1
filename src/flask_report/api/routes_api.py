from flask_restful import Resource, abort, Api
from flask import request, Response, Blueprint
import dataclasses
from dicttoxml import dicttoxml
from src.flask_report.config import pilots

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class ReportApi(Resource):
    def get(self, driver_id=None):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'asc')
        # if driver_id and driver_id.upper() not in pilots:
        #     abort(404, message=f'No driver {driver_id}')
        # else:
        result = get_result_list(driver_id, desc, 'position')
        return result if format_ != 'xml' else Response(dicttoxml(result), content_type='application/xml')


class DriversApi(Resource):
    def get(self, driver_id=None):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'acs')
        # if driver_id and driver_id.upper() not in pilots:
        #     abort(404, message=f'No driver {driver_id}')
        # else:
        result = get_result_list(driver_id, desc, 'name')
        return result if format_ != 'xml' else Response(dicttoxml(result), content_type='application/xml')


def get_result_list(driver_id, desc, sort_param):
    if driver_id and driver_id.upper() not in pilots:
        abort(404, message=f'No driver {driver_id}')
    elif driver_id:
        result = get_lap_time_right(pilots[driver_id.upper()], sort_param)
    else:
        result = {}
        if sort_param == 'position':
            sort_func = lambda x: x[1].position
        else:
            sort_func = lambda x: x[1].name.split()[1]
        for key, pilot in sorted(pilots.items(), key=sort_func, reverse=desc == 'desc'):
            result[key] = get_lap_time_right(pilot, sort_param)
    return result


def get_lap_time_right(pilot, sort_param):
    result = dataclasses.asdict(pilot)
    if sort_param == 'name':
        del result['lap_time']
    return result


api.add_resource(ReportApi, '/report/<driver_id>', '/report')
api.add_resource(DriversApi, '/report/drivers/<driver_id>', '/report/drivers')
