# -*- coding: utf-8 -*-

import json
from datetime import datetime
from arp_settings import VMSettings


class VMAct:
    """
    Virtual Machine Act Class Definition
    """

    def __init__(self, _changedate = None, _status = 0, _type = 0):
        self.changedate = _changedate if _changedate else datetime.now()
        self.status = _status
        self.type = _type


    def __str__(self):
        return "CHANGEDATE: {0}\nSTATUS: {2}\nTYPE: {3}".format(self.changedate, self.status, self.type)


    def to_json(self):
        data = {'CHANGEDATE': self.changedate, 'STATUS': self.status, 'TYPE': self.type}
        return json.dumps(data)


    def getdate(self):
        return self.date.strftime(VMSettings.date_time_format)