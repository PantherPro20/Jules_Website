# Basic Flask app structure
from flask import Flask, render_template, request, jsonify
import datetime
import pytz

app = Flask(__name__)

COMMON_TIMEZONES = ['UTC', 'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney'] # This list will no longer be used for validation in get_current_time or /api/time

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
