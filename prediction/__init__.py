# Predict the background radiation level at a certain location
# TODO conversion factor

import numpy as np
import Image
import sys
from scipy import interpolate
import geopy.distance
import os

# Predicts the (electon, proton) count per frame per second under NORMAL conditions in the given location
def predict_background((latitude, longitude)):
    predicted_counts = {}
    for t in ["beta", "proton"]:
        counts = []
        data = open(os.path.dirname(os.path.abspath(__file__)) + "/" + t + "-calgorithm-counts.csv").readlines()

        for datum in data:
        	datum = datum[:-1]  # Trim off newline char
        	if datum:
        		fields = datum.split(",")
        		timestamp, latitude, longitude, num_frames, beta = fields
        		latitude, longitude, beta, num_frames = float(latitude), float(longitude), int(beta), float(int(num_frames))
                counts.append((latitude, longitude, beta/num_frames))

        counts_sorted_distance = sorted(counts, key=lambda count:geopy.distance.great_circle((latitude, longitude), (count[0], count[1])))
        predicted_counts[t] = np.mean([c[2] for c in counts_sorted_distance[:3]])

    return(predicted_counts["beta"], predicted_counts["proton"])
