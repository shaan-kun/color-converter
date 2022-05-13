import sys
import argparse


def rgb_to_hex(red, green, blue):
	return f"{red:x}{green:x}{blue:x}"


def hex_to_rgb(hex_color):
	"""
	Переводит цвет из 16-ой формы в RGB.

	Принимает цвет в формате RRGGBB или RGB, где R - красный, G - зелёный, B - голубой.
	"""

	if len(hex_color) == 3:
		red = int(hex_color[0], 16)
		green = int(hex_color[1], 16)
		blue = int(hex_color[2], 16)
	else:
		red = int(hex_color[0:2], 16)
		green = int(hex_color[2:4], 16)
		blue = int(hex_color[4:6], 16)

	return (red, green, blue)


def rgb_to_cmyk(red, green, blue):
	red /= 255
	green /= 255
	blue /= 255

	black = 1 - max(red, green, blue)

	cyan = (1 - red - black) / (1 - black)
	magenta = (1 - green - black) / (1 - black)
	yellow = (1 - blue - black) / (1 - black)

	return (cyan, magenta, yellow, black)


def cmyk_to_rgb(cyan, magenta, yellow, black):
	red = 255 * (1 - cyan) * (1 - black)
	green = 255 * (1 - magenta) * (1 - black)
	blue = 255 * (1 - yellow) * (1 - black)

	return (red, green, blue)


def rgb_to_hsl(red, green, blue):
	red /= 255
	green /= 255
	blue /= 255

	max_color = max(red, green, blue)
	min_color = min(red, green, blue)
	delta = max_color - min_color

	h = 0
	if max_color == red:
		h = 60 * ((green - blue) / delta % 6)
	elif max_color == green:
		h = 60 * ((blue - red) / delta + 2)
	elif max_color == blue:
		h = 60 * ((red - green) / delta + 4)

	l = (max_color + min_color) / 2

	s = 0
	if delta != 0:
		s = delta / (1 - abs(2 * l - 1))

	return (h, s, l)


def hsl_to_rgb(h, s, l):
	c = (1 - abs(2 * l - 1)) * s

	x = c * (1 - abs((h / 60) % 2 - 1))

	m = l - c / 2

	if h < 60:
		r, g, b = c, x, 0
	elif h < 120:
		r, g, b = x, c, 0
	elif h < 180:
		r, g, b = 0, c, x
	elif h < 240:
		r, g, b = 0, x, c
	elif h < 300:
		r, g, b = x, 0, c
	elif h < 360:
		r, g, b = c, 0, x

	r = (r + m) * 255
	g = (g + m) * 255
	b = (b + m) * 255

	return (r, g, b)


def rgb_to_hsv(red, green, blue):
	red /= 255
	green /= 255
	blue /= 255

	max_color = max(red, green, blue)
	min_color = min(red, green, blue)
	delta = max_color - min_color

	h = 0
	if max_color == red:
		h = 60 * ((green - blue) / delta % 6)
	elif max_color == green:
		h = 60 * ((blue - red) / delta + 2)
	elif max_color == blue:
		h = 60 * ((red - green) / delta + 4)

	s = 0
	if max_color != 0:
		s = delta / max_color

	v = max_color

	return (h, s, v)


def hsv_to_rgb(h, s, v):
	c = v * s

	x = c * (1 - abs((h / 60) % 2 - 1))

	m = v - c

	if h < 60:
		r, g, b = c, x, 0
	elif h < 120:
		r, g, b = x, c, 0
	elif h < 180:
		r, g, b = 0, c, x
	elif h < 240:
		r, g, b = 0, x, c
	elif h < 300:
		r, g, b = x, 0, c
	elif h < 360:
		r, g, b = c, 0, x

	r = (r + m) * 255
	g = (g + m) * 255
	b = (b + m) * 255

	return (r, g, b)


def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-ci", "--color_in", nargs="+")
	parser.add_argument("-co", "--color_out", nargs="+")

	return parser


if __name__ == "__main__":
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])

	color_in = namespace.color_in[0]
	color_out = namespace.color_out[0]
