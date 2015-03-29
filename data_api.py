# An API for grabbing LUCID data files from the starserver

import numpy as np
import urllib
import json

def get_frames_by_run(run_name):
	# construct the frame report URL and try to query it
	report_url = "http://starserver.thelangton.org.uk/lucid-data-browser/frame-reports/" + run_name + "-frame-report.txt"
	try:
		frames = urllib.urlopen(report_url).read()
		frames = json.loads(frames)
	except:
		raise Exception("That run could not be found")
	
	return frames

def get_frame(url):
	try:
		frame_txt = urllib.urlopen(url)
	except:
		raise Exception("That data file could not be found")
		
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
	return frame

def get_xyc(url):
	try:
		frame_txt = urllib.urlopen(url)
	except:
		raise Exception("That data file could not be found")
		
	if frame_txt.getcode() == 200:
		frame_txt = frame_txt.read()
	else:
		raise Exception("That data file could not be found")

	return frame_txt