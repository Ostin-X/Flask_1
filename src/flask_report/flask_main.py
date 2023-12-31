from flask import Flask
from src.flask_report.api.routes_api import *
from src.flask_report.site.routes_html import *
from flask_swagger_ui import get_swaggerui_blueprint

db.init('pilots.db')

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(api_bp)
    app.register_blueprint(site_bp)

    swagger_url = '/swagger'
    api_url = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': 'F1 Q1 report API'
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')
