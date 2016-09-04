# Module to parse raw LUCID data files
from __future__ import print_function
import os
from binascii import hexlify
import numpy as np 
from datetime import datetime
from PIL import Image


def tohex(binary):
	if not binary:
		return "0"
	return hexlify(binary).upper()

def get_channel_id(marker):
	if marker == "C1":
		return 0
	elif marker == "C2":
		return 1
	elif marker == "C4":
		return 2
	elif marker == "C8":
		return 3
	else:
		return 4
		
CHANNEL_LENGTH = (256*256*2) + 1

class LucidFrame:
	pass

class LucidFile:
	def __init__(self, filename, num_active_detectors = None):

		self.f = open(filename, 'r')

		if tohex(self.f.read(2)) == "DCCC":
			# A HEADER! Well there's a surprise...
			header = tohex(self.f.read(14))

			active_detectors = format(int(header[0:2], 16), 'b').zfill(8)[3:]
			self.active_detectors = [False, False, False, False, False]
			self.num_active_detectors = 0
			for i in range(5):
				if active_detectors[i] == '1':
					self.num_active_detectors += 1
					self.active_detectors[4 - i] = True
			self.config = header[20:].decode("hex")[::-1]

		else:
			# Workaround for files missing a header
			print("Warning: The data file is missing a header. It could be invalid.")
			print("Using usual settings...")
			self.config = "Unknown"
			self.num_active_detectors = 3
			self.active_detectors = [True, True, False, True, False]

		# As frames can now be of various lengths, look through the file for markers...
		self.frame_markers = []
		self.f.seek(0)
		pointer = 1
		b1, b2 = self.f.read(1), self.f.read(1)
		while True:
			b1 = b2
			b2 = self.f.read(1)
			if b2 == "":
				break
			#print tohex(b1) + tohex(b2)
			if tohex(b1) + tohex(b2) == "DCDF":
				# Found one...
				#print "found!!"
				self.frame_markers.append(pointer)
			pointer += 1
		print("yay")
		self.num_frames	= len(self.frame_markers) - 1


	def get_frame(self, index):
		channels = []
		for i in range(5):
			if self.active_detectors[i]:
				channels.append(np.zeros((256, 256)))
			else:
				channels.append(None)

		self.f.seek(self.frame_markers[index])
		frame_header = tohex(self.f.read(7))[4:]
		timestamp = int(frame_header[0:8], 16)

		for i in range(self.num_active_detectors):
			channel_id = get_channel_id(tohex(self.f.read(1)))
			pixels = np.zeros((256, 256))

			x = 0
			y = 0

			while y < 256:

				pixel = bin(int(tohex(self.f.read(2)), 16))[2:].zfill(16)
				# First 2 bits are always 10 - pixel is only 14 bits long
				if pixel[0:2] == "10":	
					pixel = float(int(pixel[2:], 2))
					pixels[x][y] = pixel
					x += 1
				elif pixel[0:2] == "00":
					# RLE compression is enabled, panic...
					pixel = int(pixel, 2)
					x += pixel
					# Phew...
				elif pixel[0:2] == "11":
					# Oh no, a premature channelly thingy
					self.f.seek(self.f.tell() - 2)
					break

				# If the x pointer goes over the end of the line, reset it to 0 and increment y
				if x > 255:
					overflow = x%256 # 100 days after Monday
					times = int(x)/256 # Integer division - don't want a horrible decimal
					y += times
					x = overflow

			channels[channel_id] = pixels

		r_value = LucidFrame()
		r_value.channels = channels
		r_value.timestamp = timestamp
		return r_value
