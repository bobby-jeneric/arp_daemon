#!/usr/bin/env python3


from arp_db_current import DBCurrent
from arp_db_history import DBHistory
from arp_db_inform import DBInform
from arp_diffrecord import VMDiff
from arp_inform import VMInform
from arp_scan_scapy import ArpScanScapy
from arp_settings import VMSettings
from arp_vmrecord import VMRecord
from arp_scan_arp import ArpScanArp
from arp_dblayer import DBLayer
from arp_dump import ArpDump
from arp_vmact import VMAct
from arp_db_acts import DBAct
import imp
import sys
import time


def run():

    # connection to database
    DBLayer.connect()

    # creating (if not exists) needed tables
    DBCurrent.create_db()
    DBHistory.create_db()
    DBInform.create_db()
    DBAct.create_db()

    cur_act = VMAct()
    #ArpDump.printout(cur_act.status)
    DBAct.set_record(cur_act.changedate, cur_act.status, cur_act.type)

    # reading, scanning and analyzing
    ex_collection = DBCurrent.load_collection()
    new_collection = ArpScanScapy.scan()
    #ArpDump.printout(new_collection)
    diff_result = VMDiff.diff(ex_collection, new_collection)
    if not diff_result.empty():
        #ArpDump.printout(diff_result)
        #return
        DBCurrent.clear()
        DBCurrent.store_collection(new_collection)
        DBHistory.store_collection(diff_result)
        cur_act.status = 1
    else:
        cur_act.status = 2
    #ArpDump.printout(cur_act.status)
    DBAct.set_record(cur_act.changedate, cur_act.status, cur_act.type)

    #VMInform.send_an_email(VMSettings.inform_from_name, VMSettings.inform_to_list, 'Hello', 'I got an information!')


if __name__ == "__main__":
    # test for local settings
    try:
        imp.find_module('arp_settings_local')
        import arp_settings_local
        arp_settings_local.imprint_locals()
    except ImportError:
        pass

    #enable or disable echoing
    ArpDump.set_echoing(VMSettings.echo_output)

    if VMSettings.data_base_name == None or VMSettings.data_base_name == "":
        ArpDump.printout("data_base_name is not provided")
        exit(1)


    if (len(sys.argv) < 2):
        print("use start key to start as a daemon")
        #execute the daemon
        run()
        exit(0)

    action = sys.argv[1]
    if (action == "start"):
        while True:
            run()
            time.sleep(1)

