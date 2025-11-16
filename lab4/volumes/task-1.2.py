from scapy.all import *
import time
spoofed_dst = "10.9.0.5"
spoofed_src = "10.9.0.6"
count = 3
interval = 1.0

def make_spoofed_icmp(spoofed_dst, spoofed_src, id_num=0, seq=1):
    ip = IP(dst=spoofed_dst, src=spoofed_src)
    icmp = ICMP(type=8, id=id_num, seq=seq)  # Remeber that Echo Request is type 8
    payload = b"This is a spoofed ICMP Packet!"
    spoofed_pkt = ip/icmp/payload
    return spoofed_pkt

def main():
    print(f"""Task 2: Spoofing ICMP Packet.
                Sending {count} spoofed ICMP packets:
                src={spoofed_src}
                dst={spoofed_dst}""")
    for i in range(count):
        spoofed_pkt = make_spoofed_icmp(spoofed_dst, spoofed_src, id_num=0, seq=i)
        send(spoofed_pkt)
        print(f"Packet #{i+1} with src={spoofed_src} and dst={spoofed_dst}\n")
        time.sleep(interval)
    print(f"\nAll {count} packets were sent")

if __name__ == "__main__":
    main()