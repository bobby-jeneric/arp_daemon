# -*- coding: utf-8 -*-

from arp_vmrecord import VMRecord

class VMRecordCollection:
	def __init__(self):
		self.collection = []


	def append(self, new_rec):
		self.collection.append(new_rec)


	def __str__(self):
		str_ret = "VMRecordCollection\n"
		str_ret += "Items count: {0}\n\n".format(len(self.collection))
		for record in self.collection:
			str_ret += "{0}\n".format(record)
		return str_ret

