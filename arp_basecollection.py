# -*- coding: utf-8 -*-

class VMBaseCollection:
	def __init__(self):
		self.collection = []
		self.index = 0;


	def append(self, new_rec):
		self.collection.append(new_rec)


	def find(self, item):
		for ex_item in self.collection:
			if ex_item.equals(item):
				return ex_item
		return None

	def empty(self):
		return len(self.collection) == 0

	def __str__(self):
		str_ret = "VMBaseCollection\n"
		str_ret += "Items count: {0}\n\n".format(len(self.collection))
		return str_ret



	def __iter__(self):
		"""

		"""
		self.index = 0
		return self


	def __next__(self):
		try:
			result = self.collection[self.index]
		except IndexError:
			raise StopIteration
		self.index += 1
		return result
