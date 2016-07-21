# A complete rewrite of the CERN@school particle recognition and classification algorithm,
# for ease of integration with existing LUCID data and libraries.
# Can be imported and called from anywhere to identify particle types based on their attributes
# Author (code): Cal Hewitt, based on an algorithm from http://github.com/cernatschool/cluster-sorter

import numpy as np
from scipy.optimize import leastsq
import json
import os
from collections import OrderedDict
try:
    import common
except ImportError:
    from . import common

# Load up the types file
types = json.loads(open(os.path.dirname(os.path.realpath(__file__)) + "/types/old_algorithm.json").read())
# A list of bounds of properties of various particle types, adapted from http://github.com/cernatschool/cluster-sorter

# Stores and calculates the attributes of a single cluster ('blob') of pixels
class Blob(common.Blob):

    def classify(self):
        # Set up a dictionary of the blob's own values
        blob_values = {"num_pixels": self.num_pixels,
                        "radius": self.radius,
                        "density": self.density,
                        "squiggliness": self.squiggliness}
        # Loop through each potential particle type, looking for a match
        for particle_name, subtypes in types.items():
            for name, properties in subtypes.items():
                # Initially, presume the particle is a match
                match = True
                # Check through each property, in the form {name: (lower_bound, upper_bound)}
                for property_name, property_value in properties.items():
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

def classify_masked(blob):
    # Method for early LUCID data where half of pixels are masked:
    b = Blob(blob)
    b.num_pixels *= 2
    b.density *= 2
    return b.classify()
