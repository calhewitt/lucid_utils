# A set of helpful classes and functions which are common to most classification algorithms
# This includes a 'Blob' class which will automatically determine the properties of a cluster (yay!!)

import numpy as np
from scipy.optimize import leastsq
import json
import os
from collections import OrderedDict
from PIL import Image
import least_squares_circle

def distance(point1, point2):
    # Simple 2D distance function using Pythagoras:
    # Calculates the distance between point1 (x, y) and point2 (x, y)
    return np.sqrt(((point2[0] - point1[0])**2) + ((point2[1] - point1[1])**2))

def point_line_distance(point, centroid, theta):
    x1, y1 = centroid
    x2, y2 = (centroid[0] + np.cos(theta), centroid[1] + np.sin(theta))
    x0, y0 = point
    # cheers wikipedia
    return np.fabs( (y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1 ) / np.sqrt( (y2-y1)**2 + (x2-x1)**2 )

# Stores and calculates the attributes of a single cluster ('blob') of pixels
class Blob:

    def __init__(self, pixels):
        self.pixels = pixels
        self.num_pixels = len(pixels)
        if not self.num_pixels:
            raise Exception("Cannot work on a blank cluster!")
        # Calculate attributes
        self.centroid = self.find_centroid()
        self.radius = self.calculate_radius()
        self.density = self.calculate_density()
        self.squiggliness, self.best_fit_theta = self.calculate_squiggliness()
        self.best_fit_circle = self.find_best_fit_circle() # x, y, radius, residuals
        self.linearity = self.best_fit_circle[2]
        self.circle_residual = self.best_fit_circle[3]
        self.width = self.num_pixels / (2 * self.radius) if not self.num_pixels == 1 else 0

    def find_centroid(self):
        # Firstly, compute the centroid of the blob
        x_vals, y_vals = [], []
        for pixel in self.pixels:
            x_vals.append(pixel[0])
            y_vals.append(pixel[1])
        centroid = (np.mean(x_vals), np.mean(y_vals))
        return centroid

    def calculate_radius(self):
        # Loop through each pixel and check its distance from the centroid; set the radius to the highest of these
        radius = 0.0
        for pixel in self.pixels:
            dist = distance(self.centroid, pixel)
            if dist > radius:
                radius = dist
        return radius

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

    def calculate_squiggliness(self):
        # return angle theta anticlockwise from x axis
        # Split up into x and y value lists
        x_vals, y_vals = [], []
        for pixel in self.pixels:
            x_vals.append(pixel[0])
            y_vals.append(pixel[1])
        # Otherwise, use leastsq to estimate a line of best fit
        # x axis as inital guess
        first_guess_theta = 0.1
        # Use scipy's regression function to magic this into a good LoBF
        best_fit_theta = leastsq(self.residuals, first_guess_theta, args = (np.array(y_vals), np.array(x_vals)))[0] % (np.pi)
        #print np.degrees(best_fit_theta)
        squiggliness = np.sum([point_line_distance(p, self.centroid, best_fit_theta)**2 for p in self.pixels])
        return squiggliness, np.degrees(best_fit_theta)[0]

    def residuals(self, theta, y, x):
        return point_line_distance((x,y), self.centroid, theta)

    def find_best_fit_circle(self):
        if self.num_pixels == 1:
            return 0,0,0,0
        # Circle regression will break if only one pixel is given
        if self.num_pixels == 0:
            return 0 # We love special cases
        x_vals, y_vals = [], []
        for pixel in self.pixels:
            x_vals.append(pixel[0])
            y_vals.append(pixel[1])
        return tuple(least_squares_circle.leastsq_circle(x_vals, y_vals))

    def plot(self):
        # Plot and show an image of a blob
        blank_frame = np.zeros((256,256))
        for pixel in self.pixels:
            blank_frame[pixel[1]][pixel[0]] = 256
        B = np.argwhere(blank_frame)
        (ystart, xstart), (ystop, xstop) = B.min(0), B.max(0) + 1
        blank_frame = blank_frame[ystart:ystop, xstart:xstop]
        Image.fromarray(blank_frame).resize((blank_frame.shape[1]*50, blank_frame.shape[0]*50)).show()
