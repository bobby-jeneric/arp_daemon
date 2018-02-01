# -*- coding: utf-8 -*-

import sqlite3
from arp_settings import VMSettings


class DBLayer:

	connection = None

	@staticmethod
	def connect():
		DBLayer.connection = sqlite3.connect(VMSettings.data_base_name)


	@staticmethod
	def close():
		DBLayer.connections.close()
		DBLayer.connection = None


	@staticmethod
	def is_connected():
		return (DBLayer.connection != None)
