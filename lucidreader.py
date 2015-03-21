# Module to parse raw LUCID data files
# Part of the LUCID frame reader

import os
from binascii import hexlify
import numpy as np 
from datetime import datetime
import Image

def tohex(binary):
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
			self.ignore_length = 16
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
			print "Warning: The data file is missing a header. It could be invalid."
			self.config = "Unknown"
			byte1, byte2 = "", ""
			while not (byte1 == "DC" and byte2 == "DF"):
				byte1 = byte2
				byte2 = tohex(self.f.read(1))
			self.ignore_length = self.f.tell() - 2
			if num_active_detectors == None:
				self.num_active_detectors = input("Enter the number of active detectors: ")
			else:
				self.num_active_detectors = num_active_detectors

		# 2 bytes for each pixel
		self.frame_length = (CHANNEL_LENGTH * self.num_active_detectors) + 7
		self.num_frames = (os.path.getsize(filename) - self.ignore_length) / self.frame_length

	def get_frame(self, index):
		channels = [None, None, None, None, None]

		self.f.seek(self.ignore_length + (self.frame_length * index))
		frame_header = tohex(self.f.read(7))[4:]
		timestamp = int(frame_header[0:8], 16)

		for i in range(self.num_active_detectors):
			channel_id = get_channel_id(tohex(self.f.read(1)))
			pixels = np.zeros((256, 256))

			for x in range(0, 256):
				for y in range(0, 256):
					pixel = bin(int(tohex(self.f.read(2)), 16))[2:].zfill(16)
					# First 2 bits are always 10 - pixel is only 14 bits long
					pixel = float(int(pixel[2:], 2))
					pixel = (pixel / 11810) * 256
					pixels[x][y] = pixel
			channels[channel_id] = pixels
		r_value = LucidFrame()
		r_value.channels = channels
		r_value.timestamp = timestamp
		return r_value