from flask_restful import Resource, abort, Api
from flask import request, Response, Blueprint, jsonify
# import dataclasses
from dicttoxml import dicttoxml
# from src.flask_report.config import pilots
from src.flask_report.DB.DB import *

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class ReportApi(Resource):
    def get(self, driver_id=None):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'asc')
        result_ = get_result_list(driver_id, desc, 'position')
        result = get_result_format(result_, format_)
        return Response(result, content_type=f'application/{format_}')


class DriversApi(Resource):
    def get(self, driver_id=None):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'acs')
        result_ = get_result_list(driver_id, desc, 'name')
        result = get_result_format(result_, format_)
        return Response(result, content_type=f'application/{format_}')


def get_result_list(driver_id, desc, sort_param):
    # if driver_id and driver_id.upper() not in pilots:
    if driver_id and not Pilot.select().where(Pilot.abbr == driver_id.upper()):
        abort(404, message=f'No driver {driver_id}')
    elif driver_id:
        # result = get_result_pilot(pilots[driver_id.upper()], sort_param)
        result = get_result_pilot(Pilot.get(Pilot.abbr == driver_id.upper()), sort_param, SessionTime)
    else:
        result = {}
        # if sort_param == 'position':
        #     sort_func = lambda x: x[1].position
        # else:
        #     sort_func = lambda x: x[1].name.split()[1]
        # for key, pilot in sorted(pilots.items(), key=sort_func, reverse=desc == 'desc'):
        if desc == 'desc' and sort_param == 'name':
            sorted_db = Pilot.select().order_by(Pilot.abbr.desc())
        elif sort_param == 'name':
            sorted_db = Pilot.select().order_by(Pilot.abbr)
        elif desc == 'desc' and sort_param == 'position':
            sorted_db = Pilot.select().join(SessionTime).group_by(Pilot).order_by(SessionTime.lap_time.desc())
        else:
            sorted_db = Pilot.select().join(SessionTime).group_by(Pilot).order_by(SessionTime.lap_time)
        for key in sorted_db:
            # result[key] = get_result_pilot(pilot, sort_param)
            result[key.abbr] = get_result_pilot(Pilot.get(Pilot.abbr == key), sort_param, SessionTime)
    return result


def get_result_pilot(pilot, sort_param, SessionTime):
    # result = dataclasses.asdict(pilot)
    result = {'abbr': pilot.abbr, 'name': pilot.name, 'team': pilot.team.name}
    # if sort_param == 'name':
    #     del result['lap_time']
    if sort_param == 'position':
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
