import Image
import numpy as np

# Functions to plot LUCID frames

def colour_map(bw):
	if bw == 0:
		return (0, 0, 40)
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
	return (r, g, b)

def get_image(pixels, colourmode = "BW"):
	pilmode = "L"
	if colourmode == "RGB":
		pilmode = "RGB"
	im = Image.new(pilmode, (256, 256), "black")
	im_pixels = im.load()

	for x in range(0, 256):
		for y in range(0, 256):
			if colourmode == "RGB":
				im_pixels[x, y] = colour_map(int(pixels[x][y]))
			if colourmode == "BW":
				im_pixels[x, y] = int(pixels[x][y])
	return im