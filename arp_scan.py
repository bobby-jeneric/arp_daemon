# -*- coding: utf-8 -*-

import threading
import time
from datetime import datetime
from arp_settings import VMSettings
from arp_dump import ArpDump
from arp_commands import arp_commands
from arp_vmact import VMAct
from arp_db_acts import DBAct
from arp_scan_arp import ArpScanArp
from arp_scan_scapy import ArpScanScapy
from arp_db_current import DBCurrent
from arp_db_history import DBHistory
from arp_diffrecord import VMDiff
from arp_commands import cmdbase
from arp_init import arp_init
from arp_inform import VMInform
import json


class cmd_get_ticks_to_go(cmdbase):
    def run(self, argv):
        return int(VMSettings.arp_daemon_scan_sleep) - ArpScan.get_ticks_to_go()


class ArpScanThread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


class ArpShuttle:
    def __init__(self):
        self.event = threading.Event()
        self.cmd = ""
        self.args = []
        self.answer = ""
        self.add_keys = 0


class ArpScanThreadStrike(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


class ArpScan:
    this_object = None
    this_lock = None
    commands = None
    start_date = None
    this_pcmd = None
    this_stroke_thread = None
    this_stroke_act = None
    this_stroke_collection = None


    @staticmethod
    def start():
        if ArpScan.commands == None:
            ArpScan.commands = arp_commands.get_commands()
            #ArpScan.commands.append(cmd_get_ticks_to_go("get_ticks_to_go", 0))

        if ArpScan.this_lock == None:
            ArpScan.this_lock = threading.Lock()

        if ArpScan.this_object == None:
            ArpScan.this_object = ArpScanThread(ArpScan.do_scan_work)


    @staticmethod
    def do_scan_work():
        arp_init.dbinit()
        with ArpScan.this_lock:
            ArpScan.start_date = datetime.now()

        while True:
            time.sleep(0.05)
            pcmd = None

            with ArpScan.this_lock:
                pcmd = ArpScan.this_pcmd
                ArpScan.this_pcmd = None
            if (pcmd != None):
                ArpScan.th_analyze(pcmd)
                continue

            if ArpScan.get_ticks_to_go() >= int(VMSettings.arp_daemon_scan_sleep):
                if ArpScan.scan_act1():
                    continue

            ArpScan.scan_act3()


    @staticmethod
    def get_ticks_to_go():
        with ArpScan.this_lock:
            now_date = datetime.now()
            diff_time = now_date - ArpScan.start_date
            diff = diff_time.days * 86400 + diff_time.seconds
            return diff


    @staticmethod
    def analyze(data):
        ArpDump.printout("received: " + data)
        cmds = data.split("|")
        if len(cmds) > 0:
            pcmd = ArpShuttle()
            pcmd.cmd = cmds[0]
            pcmd.add_keys = len(cmds) - 1
            cmds.insert(0, "-")
            pcmd.args = cmds
            with ArpScan.this_lock:
                ArpScan.this_pcmd = pcmd
            pcmd.event.wait()
            return pcmd.answer
        return "{}"


    @staticmethod
    def th_analyze(pcmd):
        pcmd.answer = "{}"
        for cmd in ArpScan.commands:
            if cmd.get_cmd_name() == pcmd.cmd:
                if cmd.get_cmd_count() != pcmd.add_keys:
                    pcmd.answer = "invalid amount of add keys: should be {0}".format(cmd.get_cmd_count())
                else:
                    pcmd.answer = cmd.run(pcmd.args)
                break

        if pcmd.cmd == "get_ticks_to_go":
            tick_to_go = ArpScan.get_ticks_to_go()
            seconds = abs(int(VMSettings.arp_daemon_scan_sleep) - tick_to_go)
            startdate = ""
            with ArpScan.this_lock:
                if ArpScan.this_stroke_act != None:
                    startdate = ArpScan.this_stroke_act.getdate()
                    seconds = tick_to_go
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            if (h > 0):
                stick = "{0}:{1}:{2}".format(h, m, s)
            elif (m > 0):
                stick = "{0}:{1}".format(m, s)
            else:
                stick = ":{0}".format(s)
            pcmd.answer = json.dumps({'TICK': stick, 'STARTDATE': startdate})

        if pcmd.cmd == "manual_start":
            ArpScan.scan_act1(1)
            pcmd.answer = ""

        pcmd.event.set()
        pcmd.event.clear()
        return


    @staticmethod
    def scan_act1(_type = 0):
        with ArpScan.this_lock:
            if ArpScan.this_stroke_thread == None:
                ArpDump.printout("scan_act1")
                ArpScan.start_date = datetime.now()
                ArpScan.this_stroke_act = VMAct()
                ArpScan.this_stroke_act.type = _type
                DBAct.set_record(ArpScan.this_stroke_act.getdate(), ArpScan.this_stroke_act.status, ArpScan.this_stroke_act.type)
                ArpScan.this_stroke_collection = None
                ArpScan.this_stroke_thread = ArpScanThreadStrike(ArpScan.scan_act2)
                return True
            return False


    @staticmethod
    def scan_act2():
        if (VMSettings.arp_daemon_scan_type == '1'):
            new_collection = ArpScanArp.scan()
        elif (VMSettings.arp_daemon_scan_type == '2'):
            new_collection = ArpScanScapy.scan()
        else:
            new_collection = []

        with ArpScan.this_lock:
            ArpScan.this_stroke_collection = new_collection
            ArpDump.printout("scan_act2")


    @staticmethod
    def scan_act3():
        with ArpScan.this_lock:
            if ArpScan.this_stroke_collection == None:
                return

            ArpDump.printout("scan_act3")
            ArpScan.this_stroke_thread.join()
            ArpScan.this_stroke_thread = None
            # reading, scanning and analyzing
            ex_collection = DBCurrent.load_collection()
            # ArpDump.printout(new_collection)
            diff_result = VMDiff.diff(ex_collection, ArpScan.this_stroke_collection)
            if not diff_result.empty():
                # ArpDump.printout(diff_result)
                # return
                DBCurrent.clear()
                DBCurrent.store_collection(ArpScan.this_stroke_collection)
                DBHistory.store_collection(diff_result)
                ArpScan.this_stroke_act.status = 1
                ArpScan.do_mail(diff_result)
            else:
                ArpScan.this_stroke_act.status = 2
            # ArpDump.printout(cur_act.status)
            DBAct.set_record(ArpScan.this_stroke_act.getdate(), ArpScan.this_stroke_act.status, ArpScan.this_stroke_act.type)

            ArpScan.this_stroke_collection = None
            ArpScan.this_stroke_act = None
            ArpScan.start_date = datetime.now()


    @staticmethod
    def do_mail(diff_result):
        try:
            for recipient in VMSettings.inform_to_list:
                sbody = str(diff_result)
                VMInform.send_an_email(str(VMSettings.inform_from_name), str(recipient), "There was changes", sbody )
        except Exception as ex:
            ArpDump.printout("ArpScan.do_mail: unable to send mail")
