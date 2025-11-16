#!/usr/bin/env python3
from scapy.all import *

hostname = "google.com"

#TODO
# Modify the upper_bound variable so that 
# you can see how many routers there are 
# from you to your destination.

upper_bound = 30

for ttl in range(1, upper_bound+1):
    pkt = IP(dst=hostname, ttl=ttl) / UDP(dport=33434)
    reply = sr1(pkt, timeout = 2, verbose=0)
    if reply == None:
        print(f"{ttl} --> no reply (The router in the middle did not send back an ICMP message)")
    elif reply.type == 3:
        print("Done", reply.src)
        break
    else:
        print("%d hops away: " % ttl, reply.src)
