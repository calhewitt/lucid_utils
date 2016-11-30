# The definitive LUCID mapmaker!
from __future__ import print_function
import numpy as np
from numpy import sin,cos,tan # For convenience
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm
import scipy.spatial
from matplotlib.colors import LogNorm
import sys
from mpl_toolkits.basemap import Basemap

def distfunc(dist):
    return np.exp(((dist**2)*-100))

def sqdist(p1,p2):
    return ( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2 )

def cartesian(lat, lng):
    r = 1 # It doesn't actually matter for our purposes

    # Convert to rads
    lat = np.radians(lat)
    lng = np.radians(lng)

    x = r * cos(lat) * cos(lng)
    y = r * cos(lat) * sin(lng)
    z = r *sin(lat)

    return (x,y,z)

def lookup(lat,lng):
    print(lat)
    x,y,z = cartesian(lat,lng)
    dists, indices = tree.query((x,y,z), 100)
    val = np.average([datapoints[index][4] for index in indices], weights=[distfunc(dist) for dist in dists])
    return val
data = open("counts.txt").readlines()
datapoints = []

for datum in data:
    # latitude, longitude, num_frames, electon, proton
    if datum:
        lat, lng, num_frames, electron, proton = datum.split(",")
        datapoints.append((float(lat), float(lng), (float(electron) / float(num_frames)), (float(proton) / float(num_frames)) ))

# Convert all into cartesian coordinates
datapoints = [cartesian(lat, lng) + (electron, proton) for lat, lng, electron, proton in datapoints]

tree = scipy.spatial.KDTree([(x,y,z) for x,y,z,e,p in datapoints])

grid = [[lookup(lat,lng) for lng in range(-180,180)] for lat in range(-90,90)]

plt.figure(figsize=(10,7))

m = Basemap(projection='cyl')
m.imshow(grid,norm=SymLogNorm(linthresh=1.5))
m.drawcoastlines()

parallels = np.arange(-60,90,30)
# labels = [left,right,top,bottom]
m.drawparallels(parallels,labels=[True,False,True,False])
meridians = np.arange(-150,180,30)
m.drawmeridians(meridians,labels=[True,False,False,True])

cbar = plt.colorbar(orientation='horizontal', ticks=[0,1,2,4,8,16,32,64,128,256])
cbar.set_label("Proton Hits per Detector per Frame")

plt.show()
