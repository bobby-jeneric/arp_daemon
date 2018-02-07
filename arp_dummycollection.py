# -*- coding: utf-8 -*-
from arp_vmcollection import VMRecordCollection
from arp_vmrecord import VMRecord


class VMDummyCollection:

    @staticmethod
    def empty_collection():
        collection = VMRecordCollection()
        return collection

    @staticmethod
    def collection0():
        collection = VMRecordCollection()
        collection.append(VMRecord("192.168.0.1", "00:00:00:c0:00:08", "Host 1"))
        collection.append(VMRecord("192.168.0.2", "00:00:00:f7:9d:df", "Host 1"))
        collection.append(VMRecord("192.168.0.254", "00:00:00:ff:76:17", "Host 1"))
        return collection

    @staticmethod
    def collection1():
        collection = VMRecordCollection()
        collection.append(VMRecord("192.168.0.1", "00:00:00:c0:00:08", "Host 1"))
        collection.append(VMRecord("192.168.0.2", "00:00:00:f7:9d:df", "Host 1"))
        collection.append(VMRecord("192.168.0.254", "00:00:00:ff:76:17", "Host 1"))
        collection.append(VMRecord("192.168.0.184", "00:00:00:ff:76:17", "Host 1"))
        return collection

    @staticmethod
    def collection2():
        collection = VMRecordCollection()
        collection.append(VMRecord("192.168.0.1", "00:00:00:c0:00:08", "Host 1"))
        collection.append(VMRecord("192.168.0.2", "00:00:00:f7:9d:df", "Host 1"))
        return collection

    @staticmethod
    def collection3():
        collection = VMRecordCollection()
        collection.append(VMRecord("192.168.0.1", "00:00:00:e0:00:08", "Host 1"))
        collection.append(VMRecord("192.168.0.2", "00:00:00:f7:9d:df", "Host 1"))
        return collection


    @staticmethod
    def collection4():
        collection = VMRecordCollection()
        collection.append(VMRecord("192.168.0.1", "00:00:00:e0:00:08", "Host 1"))
        collection.append(VMRecord("192.168.0.2", "00:00:00:f7:9d:df", "Host 2"))
        return collection

    @staticmethod
    def collection5():
        collection = VMRecordCollection()
        collection.append(VMRecord("192.168.0.1", "00:00:00:e0:00:08", "Host 3"))
        collection.append(VMRecord("192.168.0.2", "00:00:00:f7:9d:df", "Host 2"))
        return collection