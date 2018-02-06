#!/usr/bin/env python3

import sys
from arp_init import arp_init
from arp_commands import arp_commands

arp_init.init()

cmd_list = arp_commands.get_commands()

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
        output = cmd.run(sys.argv)
        print(output)
        exit(0)

print("Error: unknown command given")
exit(12)
