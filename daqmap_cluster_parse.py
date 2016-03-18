# Read in the 'shapes' of clusters as xyc python objects (the format used by the DAqMAP!)
# RETURNS [(x,y)]

def parse(cluster_text):
    cluster = []
    pixels = eval(cluster_text)
    for pixel in pixels:
        cluster.append((pixel["x"], pixel["y"]))
    return cluster

def parse_file(filename):
    return parse(open(filename).read())
