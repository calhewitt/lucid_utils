from PIL import Image
import numpy as np

# Functions to plot LUCID frames

def colour_map(bw):
	if bw == 0:
		return (112, 167, 223)
	r, g, b = 0, 0, 0
	if bw < 85:
		r = bw * 3
	elif bw < 170:
		r = 255
		g = (bw - 85) * 3
	else:
		r = 255
		g = 255
		b = (bw - 170) * 3
	return (int(r), int(g), int(b))

def get_image(pixels, colourmode = "BW", normalise=False):
	if normalise:
		pixels *= (11810.0 / max(pixels.flatten()))
	pilmode = "L"
	if colourmode == "RGB":
		pilmode = "RGB"
	im = Image.new(pilmode, (256, 256), "black")
	im_pixels = im.load()

	for x in range(0, 256):
		for y in range(0, 256):
			if colourmode == "RGB":
				im_pixels[x, y] = colour_map((int(pixels[x][y]) / 11810.0) * 256)
			if colourmode == "BW":
				im_pixels[x, y] = int((pixels[x][y] / 11810) * 256)
	return im
