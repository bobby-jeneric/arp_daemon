# -*- coding: utf-8 -*-

from arp_dblayer import DBLayer
from arp_dump import ArpDump
from arp_diffrecord import VMDiffCollectionList
from arp_vmrecord import VMRecord


class DBHistory:

	@staticmethod
	def create_db():
		if not DBLayer.connection:
			ArpDump.printout("DBHistory: create_db: No connection established!")
			return

		c = DBLayer.connection.cursor()
		c.execute('''create table if not exists vms_history(ip text, mac text, name text, status int, mac_old text, name_old text, changedate text)''')
		DBLayer.connection.commit()


	@staticmethod
	def store_collection(collection):
		if not DBLayer.is_connected():
			return False
		c = DBLayer.connection.cursor()
		items = []
		for item in collection:
			mac_old = item.ex_rec.mac if item.ex_rec else ""
			name_old = item.ex_rec.name if item.ex_rec else ""
			items.append((item.new_rec.ip, item.new_rec.mac, item.new_rec.name, int(item.difftype), mac_old, name_old, item.getdate()))
		c.executemany("insert into vms_history values(?,?,?,?,?,?,?)", items )
		DBLayer.connection.commit()


	@staticmethod
	def load_collection():
		if not DBLayer.is_connected():
			return False

		collection = VMDiffCollectionList()
		try:
			c = DBLayer.connection.cursor()
			res = c.execute("select ip, mac, name, status, mac_old, name_old, changedate from vms_history order by changedate desc")
			for item in res:
				new_rec = VMRecord(item[0], item[1], item[2])
				ex_rec = VMRecord(item[0], item[4], item[5])
				collection.append(item[3], new_rec, ex_rec, item[6])
		except Exception as ex:
			ArpDump.printout("DBHistory.load_collection: unable to load collection")
		return collection


	@staticmethod
	def clear():
		if not DBLayer.is_connected():
			return False

		try:
			ArpDump.printout("clear!")
			c = DBLayer.connection.cursor()
			c.execute('''delete * from vms_history''')
			DBLayer.connection.commit()
		except Exception as ex:
			ArpDump.printout("DBHistory.clear: unable to clear vms_history table")
