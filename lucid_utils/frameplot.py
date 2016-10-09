import matplotlib as mpl
import os
if not "DISPLAY" in os.environ: # Make MPL Work if no display is available
	mpl.use('Agg')
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_agg import FigureCanvasAgg


def get_image(frame, colourmode = "BW", normalise=False):
	fig = plt.figure(frameon=False, figsize=(256,256), dpi=1)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

	cmap = cm.hot
	cmap.set_under("#82bcff")
	vm = np.max(frame) if (np.count_nonzero(frame) > 0) else 2
	ax.imshow(frame, vmin = 1, vmax=vm, cmap = cmap, interpolation='none')

	canvas = plt.get_current_fig_manager().canvas

	agg = canvas.switch_backends(FigureCanvasAgg)
	agg.draw()
	s = agg.tostring_rgb()

	l, b, w, h = agg.figure.bbox.bounds
	w, h = int(w), int(h)

	X = np.fromstring(s, np.uint8)
	X.shape = h, w, 3

	plt.close()

	try:
	    im = Image.fromstring("RGB", (w, h), s)
	except Exception:
	    im = Image.frombytes("RGB", (w, h), s)
	return im

def show_frame(frame):
	if not "DISPLAY" in os.environ:
		raise Exception("No display available")
	fig, ax = plt.subplots()
	cmap = cm.hot
	cmap.set_under("#82bcff")
	vm = np.max(frame) if (np.count_nonzero(frame) > 0) else 2
	cax = ax.imshow(frame, vmin = 1, vmax=vm, cmap = cmap, interpolation='none')
	fig.colorbar(cax)
	plt.show()

def fig_frame(frame):
	fig, ax = plt.subplots()
	cmap = cm.hot
	cmap.set_under("#82bcff")
	vm = np.max(frame) if (np.count_nonzero(frame) > 0) else 2
	cax = ax.imshow(frame, vmin = 1, vmax=vm, cmap = cmap, interpolation='none')
	fig.colorbar(cax)
	return fig

def show_blob(blob):
	xs, ys = zip(*blob)
	sizex, sizey = max(xs) - min(xs), max(ys) - min(ys)
	toshow = np.zeros((sizex+3,sizey+3))
	for i in range(len(xs)):
		toshow[1 + xs[i] - min(xs)][1 + ys[i] - min(ys)] = 1
	show_frame(toshow)
