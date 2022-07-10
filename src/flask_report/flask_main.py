from flask import Flask
from flask_restful import Api
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder

from flask_api import *
from flask_html import *


def create_app():
    app = Flask(__name__)
    api = Api(app, default_mediatype='application/xml')  # ,doc=False
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
        'operationId': 'getdrivers',
    }

    swagger = Swagger(app, template=template)
    api.add_resource(Report, '/report', '/')
    api.add_resource(Drivers, '/drivers')
    api.add_resource(HAM, '/ham')
    api.add_resource(Driver, '/api/drivers/<driver_id>', '/api/drivers/VAN/?form=<form>')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')
