# A function to read in an ASCII XYC file and return a numpy (pronounced as written) array of pixels

import numpy as np

def read(filename):
	frame = np.zeros((256, 256))
	f = open(filename)
	for line in f.readlines():
		vals = line.split("\t")
		x = int(float(vals[0].strip()))
		y = int(float(vals[1].strip()))
		c = int(float(vals[2].strip()))

		frame[x][y] = c

	return frame