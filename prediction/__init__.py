# Predict the background radiation level at a certain location
# Betabetabetabetabetabetabetabetabetabetabetabetabetabeta, so don't rely on this just yet :)

import numpy as np
from PIL import Image
import sys
from scipy import interpolate
import geopy.distance
import os

# Predicts the (electon, proton) count per frame per second under NORMAL conditions in the given location
def predict_background(lookup_lat_and_lng):
    (lookup_lat, lookup_lng) = lookup_lat_and_lng
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

        counts_sorted_distance = sorted(counts, key=lambda count:geopy.distance.great_circle((lookup_lat, lookup_lng), (count[0], count[1])).m)
        count = np.mean([c[2] for c in counts_sorted_distance[:3]])
        # Convert this number into something more 'scientific'
        count /= 2.0 # Single detector
        count /= 0.03 # Per second
        predicted_counts[t] = count

    return(predicted_counts["beta"], predicted_counts["proton"])
