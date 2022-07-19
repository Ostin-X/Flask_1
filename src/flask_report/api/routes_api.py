from flask_restful import Resource, abort, Api
from flask import request, Response, Blueprint, jsonify
from dicttoxml import dicttoxml
from src.flask_report.db.models import *

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class ReportApi(Resource):
    def get(self):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'asc')
        result = {}
        if desc == 'desc':
            sorted_db = Pilot.select().join(SessionTime).group_by(Pilot).order_by(-SessionTime.lap_time)
        else:
            sorted_db = Pilot.select().join(SessionTime).group_by(Pilot).order_by(SessionTime.lap_time)
        for pilot in sorted_db:
            result[pilot.abbr] = get_result_pilot(pilot, True)
        result = get_result_format(result, format_)
        return Response(result, content_type=f'application/{format_}')


class DriversApi(Resource):
    def get(self, driver_id=''):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'acs')
        selected_db_pilot = Pilot.select().where(Pilot.abbr == driver_id.upper())
        if not driver_id:
            result = {}
            if desc == 'desc':
                sorted_db = Pilot.select().order_by(-Pilot.abbr)
            else:
                sorted_db = Pilot.select().order_by(Pilot.abbr)
            for pilot in sorted_db:
                result[pilot.abbr] = get_result_pilot(pilot)
        elif selected_db_pilot:
            result = get_result_pilot(selected_db_pilot.get())
        else:
            abort(404, message=f'No driver {driver_id}')
        result = get_result_format(result, format_)
        return Response(result, content_type=f'application/{format_}')


def get_result_pilot(pilot, need_lap_time=None):
    result = {'abbr': pilot.abbr, 'name': pilot.name, 'team': pilot.team.name}
    if need_lap_time:
        result['lap_time'] = SessionTime.get(SessionTime.pilot_abbr == result['abbr']).lap_time
    return result


def get_result_format(result, format_):
    if format_ == 'json':
        result = jsonify(result).data
    else:
        result = dicttoxml(result)
    return result


api.add_resource(ReportApi, '/report/<driver_id>', '/report')
api.add_resource(DriversApi, '/report/drivers/<driver_id>', '/report/drivers')
