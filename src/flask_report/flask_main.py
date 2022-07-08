from flask import Flask, render_template, request, make_response, jsonify, Blueprint
from report.funcs import build_report
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder

data_dir = 'static/data'
pilots = build_report(data_dir)
pilots_dict = {}
for j in pilots.values():
    pilots_dict[j.abbr] = {'name':j.name, 'team':j.team, 'lap_time':str(j.lap_time)}


def create_app():
    app = Flask(__name__)
    # app.json_encoder = LazyJSONEncoder
    api = Api(app) #,doc=False
    template = {
        'swagger': '2.0',
        'info': {
            'title': 'F1 Q1 report API',
            'description': 'API for Q1 data',
            'contact': {
                'responsibleOrganization': 'FIA',
                'responcibleDeveloper': 'Liberty Media',
                'email': 'f1@f1.com',
                'url': 'www.formula1.com'
            },
            'termsOfService': 'https://www.formula1.com/en/toolbar/legal-notices.html',
            'version': '0.0.1'
        },
        'host': '127.0.0.1:3000',
        'basePath': '/api',
        'schemes': ['http', 'https'],
        'operationId': 'getdrivers'
    }

    swagger = Swagger(app, template=template)

    # base = 'http://127.0.0.1:3000/' + 'api/v1'
    menu = [{"name": "Report", "url": f"/report"},
            {"name": "Drivers", "url": f"/drivers?order=Ascending"},
            {"name": "HAM", "url": f"/ham"}]

    class Report(Resource):
        def get(self):
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('report.html', title='Report', menu=menu, pilots=pilots.values()), 200,
                                 headers)

    class Drivers(Resource):
        # @swag_from('drivers.yml', methods=['GET'])
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

    class Driver(Resource):
        @swag_from('drivers.yml')
        def get(self, driver_id):
            return pilots_dict[driver_id.upper()]


    class HAM(Resource):
        def get(self):
            return make_response(render_template('ham.html', title='HAM', menu=menu), 200)

    api.add_resource(Report, '/report', '/')
    api.add_resource(Drivers, '/drivers')
    api.add_resource(Driver, '/api/drivers/<driver_id>')
    api.add_resource(HAM, '/ham')

    # @app.route('/')
    # @app.route('/report')
    # def report():
    #     return render_template('report.html', title='Report', menu=menu, pilots=pilots.values())
    #
    # @app.route('/drivers', methods=['GET'])
    # def drivers():
    #     if request.method == 'GET' and request.args.get('order') == 'Descending':
    #         desc = ['Descending', True]
    #     else:
    #         desc = ['Ascending', False]
    #     if request.method == 'GET' and request.args.get('driver_id'):
    #         pilotzzz = {pilots[request.args.get('driver_id')]}
    #     else:
    #         pilotzzz = sorted(pilots.values(), key=lambda x: x.position, reverse=desc[1])
    #     return render_template('drivers.html', title='Drivers', menu=menu,
    #                            pilots=pilotzzz, desc=desc[0],
    #                            data=['Ascending', 'Descending'])
    #
    # @app.route('/ham')
    # def ham():
    #     return render_template('ham.html', title='HAM', menu=menu)
    #
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=3000, host='127.0.0.1')
