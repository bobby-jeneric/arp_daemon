# -*- coding: utf-8 -*-

from subprocess import check_output
from arp_dump import ArpDump
from arp_vmcollection import VMRecordCollection
from arp_vmrecord import VMRecord


class ArpScanArp:
	"""
	Virtual Machine Record Reader
	"""

	@staticmethod
	def parse_arp_line(arp_line):
		if len(arp_line) == 0:
			ArpDump.printout("Error: parse_arp_line: arp_line length is 0")
			return

		arp_params = arp_line.split("\t")
		if len(arp_params) != 3:
			ArpDump.printout("Error: parse_arp_line: arp_params length is not 3")
			return

		new_vm = VMRecord(arp_params[0], arp_params[1], arp_params[2])
		return new_vm


	@staticmethod
	def read_from_bytes(barray):
		collection = VMRecordCollection()
		try:
			arp_lines = barray.decode("utf-8").split("\n")
			i = 0
			for line in arp_lines:
				if i > 1:
					if len(line) > 0:
						new_vm = ArpScanArp.parse_arp_line(line)
						collection.append(new_vm)
					else:
						break
				i += 1
		except Exception as ex:
			ArpDump.printout("unable to perform file read")
		
		return collection

	@staticmethod
	def scan():
		arp_output = check_output(["arp-scan", "-l"])
		return ArpScanArp.read_from_bytes(arp_output)
