import subprocess
from optparse import OptionParser
import re
# Original MAC is 08:00:27:74:17:d4

def get_parameters():
    parser = OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Please specify interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="Please specify new mac address")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error("Interface is not specified")
    elif not options.new_mac:
        parser.error("New mac address is not specified")
    return options

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac:
        return mac.group(0)
    else:
        print("Could not find MAC address for the specified interface")

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig", interface])

options = get_parameters()
current_mac = get_current_mac(options.interface)
if options.new_mac == current_mac:
    print("The MAC address you specify is the same as current MAC address")
else:
    print("Change MAC from " + current_mac + " to " + options.new_mac + " for interface " + options.interface)
    change_mac(options.interface, options.new_mac)