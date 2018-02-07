# -*- coding: utf-8 -*-

import imp
from arp_dblayer import DBLayer
from arp_db_current import DBCurrent
from arp_db_bio import DBBio
from arp_db_history import DBHistory
from arp_db_acts import DBAct


class arp_init:

    @staticmethod
    def init():
        try:
            imp.find_module('arp_settings_local')
            import arp_settings_local

            arp_settings_local.imprint_locals()
        except ImportError:
            pass

        DBLayer.connect()
        if not DBLayer.is_connected():
            print("Error: unable to establish connection")
            exit(1)

        DBCurrent.create_db()
        DBBio.create_db()
        DBHistory.create_db()
        DBAct.create_db()
