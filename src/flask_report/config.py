from report_f1.funcs import build_report

data_dir = 'static/data'

pilots_list = build_report(data_dir)


teams = [['Sauber', 'Ferrari', 'Switzerland', 'Hinwill, CH'],
         ['Toro Rosso', 'Red Bull', 'Maranello, IT', 'Faenza, IT'],
         ['Renault', 'Renault', 'France', 'Enstone, UK'],
         ['Force India', 'Mercedes', 'United Kingdom', 'Silverstone, UK'],
         ['Ferrari', 'Ferrari', 'Italy', 'Maranello, IT'], ['Haas', 'Ferrari', 'United States', 'Kannapolis, US'],
         ['McLaren', 'Mercedes', 'United Kingdom', 'Woking, UK'], ['Mercedes', 'Mercedes', 'Germany', 'Brackley, UK'],
         ['Red Bull', 'Red Bull', 'Austria', 'Milton Keynes, UK'],
         ['Williams', 'Mercedes', 'United Kingdom', 'Grove, UK']]

pilot_nations = {'RIC': 'Australia', 'VET': 'Germany', 'HAM': 'United Kingdom', 'RAI': 'Finland', 'BOT': 'Finland',
                 'OCO': 'France', 'ALO': 'Spain', 'SAI': 'Spain', 'PER': 'Mexico', 'GAS': 'France', 'HUL': 'Germany',
                 'VAN': 'Belgium', 'SIR': 'ass', 'LEC': 'Monaco', 'GRO': 'France', 'HAR': 'United Kingdom',
                 'ERI': 'Sweden', 'STR': 'United Kingdom', 'MAG': 'Denmark'}

menu = [{"name": "Report", "url": f"/report?order=Ascending"},
        {"name": "Drivers", "url": f"/report/drivers?order=Ascending"},
        {"name": "HAM", "url": f"/ham"}]
