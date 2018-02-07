#!/usr/bin/env python3

import sys
import socket
from arp_init import arp_init
from arp_settings import VMSettings
from arp_dump import ArpDump
from arp_scan import ArpScan


def run():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (VMSettings.arp_daemon_address, int(VMSettings.arp_daemon_port))
    ArpDump.printout('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        ArpDump.printout('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            ArpDump.printout('connection from {0}'.format(client_address))

            # Receive the data in small chunks and retransmit it
            data_ = ""
            while True:
                data = connection.recv(2048).decode("utf-8")
                data_ += data
                #print("strike: " + data_ + "\n")
                if len(data_) > 1:
                    if data[0] == '|':
                        i = 1
                        strlen = ""
                        while data_[i] != '|':
                            strlen += data_[i]
                            i += 1
                        istrlen = int(strlen)

                        if istrlen + 2 + len(strlen) == len(data_):
                            data_ = data_[4:]
                            break

            if len(data_) > 0:
                data_out = ArpScan.analyze(data_)
                data_out_ = "|"
                data_out_ += str(len(data_out))
                data_out_ += "|"
                data_out_ += data_out
                connection.sendall(data_out_.encode("utf-8"))

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__":
    arp_init.init()

    ArpDump.printout("Starting daemon...")
    ArpScan.start()

    ArpDump.printout("Starting the server...")

    run()