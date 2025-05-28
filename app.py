# Basic Flask app structure
from flask import Flask, render_template, request
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
    selected_timezone = 'US/Eastern'
    if 'timezone' in request.args:
        selected_timezone = request.args.get('timezone')
        if selected_timezone not in COMMON_TIMEZONES:
            selected_timezone = 'US/Eastern' # default to US/Eastern if invalid timezone is provided

    current_time = get_current_time(selected_timezone)
    return render_template('index.html', current_time=current_time, timezones=COMMON_TIMEZONES, selected_timezone=selected_timezone)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
