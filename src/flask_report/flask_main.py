from flask import Flask
from flask_restful import Api
from flasgger import Swagger, LazyString, LazyJSONEncoder
from src.flask_report.api.flask_api import *
from src.flask_report.site.flask_html import *


def create_app():
    app = Flask(__name__)
    # api = Api(app)  # ,doc=False
    app.register_blueprint(api_bp)
    app.register_blueprint(site_bp)

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
        'basePath': '/api/v1',
        'schemes': ['http', 'https'],
        'operationId': 'getdrivers',
    }

    swagger = Swagger(app, template=template)

    # api.add_resource(Report, '/report', '/')
    # api.add_resource(Drivers, '/drivers')
    # api.add_resource(HAM, '/ham')
    # api.add_resource(DriversAPI, '/api/v1/drivers/<driver_id>', '/api/v1/drivers')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')
