import numpy as np
from scipy.spatial.distance import euclidean as dist
from copy import deepcopy
try:
	from Queue import Queue
except ImportError:
	from queue import Queue


class BlobFinder:

	def __init__(self, frame, rad):
		self.aq = Queue()
		self.rad = rad
		self.irad = int(np.ceil(rad))
		self.frame = deepcopy(frame)
		self.blobs = []
		self.blob = None # Holds currently active blob

	def circle(self, location):
		sqxs = range(max(0, location[0] - self.irad), min(256, location[0] + self.irad + 1))
		sqys = range(max(0, location[1] - self.irad), min(256, location[1] + self.irad + 1))
		square = [(x,y) for x in sqxs for y in sqys]
		return [p for p in square if (dist(p,location) <= self.rad)]

	def add(self, xy):
		x,y = xy
		self.blob.append((x,y))
		close_region = self.circle((x,y))
		for x1,y1 in close_region:
			if self.frame[x1][y1] > 0:
				self.frame[x1][y1] = 0
				self.aq.put((x1,y1))

	def find(self):
		for x in range(256):
			for y in range(256):
				if self.frame[x][y] > 0:
					self.frame[x][y] = 0
					self.blob = []
					self.aq.put((x,y))

					while not self.aq.empty():
						pixel = self.aq.get()
						self.add(pixel)

					self.blobs.append(self.blob)

		return self.blobs


def find(frame, rad=2.9):
	return BlobFinder(frame,rad).find()
