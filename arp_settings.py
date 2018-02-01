# -*- coding: utf-8 -*-


# To overload the default settings values do not set your values in
# this module. Instead of it create a new module named
# 'arp_settings_local.py' in the project directory. In this module
# define an 'imprint_locals' function and place the overloadings
# right there.
# The content of the module may look like this:
"""
# -*- coding: utf-8 -*-

from arp_settings import VMSettings


def imprint_locals():
    VMSettings.interface_to_scan = 'eth0'
    VMSettings.ip_range = '192.168.0.0/23'
    VMSettings.data_base_name = 'arp.db'
"""


class VMSettings:

    # interface to scan
    interface_to_scan = ''

    # ip range to scan
    ip_range = ''

    # physical sql database file name
    data_base_name = ''

    # sender email
    inform_from_name = 'admin@example.com'

    # recipients emails list
    inform_to_list = ['johndoe@example.com']

    # date and time print format
    date_time_format = '%Y.%m.%d %H:%M:%S'

    # enable or disable echoing the output
    echo_output = True
