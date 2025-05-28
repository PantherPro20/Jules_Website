# main.py
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
import datetime
import pytz
# import requests # Removed
# import time # Removed
import json # Good to have for potential direct JSON manipulation
# os is still used for current_dir
import datetime # Ensure datetime is still imported for get_current_time

# --- Jinja2 Template Setup ---
# Get the absolute path to the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))

# --- NewsData.io API Configuration & Cache --- (REMOVED)
# NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY')
# NEWS_API_URL = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&language=en&country=us,gb"
# headlines_cache = {
#    "data": None,
#    "timestamp": 0
# }
# CACHE_DURATION_SECONDS = 3600  # 1 hour

# --- Helper Functions ---
def get_current_time(timezone_name='UTC'):
    try:
        tz = pytz.timezone(timezone_name)
    except pytz.exceptions.UnknownTimeZoneError:
        timezone_name = 'UTC'
        tz = pytz.timezone(timezone_name)
    except Exception: # Generic fallback
        timezone_name = 'UTC'
        tz = pytz.timezone(timezone_name)
    
    now = datetime.datetime.now(tz=tz)
    return now.strftime('%H:%M:%S'), timezone_name

# def fetch_and_cache_headlines(): (REMOVED)
    # ... (function content removed)

# --- CherryPy Application Root Class ---
class Api:
    @cherrypy.expose
    @cherrypy.tools.json_out() # Automatically converts dict to JSON and sets content type
    def time(self, timezone=None): # timezone will be from query string e.g. /api/time?timezone=US/Eastern
        if timezone is None:
            timezone = 'UTC' # Default if not provided
        time_str, actual_timezone_name = get_current_time(timezone)
        return {"current_time": time_str, "timezone": actual_timezone_name}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        country_list = [{'code': code, 'name': name} for code, name in pytz.country_names.items()]
        return country_list

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def timezones_for_country(self, country_code): # country_code from path e.g. /api/timezones_for_country/US
        try:
            timezones = pytz.country_timezones(country_code)
            return timezones
        except KeyError:
            raise cherrypy.HTTPError(404, "Invalid country code")

    # def headlines(self): (REMOVED)
        # ... (method content removed)

class Root:
    api = Api() # Mount the Api class at /api

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()

# --- Main Execution ---
if __name__ == '__main__':
    # CherryPy Global Configuration
    static_dir = os.path.join(current_dir, 'static')

    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 5000,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': static_dir
        }
    }
    cherrypy.quickstart(Root(), '/', config=conf)
