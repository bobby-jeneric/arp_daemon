# -*- coding: utf-8 -*-

from arp_dblayer import DBLayer
from arp_db_current import DBCurrent
from arp_db_bio import DBBio
from arp_db_history import DBHistory
from arp_db_acts import DBAct


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
    def run(self, argv):
        ex_collection = DBCurrent.load_collection()
        return ex_collection.to_json()


class cmd_find_bio_by_ip(cmdbase):
    def run(self, argv):
        id = argv[2]
        bio = DBBio.find_by_ip(id)
        return bio.to_json()


class cmd_set_bio_by_ip(cmdbase):
    def run(self, argv):
        id = argv[2]
        param = argv[3]
        DBBio.set_ip_desc(id, param)
        return "{}"


class cmd_add_bio(cmdbase):
    def run(self, argv):
        ip = argv[2]
        desc = argv[3]
        DBBio.set_ip_desc(ip, desc)
        return "{}"


class cmd_get_bio_list(cmdbase):
    def run(self, argv):
        ex_collection = DBBio.load_collection()
        return ex_collection.to_json()


class cmd_get_bio(cmdbase):
    def run(self, argv):
        ip = argv[2]
        bio = DBBio.find_by_ip(ip)
        if bio == None:
            return "{}"
        else:
            return bio.to_json()


class cmd_delete_bio(cmdbase):
    def run(self, argv):
        ip = argv[2]
        DBBio.delete_bio(ip)
        return "{}"


class cmd_get_diff_list(cmdbase):
    def run(self, argv):
        ex_collection = DBHistory.load_collection()
        return ex_collection.to_json()


class cmd_get_act_list(cmdbase):
    def run(self, argv):
        ex_collection = DBAct.load_collection(argv[2])
        return ex_collection.to_json()


class arp_commands:
    @staticmethod
    def get_commands():
        cmd_list = []
        cmd_list.append(cmd_get_current_list("get_current_list", 0))
        cmd_list.append(cmd_find_bio_by_ip("find_bio_by_ip", 1))
        cmd_list.append(cmd_set_bio_by_ip("set_bio_by_ip", 2))
        cmd_list.append(cmd_add_bio("add_bio", 2))
        cmd_list.append(cmd_get_bio_list("get_bio_list", 0))
        cmd_list.append(cmd_get_bio("get_bio", 1))
        cmd_list.append(cmd_delete_bio("delete_bio", 1))
        cmd_list.append(cmd_get_diff_list("get_diff_list", 0))
        cmd_list.append(cmd_get_act_list("get_act_list", 1))
        return cmd_list
