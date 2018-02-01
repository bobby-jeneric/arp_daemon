# -*- coding: utf-8 -*-

from arp_basecollection import VMBaseCollection

class VMRecordCollection(VMBaseCollection):

	def __str__(self):
		str_ret = "VMRecordCollection\n"
		str_ret += "Items count: {0}\n\n".format(len(self.collection))
		for record in self.collection:
			str_ret += "{0}\n---".format(record)
		return str_ret
