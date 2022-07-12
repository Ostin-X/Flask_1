from report_f1.funcs import build_report

data_dir = 'static/data'
pilots = build_report(data_dir)
menu = [{"name": "Drivers", "url": f"/drivers?order=Ascending"},
        # {"name": "Report", "url": f"/report"},
        {"name": "HAM", "url": f"/ham"}]
