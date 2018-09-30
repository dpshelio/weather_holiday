from datetime import datetime
import urllib

from weather import Weather, Unit
import yaml
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


icons = {
    'Thunderstorms': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/thundershowers_day_night@2x.png',
    'Scattered Thunderstorms': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/scattered_showers_day_night@2x.png',
    'Scattered Showers': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/scattered_showers_day_night@2x.png',
    'Mostly Sunny': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/fair_day@2x.png',
    'Sunny': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/clear_day@2x.png',
    'Partly Cloudy': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/partly_cloudy_day@2x.png',
    'Mostly Cloudy': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/mostly_cloudy_day_night@2x.png',
    'Cloudy': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/cloudy_day_night@2x.png',
    'Rain': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/rain_day_night@2x.png',
    'Rain and Snow': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/snow_rain_mix_day_night@2x.png',
    'Breezy': 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/windy_day_night@2x.png',
}


with open('holidays.yaml', 'r') as f:
    holidays = yaml.load(f.read())
# Wow! Yaml load converts dates!!

weather = Weather(unit=Unit.CELSIUS)
date = []
pos = []
min_temp = []
max_temp = []
text = []
place = []


for location in holidays:
    if 'latlong' in location.keys():
        loc = weather.lookup_by_latlng(*location['latlong'])
    else:
        loc = weather.lookup_by_location(location['place'])

    for forecast in loc.forecast:
        # Does the time is in local time? Discrepancy between website and data received.
        if datetime.strptime(forecast.date, '%d %b %Y').date() == location['date']:
            print("Weather for {} on {:%d %b}".format(location['place'], location['date']))
            print("  {} with {}/{}".format(forecast.text,
                                           forecast.low,
                                           forecast.high))
            pos.append(location.get('latlong', None)) # TODO get the coordinates for display on map
            min_temp.append(float(forecast.low))
            max_temp.append(float(forecast.high))
            text.append(forecast.text)
            date.append(location['date'])
            place.append(location['place'])
            break


fig = plt.figure(figsize=(15, 4))
ax = fig.add_subplot(111)
ax.set_ylim(min(*min_temp, -5), max(*max_temp, 35))

plt.plot(date, max_temp)
plt.plot(date, min_temp)

# Displays icons for each day in the top.
for day, txt in zip(date, text):
    arr_img = plt.imread(urllib.request.urlopen(icons[txt]), format="png")
    imagebox = OffsetImage(arr_img, zoom=0.2)
    imagebox.image.axes = ax
    ab = AnnotationBbox(imagebox, (day, 30),
                        xybox=(0., 0.),
                        xycoords='data',
                        boxcoords="offset points",
                        pad=0.3,
                        arrowprops=dict(arrowstyle="->"),
                        bboxprops=dict(edgecolor='red', fc='black'))

    ax.add_artist(ab)


# Displays text for each day in the bottom
for day, pl in zip(date, place):
    ax.annotate(pl, xy=(day, 0), ha='center', xycoords='data')

fig.savefig('output.png')
