from flask_restful import Resource
from flask import make_response, render_template, request
from config import pilots, menu


class Report(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('report.html', title='Report', menu=menu, pilots=pilots.values()), 200,
                             headers)


class Drivers(Resource):
    def get(self):
        if request.method == 'GET' and request.args.get('order') == 'Descending':
            desc = ['Descending', True]
        else:
            desc = ['Ascending', False]
        if request.method == 'GET' and request.args.get('driver_id'):
            pilotzzz = {pilots[request.args.get('driver_id')]}
        else:
            pilotzzz = sorted(pilots.values(), key=lambda x: x.position, reverse=desc[1])
        return make_response(render_template('drivers.html', title='Drivers', menu=menu,
                                             pilots=pilotzzz, desc=desc[0],
                                             data=['Ascending', 'Descending']), 200)


class HAM(Resource):
    def get(self):
        return make_response(render_template('ham.html', title='HAM', menu=menu), 200)
