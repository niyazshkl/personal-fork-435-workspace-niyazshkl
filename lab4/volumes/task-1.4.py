from scapy.all import *

iface = ['br-dc62965e0899, ens18,docker0 lo, veth7189177,veth3d7998e']

def handle_pkt(pkt):
    if ICMP in pkt and pkt[ICMP].type == 8: #Step 1: sniff the incoming packet and ensure it is a Echo Request (type==8)
        print(f"Sniffed ICMP Echo Request: {pkt[IP].src} → {pkt[IP].dst}")

        #Step 2: Build a snooped response
        reply = IP()/ICMP()

        #Self explanatory field intiaalizations of the reply packet
        reply[IP].src = pkt[IP].dst
        reply[IP].dst = pkt[IP].src

        reply[ICMP].type = 0              # Ensure it is a Echo Reply (type =0)

        reply[ICMP].id = pkt[ICMP].id
        reply[ICMP].seq = pkt[ICMP].seq

        if Raw in pkt:
            reply = reply / pkt[Raw].load
            
        #Step 3: Send the reply packet
        send(reply, verbose=0)
        print(f"Sent Spoofed Reply: {reply[IP].src} → {reply[IP].dst}\n")

print("[*] Sniffing for ICMP Echo Requests...\n")
sniff(iface=iface, filter='icmp', prn=handle_pkt)