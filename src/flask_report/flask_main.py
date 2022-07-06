from flask import Flask, render_template, request
from report.funcs import build_report
from flask_restful import Resource, Api
import json

data_dir = 'static/data'
pilots = build_report(data_dir)
pilots_dict = {}

for j in pilots.values():
    pilots_dict[j.abbr] = [j.name, j.team, str(j.lap_time)]


def create_app():
    app = Flask(__name__)
    api = Api(app)

    menu = [{"name": "Report", "url": "/report"},
            {"name": "Drivers", "url": "/drivers?order=Ascending"},
            {"name": "HAM", "url": "/ham"}]

    class Main(Resource):
        def get(self):
            return json.dumps(pilots_dict)

    class Driver(Resource):
        def get(self, pilot_id):
            return pilots_dict[pilot_id.upper()]

    api.add_resource(Main, '/api/v1/report')
    api.add_resource(Driver, '/api/v1/report/<pilot_id>')

    @app.route('/')
    @app.route('/report')
    def report():
        return render_template('report.html', title='Report', menu=menu, pilots=pilots.values())

    @app.route('/drivers', methods=['GET'])
    def drivers():
        if request.method == 'GET' and request.args.get('order') == 'Descending':
            desc = ['Descending', True]
        else:
            desc = ['Ascending', False]
        if request.method == 'GET' and request.args.get('driver_id'):
            pilotzzz = {pilots[request.args.get('driver_id')]}
        else:
            pilotzzz = sorted(pilots.values(), key=lambda x: x.position, reverse=desc[1])
        return render_template('drivers.html', title='Drivers', menu=menu,
                               pilots=pilotzzz, desc=desc[0],
                               data=['Ascending', 'Descending'])

    @app.route('/ham')
    def ham():
        return render_template('ham.html', title='HAM', menu=menu)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=3000, host='127.0.0.1')
