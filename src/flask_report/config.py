from report_f1.funcs import build_report

data_dir = 'static/data'
pilots = build_report(data_dir)
menu = [{"name": "Report", "url": f"/report?order=Ascending"},
        {"name": "Drivers", "url": f"/report/drivers"},
        {"name": "HAM", "url": f"/ham"}]
