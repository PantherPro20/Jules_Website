# main.py
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
import datetime
import pytz
import requests
import time
import json # Good to have for potential direct JSON manipulation

# --- Jinja2 Template Setup ---
# Get the absolute path to the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))

# --- NewsData.io API Configuration & Cache ---
NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY')
NEWS_API_URL = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&language=en&country=us,gb"
headlines_cache = {
    "data": None,
    "timestamp": 0
}
CACHE_DURATION_SECONDS = 3600  # 1 hour

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

def fetch_and_cache_headlines():
    global headlines_cache # Declare global as we are modifying it
    current_time = time.time()

    # Check cache
    if headlines_cache["data"] and \
       (current_time - headlines_cache["timestamp"] < CACHE_DURATION_SECONDS):
        return headlines_cache["data"]

    if not NEWSDATA_API_KEY:
        return {"error": "API key for news service not configured."} # Return error

    try:
        response = requests.get(NEWS_API_URL, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        news_data = response.json()
        articles = news_data.get("results", [])
        
        processed_headlines = []
        for article in articles[:10]: # Get top 10 headlines
            processed_headlines.append({
                "title": article.get("title"),
                "link": article.get("link"),
                "source": article.get("source_id") or article.get("creator", "N/A")
            })
        
        # Update cache
        headlines_cache["data"] = {"articles": processed_headlines}
        headlines_cache["timestamp"] = current_time
        return headlines_cache["data"]

    except requests.exceptions.RequestException as e:
        # In a real app, log this error (e.g., cherrypy.log(str(e)))
        return {"error": f"Could not fetch news: {str(e)}"}
    except Exception as e:
        # In a real app, log this error
        return {"error": f"An unexpected error occurred while fetching news: {str(e)}"}

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


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def headlines(self):
        data = fetch_and_cache_headlines()
        if "error" in data:
             # Example: API key not configured or could not fetch news
             # cherrypy.response.status = 503 # Service unavailable - let's use HTTPError for consistency
             if "API key for news service not configured" in data["error"] or \
                "Could not fetch news" in data["error"]:
                 raise cherrypy.HTTPError(503, data["error"])
             # For other errors within data that are not server-side faults, pass them as JSON
        return data

class Root:
    api = Api() # Mount the Api class at /api

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()

# --- Main Execution ---
if __name__ == '__main__':
    # CherryPy Global Configuration
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 5000,
        }
    }
    cherrypy.quickstart(Root(), '/', config=conf)
