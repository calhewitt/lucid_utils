# A wrapper for easily accessing the LUCID data API and fetching data
try:
	import urllib2 as urllib
except ImportError:
	# For Python 3+
	import urllib.request as urllib

import numpy as np
import json

BASE_PATH = "http://starserver.thelangton.org.uk/lucid-data-browser/api/"

def get_data_files(run = None):
	stream = urllib.urlopen(BASE_PATH + "get/data_files")
	if not stream.getcode() == 200:
		raise Exception("An error occurred whilst processing the request")
	data_files = json.loads(stream.read())
	if run:
		filtered_data_files = []
		for data_file in data_files:
			if data_file['run'] == run:
				filtered_data_files.append(data_file)
		return filtered_data_files
	return data_files

def get_runs():
	# Get a list of available data files and extract runs from this
	stream = urllib.urlopen(BASE_PATH + "get/data_files")
	if not stream.getcode() == 200:
		raise Exception("An error occurred whilst processing the request")
	data_files = json.loads(stream.read())
	runs = []
	for data_file in data_files:
		if not data_file['run'] in runs:
			runs.append(data_file['run'])
	return runs

class Frame:
	pass

def get_frames(file_id, run = None):
	stream = urllib.urlopen(BASE_PATH + "get/frames?data_file=" + str(int(file_id)))
	if not stream.getcode() == 200:
		raise Exception("That data file could not be found")
	# .decode required for use in Python 3+
	frames = json.loads(stream.read().decode('utf-8'))
	updated_frames = []
	for frame in frames:
		frame_obj = Frame()
		frame_obj.__dict__ = frame
		frame = frame_obj
		new_channels = []
		for channel_id in range(5):
			channel = np.zeros((256, 256))
			if str(channel_id) in frame.channels.keys():
				for line in frame.channels[str(channel_id)].split("\n")[:-1]: # Last line is blank
					vals = line.split("\t")
					x = int(float(vals[0].strip()))
					y = int(float(vals[1].strip()))
					c = int(float(vals[2].strip()))
					channel[x][y] = c
				new_channels.append(channel)
			else:
				new_channels.append(None)
		frame.channels = new_channels
		updated_frames.append(frame)
	return updated_frames
