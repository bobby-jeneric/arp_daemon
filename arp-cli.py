#!/usr/bin/env python3

import sys
import imp
from arp_dblayer import DBLayer
from arp_db_current import DBCurrent
from arp_db_bio import DBBio
from arp_db_history import DBHistory


try:
    imp.find_module('arp_settings_local')
    import arp_settings_local

    arp_settings_local.imprint_locals()
except ImportError:
    pass


class cmdbase:
    def __init__(self, cmdname, cmdcount):
        self.cmdname = cmdname
        self.cmdcount = cmdcount

    def is_this(self, cmdname, cmdcount):
        return self.cmdname == cmdname and self.cmdcount == cmdcount

    def get_cmd_name(self):
        return self.cmdname

    def get_cmd_count(self):
        return self.cmdcount


class cmd_get_current_list(cmdbase):
    def run(self):
        ex_collection = DBCurrent.load_collection()
        print(ex_collection.to_json())
        exit(0)


class cmd_find_bio_by_ip(cmdbase):
    def run(self):
        id = sys.argv[2]
        bio = DBBio.find_by_ip(id)
        print(bio.to_json())
        exit(0)


class cmd_set_bio_by_ip(cmdbase):
    def run(self):
        id = sys.argv[2]
        param = sys.argv[3]
        DBBio.set_ip_desc(id, param)
        exit(0)


class cmd_add_bio(cmdbase):
    def run(self):
        ip = sys.argv[2]
        desc = sys.argv[3]
        DBBio.set_ip_desc(ip, desc)
        exit(0)


class cmd_get_bio_list(cmdbase):
    def run(self):
        ex_collection = DBBio.load_collection()
        print(ex_collection.to_json())
        exit(0)


class cmd_get_bio(cmdbase):
    def run(self):
        ip = sys.argv[2]
        bio = DBBio.find_by_ip(ip)
        if bio == None:
            print("{}")
        else:
            print(bio.to_json())
        exit(0)


class cmd_get_diff_list(cmdbase):
    def run(self):
        ex_collection = DBHistory.load_collection()
        print(ex_collection.to_json())
        exit(0)


cmd_list = []
cmd_list.append(cmd_get_current_list("get_current_list", 0))
cmd_list.append(cmd_find_bio_by_ip("find_bio_by_ip", 1))
cmd_list.append(cmd_set_bio_by_ip("set_bio_by_ip", 2))
cmd_list.append(cmd_add_bio("add_bio", 2))
cmd_list.append(cmd_get_bio_list("get_bio_list", 0))
cmd_list.append(cmd_get_bio("get_bio", 1))
cmd_list.append(cmd_get_diff_list("get_diff_list", 0))

DBLayer.connect()
if not DBLayer.is_connected():
    print("Error: unable to establish connection")
    exit(1)

DBCurrent.create_db()
DBBio.create_db()
DBHistory.create_db()

if (len(sys.argv) < 2):
    print("use keys to use cli")
    exit(0)

action = sys.argv[1]
add_keys = len(sys.argv) - 2

for cmd in cmd_list:
    if cmd.get_cmd_name() == action:
        if cmd.get_cmd_count() != add_keys:
            print("command: " + cmd.get_cmd_name())
            print("invalid amount of add keys: should be {0}".format(cmd.get_cmd_count()))
            exit(11)
        cmd.run()

print("Error: unknown command given")
exit(12)
