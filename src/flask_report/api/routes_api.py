from flask_restful import Resource, abort, Api
from flask import request, Response, Blueprint
import dataclasses
from dicttoxml import dicttoxml
from src.flask_report.config import pilots

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class DriversAPI(Resource):
    def get(self, driver_id=None):
        format_ = request.args.get('format', 'json')
        if driver_id and driver_id.upper() in pilots:
            result = dataclasses.asdict(pilots[driver_id.upper()])
        elif driver_id:
            abort(404, message=f'No driver {driver_id}')
        else:
            result = {}
            for key, value in pilots.items():
                result[key] = dataclasses.asdict(value)
        if format == 'xml':
            result = dicttoxml(result)
        return result if format_ != 'xml' else Response(dicttoxml(result), content_type='application/xml')


api.add_resource(DriversAPI, '/drivers/<driver_id>', '/drivers')
