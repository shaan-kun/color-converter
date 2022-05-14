import sys
import argparse


class Color:

	def __init__(self, color_model="rgb", *params):
		if color_model == "hex":
			self.__color_1 = params[0]
			self.__color_2 = params[1]
			self.__color_3 = params[2]
		else:
			self.__color_1 = int(params[0])
			self.__color_2 = int(params[1])
			self.__color_3 = int(params[2])

		self.__color_4 = None

		if color_model == "cmyk":
			self.__color_4 = int(params[3])

		self.__color_model = color_model


	def get_color_model(self):
		return self.__color_model


	def get_color_1(self):
		return self.__color_1


	def get_color_2(self):
		return self.__color_2


	def get_color_3(self):
		return self.__color_3


	def get_color_4(self):
		return self.__color_4


	def __str__(self):
		string = f"Цветовая модель: {self.__color_model}\n{self.__color_1:.2f} {self.__color_2:.2f} {self.__color_3:.2f}"
		
		if self.__color_model == "cmyk":
			string += f" {self.__color_4:.2f}"

		return string


	def to_rgb(self):
		if self.__color_model == "rgb":
			return self

		elif self.__color_model == "hex":
			self.__color_1 = int(self.__color_1, 16)
			self.__color_2 = int(self.__color_2, 16)
			self.__color_3 = int(self.__color_3, 16)

		elif self.__color_model == "cmyk":
			self.__color_1 = 255 * (1 - self.__color_1) * (1 - self.__color_4)
			self.__color_2 = 255 * (1 - self.__color_2) * (1 - self.__color_4)
			self.__color_3 = 255 * (1 - self.__color_3) * (1 - self.__color_4)
			self.__color_4 = None

		elif self.__color_model == "hsl":
			h = self.__color_1
			s = self.__color_2
			l = self.__color_3

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

			self.__color_1 = (r + m) * 255
			self.__color_2 = (g + m) * 255
			self.__color_3 = (b + m) * 255

		elif self.__color_model == "hsv":
			h = self.__color_1
			s = self.__color_2
			v = self.__color_3

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

			self.__color_1 = (r + m) * 255
			self.__color_2 = (g + m) * 255
			self.__color_3 = (b + m) * 255

		self.__color_model = "rgb"


	def to_hex(self):
		if self.__color_model == "hex":
			return self

		self.to_rgb()

		self.__color_1 = f"{self.__color_1:x}"
		self.__color_2 = f"{self.__color_2:x}"
		self.__color_3 = f"{self.__color_3:x}"
		self.__color_model = "hex"

		return self


	def to_cmyk(self):
		if self.__color_model == "cmyk":
			return self

		self.to_rgb()

		r = self.__color_1 / 255
		g = self.__color_2 / 255
		b = self.__color_3 / 255

		black = 1 - max(r, g, b)

		cyan = (1 - r - black) / (1 - black)
		magenta = (1 - g - black) / (1 - black)
		yellow = (1 - b - black) / (1 - black)

		self.__color_1 = cyan
		self.__color_2 = magenta
		self.__color_3 = yellow
		self.__color_4 = black
		self.__color_model = "cmyk"

		return self


	def to_hsl(self):
		if self.__color_model == "hsl":
			return self

		self.to_rgb()

		r = self.__color_1 / 255
		g = self.__color_2 / 255
		b = self.__color_3 / 255

		max_color = max(r, g, b)
		min_color = min(r, g, b)
		delta = max_color - min_color

		h = 0
		if max_color == r:
			h = 60 * ((g - b) / delta % 6)
		elif max_color == g:
			h = 60 * ((b - r) / delta + 2)
		elif max_color == b:
			h = 60 * ((r - g) / delta + 4)

		l = (max_color + min_color) / 2

		s = 0
		if delta != 0:
			s = delta / (1 - abs(2 * l - 1))

		self.__color_1 = h
		self.__color_2 = s
		self.__color_3 = l
		self.__color_model = "hsl"

		return self


	def to_hsv(self):
		if self.__color_model == "hsv":
			return self

		self.to_rgb()

		r = self.__color_1 / 255
		g = self.__color_2 / 255
		b = self.__color_3 / 255

		max_color = max(r, g, b)
		min_color = min(r, g, b)
		delta = max_color - min_color

		h = 0
		if max_color == r:
			h = 60 * ((g - b) / delta % 6)
		elif max_color == g:
			h = 60 * ((b - r) / delta + 2)
		elif max_color == b:
			h = 60 * ((r - g) / delta + 4)

		s = 0
		if max_color != 0:
			s = delta / max_color

		v = max_color

		self.__color_1 = h
		self.__color_2 = s
		self.__color_3 = v
		self.__color_model = "hsv"

		return self


	def convert(self, color):
		if color == "rgb":
			self.to_rgb()
		elif color == "hex":
			self.to_hex()
		elif color == "cmyk":
			self.to_cmyk()
		elif color == "hsl":
			self.to_hsl()
		elif color == "hsv":
			self.to_hsv()

		return self


def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-ci", "--color_in", nargs="+")
	parser.add_argument("-co", "--color_out", nargs="+")

	return parser


if __name__ == "__main__":
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])

	color = Color(namespace.color_in[0], *namespace.color_in[1:])
	color.convert(namespace.color_out[0])

	print(color)
