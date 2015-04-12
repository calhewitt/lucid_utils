# An API for grabbing LUCID data files from the starserver

import numpy as np
import urllib
import json
from datetime import date, datetime, timedelta

class APIFrame:
	
	def __init__(self, json_str):
		
		self.json_str = json_str
		self.channel = [json_str["channel"]]
		self.config = json_str["config"]
		self.daylight = json_str["daylight"]
		self.latitude = json_str["latitude"]
		self.longitude = json_str["longitude"]
		self.run = json_str["run"]
		self.sun_alt = json_str["sun_alt"]
		self.timestamp = json_str["timestamp"]
		self.url = {json_str["channel"]: json_str["url"]}
		
		self.channels = {}
		
	def grab(self):
		for channel_id in self.url.keys():	
			frame_txt = urllib.urlopen(self.url[channel_id])
				
			if frame_txt.getcode() == 200:
				frame_txt = frame_txt.readlines()
			else:
				raise Exception("That data file could not be found")
			
			frame = np.zeros((256, 256))
			for line in frame_txt:
				vals = line.split("\t")
				x = int(float(vals[0].strip()))
				y = int(float(vals[1].strip()))
				c = int(float(vals[2].strip()))
		
				frame[x][y] = c
				
			self.channels[channel_id] = frame
		return self.channels
		
	
	def get_xyc(self):
		try:
			frame_txt = urllib.urlopen(self.url)
		except:
		
			raise Exception("That data file could not be found")
			
		if frame_txt.getcode() == 200:
			frame_txt = frame_txt.read()
		else:
			raise Exception("That data file could not be found")
	
		return frame_txt
		
	def merge(self, other_frame):
		self.channel.append(other_frame["channel"])
		self.url[other_frame["channel"]] = other_frame["url"]
		

def get_run(timestamp):
	date_obj = datetime.fromtimestamp(timestamp).date()
	diff = date_obj - date(2014, 12, 19)
	diff = diff.days % 8
	new_date = date_obj - timedelta(days=diff)
	#print new_date	
	return new_date.strftime("%Y-%m-%d")

def get_frames_by_run(run_name):
	
	# construct the frame report URL and try to query it
	report_url = "http://starserver.thelangton.org.uk/lucid-data-browser/frame-reports/" + run_name + "-frame-report.txt"
	try:
		frames = urllib.urlopen(report_url).read()
		frames = json.loads(frames)

	except:
		raise Exception("That run could not be found")
		
	new_frames = []
	current_frame = None
	current_timestamp = 0
	
	for frame in frames:
		if frame["timestamp"] == current_timestamp:
			current_frame.merge(frame)
		else:
			if current_frame != None:
				new_frames.append(current_frame)
			current_frame = APIFrame(frame)
			current_timestamp = current_frame.timestamp
	new_frames.append(current_frame)
			
	return new_frames
	
def get_frames_by_timestamp(timestamp):
	# A bit hacky I know,
	# TODO built better support for things like this on the server side
	frames = get_frames_by_run(get_run(timestamp))
	matches = []
	for frame in frames:
		if frame.timestamp == timestamp:
			matches.append(frame)
	if not len(matches) == 0:
		return matches
	else:
		raise Exception("A frame could not be found with that timestamp")
	