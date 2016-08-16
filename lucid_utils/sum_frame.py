# Sum the pixel values in an entire frame

import lucidreader

def sum_frame(frame):
	total = 0
	for channel in frame.channels:
		if not channel == None:
			total += sum_channel(channel)
	return total

def sum_channel(channel):
	total = 0
	for x in range(256):
		for y in range(256):
			total += channel[x][y]
	return total