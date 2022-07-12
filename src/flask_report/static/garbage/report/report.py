

class Report(Resource):
    def get(self):
        return make_response(render_template('report.html', title='Report', menu=menu, pilots=pilots.values()), 200)