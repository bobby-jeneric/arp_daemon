# -*- coding: utf-8 -*-
from arp_settings import VMSettings
from arp_vmcollection import VMRecordCollection
from arp_vmrecord import VMRecord


class ArpScanScapy:

    @staticmethod
    def scan():
        from scapy.all import srp, Ether, ARP, conf
        import socket

        conf.verb = 0
        ans, uans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=VMSettings.ip_range), timeout=2,
                        iface=VMSettings.interface_to_scan, inter=0.1)

        collection = VMRecordCollection()

        for snd, rcv in ans:
            hostIP = rcv.sprintf("%ARP.psrc%")
            hostMAC = rcv.sprintf("%Ether.src%")
            try:
                host = socket.gethostbyaddr(hostIP)
            except:
                host = ('unknown', [], [hostIP])
                pass
            new_rec = VMRecord(hostIP, hostMAC, host[0])
            collection.append(new_rec)

        return collection