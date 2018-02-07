# -*- coding: utf-8 -*-

from arp_basecollection import VMBaseCollection
import json

class VMActCollection(VMBaseCollection):

	def __str__(self):
		str_ret = "VMActCollection\n"
		str_ret += "Items count: {0}\n\n".format(len(self.collection))
		for record in self.collection:
			str_ret += "{0}\n".format(record)
		return str_ret


	def to_json(self):
		data = []
		for record in self.collection:
			data.append({'CHANGEDATE': record.changedate, 'STATUS': record.status, 'TYPE': record.type})
		return json.dumps(data)
