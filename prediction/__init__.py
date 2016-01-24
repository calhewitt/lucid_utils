# A set of functions to predict the radiation level that LUCID would record under various circumstances

import numpy as np
import Image
import sys
from scipy import interpolate
import geopy.distance

# Predicts the (electon, proton) count per frame per second under NORMAL conditions in the given location
def predict_background(position):
    latitude, longtiude = position
