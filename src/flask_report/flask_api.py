from flask_restful import Resource, abort
from flask import request, Response
import dataclasses
from flasgger import swag_from
from dict2xml import dict2xml
from dicttoxml import dicttoxml
from src.flask_report.config import pilots
from xml.etree.ElementTree import Element, tostring


class Drivers_API(Resource, Response):
    @swag_from('drivers.yml')
    def get(self, driver_id=None):
        if request.method == 'GET' and request.args.get('format') and request.args.get('format') == 'xml':
            if driver_id and driver_id.upper() in pilots:
                xml_result = dicttoxml(dataclasses.asdict(pilots[driver_id.upper()]), attr_type=False)
                return Response(xml_result, content_type='application/xml')
            elif driver_id:
                abort(404, message=f'No such driver {driver_id}')
            else:
                xml_result = {}
                for key, value in pilots.items():
                    xml_result[key] = dataclasses.asdict(value)
                xml_result = dicttoxml(xml_result, attr_type=False)
                return Response(xml_result, content_type='application/xml')
        else:
            if driver_id and driver_id.upper() in pilots:
                return dataclasses.asdict(pilots[driver_id.upper()])
            elif driver_id:
                abort(404, message=f'No such driver {driver_id}')
            else:
                result = {}
                for key, value in pilots.items():
                    result[key] = dataclasses.asdict(pilots[key])
                return result

    def put(self, driver_id):
        print(request.args)
        print(request.form)
