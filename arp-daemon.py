#!/usr/bin/env python3

"""
 import daemon


def do_main_program():
    print("Hello!")


with daemon.DaemonContext():
    do_main_program()
"""

import time
from subprocess import check_output
from arp_vmrecord import VMRecord
from arp_vmrecordreader import VMRecordReader
from arp_dblayer import DBLayer
from arp_dump import ArpDump


def print_err():
    try:
        f = open("arp-scan-res.txt", "r")
        i = 0
        for cur_line in f.readlines():
            if i > 1:
                if len(cur_line) > 0:
                    ArpDump.printout(cur_line)
                else:
                    break
            i += 1
        f.close()                
    except Exception:
        print("unable to perform file read")


def scan_arp():
#    call(["ls", "-l"])
#    print("Time:{}".format(time.ctime))
    arp_output = None
    #call(["arp-scan", "-l"], stdout=STDOUT)
    arp_output = check_output(["arp-scan", "-l"])

    arp_reader = VMRecordReader()
    arp_collection = arp_reader.read_from_bytes(arp_output)
    ArpDump.printout(arp_collection)


def run():

    db_layer = DBLayer()
    db_layer.connect()
    db_layer.create_db()
    #db_layer.test_if_table_exists()

    if True:
        #time.sleep(2)
        scan_arp()

#ArpDump.set_echoing(False)

if __name__ == "__main__":
    run()

