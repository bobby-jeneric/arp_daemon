# -*- coding: utf-8 -*-

import json


class VMBio:
    """
    Virtual Machine Bio Class Definition
    """

    def __init__(self, _ip, _desc):
        self.ip = _ip
        self.desc = _desc


    def __str__(self):
        return "IP: {0}\nDESC: {2}\n".format(self.ip, self.desc)


    def to_json(self):
        data = {'IP': self.ip, 'DESC': self.desc}
        return json.dumps(data)