# -*- coding: utf-8 -*-

class VMRecord:
    """
    Virtual Machine Record Class Definition
    """

    def __init__(self, _ip, _mac, _name):
        self.ip = _ip
        self.mac = _mac
        self.name = _name


    def __str__(self):
        return "IP: {0}\nMAC: {1}\nNAME: {2}\n".format(self.ip, self.mac, self.name)

    def equals(self, item):
        return (self.ip == item.ip and self.mac == item.mac and self.name == item.name)
