# -*- coding: utf-8 -*-

import sqlite3
from arp_dump import ArpDump


class DBLayer:

	def __init__(self):
		self.connection = None


	def connect(self):
		self.connection = sqlite3.connect('arp.db')


	def test_if_table_exists(self):
		if not self.connection:
			ArpDump.printout("DBLayer: create_db: No connection established!")
			return

		c = self.connection.cursor()
		c.execute('''TABLES''')
		
	
	def create_db(self):
		if not self.connection:
			ArpDump.printout("DBLayer: create_db: No connection established!")
			return

		c = self.connection.cursor()
		c.execute('''create table if not exists vms(ip text, mac text, name text)''')
		self.connection.commit()


	def close(self):
		self.connections.close()
		self.connection = None


