#!/usr/bin/env python3

from scapy.all import *

def print_pkt(pkt):
    pkt.show()


##TODO:
# - Copy your iface value from running the ifconfig command below.
pkt = sniff(iface='', filter='icmp', prn=print_pkt)
