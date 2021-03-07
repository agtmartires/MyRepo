# Simple webapp that gets server date/time and converts to Asia/Manila time
# To demo simple API request and response handling with json

import time
from datetime import datetime
import requests
from flask import Flask

app = Flask(__name__)

def showtime():
    unix_time = int(time.time())
    print(datetime.now().date())
    print(datetime.now().time())
    print(unix_time)
    print(time.tzname[0])

    res = "<b>SERVER DATE/TIME:</b> <br>" + str(datetime.now().date()) + "<br>" + str(datetime.now().time()) + "<br>" + str(unix_time) + "<br>" 

    # Get proper zone name
    response = requests.get("http://api.timezonedb.com/v2.1/get-time-zone?key=EJGOCJW6YIQ9&format=json&by=zone&zone="+time.tzname[0])

    if response.status_code == 200:
        print('get timezone Success!')
        json_response = response.json()
        print("zoneName = " + json_response["zoneName"])
        res = res + json_response["zoneName"] + "<br><br>" + "<b>MANILA DATE/TIME:</b> <br>"

        # Convert timezone from zone to Asia/Manila
        URL = "http://api.timezonedb.com/v2.1/convert-time-zone?key=EJGOCJW6YIQ9&format=json&from=" + json_response[
                "zoneName"] + "&to=Asia/Manila&time=" + str(unix_time) 
        print(URL)
        response = requests.get(URL)

        if response.status_code == 200:
            print('Success!')
            json_response = response.json()
            print(json_response)

            print(json_response["toTimestamp"])
            value = datetime.fromtimestamp(json_response["toTimestamp"])
            print(f"{value:%Y-%m-%d %H:%M:%S}")
            res = res + (f"{value:%Y-%m-%d %H:%M:%S}")
            return res

        elif response.status_code == 404:
            return('Not Found.')

    elif response.status_code == 404:
        return ('Not Found.')


@app.route("/")
def webapp():
    return showtime()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=1234)

