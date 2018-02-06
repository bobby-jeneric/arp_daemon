# -*- coding: utf-8 -*-

from enum import IntEnum
from datetime import datetime
from arp_basecollection import VMBaseCollection
from arp_settings import VMSettings
import json


class VMDiffType(IntEnum):
    NONE = 0
    ADDED = 1
    CHANGEDMAC = 2
    CHANGEDNODE = 3
    CHANGEDMACNODE = 4
    CLOSED = 5

    @staticmethod
    def to_str(x):
        return {
            0: "None",
            1: "Added",
            2: "Changed MAC",
            3: "Changed Node",
            4: "Changed MAC and Node",
            5: "Closed"
        }.get(x, "UNKNOWN TYPE")


class VMDiffRecord:

    def __init__(self, difftype, new_rec, ex_rec = None, changedate = None):
        self.difftype = difftype
        self.new_rec = new_rec
        self.ex_rec = ex_rec
        self.date = changedate if changedate else datetime.now()

    def getdate(self):
        return self.date.strftime(VMSettings.date_time_format)

    def __str__(self):
        str_ret = "Status: {0}\n".format(VMDiffType.to_str(self.difftype))
        str_ret += "Found at: {0}\n".format(self.getdate())
        str_ret += "{0}".format(self.new_rec)

        if self.difftype == VMDiffType.CHANGEDMAC or self.difftype == VMDiffType.CHANGEDMACNODE:
            str_ret += "\nMAC was: {0}".format(self.ex_rec.mac)
        if self.difftype == VMDiffType.CHANGEDNODE or self.difftype == VMDiffType.CHANGEDMACNODE:
            str_ret += "\nNAME was: {0}".format(self.ex_rec.name)

        return str_ret


class VMDiffCollection(VMBaseCollection):

    def append(self, difftype, new_rec, ex_rec = None, changedate = None):
        if self.find_by_ip(new_rec.ip):
            return
        diff_rec = VMDiffRecord(difftype, new_rec, ex_rec, changedate)
        self.collection.append(diff_rec)

    def find_by_ip(self, ip):
        for item in self.collection:
            if item.new_rec.ip == ip:
                return True
        return False

    def __str__(self):
        str_ret = "VMDiffCollection\n"
        str_ret += "Items count: {0}\n\n".format(len(self.collection))
        for record in self.collection:
            str_ret += "{0}\n---\n".format(record)
        return str_ret

    def to_json(self):
        data = []
        for record in self.collection:
            data.append({'IP': record.new_rec.ip, 'MAC': record.new_rec.mac, 'NAME': record.new_rec.name,
                         'STATUS' : record.difftype,
                         'MACOLD' : record.ex_rec.mac if record.ex_rec else '',
                         'NAMEOLD': record.ex_rec.name if record.ex_rec else '',
                         'CHANGEDATE': record.date
                         })
        return json.dumps(data)


class VMDiffCollectionList(VMDiffCollection):

    def append(self, difftype, new_rec, ex_rec = None, changedate = None):
        diff_rec = VMDiffRecord(difftype, new_rec, ex_rec, changedate)
        self.collection.append(diff_rec)


class VMDiff:

    @staticmethod
    def diff(ex_coll, new_coll):
        collection = VMDiffCollection()
        #various diff
        for new_item in new_coll:
            for ex_item in ex_coll:
                if new_item.ip == ex_item.ip:
                    if not (new_item.mac == ex_item.mac) and not (new_item.name == ex_item.name):
                        collection.append(VMDiffType.CHANGEDMACNODE, new_item, ex_item)
                    if not (new_item.mac == ex_item.mac):
                        collection.append(VMDiffType.CHANGEDMAC, new_item, ex_item)
                    if not (new_item.name == ex_item.name):
                        collection.append(VMDiffType.CHANGEDNODE, new_item, ex_item)

        #searching for added records
        for new_item in new_coll:
            if not ex_coll.find(new_item):
                collection.append(VMDiffType.ADDED, new_item)

        #searchind for closed records
        for ex_item in ex_coll:
            if not new_coll.find(ex_item):
                collection.append(VMDiffType.CLOSED, ex_item)

        return collection
