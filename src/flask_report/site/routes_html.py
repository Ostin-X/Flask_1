from flask_restful import Resource, Api, abort
from flask import make_response, render_template, request, Blueprint
from src.flask_report.config import pilots_list, menu

site_bp = Blueprint('site', __name__)
site = Api(site_bp)


class Report(Resource):
    def get(self):
        return make_response(render_template('report.html', title='Report', menu=menu, pilots=pilots_list.values()), 200)


# class Report(Resource):
#     def get(self):
#         desc = request.args.get('order', 'Ascending')
#         pilotzzz = sorted(pilots.values(), key=lambda x: x.position, reverse=desc == 'Descending')
#         return make_response(render_template('report.html', title='Report', menu=menu,
#                                              pilots=pilotzzz, desc=desc[0],
#                                              data=['Ascending', 'Descending']), 200)


class Drivers(Resource):
    def get(self, driver_id=None):
        desc = request.args.get('order', 'Ascending')
        if driver_id:
            if driver_id.upper() not in pilots_list:
                abort(404, message=f'No driver {driver_id}')
            pilotzzz = [pilots_list[driver_id]]
        else:
            pilotzzz = sorted(pilots_list.values(), key=lambda x: x.name.split()[1], reverse=desc == 'Descending')
        return make_response(render_template('drivers.html', title='Drivers', menu=menu,
                                             pilots=pilotzzz, desc=desc[0],
                                             data=['Ascending', 'Descending']), 200)


class HAM(Resource):
    def get(self):
        return make_response(render_template('ham.html', title='HAM', menu=menu), 200)


@site_bp.app_errorhandler(404)
def handle_404(e):
    return render_template('Error404.html', title='Error 404', menu=menu), 404


site.add_resource(Report, '/report', '/', endpoint='/report')
site.add_resource(Drivers, '/report/drivers/<driver_id>', '/report/drivers')
site.add_resource(HAM, '/ham')
