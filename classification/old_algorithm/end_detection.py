# An algorithm to work out the number of end points of a 'long' cluster (beta, etc) in order to detect crossed or divergent tracks
# Note: This is currently only accurate for clusters of radius > ~20
# TODO Develop a similar algorithm for shorter blobs
# Author: Cal Hewitt

import numpy as np

def is_single_track(blob):
    return num_end_points(blob) <= 2

def num_end_points(blob):
    cluster, best_fit_line, radius, centroid = blob.pixels, blob.best_fit_line, blob.radius, blob.centroid
    m, c = best_fit_line
    radius = int(np.ceil(radius)) # Make radius into an integer, bigger is better for avoiding errors
    # Define constants and initialise arrays which we will use a lot later
    pixel_ch_x = 1 / np.sqrt( (m**2) + 1) # For efficiency, change in x between sample points
    m_normal = (-1)*(1/m) # Gradient of the normal to the line of best fit
    all_pixel_clusters = []
    num_end_points = 0
    # To begin the process, we are going to step along line of best fit from c - r to c + r, 1 pixel at a time
    # For simplicity we call this 'left to right'
    # First, find the leftmost point
    ch_x = radius / np.sqrt( (m**2) + 1 ) # Change in x between centroid and leftmost point
    start_point = ( centroid[0] - ch_x, centroid[1] - m*ch_x )
    # Now start stepping along the line of best fit, with i between 0 and diameter, 1 pixel at a time...
    for i in range( (radius*2) + 1):
        # First we locate the point on the line of best fit which corresponds to i
        current_point = (start_point[0] + (i*pixel_ch_x), start_point[1] + (m*i*pixel_ch_x))
        # We want to check for pixels which 'correspond' to this point by seeing if the normal at this point intersects them
        # Use Bresenham's Algorithm to rasterise the normal r either side of current_point, and then check for clusters
        # Make up bresenham start and end (more points than are actually needed, but probs computationally easier this way as B's alg is very light)
        p1 = (int(current_point[0] - radius), int(current_point[1] - np.ceil(m_normal*radius)))
        p2 = (int(current_point[0] + radius), int(current_point[1] + np.ceil(m_normal*radius)))
        relevant_pixels = bresenham(p1, p2)
        # Make a list of 'clusters' of these relevant pixels, which are from separate branches
        relevant_pixel_clusters = []
        last_active_pixel = None
        current_cluster = None
        for pixel in relevant_pixels:
            # Check that the pixel has been hit
            if pixel in cluster:
                if not current_cluster:
                    current_cluster = [pixel]
                else:
                    if pixels_adjacent(pixel, last_active_pixel):
                        current_cluster.append(pixel)
                    else:
                        relevant_pixel_clusters.append(current_cluster)
                        current_cluster = [pixel]
                last_active_pixel = pixel
        # If a cluster has been partially formed by the end of the loop, still use it
        if current_cluster:
            relevant_pixel_clusters.append(current_cluster)
        if relevant_pixel_clusters:
            all_pixel_clusters.append(relevant_pixel_clusters)

    # By this point, all_pixel_clusters contains a list of rows, each of these a list of clusters
    # Check for clusters with only one neighbour, as these will be end points
    for i in range(len(all_pixel_clusters)):
        active_row = all_pixel_clusters[i]
        for active_cluster in active_row:
            neighbours = 0
            for check_cluster in all_pixel_clusters[i]:
                if clusters_adjacent(active_cluster, check_cluster) and (active_cluster != check_cluster):
                    neighbours += 1
            if i > 0:
                for check_cluster in all_pixel_clusters[i-1]:
                    if clusters_adjacent(active_cluster, check_cluster):
                        neighbours += 1
            if i < (len(all_pixel_clusters) - 1):
                for check_cluster in all_pixel_clusters[i+1]:
                    if clusters_adjacent(active_cluster, check_cluster):
                        neighbours += 1
            if neighbours == 1:
                num_end_points += 1
    return num_end_points

def pixels_adjacent(pixel1, pixel2, distance = 1):
    return abs(pixel2[0] - pixel1[0]) <= distance and abs(pixel2[1] - pixel1[1]) <= distance

def clusters_adjacent(cluster1, cluster2):
    for p1 in cluster1:
        for p2 in cluster2:
            if pixels_adjacent(p1, p2, 2): # Hack as sometimes Bresenham lines will miss a pixel
                return True
    return False

# An implementation of Bresenham's line algorithm, thanks to roguebasin.com
def bresenham(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    is_steep = abs(dy) > abs(dx)
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    if swapped:
        points.reverse()
    return points
