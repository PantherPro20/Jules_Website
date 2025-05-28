# Basic Flask app structure
from flask import Flask, render_template, request, jsonify
import datetime
import pytz
import os
import requests
import time
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)

NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY')
NEWS_API_URL = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&language=en&country=us,gb" # Using f-string for clarity

# Simple in-memory cache
headlines_cache = {
    "data": None,
    "timestamp": 0
}
CACHE_DURATION_SECONDS = 3600  # 1 hour

COMMON_TIMEZONES = ['UTC', 'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney'] # This list will no longer be used for validation in get_current_time or /api/time

def fetch_and_cache_headlines():
    global headlines_cache
    current_time = time.time()

    # Check cache
    if headlines_cache["data"] and (current_time - headlines_cache["timestamp"] < CACHE_DURATION_SECONDS):
        return headlines_cache["data"] # Return cached data

    if not NEWSDATA_API_KEY:
        print("Error: NEWSDATA_API_KEY environment variable not set.") # Log for server admin
        return {"error": "API key for news service not configured."}

    try:
        response = requests.get(NEWS_API_URL, timeout=10) # Added timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        
        news_data = response.json()
        articles = news_data.get("results", [])
        
        # Extract relevant fields (e.g., title, link, source_id)
        processed_headlines = []
        for article in articles[:10]: # Get top 10 headlines
            processed_headlines.append({
                "title": article.get("title"),
                "link": article.get("link"),
                "source": article.get("source_id") or article.get("creator", "N/A") # Use source_id or creator
            })
        
        # Update cache
        headlines_cache["data"] = {"articles": processed_headlines}
        headlines_cache["timestamp"] = current_time
        return headlines_cache["data"]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}") # Log for server admin
        return {"error": f"Could not fetch news: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred while fetching news."}

def get_current_time(timezone_name='UTC'): # Default to UTC if no name is provided
    try:
        # Attempt to get the timezone object from the provided name
        tz = pytz.timezone(timezone_name)
    except pytz.exceptions.UnknownTimeZoneError:
        # If the timezone_name is unknown to pytz, fall back to UTC
        timezone_name = 'UTC'
        tz = pytz.timezone(timezone_name)
    except Exception:
        # For any other unexpected error, also fall back to UTC
        # Log this error for diagnostics if possible in a real app
        timezone_name = 'UTC'
        tz = pytz.timezone(timezone_name)

    # Get the current time in the determined timezone
    now = datetime.datetime.now(tz=tz)
    # Format the time as HH:MM:SS
    return now.strftime('%H:%M:%S'), timezone_name # Return both time and actual timezone_name used

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/time')
def api_time():
    # Get the timezone from request arguments, default to 'UTC' if not provided.
    # This default is consistent with get_current_time's default.
    requested_timezone_name = request.args.get('timezone', 'UTC')

    # Call get_current_time. It handles UnknownTimeZoneError and defaults to UTC,
    # returning the actual timezone name used.
    formatted_time_string, actual_timezone_name_used = get_current_time(requested_timezone_name)

    # Return the time and the actual timezone name that was used for the calculation.
    return jsonify(current_time=formatted_time_string, timezone=actual_timezone_name_used)

@app.route('/api/countries')
def api_countries():
    countries = [{'code': code, 'name': name} for code, name in pytz.country_names.items()]
    return jsonify(countries)

@app.route('/api/timezones_for_country/<path:country_code>')
def api_timezones_for_country(country_code):
    try:
        timezones = pytz.country_timezones(country_code)
        return jsonify(timezones)
    except KeyError:
        return jsonify(error="Invalid country code"), 404

@app.route('/api/headlines')
def api_headlines():
    data = fetch_and_cache_headlines()
    if "error" in data:
        # You might want to return a specific HTTP status code for errors
        # For now, returning 200 with error in JSON as per current pattern
        return jsonify(data), 503 if "Could not fetch news" in data.get("error","") or "API key" in data.get("error","") else 200
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
