# The start of a particle recognition algorithm...
# Author: Cal Hewitt

import numpy as np
import math
from scipy.optimize import leastsq


# Simple trig...
def distance(point1, point2):
    return math.sqrt(((point2[0] - point1[0])**2) + ((point2[1] - point1[1])**2))

def point_line_distance(point, line):
    # Calculates the shortest distance between a point and a line in the form y = mx + c
    x, y = point
    m, c = line
    return np.fabs(m * x - y + c) / np.sqrt(1 + m**2)

def residuals(line, y, x):
    # Wrapper for point_line_distance; required by regression function
    return point_line_distance((x, y), line)

class Blob:
    def __init__(self, pixels):
        self.pixels = pixels
        # Compute attributes
        self.radius, self.centroid = self.calculate_radius()
        self.squiggliness = self.calculate_squiggliness()
        self.sqi = self.squiggliness

    def calculate_radius(self):
        # Firstly, compute the centroid of the blob
        x_vals, y_vals = [], []
        for pixel in self.pixels:
            x_vals.append(pixel[0])
            y_vals.append(pixel[1])
        centroid = (np.mean(x_vals), np.mean(y_vals))
        # Loop through each pixel and check its distance from the centroid; set the radius to the highest of these
        radius = 0.0
        for pixel in self.pixels:
            dist = distance(centroid, pixel)
            if dist > radius:
                radius = dist
        return radius, centroid

    def calculate_squiggliness(self):
        # Split up into x and y value lists
        x_vals, y_vals = [], []
        for pixel in self.pixels:
            x_vals.append(pixel[0])
            y_vals.append(pixel[1])
        # Check if the blob is a straight line, so x_vals OR y_vals is made up of only one repeated element
        if x_vals.count(x_vals[0]) == len(x_vals) or y_vals.count(y_vals[0]) == len(y_vals):
            return 0
        # Otherwise, use leastsq to estimate a line of best fit
        # As an initial guess, use a horizontal line passing through the first pixel
        first_guess_line = [0, y_vals[0]] # In the form [gradient, intercept]
        # Use scipy's regression function to magic this into a good LoBF
        plsq = leastsq(residuals, first_guess_line, args = (np.array(y_vals), np.array(x_vals)))
        # Find the mean distance from each pixel to the line (the 'squiggliness')
        distances = [point_line_distance(pixel, plsq[0]) for pixel in self.pixels]
        return np.mean(distances)
