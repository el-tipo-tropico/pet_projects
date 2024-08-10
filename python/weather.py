'''
Showing the weather forecast for desired location
'''
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
import json
import argparse


def parse_shell_args():
    '''
    function that parse shell args
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-lat', type=float, help='latitude')
    parser.add_argument('-lon', type=float, help='longitude')
    parser.add_argument('-geo_name', type=str, help='city name')
    return parser.parse_args()


def get_data(url=None):
    '''
    function that get data from openmeteo
    '''
    try:
        with urlopen(url) as response:
            return json.load(response)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    return None


def from_weather_code(code):
    '''
    function that return weather description from code
    '''
    weather_codes = {
		0:	"Clear",
		1:	"Mostly Clear",
		2:	"Partly Cloudy",
		3:	"Cloudy",
		45:	"Fog",
		48:	"Freezing Fog",
		51:	"Light Drizzle",
		53:	"Drizzle",
		55:	"Heavy Drizzle",
		56:	"Light Freezing Drizzle",
		57:	"Freezing Drizzle",
		61:	"Light Rain",
		63:	"Rain",
		65:	"Heavy Rain",
		66:	"Light Freezing Rain",
		67:	"Freezing Rain",
		71:	"Light Snow",
		73:	"Snow",
		75:	"Heavy Snow",
		77:	"Snow Grains",
		80:	"Light Rain Shower",
		81:	"Rain Shower",
		82:	"Heavy Rain Shower",
		85:	"Snow Shower",
		86:	"Heavy Snow Shower",
		95:	"Thunderstorm",
		96:	"Hailstorm",
		99:	"Heavy Hailstorm",
    }
    return weather_codes[code]


def current_weather(data, date):
    '''
    the function that print nice formated weather
    '''
    index = data["hourly"]["time"].index(date.split(':')[0] + ":00")
    result = f"Date and time: {datetime.fromisoformat(date).strftime('%d %b %Y %H:%M')}\n"
    result += f"Temperature: {data['hourly']['temperature_2m'][index]} C\n"
    result += f"Weather: {from_weather_code(data['hourly']['weather_code'][index])}"
    print(result)


def weather_forecast(data, date, count=12):
    '''
    the function that print weather forecast
    weather_data - data from openmeteo
    count - number of rows to print
    '''
    print("\nWeather forecast")
    for i in range(len(data['time'])):
        # show only weather from current date
        if datetime.fromisoformat(data['time'][i]).timestamp() < date:
            continue
        if count == 0:
            break
        count = count - 1

        time = data['time'][i].split('T')[1]
        print(f"{time}: {from_weather_code(data['weather_code'][i])} " + \
              f"{data['temperature_2m'][i]} C")


if __name__ == '__main__':
    WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'
    GEO_URL     = 'https://geocoding-api.open-meteo.com/v1/search?name='
    args        = parse_shell_args()

    if args.geo_name is not None:
        geo_data = get_data(GEO_URL + args.geo_name)
        args.lat = geo_data["results"][0]["latitude"]
        args.lon = geo_data["results"][0]["longitude"]

    weather_args = f'?latitude={args.lat}' + \
                   f'&longitude={args.lon}' + \
                   '&hourly=temperature_2m,weather_code' + \
                   '&timezone=auto'
    weather_data = get_data(WEATHER_URL + weather_args)
    cdate = datetime.now().timestamp()
    current_weather(weather_data,
                    datetime.fromtimestamp(cdate).strftime('%Y-%m-%dT%H:%M'))
    weather_forecast(weather_data['hourly'], cdate, 12)
