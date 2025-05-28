# Basic Flask app structure
from flask import Flask, render_template, request, jsonify
import datetime
import pytz

app = Flask(__name__)

COMMON_TIMEZONES = ['UTC', 'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney']

def get_current_time(timezone_name):
    tz = pytz.timezone(timezone_name)
    current_time = datetime.datetime.now(tz=tz)
    return current_time.strftime('%H:%M:%S')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/time')
def api_time():
    timezone_name = request.args.get('timezone', 'US/Eastern')
    if timezone_name not in COMMON_TIMEZONES: # Optional: validate if the provided timezone is in our list
        timezone_name = 'US/Eastern' # or return jsonify(error="Invalid timezone"), 400
    
    formatted_time_string = get_current_time(timezone_name)
    return jsonify(current_time=formatted_time_string, timezone=timezone_name)

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
