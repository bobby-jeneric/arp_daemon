# -*- coding: utf-8 -*-

class ArpDump:

	do_echo = True
		
	@staticmethod
	def set_echoing(do_echo):
		ArpDump.do_echo = True if do_echo else False

			
	@staticmethod
	def print(args):
		if ArpDump.do_echo:
			print(args)
		
