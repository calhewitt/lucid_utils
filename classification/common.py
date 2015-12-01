# A set of helpful classes and functions which are common to most classification algorithms
# This includes a 'Blob' class which will automatically determine the properties of a cluster (yay!!)

import numpy as np
from scipy.optimize import leastsq
import json
import os
from collections import OrderedDict
import Image


def distance(point1, point2):
    # Simple 2D distance function using Pythagoras:
    # Calculates the distance between point1 (x, y) and point2 (x, y)
    return np.sqrt(((point2[0] - point1[0])**2) + ((point2[1] - point1[1])**2))

def point_line_distance(point, line):
    # Calculates the shortest distance between a point (x, y) and a line (m, c) where y = mx + c
    x, y = point
    m, c = line
    return np.fabs(m * x - y + c) / np.sqrt(1 + m**2)

def residuals(line, y, x):
    # Wrapper for point_line_distance in the format required by scipy's regression function
    return point_line_distance((x, y), line)


# Stores and calculates the attributes of a single cluster ('blob') of pixels
class Blob:

    def __init__(self, pixels):
        self.pixels = pixels
        self.num_pixels = len(pixels)
        if not self.num_pixels:
            raise Exception("Cannot work on a blank cluster!")
        # Calculate attributes
        self.radius, self.centroid = self.calculate_radius()
        self.squiggliness, self.best_fit_line = self.calculate_squiggliness()
        self.density = self.calculate_density()

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
            # Return a 0 squiggliness, as the blob is only one pixel, and a horizontal line as a best fit
            return 0, (0, 0)
        # Otherwise, use leastsq to estimate a line of best fit
        # As an initial guess, use a horizontal line passing through the first pixel
        first_guess_line = [0, y_vals[0]] # In the form [gradient, intercept]
        # Use scipy's regression function to magic this into a good LoBF
        best_fit_line = leastsq(residuals, first_guess_line, args = (np.array(y_vals), np.array(x_vals)))[0]
        # Find the mean distance from each pixel to the line (the 'squiggliness')
        distances = [point_line_distance(pixel, best_fit_line) for pixel in self.pixels]
        # Return both a squiggliness value and the parameters of the linear LoBF
        return np.mean(distances), best_fit_line

    def calculate_density(self):
        # Calculate the fill by hit pixels of a circle of the blob's radius around the centroid]
        # This can be >1 as the blob's radius passes through the centre of outer pixels rather than around them
        # Firstly, compute the area of the enclosing circle
        circle_area = np.pi*((self.radius)**2)
        if circle_area == 0:
            # If the blob is only one pixel in size, and so has a radius of 0, it is fully dense
            return 1
        else:
            # Divide the number of pixels in the blob by this
            return self.num_pixels / circle_area

    def plot(self):
        # Plot and show an image of a blob
        blank_frame = np.zeros((256,256))
        for pixel in self.pixels:
            blank_frame[pixel[0]][pixel[1]] = 256
        B = np.argwhere(blank_frame)
        (ystart, xstart), (ystop, xstop) = B.min(0), B.max(0) + 1
        blank_frame = blank_frame[ystart:ystop, xstart:xstop]
        Image.fromarray(blank_frame).resize((blank_frame.shape[1]*50, blank_frame.shape[0]*50)).show()
