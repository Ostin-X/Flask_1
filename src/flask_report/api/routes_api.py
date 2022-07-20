from flask_restful import Resource, abort, Api
from flask import request, Response, Blueprint, jsonify
from dicttoxml import dicttoxml
from dict2xml import dict2xml
from src.flask_report.db.models import *


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class ReportApi(Resource):
    def get(self):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'asc')

        sort_by = ~SessionTime.lap_time if desc == 'desc' else SessionTime.lap_time
        sorted_db = Pilot.select().join(SessionTime).group_by(Pilot).order_by(sort_by)

        result = get_result_list(sorted_db, True)
        result = get_result_format(result, format_)
        return Response(result, content_type=f'application/{format_}')


class DriversApi(Resource):
    def get(self, driver_id=''):
        format_ = request.args.get('format', 'json')
        desc = request.args.get('order', 'acs')

        if not driver_id:
            sort_by = -Pilot.abbr if desc == 'desc' else Pilot.abbr
            sorted_db = Pilot.select().order_by(sort_by)
            result = get_result_list(sorted_db)
        else:
            selected_db_pilot = Pilot.select().where(Pilot.abbr == driver_id.upper())
            if selected_db_pilot:
                result = [get_result_pilot(selected_db_pilot.get())]
            else:
                abort(404, message=f'No driver {driver_id}')
        result = get_result_format(result, format_)
        return Response(result, content_type=f'application/{format_}')


def get_result_list(sorted_db, need_lap_time=None):
    result = []
    for pilot in sorted_db:
        result.append(get_result_pilot(pilot, need_lap_time))
    return result


def get_result_pilot(pilot, need_lap_time=None):
    result = {'abbr': pilot.abbr, 'name': pilot.name, 'team': pilot.team.name}
    if need_lap_time:
        result['lap_time'] = SessionTime.get(SessionTime.pilot_abbr == result['abbr']).lap_time
    return result


def get_result_format(result, format_):
    if format_ == 'json':
        result = jsonify(result).data
    else:
        tmp_str = ''
        for row in result:
            tmp_str += '<driver>'
            for key, item in row.items():
                tmp_str += f'<{key}>{item}</{key}>'
            tmp_str += '</driver>'
            if len(result) == 1:
                tmp_str = tmp_str[8:-9]
        result = bytes('<?xml version="1.0" encoding="UTF-8" ?><root>' + tmp_str + '</root>', 'utf-8')
        # result = '<?xml version="1.0" encoding="UTF-8" ?><root>' + dict2xml(result, wrap="driver", newlines=False,
        #                                                                     indent="") + '</root>'
    return result


api.add_resource(ReportApi, '/report/<driver_id>', '/report')
api.add_resource(DriversApi, '/report/drivers/<driver_id>', '/report/drivers')
