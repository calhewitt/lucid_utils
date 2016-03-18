# A simple algorithm for non-continuous blobbing
# As LUCID data has a habit of being bitty, the search radius is best set to about 9

import numpy as np
import math
from copy import deepcopy
import sys

# Set the maximum recursion level to be eqaul to the maximum number of hit pixels
# in a cluster, so blobbing on a whited-out frame does not cernatschool
sys.setrecursionlimit(256**2)

class BlobFinder:

	def square(self, x, y, size):
		half_size = (size - 1) / 2
		x, y  = x - half_size, y - half_size
		# Return a sizexsize square of pixels around the coordinates
		pixels = []
		for i in range(size):
			for j in range(size):
				if (x + i < 0 or y + j < 0) or (x + i > 255 or y + j > 255):
					continue # Can't have out of bounds coordinates
				else:
					pixels.append((x + i, y + j))
		return pixels

	def add(self, x, y):
		self.frame[x][y] = 0 # Pixel has already been processed so can be set to 0
		close_region = self.square(x, y, self.SQUARE_SIZE)
		for pixel in close_region:
			if self.frame[pixel[0]][pixel[1]] > 0:
				self.blob.append((pixel[0], pixel[1]))
				self.add(pixel[0], pixel[1])

	def relativise_blob(self, active_blob):
		new_blob = []
		min_x, min_y = 256, 256
		for pixel in active_blob:
			if pixel[0] < min_x:
				min_x = pixel[0]
			if pixel[1] < min_y:
				min_y = pixel[1]
		for pixel in active_blob:
			new_blob.append(((pixel[0] - min_x) + 1, (pixel[1] - min_y) + 1))
		return new_blob

	def find_blobs(self):
		blobs = []
		self.blob = None # Holds currently active blob

		for x in range(256):
			for y in range(256):
				active_pixel = self.frame[x][y]
				if active_pixel > 0:
					# Create new blob
					self.blob = [(x, y)]

					self.add(x, y)

					blobs.append(self.blob)
					self.frame[x][y] = 0

		return blobs

	def relativise_blobs(self, blobs):
		relative_blobs = []

		for blob in blobs:
			relative_blobs.append(self.relativise_blob(blob))

		return relative_blobs

	def __init__(self, frame, search_radius):

		self.SQUARE_SIZE = search_radius
		self.frame = deepcopy(frame) # Frame object passed in is mutable; without copy original frame is made blank


def find(channel, rad = 3):
	bf = BlobFinder(channel, rad)
	return bf.find_blobs()
