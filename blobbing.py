# A simple algorithm for non-continuous blobbing
# As LUCID data has a habit of being bitty, the search radius is best set to about 9

def sqrt(x):
	return x**0.5

def dist(a, b):
	return sqrt( ((a[0] - b[0])**2) + ((a[1] - b[1])**2) )

def find(frame, radius = 3):
	blobs = []
	hit_pixels = []
	for x in range(256):
		for y in range(256):
			if frame[x][y] > 0:
				hit_pixels.append((x,y))

	for hit_pixel in hit_pixels:
		for blob in blobs:
			for p in blob:
				if dist(p, hit_pixel) <= radius:
					blob.append(hit_pixel)
					break
		else:
			blobs.append([hit_pixel])

	# Some blobs may be next to each other, so merge them
	final_blobs = []
	for subset in [set(b) for b in blobs]:
	    for candidate in final_blobs:
	        if not candidate.isdisjoint(subset):
	            candidate.update(subset)
	            break
	    else:
	        final_blobs.append(subset)
	return [list(b) for b in final_blobs]
