from __future__ import print_function
from lucidreader import LucidFile
from frameplot import get_image
from PIL import Image
import numpy as np


def generate_noise_mask(lucidfile, number):
	zeros = np.zeros((256, 256))
	mask = [zeros, zeros, zeros, zeros, zeros]
	
	frames = []
	for i in range(number):
		frames.append(lucidfile.get_frame(i))
	for channel in range(5):
		if lucidfile.active_detectors[channel] == True:
			print(channel)
			for x in range(256):
				for y in range(256):
					for frame in frames:
						if frame.channels[channel][x][y] == 0:
							break
						mask[channel][x][y] = 255
	return mask


def apply_noise_mask(nm, frame):
	for i in range(5):
		if frame.channels[i] != None:
			for x in range(256):
				for y in range(256):
					if nm[i][x][y] == 255:
						frame.channels[i][x][y] = 0
	return frame