# -*- coding: utf-8 -*-

class ArpDump:

	def __init__(self):
		pass

	do_echo = True

	@staticmethod
	def set_echoing(do_echo):
		ArpDump.do_echo = True if do_echo else False

			
	@staticmethod
	def printout(args):
		if ArpDump.do_echo:
			print(args)
