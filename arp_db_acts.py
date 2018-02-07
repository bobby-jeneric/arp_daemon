# -*- coding: utf-8 -*-

from arp_dblayer import DBLayer
from arp_dump import ArpDump
from arp_vmact import VMAct
from arp_vmactcollection import VMActCollection


class DBAct:

	@staticmethod
	def create_db():
		if not DBLayer.connection:
			ArpDump.printout("DBAct: create_db: No connection established!")
			return

		c = DBLayer.connection.cursor()
		c.execute('''create table if not exists vms_acts(changedate text, status int, type int)''')
		DBLayer.connection.commit()


	@staticmethod
	def find_by_chnagedate(changedate):
		if not DBLayer.is_connected():
			return None
		c = DBLayer.connection.cursor()
		_changedate = (str(changedate),)
		c.execute("select changedate, status, type from vms_acts where changedate=?", _changedate)
		res = c.fetchone()
		if res == None:
			return None

		vmact = VMAct(res[0], res[1], res[2])
		return vmact


	@staticmethod
	def set_record(changedate, status, type):
		c = DBLayer.connection.cursor()
		if DBAct.find_by_chnagedate(changedate) == None:
			_pack = (str(changedate), int(status), int(type),)
			c.execute("insert into vms_acts values(?,?,?)", _pack)
			DBLayer.connection.commit()
			return True

		_pack = (int(status), int(type), str(changedate),)
		c.execute("update vms_acts set status=?, type=? where changedate=?", _pack)
		DBLayer.connection.commit()
		return True


	@staticmethod
	def load_collection():
		if not DBLayer.is_connected():
			return False

		collection = VMActCollection()
		try:
			c = DBLayer.connection.cursor()
			res = c.execute("select changedate, status, type from vms_acts order by changedate desc")
			for item in res:
				print(item[1])
				collection.append(VMAct(item[0], item[1], item[2]))
		except Exception as ex:
			ArpDump.printout("DBAct.load_collection: unable to load collection")
		return collection


	@staticmethod
	def clear():
		if not DBLayer.is_connected():
			return False

		try:
			ArpDump.printout("clear!")
			c = DBLayer.connection.cursor()
			c.execute('''delete * from vms_acts''')
			DBLayer.connection.commit()
		except Exception as ex:
			ArpDump.printout("DBAct.clear: unable to clear vms_acts table")
