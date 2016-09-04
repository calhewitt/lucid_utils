from __future__ import print_function
from lucid_utils import data_api
from lucid_utils import blobbing
from lucid_utils.classification.lucid_algorithm import classify
import numpy as np


def xycparse(lines):
	frame = np.zeros((256, 256))
	for line in lines:
		vals = line.split("\t")
		x = int(float(vals[0].strip()))
		y = int(float(vals[1].strip()))
		c = int(float(vals[2].strip()))

		frame[x][y] = c

	return frame

runs = [
    "2016-05-30",
    "2016-06-07",
    "2016-06-15",
    "2016-06-23",
    "2016-07-01",
    "2016-07-09",
    "2016-07-17",
    "2016-07-25",
    "2016-08-10",
    "2016-08-18"
]
count = 1571
files= []
for run in runs:
	print("RUN STARTING", run)
	files += data_api.get_data_files(run)

files= files[1571:]
for df in files:
	print("ANALYSING FILE", count)

	count += 1

	electron, proton = 0,0
	frames = data_api.get_frames(df['id'])[:10]
	num_frames = len(frames)
	if num_frames < 10:
		continue
	lat,lng = frames[5].latitude, frames[5].longitude

	print(df['id'])

	for frame in frames:
		ch = frame.channels[0]
		blobs = blobbing.find(ch)
		for blob in blobs:
			c = classify(blob)
			if c == "beta":
				electron += 1
			if c == "proton":
				proton += 1
	of = open("counts.txt", "a")
	of.write(str(lat) + "," + str(lng) + "," + str(num_frames) + "," + str(electron) + "," + str(proton) + "\n")
	of.close()
