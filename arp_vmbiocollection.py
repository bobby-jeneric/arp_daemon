# -*- coding: utf-8 -*-

from arp_basecollection import VMBaseCollection
import json

class VMBioCollection(VMBaseCollection):

	def __str__(self):
		str_ret = "VMBioCollection\n"
		str_ret += "Items count: {0}\n\n".format(len(self.collection))
		for record in self.collection:
			str_ret += "{0}\n---".format(record)
		return str_ret


	def to_json(self):
		data = []
		for record in self.collection:
			data.append({'IP': record.ip, 'DESC': record.desc})
		return json.dumps(data)
