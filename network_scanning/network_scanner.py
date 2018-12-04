import scapy.all as scapy
from optparse import OptionParser

def scan():
    parser = OptionParser()
    parser.add_option("-i", "--ip", dest="ip", help="Please specify ip")
    (options, args) = parser.parse_args()
    if not options.ip:
        parser.error("IP is not specified")

    arp_request = scapy.ARP(pdst=options.ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_request = broadcast/arp_request
    answered_list = scapy.srp(broadcast_request, timeout=1, verbose=False)[0]

    client_list = []
    for pkg in answered_list:
        client_dict = {"ip":pkg[1].psrc, "mac":pkg[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result):
    print("IP\t\t\t" + "MAC Address")
    print("-----------------------------------")
    for element in result:
        print(element["ip"] + "\t\t" + element["mac"])

result = scan()
print_result(result)