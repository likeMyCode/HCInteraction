#!/usr/bin/env python
from __future__ import division           
import matplotlib
matplotlib.use('Agg')         
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from matplotlib import colors
import math as math

def plot_color_gradients(gradients, names):
	rc('legend', fontsize=10)

	column_width_pt = 400        
	pt_per_inch = 72
	
	size = column_width_pt / pt_per_inch

	fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
	fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


	for ax, gradient, name in zip(axes, gradients, names):
		img = np.zeros((2, 1024, 3))
	
		for i, v in enumerate(np.linspace(0, 1, 1024)):
			img[:, i] = gradient(v)
	

		im = ax.imshow(img, aspect='auto')
		im.set_extent([0, 1, 0, 1])
		ax.yaxis.set_visible(False)

		pos = list(ax.get_position().bounds)
		x_text = pos[0] - 0.25
		y_text = pos[1] + pos[3]/2.
		fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

		fig.savefig('my-gradients.pdf')



def Interpolate2Colors(A, B, pos, max_pos):
	A_R = A >> 16
	A_G = (A >> 8) & 0xff
	A_B = A & 0xff

	B_R = B >> 16
	B_G = (B >> 8) & 0xff
	B_B = B & 0xff

	C_R = (((B_R - A_R) * pos) / max_pos + A_R) / 255
	C_G = (((B_G - A_G) * pos) / max_pos + A_G) / 255
	C_B = (((B_B - A_B) * pos) / max_pos + A_B) / 255

	return (C_R, C_G, C_B)



def InterpolateNColors(c_list, value, max_value):
	for i in range(1, len(c_list)):
		if (value < i * max_value / (len(c_list)-1)):
			color = Interpolate2Colors(c_list[i-1], c_list[i], value - (((i-1)*max_value) / (len(c_list)-1)), max_value / (len(c_list)-1))			
			return color



def hsv2rgb(h, s, v):
	h = float(h)
	s = float(s)
	v = float(v)
	h60 = h / 60.0
	h60f = math.floor(h60)
	hi = int(h60f) % 6
	f = h60 - h60f
	p = v * (1 - s)
	q = v * (1 - f * s)
	t = v * (1 - (1 - f) * s)
	r, g, b = 0, 0, 0
	if hi == 0: r, g, b = v, t, p
	elif hi == 1: r, g, b = q, v, p
	elif hi == 2: r, g, b = p, v, t
	elif hi == 3: r, g, b = p, q, v
	elif hi == 4: r, g, b = t, p, v
	elif hi == 5: r, g, b = v, p, q
	r, g, b = int(r * 255), int(g * 255), int(b * 255)
	return int('0x%02x%02x%02x' % (r, g, b), 16)



def gradient_rgb_bw(v):
	return (v, v, v)



def gradient_rgb_gbr(v):
	return InterpolateNColors([0x00FF00, 0x0000FF, 0xFF0000], v, 1)



def gradient_rgb_gbr_full(v):
	return InterpolateNColors([0x00FF00, 0x00FFFF, 0x0000FF, 0xFF00FF, 
		0xFF0000], v, 1)



def gradient_rgb_wb_custom(v):
	return InterpolateNColors([0xFFFFFF, 0xFF00FF, 0x0000FF, 0x00FFFF, 
		0x00FF00, 0xFFFF00, 0xFF0000, 0x000000], v, 1)



def gradient_hsv_bw(v):
	return InterpolateNColors([hsv2rgb(0,1,0), hsv2rgb(0,0,1)], v, 1)



def gradient_hsv_gbr(v):
	return InterpolateNColors([hsv2rgb(120,1,1), hsv2rgb(180,1,1), 
		hsv2rgb(240,1,1), hsv2rgb(300,1,1), hsv2rgb(0,1,1)], v, 1)



def gradient_hsv_unknown(v):
	return InterpolateNColors([hsv2rgb(120,0.502,1), hsv2rgb(72, 0.502, 1), 
		hsv2rgb(0, 0.502, 1)], v, 1)



def gradient_hsv_custom(v):
	return InterpolateNColors([hsv2rgb(360,1,0.94), hsv2rgb(30,1,1), hsv2rgb(60,1,1), 
		hsv2rgb(152,1,0.47), hsv2rgb(240,0.75,0.99), hsv2rgb(291,1,0.75)], v, 1)	
	


if __name__ == '__main__':
	def toname(g):
		return g.__name__.replace('gradient_', '').replace('_', '-').upper()

	gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
		gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

	plot_color_gradients(gradients, [toname(g) for g in gradients])
