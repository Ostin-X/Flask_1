from flask import Flask, render_template, request, url_for
from src.report.funcs import build_report

data_dir = 'src/report/static/data'
pilots = build_report(data_dir)


def create_app():
    app = Flask(__name__)

    menu = [{"name": "Report", "url": "/report"},
            {"name": "Drivers", "url": "/drivers?order=Ascending"},
            {"name": "HAM", "url": "/ham"}]

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
    app.run(debug=True)
