# -*- coding: utf-8 -*-

from arp_dblayer import DBLayer
from arp_dump import ArpDump
from arp_vmbiocollection import VMBioCollection
from arp_vmbio import VMBio


class DBBio:

    @staticmethod
    def create_db():
        if not DBLayer.connection:
            ArpDump.printout("DBBio: create_db: No connection established!")
            return

        c = DBLayer.connection.cursor()
        c.execute('''create table if not exists vms_bio(ip text, desc text)''')
        DBLayer.connection.commit()


    @staticmethod
    def find_by_ip(ip):
        if not DBLayer.is_connected():
            return None
        c = DBLayer.connection.cursor()
        _ip = (str(ip),)
        c.execute("select ip, desc from vms_bio where ip=?", _ip)
        res = c.fetchone()
        if res == None:
            return None

        vmbio = VMBio(res[0], res[1])
        return vmbio


    @staticmethod
    def set_ip_desc(ip, desc):
        c = DBLayer.connection.cursor()
        if DBBio.find_by_ip(ip) == None:
            _pack = (str(ip), str(desc),)
            c.execute("insert into vms_bio values(?,?)", _pack)
            DBLayer.connection.commit()
            return True

        _pack = (str(desc), str(ip),)
        c.execute("update vms_bio set desc=? where ip=?", _pack )
        DBLayer.connection.commit()
        return True


    @staticmethod
    def load_collection():
        if not DBLayer.is_connected():
            return 0

        collection = VMBioCollection()
        try:
            c = DBLayer.connection.cursor()
            res = c.execute("select ip, desc from vms_bio")
            for item in res:
                item = VMBio(item[0], item[1])
                collection.append(item)
        except Exception as ex:
            ArpDump.printout("DBBio.load_collection: unable to load collection")
        return collection


    @staticmethod
    def clear():
        if not DBLayer.is_connected():
            return 0

        try:
            c = DBLayer.connection.cursor()
            c.execute("delete from vms_bio")
            DBLayer.connection.commit()
        except Exception as ex:
            ArpDump.printout("DBBio.clear: unable to clear vms_current table")
