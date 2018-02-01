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
import imp


def run():

    # connection to database
    DBLayer.connect()

    # creating (if not exists) needed tables
    DBCurrent.create_db()
    DBHistory.create_db()
    DBInform.create_db()

    # reading, scanning and analyzing
    ex_collection = DBCurrent.load_collection()
    new_collection = ArpScanScapy.scan()
    ArpDump.printout(new_collection)
    diff_result = VMDiff.diff(ex_collection, new_collection)
    if not diff_result.empty():
        ArpDump.printout(diff_result)
        return
        DBCurrent.clear()
        DBCurrent.store_collection(new_collection)
        DBHistory.store_collection(diff_result)

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


    #execute the daemon
    run()
