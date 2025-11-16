#!/usr/bin/env python3

from scapy.all import *

def print_pkt(pkt):
    pkt.show()


##TODO:
# - Copy your iface value from running the ifconfig command below.
iface_value = 'br-dc62965e0899'
# - Modify the filter parameter to

#   (1) Capture any TCP packet the comes from a particular IP and with a destination port number 23.
tcp_filter = 'tcp and src host 10.9.0.1 and dst port 23'
#   Make sure you take screenshots
# pkt = sniff(iface=iface_value, filter=tcp_filter, prn=print_pkt)

#   (2) Capture packets that come from or go to the subnet
#       10.9.0.0/24

subnet_filter = 'net 10.9.0.0/24'
pkt = sniff(iface=iface_value, filter=subnet_filter, prn=print_pkt)