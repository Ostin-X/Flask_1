from flask_restful import Resource
from flask import request
import dataclasses
from flasgger import swag_from
from dict2xml import dict2xml
from dicttoxml import dicttoxml
from src.flask_report.config import pilots


class Driver(Resource):
    @swag_from('drivers.yml')
    def get(self, driver_id):
        print(request.args)
        print(request.form)
        headers = {'Content-Type': 'application/xml'}
        # print(request.args)
        # if form == 'xml':
        xml_str = dicttoxml(dataclasses.asdict(pilots[driver_id.upper()]))
        # api.representations['application/xml'] = headers
        # return xml_str
        return dataclasses.asdict(pilots[driver_id.upper()])

    def put(self, driver_id):
        print(request.args)
        print(request.form)
