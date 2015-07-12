# A complete rewrite of the CERN@school particle recognition and classification algorithm,
# for ease of integration with existing LUCID data and libraries.
# Can be imported and called from anywhere to identify particle types based on their attributes
# Author (code): Cal Hewitt, based on an algorithm from http://github.com/cernatschool/cluster-sorter

import numpy as np
from scipy.optimize import leastsq
import json
import os


# Load up the types file
types = json.loads(open(os.path.dirname(os.path.realpath(__file__)) + "/types.json").read())
# A list of bounds of properties of various particle types, adapted from http://github.com/cernatschool/cluster-sorter


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

    def classify(self):
        # Set up a dictionary of the blob's own values
        blob_values = {"num_pixels": self.num_pixels,
                        "radius": self.radius,
                        "density": self.density,
                        "squiggliness": self.squiggliness}
        # Loop through each potential particle type, looking for a match
        for particle_name, subtypes in types.iteritems():
            for name, properties in subtypes.iteritems():
                # Initially, presume the particle is a match
                match = True
                # Check through each property, in the form {name: (lower_bound, upper_bound)}
                for property_name, property_value in properties.iteritems():
                    # If the blob's properties lie outside the bounds specified in the types file, the blob is not a match
                    if (blob_values[property_name] < property_value[0]) or (blob_values[property_name] > property_value[1]):
                        match = False
                # If the current particle matches the attributes of the blob, then return its name
                if match:
                    return particle_name
        # By this point, all potential particles have been checked, so the blob must be something else
        return "other"


def classify(blob):
    # A quick wrapper method for ease of use
    b = Blob(blob)
    return b.classify()

def classify_multiple(blobs):
    classifications = []
    for blob in blobs:
        classifications.append(classify(blob))
    return classifications
