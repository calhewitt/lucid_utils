import ephem
import datetime
from PIL import Image, ImageDraw
import os

class lucid_telemetry:
	pass

def dms_to_dd(dms):
	values = str(dms).split(':')
	deg = float(values[0])
	mins = float(values[1])
	sec = float(values[2])
	if deg >= 0:
		dd = deg + (mins / 60) + (sec / 3600)
	else:
		dd = deg - (mins / 60) - (sec / 3600)
	return dd

def get_position(*args):

	if len(args) == 1: tle_file, time = "tds1.txt", args[0]
	else: tle_file, time = args[0], args[1]

	# Open TLE file and pass it to pyEphem
	tle_file = open(os.path.dirname(os.path.realpath(__file__)) + "/" + tle_file, 'r').read()
	tle_lines = tle_file.split("\n")
	tle_rec = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])
	if time == None:
		tle_rec.compute()
	else:
		time = datetime.datetime.utcfromtimestamp(time).strftime('%Y/%m/%d %H:%M:%S')
		tle_rec.compute(time)

	lat = dms_to_dd(tle_rec.sublat)
	lng = dms_to_dd(tle_rec.sublong)

	data = lucid_telemetry()
	data.latitude = lat
	data.longitude = lng

	return data

def get_current_position(tle_file = "tds1.txt"):
	return get_position(tle_file, None)

def get_map(latitude, longitude):
	# Picture is 360 by 180
	coordinates = {'x': 0, 'y': 0}
	coordinates['x'] = int(longitude + 180)
	coordinates['y'] = int(180 - (latitude + 90))

	image = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/img/map.png")
	# Paint on position
	draw = ImageDraw.Draw(image)
	box = (coordinates['x'] - 5, coordinates['y'] - 5, coordinates['x'] + 5, coordinates['y'] + 5)
	draw.ellipse(box, fill = "#ff0000")

	return image

def compute_sun_altitude(timestamp):
	position = get_position("tds1.txt", timestamp)
	gatech = ephem.Observer()
	gatech.lon, gatech.lat = str(position.longitude), str(position.latitude)
	current_datetime = datetime.datetime.fromtimestamp(
		int(timestamp)
	).strftime('%Y/%m/%d %H:%M:%S')
	gatech.date = current_datetime
	gatech.pressure = 0
	gatech.elevation = 635000
	sun = ephem.Sun()
	sun.compute(gatech)

	return sun.alt * 57.2957795

# Some definitions...
sunlight = "SUNLIGHT"
twilight = "TWILIGHT"
night = "NIGHT"

def is_in_sunlight(timestamp):
	altitude = compute_sun_altitude(timestamp)
	if altitude < -24.85:
		return night
	elif altitude < -24.32:
		return twilight
	else:
		return sunlight
