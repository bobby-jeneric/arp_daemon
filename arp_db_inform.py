# -*- coding: utf-8 -*-

from arp_dblayer import DBLayer
from arp_dump import ArpDump
from arp_vmcollection import VMRecordCollection
from arp_vmrecord import VMRecord


class DBInform:

	@staticmethod
	def create_db():
		if not DBLayer.connection:
			ArpDump.printout("DBInform: create_db: No connection established!")
			return

		c = DBLayer.connection.cursor()
		c.execute('''create table if not exists vms_inform(ip text, mac text, name text, status int)''')
		DBLayer.connection.commit()


	@staticmethod
	def store_collection(collection):
		if not DBLayer.is_connected():
			return 0
		c = DBLayer.connection.cursor()
		items = []
		for item in collection:
			items.append((item.ip, item.mac, item.name))
		c.executemany("insert into vms_history values(?,?,?)", items )
		DBLayer.connection.commit()


	@staticmethod
	def load_collection():
		if not DBLayer.is_connected():
			return 0

		collection = VMRecordCollection()
		try:
			c = DBLayer.connection.cursor()
			res = c.execute("select ip, mac, name from vms_current")
			for item in res:
				item = VMRecord(item[0], item[1], item[2])
				collection.append(item)
		except Exception as ex:
			ArpDump.printout("DBCurrent.load_collection: unable to load collection")
		return collection


	@staticmethod
	def clear():
		if not DBLayer.is_connected():
			return 0

		try:
			c = DBLayer.connection.cursor()
			c.execute('''delete * from vms_current''')
			DBLayer.connection.commit()
		except Exception as ex:
			ArpDump.printout("DBCurrent.clear: unable to clear vms_current table")
