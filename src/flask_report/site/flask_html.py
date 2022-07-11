from flask_restful import Resource, Api
from flask import make_response, render_template, request, Blueprint
from src.flask_report.config import pilots, menu

site_bp = Blueprint('site', __name__)
site = Api(site_bp)


class Report(Resource):
    def get(self):
        # headers = {'Content-Type': 'text/html'}
        return make_response(render_template('report.html', title='Report', menu=menu, pilots=pilots.values()), 200)


class Drivers(Resource):
    def get(self):
        if request.method == 'GET' and request.args.get('order') == 'Descending':
            desc = ['Descending', True]
        else:
            desc = ['Ascending', False]
        if request.method == 'GET' and request.args.get('driver_id'):
            pilotzzz = [pilots[request.args.get('driver_id')]]
        else:
            pilotzzz = sorted(pilots.values(), key=lambda x: x.position, reverse=desc[1])
        return make_response(render_template('drivers.html', title='Drivers', menu=menu,
                                             pilots=pilotzzz, desc=desc[0],
                                             data=['Ascending', 'Descending']), 200)


class HAM(Resource):
    def get(self):
        return make_response(render_template('ham.html', title='HAM', menu=menu), 200)


site.add_resource(Report, '/report', '/')
site.add_resource(Drivers, '/drivers')
site.add_resource(HAM, '/ham')
