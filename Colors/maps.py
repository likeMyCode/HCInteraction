import csv          
import matplotlib.pyplot as plt
import numpy as np
import math as math


def str_to_float(string):
	try:
		string = float(string)
	except ValueError:
		pass
	return string


def prepare_array(arr):
	new_arr = []
	for row in arr:
		temp = []
		for cell in row[0:-1]:
			temp.append(str_to_float(cell))
		new_arr.append(temp)
	return new_arr



def read_file(filename):
	arr = []
	with open(filename, newline='') as csvfile:
		handler = csv.reader(csvfile, delimiter=' ')
		for row in handler:
			arr.append(row)
	return arr



def lowest_point(arr):
	lowest_point = 9999999
	for row in arr[1:]:
		for cell in row:
			if (cell < lowest_point): lowest_point = cell
	return lowest_point	



def highest_point(arr):
	highest_point = 0
	for row in arr[1:]:
		for cell in row:
			if (cell > highest_point): highest_point = cell
	return highest_point


def Interpolate2Colors(A, B, pos, max_pos):
	A_R = A >> 16
	A_G = (A >> 8) & 0xff
	A_B = A & 0xff

	B_R = B >> 16
	B_G = (B >> 8) & 0xff
	B_B = B & 0xff

	C_R = (((B_R - A_R) * pos) / max_pos + A_R) 
	C_G = (((B_G - A_G) * pos) / max_pos + A_G) 
	C_B = (((B_B - A_B) * pos) / max_pos + A_B)

	return (C_R, C_G, C_B)



def InterpolateNColors(c_list, value, max_value):
	for i in range(1, len(c_list)):
		if (value <= i * max_value / (len(c_list)-1)):
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



def count_angle (s, v):
	cosL = (s[0] * v[0] + s[1] * v[1]) / ( math.sqrt(math.pow(s[0], 2) + math.pow(s[1], 2)) * math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2)) ) 
	radians = math.acos(cosL)	
	degree = radians * ((180) / math.pi) 
	return degree


def find_vector(A, B):
	return 2


def saturation(angle):
	if (angle <= 90): return 1
	elif (angle > 93): return 0.2
	elif (angle > 92.5): return 0.4
	elif (angle > 92): return 0.5
	elif (angle > 91): return 0.6
	elif (angle > 90.5): return 0.7
	elif (angle > 90): return 0.75


def value(angle):
	if (angle < 89.5): return 0.6
	elif (angle < 90 ): return 0.9
	elif (angle >= 90): return 1



def gradient(name, angle):
	if (name == 1):  return [hsv2rgb(120,saturation(angle),value(angle)), hsv2rgb(60,saturation(angle),value(angle)), hsv2rgb(0,saturation(angle),value(angle))]
	elif (name == 2): return [hsv2rgb(291,saturation(angle),value(angle)), hsv2rgb(240,saturation(angle),value(angle)), 
		hsv2rgb(152,saturation(angle),value(angle)), hsv2rgb(60,saturation(angle),value(angle)), 
		hsv2rgb(30,saturation(angle),value(angle)), hsv2rgb(360,saturation(angle),value(angle))]
	elif (name == 3): return [hsv2rgb(240,saturation(angle),value(angle)), hsv2rgb(180,saturation(angle),value(angle)), hsv2rgb(120,saturation(angle),value(angle)),
				hsv2rgb(60,saturation(angle),value(angle)), hsv2rgb(0,saturation(angle),value(angle))]
	elif (name == 4): return [hsv2rgb(55,saturation(angle),value(angle)), hsv2rgb(25,saturation(angle),value(angle)), hsv2rgb(0,saturation(angle),value(angle))]
	elif (name == 5): return [hsv2rgb(240,saturation(angle),value(angle)),
				hsv2rgb(60,saturation(angle),value(angle)), hsv2rgb(0,saturation(angle),value(angle))]
	elif (name == 6): return [hsv2rgb(240,saturation(angle),value(angle)), hsv2rgb(120,saturation(angle),value(angle)), hsv2rgb(60,saturation(angle),value(angle)),
				hsv2rgb(0,saturation(angle),value(angle)), hsv2rgb(0,saturation(angle),value(angle))]



def draw_image(arr, lowest_point, highest_point):
	width = int(arr[0][0])	
	height = int(arr[0][1])
	img = np.zeros((width,height,3), dtype=np.uint8)	
	max_pos = float(highest_point - lowest_point)
	sun = [1, -1]

	for i in range(3, width - 2):
		for j in range(3, height - 2):	
			pos = float(arr[i][j] - lowest_point)
			vector = [arr[i-1][j], arr[i][j]]
			angle = count_angle (sun, vector)
			#if (j%2 == 0): img[i][j] = InterpolateNColors(gradient(1,angle), pos, max_pos)
			#else: img[i][j] = InterpolateNColors(gradient(2,angle), pos, max_pos)
			img[i][j] = InterpolateNColors(gradient(6,angle), pos, max_pos)

	imgplot = plt.imshow(img)
	plt.savefig('mapa.pdf')



if __name__ == '__main__':
	arr = prepare_array(read_file('big.dem'))
	draw_image(arr, lowest_point(arr), highest_point(arr))
