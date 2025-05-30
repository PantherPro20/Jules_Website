# app.py
from flask import Flask, render_template, request, jsonify
import datetime
import pytz

app = Flask(__name__)

# --- Helper Function for Time ---
def get_current_time(timezone_name='UTC'):
    try:
        tz = pytz.timezone(timezone_name)
    except pytz.exceptions.UnknownTimeZoneError:
        timezone_name = 'UTC' # Default to UTC on error
        tz = pytz.timezone(timezone_name)
    except Exception:
        timezone_name = 'UTC' # Generic fallback
        tz = pytz.timezone(timezone_name)

    now = datetime.datetime.now(tz=tz)
    return now.strftime('%H:%M:%S'), timezone_name

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/time')
def api_time():
    timezone_param = request.args.get('timezone', 'UTC') # Default to UTC if not provided
    current_time_str, actual_timezone_name = get_current_time(timezone_param)
    return jsonify(current_time=current_time_str, timezone=actual_timezone_name)

@app.route('/api/countries')
def api_countries():
    country_list = [{'code': code, 'name': name} for code, name in pytz.country_names.items()]
    return jsonify(country_list)

@app.route('/api/timezones_for_country/<path:country_code>')
def api_timezones_for_country(country_code):
    try:
        timezones = pytz.country_timezones(country_code)
        return jsonify(timezones)
    except KeyError:
        return jsonify(error="Invalid country code"), 404

@app.route('/play_dino_game')
def play_dino_game():
    return render_template('dino_game.html')

if __name__ == '__main__':
    # Note: When run with "flask run", it uses host/port from ENV vars or defaults.
    # For direct "python app.py" execution (not used by Docker typically):
    # app.run(host='0.0.0.0', port=5000, debug=False)
    # We will rely on "flask run" via Docker CMD, so the above app.run is not strictly needed here
    # but doesn't hurt for potential local direct execution.
    # For now, let's omit the app.run() specific to direct python execution
    # as the Docker CMD will be 'flask run'.
    pass # No app.run() needed for 'flask run'
