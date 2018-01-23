# -*- coding: utf-8 -*-

from arp_vmrecord import VMRecord
from arp_vmcollection import VMRecordCollection
from arp_dump import ArpDump


class VMRecordReader:
	"""
	Virtual Machine Record Reader
	"""

	def __str__(self):
		return "IP: {0}\nMAC: {1}\nNAME: {2}\n".format(self.ip, self.mac, self.name)


	def parse_arp_line(self, arp_line):
		if len(arp_line) == 0:
			ArpDump.print("Error: parse_arp_line: arp_line length is 0")
			return

		arp_params = arp_line.split("\t")
		#print(arp_params)
		if len(arp_params) != 3:
			ArpDump.print("Error: parse_arp_line: arp_params length is not 3")
			return

		new_vm = VMRecord(arp_params[0], arp_params[1], arp_params[2])
		#print("class created")
		return new_vm


	def read_from_bytes(self, barray):
		collection = VMRecordCollection()
		try:
			arp_lines = barray.decode("utf-8").split("\n")
			i = 0;
			for line in arp_lines:
				if i > 1:
					if len(line) > 0:
						new_vm = self.parse_arp_line(line)
						collection.append(new_vm)
					else:
						break
				i += 1
		except Exception as ex:
			ArpDump.print("unable to perform file read")    
		
		return collection



