import numpy as np
import math
try:
	import Image
except ImportError:
	from PIL import Image as Image
import sys
from scipy import interpolate
import geopy.distance
try:
	from pylab import figure, cm
except ImportError:
	from matplotlib.pylab import figure, cm
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm

def geoplot(latitudes, longitudes, counts):
	def xyz(lat,lng):
		phi, theta = np.radians(latitude), np.radians(longitude)
		rho = 1
		x = math.cos(phi) * math.cos(theta) * rho
		y = math.cos(phi) * math.sin(theta) * rho
		z = math.sin(phi) * rho
		return x,y,z

	xs, ys, zs = [], [], []
	counts = []

	for i in range(len(latitudes)):
			latitude, longitude, count = latitudes[i], longitudes[i], counts[i]
			x,y,z = xyz(latitude, longitude)
			xs.append(x)
			ys.append(y)
			zs.append(z)
			counts.append(count)

	def geodist(p1, p2):
		ed = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)
		return 2*np.arcsin(ed/2)

	interpolation_model = interpolate.Rbf(xs, ys, zs, counts, function='thin_plate')

	themap = np.zeros((180,360))

	for latitude in range(-89, 91):
		for longitude in range(-180, 180):
			x,y,z = xyz(latitude, longitude)
			themap[90-latitude][longitude-180] = interpolation_model(x,y,z)

	themap = themap[10:170]
	plt.imshow(themap)
	plt.show()



