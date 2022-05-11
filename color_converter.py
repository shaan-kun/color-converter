import math


class Color:
	"""Класс цвета

	Хранит цвет в следующих форматах:

	hex / шестнадцатеричный
	rgb / цвета из отрезка [0; 1]
	cmyk
	hsi
	yiq
	"""
	def __init__(self, first=0, second=0, third=0, color_model="rgb"):
		self.__first = first
		self.__second = second
		self.__third = third

		self.__color_model = color_model

	def get_first(self):
		return self.__first

	def get_second(self):
		return self.__second

	def get_third(self):
		return self.__third

	def to_cmyk(self):
		cyan = 1 - self.red
		magenta = 1 - self.green
		yellow = 1 - self.blue

		return Color(cyan, magenta, yellow, "cmyk")

	def to_hsi(self):
		theta = math.acos(1 / 2 * ((self.red - self.green)
				+ (self.red - self.blue))
				/ math.sqrt((self.red - self.green) ** 2
				+ (self.red - self.blue) * (self.green - self.blue)))

		if self.blue <= self.green:
			h = theta
		else:
			h = 360 - theta

		s = 1 - 3 / (self.red + self.green + self.blue) * min(self.red,
			self.green, self.blue)

		i = 1 / 3 * (self.red + self.green + self.blue)

		return Color(h, s, i, "hsi")

	def to_yiq(self):
		y = 0.299 * self.red + 0.587 * self.green + 0.114 * self.blue
		i = 0.596 * self.red - 0.274 * self.green - 0.321 * self.blue
		q = 0.211 * self.red - 0.526 * self.green + 0.311 * self.blue

		return Color(y, i, q, "yiq")

	def __str__(self):
		return "color model: {} / {:.2f} / {:.2f} / {:.2f}".format(
			self.__color_model,
			self.__first,
			self.__second,
			self.__third
		)
